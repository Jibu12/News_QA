from django import forms
from .models import Category, Subcategory, NewsPost

# Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

# Subcategory Form
class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from datetime import datetime

class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ['title', 'slug', 'content', 'excerpt', 'category_id', 'subcategory_id',
                  'published_at', 'is_published', 'tags', 'author_name', 'meta_description', 
                  'meta_keywords', 'cover_image', 'news_image']
        
        widgets = {
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            # Customize the layout as per your needs
            'title',
            'slug',
            'content',
            'excerpt',
            'category_id',
            'subcategory_id',
            'published_at',
            'is_published',
            'tags',
            'author_name',
            'meta_description',
            'meta_keywords',
            'cover_image',
            'news_image',
            Submit('submit', 'Add News Post', css_class='btn btn-primary')
        )

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if NewsPost.objects.filter(slug=slug).exists():
            raise forms.ValidationError("This slug is already in use. Please choose another.")
        return slug
    
    def clean_published_at(self):
        published_at = self.cleaned_data.get('published_at')
        if published_at is not None and not isinstance(published_at, datetime):
            raise forms.ValidationError("Please enter a valid date and time.")
        return published_at
        



class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True, help_text='Enter your registered email.')

