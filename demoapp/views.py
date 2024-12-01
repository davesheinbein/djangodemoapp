from django.http import HttpResponse

def home(request):
    return HttpResponse("Hi there! This is the Home page.")

def about(request):
    return HttpResponse("Hi there! This is the About page.")
