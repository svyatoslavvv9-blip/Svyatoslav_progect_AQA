import allure
from ui.pages.check_out_page import CheckOutPage
from playwright.sync_api import Page, expect

class CheckOutSteps:
    def __init__(self, page: Page):
        self.page = page
        self.checkout = CheckOutPage(page)

    @allure.step("Начинаем checkout: {first_name} {last_name}, {postal_code}")
    def start_checkout(self, first_name : str, last_name : str, postal_code : str):
        self.checkout.start_checkout(first_name, last_name, postal_code)
        return self

    @allure.step("Заканчиваем checkout")
    def finish_checkout(self):
        self.checkout.finish_checkout()
        return self

    @allure.step("Получаем тест ошибки")
    def get_error_text(self) -> str:
        return self.checkout.get_error_text()

    @allure.step("Получаем общее количество элементов после продолжение")
    def get_item_total_after_continue(self) -> float:
        return self.checkout.get_item_total_after_continue()

