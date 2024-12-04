from django.test import TestCase, Client
from django.urls import reverse
from .models import HomePage, AboutPage, ContactPage, Visitor  # Import models
from django.contrib.auth.models import User

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

class ContactPageTestCase(TestCase):
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

class VisitorTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating a Visitor instance.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        Visitor.objects.create(
            name="Visitor Name",
            email="visitor@example.com",
            phone="1234567890",
            favorite_thing_to_cook="Pizza",
            additional_comments="No comments",
            created_by=user
        )

    def test_visitor_str(self):
        """
        Test the string representation of the Visitor model.
        """
        visitor = Visitor.objects.get(name="Visitor Name")
        self.assertEqual(str(visitor), "Visitor Name")

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_contact_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_visitors_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('visitors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'visitors.html')

