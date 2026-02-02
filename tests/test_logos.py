import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.main_page import MainPage
from pages.dzen_page import DzenPage

@pytest.mark.parametrize("order_button_position", ["top", "bottom"])
def test_logos_redirects(driver, base_url, order_button_position):
    main_page = MainPage(driver, base_url)
    main_page.open()
    main_page.close_cookie()

    wait = WebDriverWait(driver, 10)

    # 1. Переход по кнопке "Заказать"
    main_page.click_order(order_button_position)

    # Переключаемся на страницу "Для кого самокат"
    driver.switch_to.window(driver.window_handles[-1])
    wait.until(lambda d: d.title != "")

    # 2. Проверка логотипа "Самокат"
    scooter_logo = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "Header_LogoScooter__3lsAR"))
    )
    scooter_logo.click()

    # Должны вернуться на стартовую страницу Самоката
    wait.until(lambda d: base_url in d.current_url)
    assert base_url in driver.current_url, f"Не вернулись на главную страницу Самоката, получили: {driver.current_url}"

    # 3. Проверка логотипа "Яндекса"
    yandex_logo = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "Header_LogoYandex__3TSOI"))
    )
    yandex_logo.click()

    # Переключаемся на новую вкладку
    driver.switch_to.window(driver.window_handles[-1])
    dzen_page = DzenPage(driver)

    # Проверяем, что URL содержит dzen.ru (учитываем редирект через SSO)
    wait.until(lambda d: "dzen.ru" in d.current_url)
    assert "dzen.ru" in driver.current_url, f"Не открылась главная страница Дзена, получили: {driver.current_url}"