from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box.
        self.browser.get(self.server_url)
        self.get_form().submit()

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank.
        error = self.browser.find_element_by_css_selector(".has-error")
        self.assertEqual(error.text, "You can't have an empty list item")

        # She tries again with some text for the item, which now works.
        self.get_item_input_box().send_keys("Buy milk")
        self.get_form().submit()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "todo-1"))
        )
        self.check_for_row_in_list_table("1: Buy milk")

        # Perversely, she now decides to submit a second blank list item.
        self.get_form().submit()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".has-error"))
        )

        # She receives a similar warning on the list page.
        # self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector(".has-error")
        self.assertEqual(error.text, "You can't have an empty list item")

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys("Make tea")
        self.get_form().submit()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "todo-2"))
        )
        self.check_for_row_in_list_table("2: Make tea")
