import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

questions_data = [
    (
        "Сколько это стоит? И как оплатить?",
        "Сутки — 400 рублей. Оплата курьеру — наличными или картой."
    ),
    (
        "Хочу сразу несколько самокатов! Так можно?",
        "Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями, можете просто сделать несколько заказов — один за другим."
    ),
    (
        "Как рассчитывается время аренды?",
        "Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня. Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30."
    ),
    (
        "Можно ли заказать самокат прямо на сегодня?",
        "Только начиная с завтрашнего дня. Но скоро станем расторопнее."
    ),
    (
        "Можно ли продлить заказ или вернуть самокат раньше?",
        "Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010."
    ),
    (
        "Вы привозите зарядку вместе с самокатом?",
        "Самокат приезжает к вам с полной зарядкой. Этого хватает на восемь суток — даже если будете кататься без передышек и во сне. Зарядка не понадобится."
    ),
    (
        "Можно ли отменить заказ?",
        "Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои."
    ),
    (
        "Я жизу за МКАДом, привезёте?",
        "Да, обязательно. Всем самокатов! И Москве, и Московской области."
    )
]

class MainPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.COOKIE_BTN = (By.ID, "rcc-confirm-button")
        self.QUESTIONS = (By.CSS_SELECTOR, ".accordion__button")
        self.ANSWERS = (By.CSS_SELECTOR, ".accordion__panel")

    def open(self):
        self.driver.get(self.base_url)

    def close_cookie(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.COOKIE_BTN)
            ).click()
        except:
            pass

    def click_question(self, question_text):
        wait = WebDriverWait(self.driver, 10)
        questions = wait.until(EC.presence_of_all_elements_located(self.QUESTIONS))
        for question in questions:
            if question_text in question.text:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", question)
                ActionChains(self.driver).move_to_element(question).click().perform()
                return
        raise Exception(f"Вопрос '{question_text}' не найден на странице")

    def get_answer_text(self, question_text):
        wait = WebDriverWait(self.driver, 10)
        questions = wait.until(EC.presence_of_all_elements_located(self.QUESTIONS))
        answers = wait.until(EC.presence_of_all_elements_located(self.ANSWERS))

        for i, question in enumerate(questions):
            if question_text in question.text:
                # Ждем, пока ответ станет видимым
                wait.until(EC.visibility_of(answers[i]))
                return answers[i].text
        raise Exception(f"Ответ для вопроса '{question_text}' не найден")

@pytest.mark.parametrize("question, answer", questions_data)
def test_questions(driver, base_url, question, answer):
    page = MainPage(driver, base_url)
    page.open()
    page.close_cookie()
    page.click_question(question)
    actual_answer = page.get_answer_text(question)
    assert actual_answer == answer