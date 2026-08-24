from playwright.sync_api import expect
import pytest
from pages.basket_page import BasketPage
from pages.catalog_page import CatalogPage
from pages.check_out_page import CheckOutPage


def test_add_item_and_check_in_cart(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")

def test_add_item_and_check_in_cart_second_version(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

def test_remove_item_from_cart(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")

    basket.remove_item("Sauce Labs Fleece Jacket")
    basket.expect_item_not_in_cart("Sauce Labs Fleece Jacket")

def test_remove_item_from_cart_second_version(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Test.allTheThings() T-shirt (Red)")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Test.allTheThings() T-shirt (Red)")

    basket.remove_item("Sauce Labs Fleece Jacket")
    basket.remove_item("Test.allTheThings() T-shirt (Red)")

    basket.expect_item_not_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_not_in_cart("Test.allTheThings() T-shirt (Red)")

def test_e2e_full(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)
    checkout = CheckOutPage(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

    basket_total = basket.get_items_total_price()

    basket.checkout()
    checkout.start_checkout(first_name="Test", last_name="User", postal_code="12345")

    checkout_total = checkout.get_item_total_after_continue()
    assert checkout_total == basket_total, "Сумма товаров не совпадает с корзиной"

def test_checkout_without_items(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)
    checkout = CheckOutPage(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    basket.open_cart()
    items = basket.get_item_names()
    assert len(items) == 0, "Корзина не пуста"

    basket.checkout()
    checkout.start_checkout(first_name="NewUser", last_name="Nrk", postal_code="")
    error_text = checkout.get_error_text()
    assert error_text != "", "Ожидалась ошибка при оформлении пустой корзины"