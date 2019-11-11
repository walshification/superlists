from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from lists.forms import EMPTY_ITEM_ERROR, ItemForm
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_home_page_renders_home_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "lists/home.html")

    def test_home_page_uses_item_form(self):
        response = self.client.get(reverse("homepage"))
        self.assertIsInstance(response.context["form"], ItemForm)


class ListViewTest(TestCase):
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(f"/lists/{list_.id}/", data={"text": ""})

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(reverse("view_list", args=[list_.id]))
        self.assertTemplateUsed(response, "lists/list.html")

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item 1", list=other_list)
        Item.objects.create(text="other list item 2", list=other_list)

        response = self.client.get(reverse("view_list", args=[correct_list.id]))

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item 1")
        self.assertNotContains(response, "other list item 2")

    def test_passes_correct_list_to_template(self):
        List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(reverse("view_list", args=[correct_list.id]))
        self.assertEqual(response.context["list"], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            reverse("view_list", args=[correct_list.id]),
            data={"text": "A new item for an existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_post_redirects_to_list_view(self):
        List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            reverse("view_list", args=[correct_list.id]),
            data={"text": "A new item for an existing list"},
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def test_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_templates(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lists/list.html")

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(reverse("view_list", args=[list_.id]))
        self.assertIsInstance(response.context["form"], ItemForm)
        self.assertContains(response, 'name="text"')


class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post("/lists/new", data={"text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post(
            reverse("new_list"), data={"text": "A new list item"}
        )
        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("view_list", args=[new_list.id]))

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post(reverse("new_list"), data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lists/home.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post(reverse("new_list"), data={"text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post(reverse("new_list"), data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lists/home.html")

    def test_validation_errors_are_shown_on_the_home_page(self):
        response = self.client.post(reverse("new_list"), data={"text": ""})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_the_template(self):
        response = self.client.post(reverse("new_list"), data={"text": ""})
        self.assertIsInstance(response.context["form"], ItemForm)
