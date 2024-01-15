from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as loginuser, authenticate, logout
from myapp.models import profile as profile_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.mail import send_mail
from shraddha.settings import EMAIL_HOST_USER
from django.contrib import messages
import random
from .models import User
from django.http import HttpResponseForbidden

from django.contrib.auth.decorators import user_passes_test
User = get_user_model()
# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        rejection_message = request.session.pop('rejection_message', None)
        context = {
            "form": form,
            "rejection_message":rejection_message
        }

        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                loginuser(request, user)
                # return HttpResponse("logi succs")

                return redirect('profile')
        else:
            context = {
                "form": form
            }

            return render(request, 'login.html', context=context)

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            user = User.objects.create_user(
                username=username, password=password1)
            user = authenticate(username=username, password=password1)
            print(user)

            if user is not None:
                otp = random.randint(100000,999999)
                send_mail("User data",f"Verfiy your mail by otp:\n {otp}",EMAIL_HOST_USER,[email])
                request.session['otp'] = otp
                # loginuser(request,user)
                return render(request,'verify.html',{"otp":otp})
                #return HttpResponse("registration success")
            else:
                return HttpResponse("password didnt match"
                                    )
    return render(request, 'signup.html')
def verifyOTP(request):
    if request.method == 'POST':
        submittedOTP = request.POST.get('otp')
        storedOTP = request.session.get('otp')


        if submittedOTP == str(storedOTP):
            messages.success(request,"email verified successfully")
            #return  HttpResponse('verfied')
            return redirect('login')
        else:
            messages.error(request,"invalid otp")
            return HttpResponse("wrong otp")
# def signout(request):
#     logout(request)
#     return redirect('index')
#     return render(request,'index.html')


def signout(request):
    logout(request)
    return redirect('index')


# def profile(request):
#     return render(request,'profile.html')
@login_required
def profile(request):
    profiles = profile_model.objects.filter(user=request.user)

    context = {
        "profiles": profiles
    }

    return render(request, 'profile.html', context)


def add(request):
    user = request.user

    if request.method == 'POST':
        name = request.POST.get('name')
        domain = request.POST.get('domain')
        bio = request.POST.get('bio')

        try:
            # print(request.user,"shraddha"==request.user,str(request.user))
            # print(request.user.name)
            user = User.objects.get(username=str(user))
            print(user)
        except Exception as e:
            print(e)
            print("not found ")
            return redirect("profile")
        
        if name and domain and bio:
            # print(dict(profile(request)))
            # print(type(User),type(profile))
            new_user = profile_model(
                user=user, name=name, domain=domain, bio=bio)
            print(new_user)

            new_user.save()
            profiles_list = []
            for pr in profile_model.objects.filter(user=user):
                profiles_list.append(pr)
            print(profiles_list)
            return render(request, "profile.html", {"profiles": profiles_list})
    profiles = profile_model.objects.filter(user=user)

    context = {
        "profiles": profiles
    }

    return render(request, 'profile.html', context)


# def update(request, id):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         domain = request.POST.get('domain')
#         bio = request.POST.get('bio')

#         try:
#             profiles = profile_model.objects.get(id=id)
#             profiles.name = name
#             profiles.domain = domain
#             profiles.bio = bio
#             profiles.save()

#             return redirect('profile')
#         except profiles.DoesNotExist:
#             pass
#     return render(request, 'profile.html')
 
 

def delete_profile(request, profile_id):
    profile_instance = get_object_or_404(profile_model, id=profile_id)

    if request.method == 'POST':
        profile_instance.delete()
        return redirect('profile')

    return HttpResponse("Invalid request method for delete")


def update(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        domain = request.POST.get('domain')
        bio = request.POST.get('bio')

        try:
            profile_instance = profile_model.objects.get(id=id)
            profile_instance.name = name
            profile_instance.domain = domain
            profile_instance.bio = bio
            profile_instance.save()

            return redirect('profile')
        except profile_model.DoesNotExist:
            raise Http404

    return render(request, 'profile.html')


@login_required
def admin_dashboard(request):
    if request.user.is_staff:
        users = User.objects.all()
        return render(request, 'admin_dashboard.html', {'users': users})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")
    

@login_required(login_url='login')
def admin_approve_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'User {user.username} approved successfully!')
    return redirect('admin_dashboard')

@login_required(login_url='login')
def admin_reject_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'User {user.username} rejected!')
    request.session['rejection_message'] = f'Sorry, your registration request has been rejected. Please contact the admin for further details.'
    return redirect('admin_dashboard')