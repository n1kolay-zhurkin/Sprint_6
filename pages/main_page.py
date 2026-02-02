from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class MainPage:
    # Локаторы кнопок "Заказать"
    ORDER_TOP_BTN = (By.CSS_SELECTOR, ".Header_Nav__AGCXC .Button_Button__ra12g")       # верхняя кнопка
    ORDER_BOTTOM_BTN = (By.CSS_SELECTOR, ".Home_FinishButton__1_cWm .Button_Button__ra12g")  # нижняя кнопка

    # Локаторы FAQ и куки
    COOKIE_BTN = (By.ID, "rcc-confirm-button")
    QUESTIONS = (By.CSS_SELECTOR, ".accordion__button")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    # Основные методы
    def open(self):
        self.driver.get(self.base_url)

    def close_cookie(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.COOKIE_BTN)
            ).click()
        except:
            pass

    # Методы для FAQ
    def click_question(self, question_text):
        wait = WebDriverWait(self.driver, 15)
        questions = wait.until(
            EC.presence_of_all_elements_located(self.QUESTIONS)
        )

        for q in questions:
            if q.text.strip() == question_text:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", q
                )
                q.click()
                return q

        raise Exception(f"Вопрос '{question_text}' не найден")

    def get_answer_text(self, question_text):
        question = self.click_question(question_text)

        answer = question.find_element(
            By.XPATH, "./ancestor::div[@class='accordion__item']//div[@class='accordion__panel']"
        )

        WebDriverWait(self.driver, 15).until(
            lambda d: answer.is_displayed() and answer.text.strip() != ""
        )

        return answer.text.strip()

    # Метод для тестов заказа
    def click_order(self, position="top"):
        wait = WebDriverWait(self.driver, 10)
        actions = ActionChains(self.driver)

        if position == "top":
            btn = wait.until(EC.element_to_be_clickable(self.ORDER_TOP_BTN))
        elif position == "bottom":
            btn = wait.until(EC.element_to_be_clickable(self.ORDER_BOTTOM_BTN))
            # Скролл вниз для нижней кнопки
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        else:
            raise ValueError(f"Unknown entry point: {position}")

        actions.move_to_element(btn).click().perform()
        