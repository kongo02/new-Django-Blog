from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from .models import Post
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.


def searchPost(request):
    post_search = ""
    if request.GET.get('search'):
        post_search = request.GET.get('search')
    posts = Post.objects.filter(
        Q(title__icontains=post_search) | Q(body__icontains=post_search))
    return posts


def index(request):
    posts = searchPost(request)
    # Assuming you have a list of items to display
    # items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    # paginator = Paginator(items, 5)  # Display 5 items per page
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    featuredPost = Post.objects.filter(is_featured=True)
    context = {
        "posts": posts,
        'featuredPost': featuredPost
    }
    return render(request, "index.html", context)


def getPost(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, 'post_detail.html', {
        'post': post
    })


@login_required(login_url='login')
def createPost(request):
    context = {}
    if request.method == 'POST':
        try:
            Post.objects.create(
                title=request.POST.get('title'),
                body=request.POST.get('description'),
                image=request.FILES.get('image'),
                author=request.user
            )
            return redirect('index')
        except:
            context["message"] = "Invalid details"

    return render(request, 'create_post.html', context)


@login_required(login_url='login')
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post': post}
    if request.method == "POST":
        if request.user == post.author:
            post.title = request.POST.get('title')
            post.body = request.POST.get('description')
            # image = request.FILES.get('image_upload')
            post.save()
        else:
            return HttpResponse("403 FORBIDDEN")
        return redirect('index')

    return render(request, 'post_update.html', context)


@login_required(login_url='login')
def deletePost(request, pk):

    post = Post.objects.get(id=pk)
    if request.user == post.author:
        post.delete()
    else:
        return HttpResponse("403 Forbidden")

    return redirect('index')


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create the user
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.save()
            # Additional steps (if needed)
            # For example, you might want to log in the user automatically after registration
            # login(request, user)

            # Redirect to a success page or login page
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('index')
