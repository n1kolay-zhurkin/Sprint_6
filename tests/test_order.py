import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.order_page import OrderPage

# Тестовые данные
order_data = [
    {
        "name": "Иван",
        "surname": "Иванов",
        "address": "ул. Пушкина, 10",
        "metro": "Пушкинская",
        "phone": "+79991112233"
    },
    {
        "name": "Мария",
        "surname": "Петрова",
        "address": "ул. Ленина, 15",
        "metro": "Ленинская",
        "phone": "+79994445566"
    }
]

# Точки входа для заказа
entry_points = ["top", "bottom"]

# Тест
@pytest.mark.parametrize("data", order_data)
@pytest.mark.parametrize("entry", entry_points)
def test_order_scooter(driver, base_url, data, entry):
    # Открываем главную страницу
    main_page = MainPage(driver, base_url)
    main_page.open()
    main_page.close_cookie()

    # Клик по кнопке заказа
    main_page.click_order(entry)

    # Переключение на новую вкладку /order
    driver.switch_to.window(driver.window_handles[-1])

    # Инициализация страницы заказа
    order_page = OrderPage(driver)

    # Форма "Ваши данные"
    order_page.fill_order_form(data)
    order_page.click_next()

    # Форма "Про аренду"
    rent_days = 3        # пример: выбрать 3 дня аренды
    color = "black"      # цвет самоката
    comment = "Позвонить за 5 минут"

    order_page.fill_rent_form(rent_days=rent_days, color=color, comment=comment)

    # Клик "Заказать" и подтверждение
    order_page.click_order()

    # Проверка успешного оформления заказа
    confirmation_text = order_page.get_confirmation_text()
    assert "Заказ оформлен" in confirmation_text
    
