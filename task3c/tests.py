import pytest

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def browser():
    driver = Chrome(ChromeDriverManager().install())

    driver.implicitly_wait(10)

    URL = "https://www.metric-conversions.org"
    driver.get(URL)

    yield driver

    driver.quit()


def input_data(data: str, browser: Chrome) -> str:
    input_field = browser.find_element_by_id("argumentConv")
    input_field.send_keys(data + Keys.RETURN)

    return browser.find_element_by_id("answer").text


def test_celsius_to_fahrenheit(browser: Chrome):
    browser.find_element_by_partial_link_text("Celsius to Fahrenheit").click()

    assert input_data("10", browser) == "10°C= 50.00000°F"


def test_meters_to_feet(browser: Chrome):
    browser.find_element_by_partial_link_text("Meters to Feet").click()

    assert input_data("1", browser) == "1m= 3ft 3.370079in"


def test_ounces_to_grams(browser: Chrome):
    browser.find_element_by_link_text("Weight").click()
    browser.find_element_by_link_text("Ounces").click()
    browser.find_element_by_link_text("Ounces to Grams").click()

    assert input_data("1", browser) == "1oz= 28.34952g"
