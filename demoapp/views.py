import logging
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from .forms import VisitorForm, LoginForm, ProfileForm, ArticleForm, TagForm, CategoryForm, AuthorForm, BookForm
from .models import Visitor, Profile, Category, Tag, Article, Author, Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

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
        return render(request, 'pages/home.html', {'visitors': visitors})
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
                return render(request, 'pages/contact.html', {'form': form, 'success': True, 'visitors': visitors})
        else:
            form = VisitorForm() if request.user.is_authenticated else None
        return render(request, 'pages/contact.html', {'form': form, 'visitors': visitors})
    except Exception as e:
        logger.error(f"Error rendering contact view: {e}")
        return HttpResponseNotFound("Page not found")

def about(request):
    try:
        logger.info("About view accessed")
        visitors = Visitor.objects.all()
        return render(request, 'pages/about.html', {'visitors': visitors})
    except Exception as e:
        logger.error(f"Error rendering about view: {e}")
        return HttpResponseNotFound("Page not found")

@login_required(login_url='/login/')
def visitors(request):
    try:
        logger.info("Visitors view accessed")
        visitors_list = Visitor.objects.all()
        logger.info(f"visitors_list: {visitors_list}")
        return render(request, 'pages/visitors.html', {'visitors': visitors_list})
    except Exception as e:
        logger.error(f"Error rendering visitors view: {e}")
        return HttpResponseNotFound("Page not found")

@require_GET
@login_required(login_url='/login/')
def edit_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if request.user != visitor.created_by and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit this visitor.")
    form = VisitorForm(instance=visitor)
    return render(request, 'edit_visitor.html', {'form': form, 'visitor': visitor})

@require_POST
@login_required(login_url='/login/')
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
@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
@require_POST
def ajax_update_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if request.user != visitor.created_by and not request.user.is_staff:
        response_data = {'success': False, 'error': 'You do not have permission to update this visitor.'}
        logger.debug(f"ajax_update_visitor response: {response_data}")
        return JsonResponse(response_data)
    form = VisitorForm(request.POST, instance=visitor)
    if form.is_valid():
        form.save()
        response_data = {'success': True, 'visitor': {
            'id': visitor.id,
            'name': visitor.name,
            'email': visitor.email,
            'phone': visitor.phone,
            'favorite_thing_to_cook': visitor.favorite_thing_to_cook,
            'additional_comments': visitor.additional_comments,
        }}
        logger.debug(f"ajax_update_visitor response: {response_data}")
        return JsonResponse(response_data)
    response_data = {'success': False, 'errors': form.errors}
    logger.debug(f"ajax_update_visitor response: {response_data}")
    return JsonResponse(response_data)

@login_required(login_url='/login/')
@require_POST
def ajax_delete_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if not request.user.is_staff:
        response_data = {'success': False, 'error': 'You do not have permission to delete this visitor.'}
        logger.debug(f"ajax_delete_visitor response: {response_data}")
        return JsonResponse(response_data)
    visitor.delete()
    response_data = {'success': True}
    logger.debug(f"ajax_delete_visitor response: {response_data}")
    return JsonResponse(response_data)

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

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
@require_POST
def ajax_update_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if request.user != visitor.created_by and not request.user.is_staff:
        response_data = {'success': False, 'error': 'You do not have permission to update this visitor.'}
        logger.debug(f"ajax_update_visitor response: {response_data}")
        return JsonResponse(response_data)
    form = VisitorForm(request.POST, instance=visitor)
    if form.is_valid():
        form.save()
        response_data = {'success': True, 'visitor': {
            'id': visitor.id,
            'name': visitor.name,
            'email': visitor.email,
            'phone': visitor.phone,
            'favorite_thing_to_cook': visitor.favorite_thing_to_cook,
            'additional_comments': visitor.additional_comments,
        }}
        logger.debug(f"ajax_update_visitor response: {response_data}")
        return JsonResponse(response_data)
    response_data = {'success': False, 'errors': form.errors}
    logger.debug(f"ajax_update_visitor response: {response_data}")
    return JsonResponse(response_data)

@login_required(login_url='/login/')
@require_POST
def ajax_delete_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    if not request.user.is_staff:
        response_data = {'success': False, 'error': 'You do not have permission to delete this visitor.'}
        logger.debug(f"ajax_delete_visitor response: {response_data}")
        return JsonResponse(response_data)
    visitor.delete()
    response_data = {'success': True}
    logger.debug(f"ajax_delete_visitor response: {response_data}")
    return JsonResponse(response_data)

def practice(request):
    logger.info("Practice view accessed")
    profiles = Profile.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    articles = Article.objects.all()
    authors = Author.objects.all()
    books = Book.objects.all()
    return render(request, 'practice/practice.html', {
        'profiles': profiles,
        'categories': categories,
        'tags': tags,
        'articles': articles,
        'authors': authors,
        'books': books,
    })

@login_required(login_url='/login/')
def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, user_id=profile_id)
    if request.user != profile.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit this profile.")
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'profile': {
                'id': profile.user.id,
                'username': profile.user.username,
                'bio': profile.bio,
            }})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProfileForm(instance=profile)
        html = render_to_string('practice/edit_profile.html', {'form': form, 'profile': profile}, request=request)
        return JsonResponse({'success': True, 'html': html})

@csrf_exempt
@require_http_methods(["PUT", "GET"])
def update_profile(request, profile_id):
    profile = get_object_or_404(Profile, user_id=profile_id)
    if request.user != profile.user and not request.user.is_staff:
        response_data = {'success': False, 'error': 'You do not have permission to update this profile'}
        logger.debug(f"update_profile response: {response_data}")
        return JsonResponse(response_data)
    if request.method == 'PUT':
        data = json.loads(request.body)
        form = ProfileForm(data, instance=profile)
        if form.is_valid():
            form.save()
            response_data = {'success': True, 'profile': {
                'id': profile.user.id,
                'username': profile.user.username,
                'bio': profile.bio,
            }}
            logger.debug(f"update_profile response: {response_data}")
            return JsonResponse(response_data)
        response_data = {'success': False, 'errors': form.errors}
        logger.debug(f"update_profile response: {response_data}")
        return JsonResponse(response_data)
    else:
        form = ProfileForm(instance=profile)
        html = render_to_string('practice/update_profile.html', {'form': form, 'profile': profile}, request=request)
        response_data = {'success': True, 'html': html}
        logger.debug(f"update_profile response: {response_data}")
        return JsonResponse(response_data)

@csrf_exempt
@require_http_methods(["DELETE"])
@login_required(login_url='/login/')
def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, user_id=profile_id)
    if request.user != profile.user and not request.user.is_staff:
        response_data = {'success': False, 'error': 'You do not have permission to delete this profile.'}
        logger.debug(f"delete_profile response: {response_data}")
        return JsonResponse(response_data)
    profile.user.delete()
    response_data = {'success': True, 'message': 'Profile deleted successfully'}
    logger.debug(f"delete_profile response: {response_data}")
    return JsonResponse(response_data)

@login_required(login_url='/login/')
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {'success': True}
            logger.debug(f"add_article response: {response_data}")
            return JsonResponse(response_data)
        response_data = {'success': False, 'errors': form.errors}
        logger.debug(f"add_article response: {response_data}")
        return JsonResponse(response_data)
    else:
        form = ArticleForm()
        html = render_to_string('practice/add_article.html', {'form': form}, request=request)
        response_data = {'success': True, 'html': html}
        logger.debug(f"add_article response: {response_data}")
        return JsonResponse(response_data)

@login_required(login_url='/login/')
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    tag.delete()
    return JsonResponse({'success': True})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            response_data = {'success': True, 'message': 'Category added successfully', 'category': {'id': category.id, 'name': category.name}}
            logger.debug(f"add_category response: {response_data}")
            return JsonResponse(response_data)
        response_data = {'success': False, 'errors': form.errors}
        logger.debug(f"add_category response: {response_data}")
        return JsonResponse(response_data)
    else:
        form = CategoryForm()
        html = render_to_string('practice/add_category.html', {'form': form}, request=request)
        response_data = {'success': True, 'html': html}
        logger.debug(f"add_category response: {response_data}")
        return JsonResponse(response_data)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    response_data = {'success': True, 'message': 'Article deleted successfully'}
    logger.debug(f"delete_article response: {response_data}")
    return JsonResponse(response_data)

@login_required(login_url='/login/')
def add_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        username = request.POST.get('username')
        if form.is_valid() and username:
            user = User.objects.create(username=username)
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            response_data = {
                'success': True,
                'profile': {
                    'id': profile.user.id,
                    'username': profile.user.username,
                    'bio': profile.bio,
                }
            }
            logger.debug(f"add_profile response: {response_data}")
            return JsonResponse(response_data)
        errors = form.errors
        if not username:
            errors['username'] = ['This field is required.']
        response_data = {'success': False, 'errors': errors}
        logger.debug(f"add_profile response: {response_data}")
        return JsonResponse(response_data)
    else:
        form = ProfileForm()
        html = render_to_string('practice/add_profile.html', {'form': form}, request=request)
        response_data = {'success': True, 'html': html}
        logger.debug(f"add_profile response: {response_data}")
        return JsonResponse(response_data)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {'success': True, 'message': 'Tag added successfully'}
            logger.debug(f"add_tag response: {response_data}")
            return JsonResponse(response_data)
        response_data = {'success': False, 'errors': form.errors}
        logger.debug(f"add_tag response: {response_data}")
        return JsonResponse(response_data)
    else:
        form = TagForm()
        html = render_to_string('practice/add_tag.html', {'form': form}, request=request)
        response_data = {'success': True, 'html': html}
        logger.debug(f"add_tag response: {response_data}")
        return JsonResponse(response_data)

@login_required(login_url='/login/')
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {'success': True}
            logger.debug(f"add_author response: {response_data}")
            return JsonResponse(response_data)
        response_data = {'success': False, 'errors': form.errors}
        logger.debug(f"add_author response: {response_data}")
        return JsonResponse(response_data)
    else:
        form = AuthorForm()
        html = render_to_string('practice/add_author.html', {'form': form}, request=request)
        response_data = {'success': True, 'html': html}
        logger.debug(f"add_author response: {response_data}")
        return JsonResponse(response_data)

@login_required(login_url='/login/')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {'success': True}
            logger.debug(f"add_book response: {response_data}")
            return JsonResponse(response_data)
        response_data = {'success': False, 'errors': form.errors}
        logger.debug(f"add_book response: {response_data}")
        return JsonResponse(response_data)
    else:
        form = BookForm()
        html = render_to_string('practice/add_book.html', {'form': form}, request=request)
        response_data = {'success': True, 'html': html}
        logger.debug(f"add_book response: {response_data}")
        return JsonResponse(response_data)