from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Task 1: Register
def register_view(request):
    if request.method == "POST":
        name = request.POST.get('name') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            # ننشئ المستخدم ونضع الإيميل في خانة الـ username والـ email
            user = User.objects.create_user(username=email, email=email, password=password)
            user.name = name
            user.save()
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect('my_bookings')
    return render(request, "users/register.html")


# Task 2: Login
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successfully")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password")
            
    return render(request, "users/login.html", {"form": form})

# Task 4: Logout
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        email = request.POST.get('username') # الحقل في الفورم اسمه username افتراضياً
        password = request.POST.get('password')
        
        try:
            # نبحث عن اليوزر اللي يملك هذا الإيميل
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successfully")
                return redirect('my_bookings') # يوجهك لصفحة حجوزاتك فوراً
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('/')


def register_view(request):
    if request.method == "POST":
        # نأخذ الحقول من الفورم (بما فيها الاسم الكامل)
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            # إنشاء المستخدم وتخزين اسمه في حقل first_name
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_name 
            user.save()
            
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('my_bookings')
            
    return render(request, "users/register.html")


@login_required
def delete_account(request):

    if request.method == "POST":
        user = request.user
        logout(request) # تسجيل خروج المستخدم أولاً
        user.delete()   # حذف المستخدم من قاعدة البيانات
        messages.success(request, "Your account has been permanently deleted.")
        return redirect('/')
    
    # إذا زار الصفحة عن طريق الخطأ نرجعه لصفحة الحجز
    return redirect('my_bookings')


@login_required
def profile_settings(request):
    user = request.user
    if request.method == "POST":
        # تحديث البيانات من الفورم
        user.first_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        # ملاحظة سيبرانية: تغيير اليوزر نيم ليتطابق مع الإيميل الجديد لضمان الدخول
        user.username = request.POST.get('email')
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile_settings')

    return render(request, "users/profile_settings.html", {'user': user})