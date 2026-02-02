from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class OrderPage:
    def __init__(self, driver):
        self.driver = driver

    # Локаторы формы "Ваши данные"
    NAME = (By.XPATH, "//input[@placeholder='* Имя']")
    SURNAME = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO = (By.XPATH, "//input[@placeholder='* Станция метро']")
    METRO_OPTION = (By.CSS_SELECTOR, ".select-search__row")
    PHONE = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    # Локаторы формы "Про аренду"
    DATE_FIELD = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    CALENDAR_DAY = (By.CSS_SELECTOR, ".react-datepicker__day--selected, .react-datepicker__day:not(.react-datepicker__day--outside-month)")
    RENT_PERIOD_FIELD = (By.CSS_SELECTOR, ".Dropdown-placeholder")  # поле "Срок аренды"
    RENT_PERIOD_OPTION = (By.CSS_SELECTOR, ".Dropdown-option")       # варианты аренды
    COLOR_BLACK = (By.ID, "black")
    COLOR_GREY = (By.ID, "grey")
    COMMENT_FIELD = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")

    # Кнопка "Заказать" в форме аренды
    ORDER_BUTTON = (By.XPATH, "//div[contains(@class,'Order_Content')]//button[text()='Заказать']")

    # Модальное окно подтверждения
    CONFIRM_YES = (By.XPATH, "//button[text()='Да']")
    CONFIRMATION_TEXT = (By.CLASS_NAME, "Order_ModalHeader__3FDaJ")  # окно "Заказ оформлен"

    # Методы
    def fill_order_form(self, data):
        wait = WebDriverWait(self.driver, 10)

        wait.until(EC.element_to_be_clickable(self.NAME)).send_keys(data["name"])
        wait.until(EC.element_to_be_clickable(self.SURNAME)).send_keys(data["surname"])
        wait.until(EC.element_to_be_clickable(self.ADDRESS)).send_keys(data["address"])

        metro_field = wait.until(EC.element_to_be_clickable(self.METRO))
        metro_field.click()
        metro_field.send_keys(data["metro"])
        wait.until(EC.element_to_be_clickable(self.METRO_OPTION)).click()

        wait.until(EC.element_to_be_clickable(self.PHONE)).send_keys(data["phone"])

    def click_next(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

    def fill_rent_form(self, rent_days=1, color="black", comment="Позвонить за 5 минут"):
        wait = WebDriverWait(self.driver, 10)
        actions = ActionChains(self.driver)

        # Выбор даты
        date_field = wait.until(EC.element_to_be_clickable(self.DATE_FIELD))
        date_field.click()
        wait.until(EC.element_to_be_clickable(self.CALENDAR_DAY)).click()

        # Срок аренды
        rent_field = wait.until(EC.element_to_be_clickable(self.RENT_PERIOD_FIELD))
        actions.move_to_element(rent_field).click().perform()
        rent_options = wait.until(EC.presence_of_all_elements_located(self.RENT_PERIOD_OPTION))
        rent_options[min(rent_days-1, len(rent_options)-1)].click()

        # Цвет самоката
        color_elem = self.COLOR_BLACK if color.lower() == "black" else self.COLOR_GREY
        wait.until(EC.element_to_be_clickable(color_elem)).click()

        # Комментарий
        wait.until(EC.element_to_be_clickable(self.COMMENT_FIELD)).send_keys(comment)

    def click_order(self):
        wait = WebDriverWait(self.driver, 10)

        # Скролл вниз до кнопки, чтобы избежать MoveTargetOutOfBounds
        order_btn = wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", order_btn)

        # Клик по кнопке "Заказать"
        order_btn.click()

        # Подтверждаем модальное окно "Хотите оформить заказ?"
        wait.until(EC.element_to_be_clickable(self.CONFIRM_YES)).click()

    # Вспомогательные методы
    def get_confirmation_text(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.visibility_of_element_located(self.CONFIRMATION_TEXT)).text

