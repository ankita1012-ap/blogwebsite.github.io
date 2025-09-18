import json
from . import utils
from .models import Blog, Category, Comment, Reply
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, F
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout as auth_logout


# Create your views here.
def home(request):
    # blog_obj     = Blog.objects.all().values('id','title','author','category','short_description','blog_image','blog_body')
    category_obj = Category.objects.all().values_list("category_name", flat=True).distinct()
    
    # Trending blogs (latest 3 for now)
    trending_blogs = Blog.objects.all().order_by('-id')[:3]  
    
    # Top author by number of blogs
    top_author = Blog.objects.values('author').annotate(total=Count('id')).order_by('-total').first()
    top_author_blogs = []
    if top_author:
        # Limit to only 2 blogs
        top_author_blogs = list(
            Blog.objects.filter(author=top_author['author'])
            .values('id', 'title', 'short_description', 'blog_image', 'category')[:2]  # ✅ only 2 blogs
        )


    if request.method == 'POST':
        email = request.POST.get('email')
        utils.send_test_email(email)

    context = {
        # 'blogs': list(blog_obj),
        'category': list(category_obj),
        'trending_blogs': trending_blogs,
        'top_author': top_author,
        'top_author_blogs': top_author_blogs,
    }
    
    # print(context['top_author_blogs'])
    return render(request,'index.html',context)


# def blog_detail(request, pk):
#     blog = get_object_or_404(Blog, id=pk)
#     comments = Comment.objects.filter(blog=blog).order_by('-created_at')
    
#     # Optional: prefetch replies to reduce queries
#     comments = comments.prefetch_related('replies')

#     context = {
#         'blog_detail': blog,
#         'comments': comments,
#         # 'replies' : replies,
#     }
#     return render(request, 'blog-detail.html', context)

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, id=pk)

    # Get top-level comments (parent=None)
    comments = Comment.objects.filter(blog=blog, parent__isnull=True).order_by('-created_at')

    # Attach replies and sub-replies
    for comment in comments:
        # Top-level replies for this comment
        comment.top_replies = comment.replies.filter(parent__isnull=True).order_by('created_at')

        # For each reply, attach sub-replies
        for reply in comment.top_replies:
            reply.sub_replies_list = reply.sub_replies.all().order_by('created_at')

    context = {
        'blog_detail': blog,
        'comments': comments,
    }
    return render(request, 'blog-detail.html', context)




@login_required(login_url='auth')
def add_comment(request, blog_id):
    # if not request.user.is_superuser:
    #     return JsonResponse({'success': False, 'error': 'Only superusers can comment.'})

    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        if not content:
            return JsonResponse({'success': False, 'error': 'Content cannot be empty.'})

        blog = get_object_or_404(Blog, id=blog_id)
        Comment.objects.create(blog=blog, user=request.user, content=content)
        
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

# def add_reply(request, comment_id, parent_id=None):
    comment = get_object_or_404(Comment, id=comment_id)
    parent = None
    if parent_id:
        parent = get_object_or_404(Reply, id=parent_id)

    if request.method == "POST":
        content = request.POST.get("content")
        reply = Reply.objects.create(
            comment=comment,
            parent=parent,
            user=request.user,
            content=content
        )
        return redirect("blog_detail", pk=comment.blog.id)
@login_required(login_url='auth')
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    parent_id = None
    data = json.loads(request.body)
    content = data.get("content")
    parent_id = data.get("parent_id")

    parent = None
    if parent_id:
        parent = get_object_or_404(Reply, id=parent_id)

    reply = Reply.objects.create(
        comment=comment,
        parent=parent,
        user=request.user,
        content=content
    )

    return JsonResponse({
        "success": True,
        "user": reply.user.username,
        "created_at": reply.created_at.strftime('%b %d, %Y %H:%M'),
        "content": reply.content,
        "reply_id": reply.id
    })

def blogs(request):

    blog_obj = Blog.objects.select_related("author", "category").all().values('id','title','views','short_description','blog_image','blog_body',created_date=F("created_at__date"),author_name=F("author__username"),category_name=F("category__category_name"))

    
    context = {
        'blogs': list(blog_obj),
    }

    return render(request,'blogs.html',context)


def trending(request):
    # Trending blogs (latest 3 for now)
    trending_blogs = Blog.objects.all().order_by('-id')[:3]  
    
    context = {
        'trending_blogs': trending_blogs,
    }

    return render(request,'trending.html',context)


def categories(request):
    category_obj = Category.objects.all()

    context = {
        'category': category_obj,
    }

    # print(context['category'])
    return render(request,'categories.html',context)

def category_blog(request,cn):
    
    blog_obj = Blog.objects.filter(category__category_name=cn)

    context = {
        'blog' : blog_obj,
    }

    return render(request,'category-blog.html',context)


def authors(request):
    return render(request,'authors.html')


def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')



def auth(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')

        elif 'signup' in request.POST:

            # full_name = request.POST.get('fullname')
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
            else:
                username = email.split('@')[0]  # Generate username from email
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,last_name=last_name)
                user.save()
                messages.success(request, 'Your account has been set up! Log in to access your dashboard..')

    return render(request, 'auth.html')

def logout(request):
    auth_logout(request)  # Logs out the user
    return redirect('home')  # Redirect to homepage after logout