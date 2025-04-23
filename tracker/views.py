from django.shortcuts import render, redirect

from .models import Student, Faculty, Administrator, LostItem, FoundItem


from django.http import HttpResponse

# Create your views here.

# def login_view(request):
#     if request.method == 'POST':
#         user_type = request.POST.get('user_type')
#         user_id = request.POST.get('user_id')
#         password = request.POST.get("password")
#         user = None

#         if user_type=="Student":
#             user = Student.objects.filter(user_id=user_id, password=password).first()
#         elif user_type == "Faculty":
#             user = Faculty.objects.filter(user_id=user_id, password=password).first()
#         elif user_type == "Administrator":
#             user = Administrator.objects.filter(user_id=user_id, password=password).first()

#         if user:
#             request.session['user_name'] = user.name

#             return redirect('home')
#         else:
#             return render(request, 'login.html', {'error': 'please fill all fields'})
#     return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        user = None
        user_type = None

        # Check in Student table
        try:
            user = Student.objects.get(user_id=user_id, password=password)
            user_type = 'Student'
        except Student.DoesNotExist:
            pass

        # Check in Faculty table
        if not user:
            try:
                user = Faculty.objects.get(user_id=user_id, password=password)
                user_type = 'Faculty'
            except Faculty.DoesNotExist:
                pass

        # Check in Administrator table
        if not user:
            try:
                user = Administrator.objects.get(user_id=user_id, password=password)
                user_type = 'Administrator'
            except Administrator.DoesNotExist:
                pass

        # If user is found in any table
        if user:
            request.session['user_id'] = user.user_id
            request.session['user_name'] = user.name
            request.session['user_type'] = user_type
            return redirect('home')  # Redirect to home page
        else:
            return render(request, 'login.html', {'error': 'No user data found. Please try again.'})

    return render(request, 'login.html')


def home_view(request):
    if 'user_name' in request.session:
        return render(request, 'home.html', {'name': request.session['user_name']})
    else:
        return redirect('login') 

# def home_view(request):
#     return HttpResponse("""
#         <html>
#         <head>
#             <title>Home</title>
#             <style>
#                 body {
#                     margin: 0;
#                     padding: 0;
#                     display: flex;
#                     justify-content: center;
#                     align-items: center;
#                     height: 100vh;
#                     background-color: #f9f9f9;
#                     font-family: Arial, sans-serif;
#                 }
#                 h1 {
#                     color: #333;
#                 }
#             </style>
#         </head>
#         <body>
#             <h1>Welcome to the Lost And Found Home Page!</h1>
#         </body>
#         </html>
#     """)

def create_account_view(request):
    if request.method == "POST":
        user_type = request.POST.get("user_type")
        user_id = request.POST.get("user_id")
        name = request.POST.get("name")
        department = request.POST.get("department")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if user_type == "student":
            Student.objects.create(user_id=user_id, name=name, department=department, email=email, password=password)
        elif user_type == "faculty":
            Faculty.objects.create(user_id=user_id, name=name, department=department, email=email, password=password)
        elif user_type == "administrator":
            Administrator.objects.create(user_id=user_id, name=name, department=department, email=email, password=password)

        return redirect('login')

    return render(request, 'create_account.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')



def my_profile_view(request):
    user_id = request.session.get('user_id')
    name = request.session.get('user_name')
    user_type = request.session.get('user_type')

    # Determine user model
    if user_type == "Student":
        from .models import Student as UserModel
    elif user_type == "Faculty":
        from .models import Faculty as UserModel
    elif user_type == "Administrator":
        from .models import Administrator as UserModel

    user = UserModel.objects.get(user_id=user_id)

    # Fetch posts
    from .models import LostItem, FoundItem
    lost_posts = LostItem.objects.filter(posted_by_id=user_id)
    found_posts = FoundItem.objects.filter(posted_by_id=user_id)

    context = {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "department": user.department,
        "user_type": user_type,
        "total_posts": lost_posts.count() + found_posts.count(),
        "lost_count": lost_posts.count(),
        "found_count": found_posts.count(),
        "lost_posts": lost_posts,
        "found_posts": found_posts
    }

    return render(request, 'my_profile.html', context)

def home_view(request):
    return render(request, 'home.html')

