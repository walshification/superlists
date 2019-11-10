import unittest

from selenium import webdriver


class BrowserTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_browser_can_navigate_to_site(self):
        self.browser.get("http://localhost:8000")
        assert "Django" in self.browser.title

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()
