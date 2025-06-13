# bnb_ui_tests/conftest.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# ───────────────────────── Tarayıcı FIXTURE'I ─────────────────────────
@pytest.fixture
def browser():
    """Her test için yeni Chrome örneği aç / kapat."""
    opts = Options()
    # Başsız çalıştırmak istersen yorum satırını aç:
    # opts.add_argument("--headless=new")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )
    driver.maximize_window()
    driver.implicitly_wait(10)          # global basit wait

    yield driver                        # -----> testler burada çalışır

    driver.quit()                       # teardown


# ───────────── HTML RAPORU VE METADATA (pytest-html + pytest-metadata) ────────────
def pytest_configure(config):
    # pytest - html parametresi verilmediyse varsayılan adı ayarla
    if config.option.htmlpath is None:
        config.option.htmlpath = "report.html"

    # metadata eklentisi yüklüyse tabloya ekstra alanlar ekle
    if hasattr(config, "_metadata"):
        config._metadata.update({
            "Project":  "AutomationInTesting UI",
            "Browser":  "Chrome",
        })


# ───────────────────── Test Fail'de Ekran Görüntüsü Ekle ─────────────────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Test 'call' aşaması FAILED ise:
      • screenshots/ klasörüne PNG kaydet
      • pytest-html raporuna göm
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("browser")     # fixture varsa
        if driver:
            ss_dir = os.path.join(item.config.rootpath, "screenshots")
            os.makedirs(ss_dir, exist_ok=True)

            file_name = f"{item.name}.png".replace(os.sep, "_")
            file_path = os.path.join(ss_dir, file_name)
            driver.save_screenshot(file_path)

            # pytest-html eklentisi yüklüyse rapora ekle
            if item.config.pluginmanager.hasplugin("html"):
                from pytest_html import extras
                rep.extras = getattr(rep, "extras", []) + [extras.png(file_path)]
