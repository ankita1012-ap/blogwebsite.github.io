from pickle import TRUE
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django import views
from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    category_image = models.ImageField(upload_to='uploads/%y/%m/%d',null=True)
    category_text = models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.category_name}'


class Blog(models.Model):

    STATUS_CHOICE = (
        ('draft','Draft'),
        ('published','Published')
    )

    title = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(unique=TRUE,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    blog_image = models.ImageField(upload_to='uploads/%y/%m/%d')
    short_description = models.TextField(max_length=1000)
    blog_body = models.TextField(max_length=3000)
    views = models.IntegerField(null=True)
    comment = models.IntegerField(null=True)
    status = models.CharField(max_length=100,choices= STATUS_CHOICE, default='draft')
    is_feacherd = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.title}'

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='repl')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username}| {self.content}'
    
class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='sub_replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by {self.user.username}| {self.comment} | {self.content}'
    