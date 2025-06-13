import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def rezervasyon_yap(thread_id):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        service = Service()  # Chromedriver yolu otomatik
        driver = webdriver.Chrome(service=service, options=options)

        wait = WebDriverWait(driver, 10)
        driver.get("https://automationintesting.online/#/")

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='openBooking']"))).click()

        driver.find_element(By.ID, "room-checkin").clear()
        driver.find_element(By.ID, "room-checkin").send_keys("14/06/2025")
        driver.find_element(By.ID, "room-checkout").clear()
        driver.find_element(By.ID, "room-checkout").send_keys("17/06/2025")

        driver.find_element(By.ID, "firstname").send_keys(f"Test{thread_id}")
        driver.find_element(By.ID, "lastname").send_keys("ThreadUser")
        driver.find_element(By.ID, "email").send_keys(f"thread{thread_id}@test.com")
        driver.find_element(By.ID, "phone").send_keys("123456789")

        driver.find_element(By.CSS_SELECTOR, "button[class*='book-room']").click()

        time.sleep(2)
        if "Booking Successful!" in driver.page_source:
            print(f"[Thread {thread_id}] Rezervasyon başarılı.")
        else:
            print(f"[Thread {thread_id}] Rezervasyon başarısız veya engellendi.")

        driver.quit()

    except Exception as e:
        print(f"[Thread {thread_id}] Hata oluştu: {e}")

if __name__ == "__main__":
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=rezervasyon_yap, args=(i + 1,))
        t.start()
        thread_list.append(t)
        time.sleep(2)  # ⚠️ 2 saniye gecikme ver: Aynı anda çakışmayı önler

    for t in thread_list:
        t.join()

    print("Tüm thread denemeleri tamamlandı.")
