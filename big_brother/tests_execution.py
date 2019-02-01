import subprocess

import requests
from .models import (
    ActionToken,
    Application, Execution, Test, TestType)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def run(test_id):
    test = Test.objects.get(pk=test_id)
    if test.test_type.id == 2:
        execution_result = run_command(test)
    elif test.test_type.id == 3:
        execution_result = run_selenium(test)
    else:
        execution_result = run_url(test)

    execution = Execution.objects.create(
        test=test,
        success=execution_result,
    )

    execution.save()

    return execution_result


def run_url(test):
    try:
        r = requests.get(test.url)

        execution_result = 200 <= r.status_code < 300

    except requests.exceptions.ConnectionError as e:
        execution_result = False

    execution = Execution.objects.create(
        test=test,
        success=execution_result,
    )

    execution.save()

    return execution_result


def run_command(test):
    try:
        completed_process = subprocess.run(test.script.split(),
                                           stderr=subprocess.STDOUT)

        print(completed_process.stdout)

        execution_result = completed_process.returncode == 0

    except OSError as e:
        execution_result = False

    return execution_result


def run_selenium(test):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(chrome_options=options)

    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    driver.save_screenshot('screenshot.png')
    assert "No results found." not in driver.page_source
    driver.close()

    return True


def run_python(test):
    try:
        completed_process = subprocess.run(test.script.split(),
                                           stderr=subprocess.STDOUT)

        print(completed_process.stdout)

        execution_result = completed_process.returncode == 0

    except OSError as e:
        execution_result = False

    return execution_result
