import allure
from ui.pages.basket_page import BasketPage
from playwright.sync_api import Page, expect

class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket = BasketPage(page)

    @allure.step("Открываем корзину")
    def open_cart(self):
        self.open_cart