from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import User, Item, ItemImage
from django.contrib.auth.hashers import make_password
from .forms import ItemForm, MultiImageForm


# ------------------- LOGIN VIEW -------------------
def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        try:
            user = User.objects.get(user_id=user_id, password=password)
            request.session['user_id'] = user.user_id
            request.session['user_name'] = user.name
            request.session['user_type'] = user.get_user_type_display()
            return redirect('home')
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'No user data found. Please try again.'})

    return render(request, 'login.html')


# ------------------- LOGOUT -------------------
def logout_view(request):
    request.session.flush()
    return redirect('login')


# ------------------- CREATE ACCOUNT -------------------
def create_account_view(request):
    if request.method == "POST":
        user_type = request.POST.get("user_type")
        user_id = request.POST.get("user_id")
        name = request.POST.get("name")
        department = request.POST.get("department")
        email = request.POST.get("email")
        password = make_password(request.POST.get("password"))
        user_type_map = {
            "administrator": 1,
            "faculty": 2,
            "student": 3,
        }

        if user_type in user_type_map:
            User.objects.create(
                user_id=user_id,
                name=name,
                department=department,
                email=email,
                password=password,
                user_type=user_type_map[user_type]
            )
            return redirect('login')
        else:
            return render(request, 'create_account.html', {'error': 'Invalid user type selected.'})

    return render(request, 'create_account.html')


# ------------------- PROFILE -------------------
def my_profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, user_id=user_id)
    user_items = Item.objects.filter(posted_by_id=user_id)
    lost_posts = user_items.filter(is_found=False)
    found_posts = user_items.filter(is_found=True)
    user_type_map = {
        1: "Administrator",
        2: "Faculty",
        3: "Student"
    }

    context = {
    "user_id": user.user_id,
    "name": user.name,
    "email": user.email,
    "department": user.department,
    "user_type": user_type_map.get(user.user_type, "Unknown"),
    "total_posts": user_items.count(),
    "lost_count": lost_posts.count(),
    "found_count": found_posts.count(),
    "lost_posts": lost_posts,
    "found_posts": found_posts
    }

    return render(request, 'my_profile.html', context)


# ------------------- HOME PAGE (FEED) -------------------

def home_view(request):
    return render(request, 'home.html')

def post_list_view(request):
    posts = Item.objects.filter(is_found=True).order_by('-item_id')
    return render(request, 'post_list.html', {'posts': posts})


def create_found_item_view(request):
    if request.method == 'POST':
        form = FoundItemOnlyForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.posted_by_id = request.session.get('user_id')
            item.posted_by_name = request.session.get('user_name')
            item.is_found = True  # Enforce found flag
            item.save()
            return redirect('post_list')
    else:
        form = FoundItemOnlyForm()
    return render(request, 'create_post.html', {'form': form})



def create_item_view(request):
    if request.method == 'POST':
        item_form = ItemForm(request.POST)
        image_form = MultiImageForm(request.POST, request.FILES)

        if item_form.is_valid() and image_form.is_valid():
            item = item_form.save(commit=False)
            item.posted_by_id = request.session.get('user_id')
            item.posted_by_name = request.session.get('user_name')
            item.save()

            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for image in images:
                ItemImage.objects.create(item=item, image=image)

            return redirect('post_list')
    else:
        item_form = ItemForm()
        image_form = MultiImageForm()

    return render(request, 'create_post.html', {
        'item_form': item_form,
        'image_form': image_form
    })
