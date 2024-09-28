from django.urls import path
from . import views

urlpatterns = [
    # -------------ADMIN-------------------
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_dashboard/', views.admin_home, name='admin_dashboard'),
    path('admin_index/', views.admin_index, name='admin_index'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_subcategory/', views.add_subcategory, name='add_subcategory'),
    path('add_newspost/', views.add_newspost, name='add_newspost'),
    path('post/delete/<uuid:post_id>/', views.delete_newspost, name='delete_newspost'),

    path('categories/', views.categories_subcategories_view, name='categories_subcategories'),
    path('news/', views.news_posts_view, name='news_posts'),
    path('news/<slug:slug>/', views.news_post_detail, name='post_detail'),
    path('news/<slug:slug>/like/', views.like_post, name='like_post'),
    # path('toggle_like/', views.toggle_like, name='toggle_like'),
    path('latest_news/', views.latest_news, name='latest_news'),
    path('trending/', views.trending_news_post, name='trending_news_post'),

    path('visualize/', views.visualization, name='visualize'),
    path('more_visualize/', views.more_visualization, name='more_visualize'),

    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('post/<slug:slug>/ask/', views.ask_question, name='ask_question'),


    # -----------USER------------------------
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('user_common', views.user_common, name='user_common'),
    path('user_home', views.user_home, name='user_home'),
    path('user_register', views.user_register, name='user_register'),
    path('user_login/', views.user_login, name='user_login'),
    path('upost/<slug:slug>/ask/', views.user_ask_question, name='uask_question'),
    path('usernews/', views.user_news_postsview, name='usernews_posts'),
    path('usernews/<slug:slug>/', views.user_news_postdetail, name='userpost_detail'),
    path('usernews/<slug:slug>/like/', views.userlike_post, name='userlike_post'),
    path('usernews/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    # path('whats-new/', views.whats_new, name='whats_new'),

    path('category/<str:category_slug>/', views.category_posts, name='category_posts'),

    path('user_logout/', views.user_logout, name='user_logout'),

    path('search/', views.search, name='search'),



    path('forgot_password/', views.password_reset_request, name='forgot_password'),
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),

]
