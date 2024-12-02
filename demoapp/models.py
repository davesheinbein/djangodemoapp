from django.db import models

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
