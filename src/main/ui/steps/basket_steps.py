import allure
from ui.pages.basket_page import BasketPage
from playwright.sync_api import Page, expect

class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket = BasketPage(page)

    @allure.step("Открываем корзину")
    def open_cart(self):
        self.basket.open_cart()
        return self

    @allure.step("Checkout click()")
    def checkout(self):
        self.basket.checkout()
        return self

    @allure.step("Удаляем товар из корзины {product_name}")
    def remove_item(self, product_name):
        self.basket.remove_item(product_name)
        return self

    @allure.step("Проверяем наличие товара в корзине {product_name}")
    def expect_item_in_cart(self, product_name):
        return self.basket.expect_item_in_cart(product_name)

    @allure.step("Проверяем отсутствие товара в корзине {product_name}")
    def expect_item_not_in_cart(self, product_name):
        return self.basket.expect_item_not_in_cart(product_name)

    @allure.step("Возвращаем имена товаров")
    def get_item_names(self) -> list[str]:
        return self.basket.get_item_names()

    @allure.step("Возвращаем стоимость товаров")
    def get_item_price(self) -> list[float]:
        return self.basket.get_item_prices()

    @allure.step("Возвращаем итоговую стоимость")
    def get_items_total_price(self) -> float:
        return self.basket.get_items_total_price()