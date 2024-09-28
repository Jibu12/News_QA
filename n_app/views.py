from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse,JsonResponse
from .models import *



# ------------------------------ADMIN---------------------------------------------------
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CategoryForm, SubcategoryForm, NewsPostForm


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:  # Ensure the user is an admin (superuser)
            login(request, user)
            return redirect('admin_home')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials or not an admin user'})
    
    return render(request, 'admin_login.html')


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def admin_index(request):
    return render(request, 'admin_index.html')


def admin_home(request):
    if not request.user.is_superuser:
        return redirect('admin_login')  # Restrict non-admin users
     # Get user statistics
    total_users = MyUsers.objects.count()
    
    # Get the top 10 most popular posts by likes, views, or comments
    most_popular_posts = NewsPost.objects.order_by('-likes_count')[:5]  # Top 10 by likes
    
    # Pass data to the template
    context = {
        'total_users': total_users,
        'most_popular_posts': most_popular_posts,
    }
    return render(request, 'admin_home.html', context)





# Category View

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            # Check if the category already exists
            if Category.objects.filter(name=category_name).exists():
                messages.error(request, f"The category '{category_name}' already exists.")
            else:
                form.save()
                messages.success(request, f"Category '{category_name}' added successfully!")
                return redirect(reverse('add_category'))  # Redirect after successful save
    else:
        form = CategoryForm()
    
    return render(request, 'add_category.html', {'form': form})

# Subcategory View

def add_subcategory(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            subcategory_name = form.cleaned_data['name']
            # Check if the subcategory already exists
            if Subcategory.objects.filter(name=subcategory_name).exists():
                messages.error(request, f"The subcategory '{subcategory_name}' already exists.")
            else:
                form.save()
                messages.success(request, f"Subcategory '{subcategory_name}' added successfully!")
                return redirect(reverse('add_subcategory'))  # Redirect after successful save
    else:
        form = SubcategoryForm()
    
    return render(request, 'add_subcategory.html', {'form': form})

# NewsPost View

def add_newspost(request):
    if request.method == 'POST':
        form = NewsPostForm(request.POST, request.FILES)  # Add request.FILES for image uploads
        if form.is_valid():
            form.save()
            return redirect(reverse('add_newspost'))
    else:
        form = NewsPostForm()
    return render(request, 'add_newspost.html', {'form': form})




def delete_newspost(request, post_id):
    post = get_object_or_404(NewsPost, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('news_posts')  # Redirect to the news posts list
    return render(request, 'confirm_delete.html', {'post': post})



# View for displaying categories and subcategories
def categories_subcategories_view(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    return render(request, 'categories_subcategories_view.html', {'categories': categories, 'subcategories': subcategories})



# View for displaying news posts
def news_posts_view(request):
    posts = NewsPost.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'news_post_view.html', {'posts': posts})

from django.shortcuts import get_object_or_404

def news_post_detail(request, slug):
    post = get_object_or_404(NewsPost, slug=slug, is_published=True)
    return render(request, 'news_post_detail.html', {'post': post})



from django.db.models import Count

def visualization(request):
    # Get user statistics
    total_users = MyUsers.objects.count()
    
    # Get the top 10 most popular posts by likes
    most_popular_posts = NewsPost.objects.filter(is_published=True).order_by('-likes_count')[:5]
    
     # Get the count of posts by category
    posts_by_category = NewsPost.objects.values('category_id__name').annotate(count=Count('post_id')).order_by('-count')
    # Pass data to the template

    trending_posts = NewsPost.objects.order_by('-trending_score')[:5]


    context = {
        'total_users': total_users,
        'most_popular_posts': most_popular_posts,
        'posts_by_category': posts_by_category,
        'trending_posts': trending_posts,
    }
    return render(request, 'visualization.html', context)


from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

def more_visualization(request):
    # Get user statistics
    total_users = MyUsers.objects.count()
    
    # Get the top 10 most popular posts by likes
    most_popular_posts = NewsPost.objects.filter(is_published=True).order_by('-likes_count')[:5]
    
     # Get the count of posts by category
    posts_by_category = NewsPost.objects.values('category_id__name').annotate(count=Count('post_id')).order_by('-count')
    # Pass data to the template

    trending_posts = NewsPost.objects.order_by('-trending_score')[:5]


    total_comments_per_post = [(post.title, post.comments.count()) for post in NewsPost.objects.prefetch_related('comments')]
    # Get the top 10 viewed posts
    post_views = NewsPost.objects.values('title').annotate(total_views=Sum('views_count')).order_by('-total_views')[:10]

    category_views = NewsPost.objects.values('category_id__name').annotate(total_views=Sum('views_count')).order_by('-total_views')
    context = {
        'total_users': total_users,
        'most_popular_posts': most_popular_posts,
        'posts_by_category': posts_by_category,
        'trending_posts': trending_posts,
        'total_comments_per_post': total_comments_per_post,
        'post_views': post_views,
        'category_views': category_views,
    }

    return render(request, 'more_visualization.html', context)

from django.contrib.auth import logout  # Add this import
def admin_logout(request):
    logout(request)
    return redirect('index') 

# --------------------------------------------------------------------------------------





def index(request):
    # Fetch all published posts
    posts = NewsPost.objects.filter(is_published=True)

    # Calculate the trending score for each post
    for post in posts:
        post.trending_score = (
            (post.views_count * 0.5) +
            (post.likes_count * 0.3) +
            (post.comments_count * 0.15) +
            (post.shares_count * 0.05)
        )
        post.save()
    top_trending_post = posts.order_by('-trending_score').first()
    categories = Category.objects.all()


    # Fetch the top 5 most liked posts
    top_liked_posts = NewsPost.objects.filter(is_published=True).order_by('-likes_count')[:5]

    all_posts = NewsPost.objects.all()
    old_posts = NewsPost.objects.filter(is_published=True).order_by('created_at')[:3]

    return render(request, 'index.html', {
         'top_trending_post': top_trending_post,'categories': categories,'top_liked_posts': top_liked_posts,'all_posts': all_posts,'old_posts': old_posts,
    })


def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('user_register')
        
        # Check if the username or email already exists
        if MyUsers.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('user_register')
        
        if MyUsers.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('user_register')

        # Hash the password and create the user
        hashed_password = make_password(password)
        user = MyUsers(
            username=username,
            email=email,
            password_hash=hashed_password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('user_login')
    
    return render(request, 'user_register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = MyUsers.objects.get(username=username)
            if check_password(password, user.password_hash):
                # Simulate session or token creation
                request.session['user_id'] = user.user_id
                return redirect('user_home')
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                return redirect('user_login')
            
        except MyUsers.DoesNotExist:
            messages.error(request, "User does not exist. Please check your username.")
            return redirect('user_login')

    return render(request, 'user_login.html')



def user_common(request):
    return render(request, 'user_common.html')


def user_home(request):
    # Fetch all published posts
    posts = NewsPost.objects.filter(is_published=True)

    # Calculate the trending score for each post
    for post in posts:
        post.trending_score = (
            (post.views_count * 0.5) +
            (post.likes_count * 0.3) +
            (post.comments_count * 0.15) +
            (post.shares_count * 0.05)
        )
        post.save()
    top_trending_post = posts.order_by('-trending_score').first()
    categories = Category.objects.all()


    # Fetch the top 5 most liked posts
    top_liked_posts = NewsPost.objects.filter(is_published=True).order_by('-likes_count')[:5]

    all_posts = NewsPost.objects.all()
    old_posts = NewsPost.objects.filter(is_published=True).order_by('created_at')[:3]


    return render(request, 'user_home.html', {
        'top_trending_post': top_trending_post,'categories': categories,'top_liked_posts': top_liked_posts,'all_posts': all_posts,'old_posts':old_posts,
    
    })

def user_logout(request):
    request.session.flush()
    return redirect('user_login')

# ----------------------------------------------------------------------------------------------------

def like_post(request, slug):
    # Ensure the user is logged in by checking the session
    if 'user_id' not in request.session:
        return redirect('user_login')

    # Get the logged-in user's ID from the session
    user_id = request.session.get('user_id')

    # Fetch the post
    post = get_object_or_404(NewsPost, slug=slug)

    # Get the logged-in user
    user = MyUsers.objects.get(user_id=user_id)

    # Check if the user has already liked the post
    if PostLiked.objects.filter(user=user, post=post).exists():
        # If the user has liked the post, remove the like
        PostLiked.objects.filter(user=user, post=post).delete()
        post.likes_count -= 1
    else:
        # Otherwise, add a like
        PostLiked.objects.create(user=user, post=post)
        post.likes_count += 1

    post.save()
    return redirect('post_detail', slug=slug)

def userlike_post(request, slug):
    # Ensure the user is logged in by checking the session
    if 'user_id' not in request.session:
        return JsonResponse({'success': False, 'message': 'User not logged in'}, status=401)

    # Get the logged-in user's ID from the session
    user_id = request.session.get('user_id')

    # Fetch the post
    post = get_object_or_404(NewsPost, slug=slug)

    # Get the logged-in user
    user = MyUsers.objects.get(user_id=user_id)

    # Check if the user has already liked the post
    liked = False
    if PostLiked.objects.filter(user=user, post=post).exists():
        # If the user has liked the post, remove the like
        PostLiked.objects.filter(user=user, post=post).delete()
        post.likes_count -= 1
        liked = False
    else:
        # Otherwise, add a like
        PostLiked.objects.create(user=user, post=post)
        post.likes_count += 1
        liked = True
        
    
    post.save()

    # Return a JSON response with the updated like count and status
    return JsonResponse({
        'success': True,
        'likes_count': post.likes_count,
        'liked': liked
    })



import google.generativeai as genai

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get the API key
api_key = os.getenv('API_KEY')

# Use the API key in your project
genai.configure(api_key=api_key)



# The question-answering view
def ask_question(request, slug):
    post = get_object_or_404(NewsPost, slug=slug)
    response_text = None

    if request.method == 'POST':
        article_content = request.POST.get('article_content')
        question_input = request.POST.get('question_input')

        if article_content and question_input:
            # Combine article content and the question
            combined_input = f"Content: {article_content}\n\nQuestion: {question_input}"
            
            # Call the Generative AI to get the response
            chat_session = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 64,
                    "max_output_tokens": 8192,
                    "response_mime_type": "text/plain",
                }
            ).start_chat()
            response = chat_session.send_message(combined_input)
            response_text = response.text

    return render(request, 'news_post_detail.html', {
        'post': post,
        'response_text': response_text
    })
# -----------------------------------------------------------------------------------------------------------------

def user_news_postsview(request):
    posts = NewsPost.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'user_news_postview.html', {'posts': posts})


def user_news_postdetail(request, slug):
    post = get_object_or_404(NewsPost, slug=slug, is_published=True)
    post.views_count += 1
    post.save(update_fields=['views_count']) 
   
    post.save()
    
    comments = post.comments.all()  # Retrieve related comments
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'user_news_postdetail.html', context)


def latest_news(request):
    # Fetch the latest news posts, ordered by creation date
    latest_posts = NewsPost.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'latest_news.html', {'latest_posts': latest_posts})



def trending_news_post(request):
     

    # Fetch all published posts
    posts = NewsPost.objects.filter(is_published=True)

    # Calculate the trending score for each post
    for post in posts:
        post.trending_score = (
            (post.views_count * 0.5) +
            (post.likes_count * 0.3) +
            (post.comments_count * 0.15) +
            (post.shares_count * 0.05)
        )
        post.save()

    # Get the top trending post
    top_trending_post = max(posts, key=lambda p: p.trending_score, default=None)

    return render(request, 'user_news_postdetail.html', {
        'top_trending_post': top_trending_post,
    })


def add_comment(request, slug):
    if request.method == 'POST':
        content = request.POST.get('content')
        post = get_object_or_404(NewsPost, slug=slug)

        if 'user_id' in request.session:
            user = MyUsers.objects.get(user_id=request.session['user_id'])
            Comment.objects.create(post=post, user=user, content=content)


            # Increment the comments count for the post
            post.comments_count += 1
            
            post.save()

    return redirect('userpost_detail', slug=slug)



# The question-answering view
def user_ask_question(request, slug):
    post = get_object_or_404(NewsPost, slug=slug)
    response_text = None

    if request.method == 'POST':
        article_content = request.POST.get('article_content')
        question_input = request.POST.get('question_input')

        if article_content and question_input:
            # Combine article content and the question
            combined_input = f"Content: {article_content}\n\nQuestion: {question_input}"
            
            # Call the Generative AI to get the response
            chat_session = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 64,
                    "max_output_tokens": 8192,
                    "response_mime_type": "text/plain",
                }
            ).start_chat()
            response = chat_session.send_message(combined_input)
            response_text = response.text

    return render(request, 'user_news_postdetail.html', {
        'post': post,
        'response_text': response_text
    })

# def whats_new(request):
#     # Fetch all categories
#     categories = Category.objects.all()

#     # Fetch all published posts
#     all_posts = NewsPost.objects.filter(is_published=True)

#     return render(request, 'user_home.html', {
#         'categories': categories,
#         'all_posts': all_posts
#     })


def category_posts(request, category_slug):
    # Use the name field for matching
    category = get_object_or_404(Category, name__iexact=category_slug)
    posts = NewsPost.objects.filter(category_id=category, is_published=True)

    return render(request, 'category_post.html', {
        'category_name': category.name,
        'posts': posts
    })




# password reset:


from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import PasswordResetForm
import random
import string




# Generate a random password reset token
def generate_token(length=50):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Password Reset Request View
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = MyUsers.objects.get(email=email)
                # Generate a reset token
                reset_token = generate_token()

                # Save the token in the user's session or send via email
                request.session['reset_token'] = reset_token
                request.session['user_email'] = email

                # Send email with reset link (simplified)
                send_mail(
                    subject='Password Reset Request',
                    message=f'Click the link to reset your password: {settings.SITE_URL}/reset_password/{reset_token}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )

                messages.success(request, 'A password reset link has been sent to your email.')
                return redirect('index')
            except MyUsers.DoesNotExist:
                messages.error(request, 'No user with this email found.')
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset_form.html', {'form': form})

# Password Reset Confirm View
def reset_password(request, token):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        email = request.session.get('user_email')
        try:
            user = MyUsers.objects.get(email=email)
            user.password_hash = new_password  # You'll need to hash the password properly
            user.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('user_login')
        except MyUsers.DoesNotExist:
            messages.error(request, 'Invalid reset attempt.')
    return render(request, 'reset_password.html')




def search(request):
    query = request.GET.get('q', '')
    results = NewsPost.objects.filter(title__icontains=query)  # Adjust filter based on your search logic
    return render(request, 'search_results.html', {'results': results, 'query': query})