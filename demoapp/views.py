import logging
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST, require_GET
from .forms import VisitorForm
from .models import Visitor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test

logger = logging.getLogger(__name__)

def error_404_view(request, exception):
    logger.info("request", request)
    logger.info("exception", exception)
    return render(request, '404.html')

@cache_page(60 * 15)  # Cache the home view for 15 minutes
def home(request):
    try:
        logger.info("Home view accessed")
        return render(request, 'home.html')
    except Exception as e:
        logger.error(f"Error rendering home view: {e}", exc_info=True)
        return HttpResponseNotFound("Page not found due to an internal error. Please try again later.")

@cache_page(60 * 15)  # Cache the contact view for 15 minutes
def contact(request):
    try:
        logger.info("Contact view accessed")
        if request.method == 'POST' and request.user.is_authenticated:
            form = VisitorForm(request.POST)
            if form.is_valid():
                visitor = form.save(commit=False)
                visitor.created_by = request.user
                visitor.save()
                form = VisitorForm()  # Clear the form after submission
                return render(request, 'contact.html', {'form': form, 'success': True})
        else:
            form = VisitorForm() if request.user.is_authenticated else None
        return render(request, 'contact.html', {'form': form})
    except Exception as e:
        logger.error(f"Error rendering contact view: {e}")
        return HttpResponseNotFound("Page not found")

@cache_page(60 * 15)  # Cache the about view for 15 minutes
def about(request):
    try:
        logger.info("About view accessed")
        return render(request, 'about.html')
    except Exception as e:
        logger.error(f"Error rendering about view: {e}")
        return HttpResponseNotFound("Page not found")

@cache_page(60 * 15)  # Cache the visitors view for 15 minutes
@login_required
def visitors(request):
    try:
        logger.info("Visitors view accessed")
        visitors_list = Visitor.objects.all()
        logger.info(f"visitors_list: {visitors_list}")
        return render(request, 'visitors.html', {'visitors': visitors_list})
    except Exception as e:
        logger.error(f"Error rendering visitors view: {e}")
        return HttpResponseNotFound("Page not found")

@require_GET
@login_required
def edit_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if request.user != visitor.created_by and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit this visitor.")
    form = VisitorForm(instance=visitor)
    return render(request, 'edit_visitor.html', {'form': form, 'visitor': visitor})

@require_POST
@login_required
def update_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if request.user != visitor.created_by and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'You do not have permission to update this visitor.'})
    form = VisitorForm(request.POST, instance=visitor)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})

@require_POST
@login_required
def delete_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to delete this visitor.")
    visitor.delete()
    return redirect('visitors')

@require_POST
@login_required
def register(request):
    try:
        logger.info("Register view accessed")
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')
        else:
            form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})
    except Exception as e:
        logger.error(f"Error rendering register view: {e}", exc_info=True)
        return HttpResponseNotFound("Page not found due to an internal error. Please try again later.")

@user_passes_test(lambda u: u.is_staff)
def admin_view(request):
    # Admin-specific view logic
    return render(request, 'admin_view.html')