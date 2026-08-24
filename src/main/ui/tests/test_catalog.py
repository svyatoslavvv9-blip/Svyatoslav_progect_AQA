from playwright.sync_api import expect
from pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps

def test_count_catalog(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")
    assert steps.get_products_count() == 6

def test_sorted_by_name(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.sort_items('az')
    assert steps.get_product_names() == sorted(steps.get_product_names())

    steps.sort_items('za')
    assert steps.get_product_names() == sorted(steps.get_product_names(), reverse=True)

def test_sorted_by_price(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.sort_items('lohi')
    assert steps.get_product_prices() == sorted(steps.get_product_prices())

    steps.sort_items('hilo')
    assert steps.get_product_prices() == sorted(steps.get_product_prices(), reverse=True)

def test_add_to_cart(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")
    button = steps.add_to_cart("Sauce Labs Bike Light")
    expect(button).to_have_text("Remove")
    assert steps.get_cart_count() == 1

def test_add_to_cart_and_remove(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Bike Light")

    assert steps.get_cart_count() == 1

    steps.remove_from_cart("Sauce Labs Bike Light")

    assert steps.get_cart_count() == 0

def test_product_details_onesie(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    name, price, detail_name, detail_price = steps.open_product_details("Sauce Labs Onesie")
    assert name == detail_name
    assert price == detail_price

def test_product_details_jacket(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    name, price, detail_name, detail_price = steps.open_product_details("Jacket Light")
    assert name == detail_name
    assert price == detail_price

def test_remove_item_from_catalog(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.remove_from_cart("Test.allTheThings() T-shirt (Red)")

def test_remove_item_from_cart_second_version(auth_page):
    product_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Onesie")
    product_button = product_card.locator('[data-test="add-to-cart-sauce-labs-onesie"]')
    product_button.click()

    remove_button = product_card.locator('[data-test="remove-sauce-labs-onesie"]')
    assert remove_button.is_visible(), "Кнопка не появилась"

    remove_button.click()

    add_button = product_card.locator('[data-test="add-to-cart-sauce-labs-onesie"]')
    assert add_button.is_visible(), "Кнопка add to cart не вернулась после удаления"