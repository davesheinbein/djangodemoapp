from django.test import TestCase
from .models import HomePage, AboutPage, ContactPage  # Import models

class HomePageTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating a HomePage instance.
        """
        HomePage.objects.create(title="Home Title", content="Home Content")

    def test_home_page_str(self):
        """
        Test the string representation of the HomePage model.
        """
        home_page = HomePage.objects.get(title="Home Title")
        self.assertEqual(str(home_page), "Home Title")

class AboutPageTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating an AboutPage instance.
        """
        AboutPage.objects.create(title="About Title", content="About Content")

    def test_about_page_str(self):
        """
        Test the string representation of the AboutPage model.
        """
        about_page = AboutPage.objects.get(title="About Title")
        self.assertEqual(str(about_page), "About Title")

class ContactPageTestCase(TestCase):  # New test case
    def setUp(self):
        """
        Set up the test case by creating a ContactPage instance.
        """
        ContactPage.objects.create(title="Contact Title", content="Contact Content")

    def test_contact_page_str(self):
        """
        Test the string representation of the ContactPage model.
        """
        contact_page = ContactPage.objects.get(title="Contact Title")
        self.assertEqual(str(contact_page), "Contact Title")

