from django.db import models
from django.contrib.auth.models import User

class HomePage(models.Model):
    """
    Model representing the home page content.
    """
    title = models.CharField(max_length=100, verbose_name="Title")  # Title of the home page
    content = models.TextField(verbose_name="Content")  # Content of the home page

    def __str__(self):
        """
        String representation of the HomePage model.
        """
        return self.title

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

class AboutPage(models.Model):
    """
    Model representing the about page content.
    """
    title = models.CharField(max_length=100, verbose_name="Title")  # Title of the about page
    content = models.TextField(verbose_name="Content")  # Content of the about page

    def __str__(self):
        """
        String representation of the AboutPage model.
        """
        return self.title

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Pages"

class ContactPage(models.Model):  
    """
    Model representing the contact page content.
    """
    title = models.CharField(max_length=100, verbose_name="Title")  # Title of the contact page
    content = models.TextField(verbose_name="Content")  # Content of the contact page

    def __str__(self):
        """
        String representation of the ContactPage model.
        """
        return self.title  # Fix syntax error

    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Pages"

class Visitor(models.Model):
    """
    Model representing a visitor.
    """
    name = models.CharField(max_length=100, verbose_name="Name")  # Visitor's name
    email = models.EmailField(verbose_name="Email")  # Visitor's email
    phone = models.CharField(max_length=15, verbose_name="Phone")  # Visitor's phone number
    favorite_thing_to_cook = models.CharField(max_length=255, verbose_name="Favorite Thing to Cook")  # Visitor's favorite thing to cook
    additional_comments = models.TextField(blank=True, null=True, verbose_name="Additional Comments")  # Additional comments
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visitors', null=True, blank=True, verbose_name="Created By")  # User who created the visitor

    def __str__(self):
        """
        String representation of the Visitor model.
        """
        return self.name  # Fix syntax error

    class Meta:
        verbose_name = "Visitor"
        verbose_name_plural = "Visitors"
