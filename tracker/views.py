from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import User, LostItem, FoundItem, Comment, Upvote


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
        password = request.POST.get("password")

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

    lost_posts = LostItem.objects.filter(posted_by_id=user_id)
    found_posts = FoundItem.objects.filter(posted_by_id=user_id)

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
        "total_posts": lost_posts.count() + found_posts.count(),
        "lost_count": lost_posts.count(),
        "found_count": found_posts.count(),
        "lost_posts": lost_posts,
        "found_posts": found_posts
    }
    return render(request, 'my_profile.html', context)


# ------------------- HOME PAGE (FEED) -------------------
def home_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, user_id=user_id)

    # Order by upvotes first, then most recent using item_id
    items = LostItem.objects.annotate(upvote_count=Count('upvote')).order_by('-upvote_count', '-item_id')

    # Fetch all comments and group by item_id
    comments = Comment.objects.select_related('user', 'item')
    comment_map = {}
    for comment in comments:
        comment_map.setdefault(comment.item.item_id, []).append(comment)

    context = {
        'items': items,
        'comment_map': comment_map,
        'user': user
    }
    return render(request, 'home.html', context)


# ------------------- COMMENT POSTING -------------------
def post_comment(request, item_id):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        user = get_object_or_404(User, user_id=user_id)
        item = get_object_or_404(LostItem, item_id=item_id)
        content = request.POST.get('content')

        if content:
            Comment.objects.create(user=user, item=item, content=content)

    return redirect('home')


# ------------------- UPVOTE HANDLING -------------------
def upvote_post(request, item_id):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, user_id=user_id)
    item = get_object_or_404(LostItem, item_id=item_id)

    if not Upvote.objects.filter(user=user, item=item).exists():
        Upvote.objects.create(user=user, item=item)

    return redirect('home')
