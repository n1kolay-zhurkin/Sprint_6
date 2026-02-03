import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.main_page import MainPage
from pages.dzen_page import DzenPage
from config import DZEN_URL_PART


@pytest.mark.parametrize("order_button_position", ["top", "bottom"])
def test_logos_redirects(driver, base_url, order_button_position):
    main_page = MainPage(driver, base_url)
    main_page.open()
    main_page.close_cookie()

    wait = WebDriverWait(driver, 10)

    # 1. Переход по кнопке "Заказать"
    main_page.click_order(order_button_position)
    driver.switch_to.window(driver.window_handles[-1])

    # 2. Логотип "Самокат"
    scooter_logo = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "Header_LogoScooter__3lsAR"))
    )
    scooter_logo.click()

    wait.until(lambda d: base_url in d.current_url)
    assert base_url in driver.current_url

    # 3. Логотип "Яндекс"
    yandex_logo = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "Header_LogoYandex__3TSOI"))
    )
    yandex_logo.click()

    driver.switch_to.window(driver.window_handles[-1])
    dzen_page = DzenPage(driver)

    wait.until(lambda d: DZEN_URL_PART in d.current_url)
    assert DZEN_URL_PART in dzen_page.get_url()