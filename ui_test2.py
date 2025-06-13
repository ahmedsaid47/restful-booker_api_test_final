import time
from datetime import datetime, timedelta

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = "https://automationintesting.online/"
WAIT = 20
POLL = 0.5


# --------------------------------------------------------------------------- #
# Yardımcı fonksiyonlar                                                       #
# --------------------------------------------------------------------------- #
def _open_booking_section(drv):
    """Ana sayfayı aç → Booking bölümüne kadar kaydır."""
    drv.get(BASE)
    wait = WebDriverWait(drv, WAIT, POLL)
    booking_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Booking")))
    drv.execute_script("arguments[0].scrollIntoView(true);", booking_link)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".booking-card")))


def _set_date(inp_el, offset_days: int):
    """Bugünden offset kadar sonraki tarihi DD/MM/YYYY formatında yaz."""
    date_str = (datetime.today().date() + timedelta(days=offset_days)).strftime("%d/%m/%Y")
    inp_el.click()
    inp_el.send_keys(Keys.CONTROL, "a", Keys.DELETE, date_str, Keys.TAB)


def _pick_dates(drv, checkin_offset=1, checkout_offset=2):
    """Booking kartındaki tarih inputlarını doldur."""
    inputs = drv.find_elements(By.CSS_SELECTOR, ".booking-card input.form-control")
    assert len(inputs) >= 2, "Tarih inputları bulunamadı"
    _set_date(inputs[0], checkin_offset)
    _set_date(inputs[1], checkout_offset)


def _click_check_availability(drv):
    btn = drv.find_element(By.XPATH, "//button[normalize-space()='Check Availability']")
    drv.execute_script("arguments[0].scrollIntoView(true);", btn)
    btn.click()


def _assert_success(drv):
    """/reservation/ sayfasına geçtiyse veya oda kartı varsa başarılı say."""
    WebDriverWait(drv, WAIT).until(
        lambda d: "/reservation/" in d.current_url
        or d.find_elements(By.CSS_SELECTOR, ".room-card")
    )


# --------------------------------------------------------------------------- #
# PyTest fixture                                                              #
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="session")
def driver():
    opts = webdriver.ChromeOptions()
    # opts.add_argument("--headless=new")  # arka planda çalıştırmak istersen aç
    drv = webdriver.Chrome(options=opts)
    drv.maximize_window()
    yield drv
    drv.quit()


# --------------------------------------------------------------------------- #
# Test senaryoları                                                            #
# --------------------------------------------------------------------------- #
def test_booking_success(driver):
    """Geçerli tarihlerle arama – odalar listelenmeli veya /reservation/ sayfası açılmalı."""
    _open_booking_section(driver)
    _pick_dates(driver, checkin_offset=7, checkout_offset=10)
    _click_check_availability(driver)
    _assert_success(driver)


def test_booking_invalid_dates(driver):
    """Check-out, Check-in’den önceyse hata mesajı HTML içinde görünmeli."""
    _open_booking_section(driver)
    _pick_dates(driver, checkin_offset=10, checkout_offset=7)  # geçersiz tarih
    _click_check_availability(driver)
    time.sleep(1)  # animasyonlu mesaj gecikmesin diye

    assert "Check out must be after check in" in driver.page_source
