from django.db import models
from django.contrib.auth.models import User

class HomePage(models.Model):
    """
    Model representing the home page content.
    """
    title = models.CharField(max_length=100)  # Title of the home page
    content = models.TextField()  # Content of the home page

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
    title = models.CharField(max_length=100)  # Title of the about page
    content = models.TextField()  # Content of the about page

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
    title = models.CharField(max_length=100)  # Title of the contact page
    content = models.TextField()  # Content of the contact page

    def __str__(self):
        """
        String representation of the ContactPage model.
        """
        return self.title

    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Pages"

class Visitor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    favorite_thing_to_cook = models.CharField(max_length=255)
    additional_comments = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visitors', default=1)  # Default user ID

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Visitor"
        verbose_name_plural = "Visitors"
