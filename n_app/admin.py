from django.contrib import admin
from .models import *


admin.site.register(MyUsers)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(NewsPost)
admin.site.register(PostLiked)
admin.site.register(Comment)
