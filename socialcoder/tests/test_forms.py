from django.test import SimpleTestCase
from socialcoder.forms import ResponseForm, CategoryForm, PostForm

class TestForms(SimpleTestCase):

    def test_response_form_valid_data(self):
        form = ResponseForm(data={
            'code': '<p>hello world</p>',

        })
        self.assertTrue(form.is_valid())

    def test_response_form_no_data(self):
        form = ResponseForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_category_form_valid_data(self):
        form = CategoryForm(data={
            'name': 'Python',
            'image': 'folder/python.jpg',
            'description': 'description of Python programming language',

        })
        self.assertTrue(form.is_valid())

    def test_category_form_no_data(self):
        form = CategoryForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_post_form_valid_data(self):
        form = PostForm(data={
            'title': 'Why do...',
            'code': 'code',
        })
        self.assertTrue(form.is_valid())
