import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://automationintesting.online/"
WAIT_TIME = 30
POLL_FREQ = 0.5
SUCCESS_TEXT = "Thanks for getting in touch"


def _open_contact_page(drv):
    """Navigate to the Contact section and wait until the form is visible."""
    drv.get(BASE_URL)
    wait = WebDriverWait(drv, WAIT_TIME, POLL_FREQ)

    # Scroll & click the Contact link (sometimes hidden below the fold)
    contact_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Contact")))
    drv.execute_script("arguments[0].scrollIntoView(true);", contact_link)
    drv.execute_script("arguments[0].click();", contact_link)

    # Wait until the first field is visible (form ready)
    wait.until(EC.visibility_of_element_located((By.ID, "name")))


def _fill_field(drv, locator, value):
    elem = drv.find_element(*locator)
    elem.clear()
    elem.send_keys(value)


def _submit_form(drv, name="", email="", phone="", subject="", description=""):
    _fill_field(drv, (By.ID, "name"), name)
    _fill_field(drv, (By.ID, "email"), email)
    _fill_field(drv, (By.ID, "phone"), phone)
    _fill_field(drv, (By.ID, "subject"), subject)
    _fill_field(drv, (By.ID, "description"), description)

    submit_btn = drv.find_element(By.XPATH, '//button[text()="Submit"]')
    drv.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    drv.execute_script("arguments[0].click();", submit_btn)


@pytest.fixture(scope="session")
def driver():
    drv = webdriver.Chrome()
    drv.maximize_window()
    yield drv
    drv.quit()


# 1️⃣ Başarılı form gönderimi --------------------------------------------------------------

def test_successful_submission(driver):
    _open_contact_page(driver)
    _submit_form(
        driver,
        name="Ada Lovelace",
        email="ada@example.com",
        phone="01234567890",
        subject="Booking question",
        description="I would like to know more about room availability."
    )
    time.sleep(2)  # küçük gecikme, toast'ın DOM'a düşmesi için
    assert SUCCESS_TEXT in driver.page_source


# 2️⃣ Hatalı e‑posta ile gönderim -----------------------------------------------------------

def test_invalid_email_submission(driver):
    _open_contact_page(driver)
    _submit_form(
        driver,
        name="Alan Turing",
        email="abc",  # geçersiz
        phone="123",
        subject="Invalid email test",
        description="Testing invalid email handling."
    )
    time.sleep(2)
    assert SUCCESS_TEXT not in driver.page_source


# 3️⃣ Boş zorunlu alanlarla gönderim --------------------------------------------------------

def test_empty_required_fields(driver):
    _open_contact_page(driver)
    _submit_form(
        driver,
        name="",
        email="",
        phone="",
        subject="",
        description="Test"
    )
    time.sleep(2)
    assert SUCCESS_TEXT not in driver.page_source


# 4️⃣ Aşırı uzun metin gönderimi ------------------------------------------------------------

def test_long_description_submission(driver):
    _open_contact_page(driver)
    long_text = "A" * 10000  # 10.000 karakter
    _submit_form(
        driver,
        name="Grace Hopper",
        email="grace@navy.mil",
        phone="5551234",
        subject="Very long description",
        description=long_text
    )
    time.sleep(2)
    assert SUCCESS_TEXT not in driver.page_source  # sistem engelleyebilir


# 5️⃣ Özel karakter / SQL injection denemesi -----------------------------------------------

def test_sql_injection_attempt(driver):
    _open_contact_page(driver)
    _submit_form(
        driver,
        name="'; DROP TABLE users;--",
        email="injection@test.com",
        phone="666",
        subject="Injection test",
        description="Trying SQL injection"
    )
    time.sleep(2)
    assert SUCCESS_TEXT not in driver.page_source


# 6️⃣ Sayfa yenileme sonrasında alanların sıfırlanması --------------------------------------

def test_refresh_clears_form(driver):
    _open_contact_page(driver)
    _submit_form(
        driver,
        name="Refresh Test",
        email="refresh@test.com",
        phone="111",
        subject="Refresh",
        description="Will refresh page"
    )
    # Sayfa yenile
    driver.refresh()
    WebDriverWait(driver, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, "name")))
    assert driver.find_element(By.ID, "name").get_attribute("value") == ""
    assert driver.find_element(By.ID, "email").get_attribute("value") == ""


# 7️⃣ Sadece boşluk karakterleri ile gönderim -----------------------------------------------

def test_whitespace_only_submission(driver):
    _open_contact_page(driver)
    spaces = "   "
    _submit_form(
        driver,
        name=spaces,
        email=spaces,
        phone=spaces,
        subject=spaces,
        description=spaces
    )
    time.sleep(2)
    assert SUCCESS_TEXT not in driver.page_source
