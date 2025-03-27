from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.core.mail import send_mail
from .models import OTPModel,Users,Story
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm,StoryForm

# 📌 Function to send OTP
def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            otp = OTPModel().generate_otp()  # Generate 6-digit OTP
            request.session['otp'] = otp  # Store OTP in session
            request.session['email'] = email  # Store email for verification

            # 📧 Send OTP via Email
            send_mail(
                'Your OTP Code',
                f'Your OTP for verification is {otp}. Do not share it with anyone.',
                'your_email@gmail.com',  # Sender Email
                [email],  # Recipient
                fail_silently=False,
            )
            return redirect('verify_otp')  # Redirect to OTP verification page

    return render(request, 'send_otp.html')


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        email = request.session.get('email')

        if entered_otp == stored_otp:
            user = User.objects.filter(email=email).first()
            if user:
                login(request, user)  # 🔐 Django Authentication Login
                del request.session['otp']  # Remove OTP from session

                # Check if user profile exists, if not, redirect to profile update page
                profile_exists = Users.objects.filter(user=user).exists()
                if not profile_exists:
                    return redirect('update_profile')

                return redirect('dashboard')
            return HttpResponse(f"✅ OTP Verified Successfully for {email}!")
        else:
            return HttpResponse("❌ Invalid OTP, Try Again!")

    return render(request, 'verify_otp.html')

@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('dashboard')  # Redirect after saving

    else:
        form = ProfileForm()

    return render(request, 'update_profile.html', {'form': form})


def homepage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request,'homepage.html')

@login_required
def dashboard(request):
    stories = Story.objects.all().order_by('-created_at')  # Get all stories (latest first)

    if request.method == 'POST':  # If user submits a story
        if request.user.is_authenticated:
            form = StoryForm(request.POST)
            if form.is_valid():
                story = form.save(commit=False)
                story.user = request.user  # Assign the logged-in user
                story.save()
                return redirect('dashboard')  # Reload page after submission
        else:
            return redirect('send_otp')  # Redirect unauthenticated users

    else:
        form = StoryForm()

    return render(request, 'dashboard.html', {'stories': stories, 'form': form})


def logout_user(request):
    logout(request)
    request.session.flush()
    return redirect('homepage')
