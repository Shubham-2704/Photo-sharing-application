from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import Count
from django.core.mail import send_mail
from myproject.settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required




# Create your views here.

def index (request):
    # Get the sorting parameter from the request
    sort_by = request.GET.get('sort_by', 'latest')  # Default to 'latest'

    # Fetch all photos and apply sorting
    if sort_by == 'most_liked':
        photos = UserPhoto.objects.annotate(like_count=Count('likes')).order_by('-like_count')
    elif sort_by == 'most_disliked':
        photos = UserPhoto.objects.annotate(dislike_count=Count('dislikes')).order_by('-dislike_count')
    elif sort_by == 'oldest':
        photos = UserPhoto.objects.all().order_by('uploaded_at')  # Oldest first
    else:
        photos = UserPhoto.objects.all().order_by('-uploaded_at')  # Default to latest

    context = {
        'photos' : photos,
        'sort_by' : sort_by
    }
    return render (request, 'index.html', context)

def loginpage (request):
    if request.method == 'POST':
        username = request.POST.get ('username')
        password = request.POST.get ('password')

        user = authenticate (request, username  =username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, "Username or Password is incorrect.")

    return render (request, 'login.html')

def signuppage (request):
    if request.method == 'POST':
        username = request.POST.get ('username')
        firstname =  request.POST.get ('firstname')
        lastname =  request.POST.get ('lastname')
        email =  request.POST.get ('email')
        password1 =  request.POST.get ('password1')
        password2 =  request.POST.get ('password2')

        if password1 != password2:
            messages.error (request , "Your Password and Confirm Password do not match.")
            return redirect ('signup')
        
        if User.objects.filter (username = username).exists():
            messages.error (request, "Username already taken. Please choose another one.")
            return redirect ('signup')
        
        if User.objects.filter (email = email).exists():
           messages.error (request, "Email is already registered. Try logging in instead.") 
           return redirect ('signup')
        
        user = User.objects.create_user (username, email, password1)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        messages.success (request, "Your account has been successfully created. You can now log in.")
        return redirect ('login')
    
    return render (request, 'signup.html')

def logoutpage (request):
    logout (request)
    return redirect ('index')

@login_required (login_url='login')
def upload_photos (request):
    if request.method == 'POST':
        photos = request.FILES.getlist('photos')
        
        # Check if the user has already uploaded 5 photos
        existing_photos_count = UserPhoto.objects.filter(user=request.user).count()
        if existing_photos_count + len(photos) > 50:
            messages.error(request, "You can only upload a maximum of 5 photos.")
            return redirect('upload')
        
        # Save each photo
        for photo in photos:
            UserPhoto.objects.create(user=request.user, photo=photo)
        
        messages.success(request, "Photos uploaded successfully!")
        return redirect('upload')

    return render (request, 'upload.html')

@login_required (login_url='login')
def update_photo (request, photo_id):
    photo = UserPhoto.objects.get (id=photo_id, user=request.user)
    
    if request.method == 'POST':
        new_photo = request.FILES.get('photo')
        if new_photo:
            photo.photo = new_photo
            photo.save()
            messages.success(request, "Photo updated successfully!")
            return redirect('profile')
        
    return render (request, 'update.html')

@login_required (login_url='login')
def delete_photo (request, photo_id):
    photo = UserPhoto.objects.get (id=photo_id, user=request.user)
    photo.delete()
    messages.success(request, "Photo deleted successfully!")
    return redirect('profile')


def like_photo(request, photo_id):
    photo = UserPhoto.objects.get(id=photo_id)
    
    if request.user in photo.likes.all():
        messages.warning(request, "You have already liked this photo.")
    elif request.user in photo.dislikes.all():
        photo.dislikes.remove(request.user)
        photo.likes.add(request.user)
        messages.success(request, "You liked this photo.")
    else:
        photo.likes.add(request.user)
        messages.success(request, "You liked this photo.")
    
    return redirect('index')


def dislike_photo(request, photo_id):
    photo = UserPhoto.objects.get(id=photo_id)
    
    if request.user in photo.dislikes.all():
        messages.warning(request, "You have already disliked this photo.")
    elif request.user in photo.likes.all():
        photo.likes.remove(request.user)
        photo.dislikes.add(request.user)
        messages.success(request, "You disliked this photo.")
    else:
        photo.dislikes.add(request.user)
        messages.success(request, "You disliked this photo.")
    
    return redirect('index')

@login_required (login_url='login')
def profile (request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST' and 'profile_photo' in request.FILES:
        profile.profile_photo = request.FILES['profile_photo']
        profile.save()
        messages.success(request, "Profile photo updated successfully!")
        return redirect('profile')

    user_photos = UserPhoto.objects.filter(user=request.user)
    context = {
        'profile': profile,
        'user_photos': user_photos,
    }
    return render (request, 'profile.html', context)

@login_required (login_url='login')
def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Update user details
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.username = request.POST.get('username', user.username)
        user.save()

        # Update profile photo
        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']
            profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    context = {
        'profile': profile
    }
    return render(request, 'edit_profile.html', context)

def forgotpassword (request):
    if request.method == "POST":
        email = request.POST.get ("email")
        print(email)

        if User.objects.filter (email = email).exists():
            user = User.objects.get (email = email)
            print("User Exists")

            send_mail ("Reset Your Password : ", f"Hey User : {user}! To Reset Password, Click on the Given Link \n http://127.0.0.1:8000/resetpassword/{user}/", EMAIL_HOST_USER, [email], fail_silently=True)
            messages.success (request, f"Hey User : {user}! A password reset link has been sent to your email. Please check your inbox.")
        
        else:
            messages.error(request, "No account found with this email address.")

        return render (request ,'forgotpassword.html')
    return render (request ,'forgotpassword.html')

def resetpassword (request, user):
    userid = User.objects.get (username = user)
    print(userid)
    if request.method == "POST":
        pass1 = request.POST.get ("newpassword")
        pass2 = request.POST.get ("confirmpassword")
        print(pass1, pass2)

        if pass1 != pass2:
            messages.error (request , "Your Password and Confirm Password do not match.")


        if pass1 == pass2:
            userid.set_password(pass1)
            userid.save()
            messages.success (request, "Your Password has been successfully Changed. You can now log in.")
            # return redirect ('login')

    return render (request ,'resetpassword.html')

def contact_us (request):
    if request.method == "POST":

        Name = request.POST.get("name")
        Email = request.POST.get("email")
        Messages = request.POST.get("message")
        Subject = request.POST.get("subject")
        formdata = ContactForm(name=Name, email=Email, subject=Subject, message=Messages)

        formdata.save()
        messages.success (request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact_us')

    return render (request, 'contact-us.html')