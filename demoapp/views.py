import logging
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from .forms import VisitorForm, LoginForm
from .models import Visitor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)  # Session expires when the browser is closed
        auth_login(self.request, form.get_user())  # Log the user in
        return super().form_valid(form)

def error_404_view(request, exception):
    logger.info("request", request)
    logger.info("exception", exception)
    return render(request, '404.html')

def home(request):
    try:
        logger.info("Home view accessed")
        visitors = Visitor.objects.all()
        return render(request, 'home.html', {'visitors': visitors})
    except Exception as e:
        logger.error(f"Error rendering home view: {e}", exc_info=True)
        return HttpResponseNotFound("Page not found due to an internal error. Please try again later.")

def contact(request):
    try:
        logger.info("Contact view accessed")
        visitors = Visitor.objects.all()
        if request.method == 'POST' and request.user.is_authenticated:
            form = VisitorForm(request.POST)
            if form.is_valid():
                visitor = form.save(commit=False)
                if request.user.is_authenticated:
                    if request.user.is_staff:
                        try:
                            admin_user = User.objects.get(email='admin@example.com')
                        except User.DoesNotExist:
                            logger.error("Admin user with email 'admin@example.com' does not exist.")
                            return HttpResponseNotFound("Admin user does not exist.")
                        visitor.created_by = admin_user
                    else:
                        visitor.created_by = request.user
                visitor.save()
                form = VisitorForm()  # Clear the form after submission
                return render(request, 'contact.html', {'form': form, 'success': True, 'visitors': visitors})
        else:
            form = VisitorForm() if request.user.is_authenticated else None
        return render(request, 'contact.html', {'form': form, 'visitors': visitors})
    except Exception as e:
        logger.error(f"Error rendering contact view: {e}")
        return HttpResponseNotFound("Page not found")

def about(request):
    try:
        logger.info("About view accessed")
        visitors = Visitor.objects.all()
        return render(request, 'about.html', {'visitors': visitors})
    except Exception as e:
        logger.error(f"Error rendering about view: {e}")
        return HttpResponseNotFound("Page not found")

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

@require_http_methods(["GET", "POST"])
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

@login_required
def ajax_edit_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if request.user != visitor.created_by and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit this visitor.")
    if request.method == 'POST':
        form = VisitorForm(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = VisitorForm(instance=visitor)
        html = render_to_string('edit_visitor_modal.html', {'form': form, 'visitor': visitor}, request=request)
        return JsonResponse({'success': True, 'html': html})

@login_required
@require_POST
def ajax_update_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if request.user != visitor.created_by and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'You do not have permission to update this visitor.'})
    form = VisitorForm(request.POST, instance=visitor)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def ajax_delete_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'You do not have permission to delete this visitor.'})
    visitor.delete()
    return JsonResponse({'success': True})