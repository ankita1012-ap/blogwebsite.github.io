
from django.urls import path


# from .views import  blog_detail, home, blogs, trending, categories, authors, about, contact, auth, blog_detail, category_blog
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('blogs',views.blogs,name='blogs'),
    path('trending',views.trending,name='trending'),
    path('categories',views.categories,name='categories'),
    path('authors',views.authors,name='authors'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('auth',views.auth,name='auth'),
    path('blog-detail/<int:pk>/',views.blog_detail,name='blog-detail'),
    path('category-blog/<str:cn>/',views.category_blog,name='category-blog'),
    path('blog/<int:blog_id>/add_comment/', views.add_comment, name='add_comment'),
    path('logout',views.logout,name='logout'),
    path('add_reply/<int:comment_id>/', views.add_reply, name='add_reply'),


]
