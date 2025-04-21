from django.shortcuts import render, redirect

from .models import Student, Faculty, Administrator


from django.http import HttpResponse

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        user_id = request.POST.get('user_id')
        password = request.POST.get("password")
        user = None

        if user_type=="Student":
            user = Student.objects.filter(user_id=user_id, password=password).first()
        elif user_type == "Faculty":
            user = Faculty.objects.filter(user_id=user_id, password=password).first()
        elif user_type == "Administrator":
            user = Administrator.objects.filter(user_id=user_id, password=password).first()

        if user:
            request.session['user_name'] = user.name

            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'please fill all fields'})
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



