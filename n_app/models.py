from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class MyUsers(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
import uuid

class Category(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class Subcategory(models.Model):
    subcategory_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class NewsPost(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    category_id = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    subcategory_id = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    trending_score = models.IntegerField(default=0)
    tags = models.CharField(max_length=255, blank=True)
    author_name = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    cover_image = models.URLField(blank=True)
    news_image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.title

        
    def update_trending_score(self):
        # Example weights: adjust these as needed
        views_weight = 0.5
        likes_weight = 0.3
        comments_weight = 0.15
        shares_weight = 0.05

        # Calculate the trending score
        self.trending_score = (
            (self.views_count * views_weight) +
            (self.likes_count * likes_weight) +
            (self.comments_count * comments_weight) +
            (self.shares_count * shares_weight)
        )
        print(f"Calculating trending score: Views: {self.views_count}, Likes: {self.likes_count}, Comments: {self.comments_count}, Shares: {self.shares_count}, Score: {self.trending_score}")  # Debug print
        self.save()
    

from django.conf import settings

class PostLiked(models.Model):
    user = models.ForeignKey(MyUsers, on_delete=models.CASCADE)  # Reference to MyUsers
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')



class Comment(models.Model):
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
