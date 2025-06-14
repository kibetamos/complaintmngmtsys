from django.shortcuts import render,redirect,HttpResponse
from cmsapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import  logout,login
from django.contrib import messages
from cmsapp.models import CustomUser,Complaints
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from cmsapp.models import Category,Subcategory,State,Complaints,ComplaintRemark,UserReg,Team
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime



User = get_user_model()

from django.contrib.auth.decorators import login_required

def BASE(request):
       return render(request,'base.html')




def LOGIN(request):
    return render(request,'login.html')

def notifications(request):
    complaints1 = Complaints.objects.all()
    newcom_count1 = Complaints.objects.filter(status='0').count() 
    context = {
    'newcom_count1':newcom_count1,
    'complaints1':complaints1        
    }
    return render(request, 'includes/header.html', context)



def doLogout(request):
    logout(request)
    request.session.flush()  # Clear the session including CSRF token
    return redirect('login')

def doLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        keep_signed_in = request.POST.get('keep_signed_in')

        user = EmailBackEnd.authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('admin_home')
            elif user_type == '2':
                return redirect('user_home')
            elif user_type == '3':
                return redirect('staff_dashboard')
            
            else:
                return redirect('user_home')
            # user_type = user.user_type

            # if user_type == '3':
            #     return redirect('superadmin_dashboard')
            # elif user_type == '1':
            #     return redirect('admin_home')
            # elif user_type == '2':
            #     return redirect('user_home')
            # else:
            #     return redirect('user_home')
        else:
            messages.error(request, 'Email or Password is not valid')
            return redirect('login')  # Redirect back to the login page with an error message
    else:
        # If the request method is not POST, redirect to the login page with an error message
        # messages.error(request, 'Invalid request method')
        return redirect('login')


# @login_required
# def dashboard_redirect(request):
#     user_type = request.user.user_type

#     if user_type == 'superadmin':
#         return redirect('superadmin/admindashboard')
#     elif user_type == 'admin':
#         return redirect('admin/admindashboard')
#     elif user_type == 'staff':
#         return redirect('user/userdashboard')
#     else:
#         return redirect('user/userdashboard')
    


login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user":user,
    }
    return render(request,'profile.html',context)


# @login_required(login_url = '/')
# def PROFILE_UPDATE(request):
#     if request.method == "POST":
#         profile_pic = request.FILES.get('profile_pic')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         username = request.POST.get('username')
#         print(profile_pic)
        

#         try:
#             customuser = CustomUser.objects.get(id = request.user.id)
#             customuser.first_name = first_name
#             customuser.last_name = last_name
            

            
#             if profile_pic !=None and profile_pic != "":
#                customuser.profile_pic = profile_pic
#             customuser.save()
#             messages.success(request,"Your profile has been updated successfully")
#             return redirect('profile')

#         except:
#             messages.error(request,"Your profile updation has been failed")
#     return render(request, 'profile.html')
@login_required(login_url='/')
def PROFILE_UPDATE(request):
    user = CustomUser.objects.get(id=request.user.id)

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        try:
            user.first_name = first_name
            user.last_name = last_name

            # Update profile picture only if a new one is uploaded
            if profile_pic:
                user.profile_pic = profile_pic

            user.save()
            messages.success(request, "Your profile has been updated successfully")
            return redirect('profile')

        except Exception as e:
            messages.error(request, f"Profile update failed: {e}")

    # If GET or POST failed, render the form with current user data
    context = {
        "user": user,
    }
    return render(request, 'profile.html', context)

def CHANGE_PASSWORD(request):
     context ={}
     ch = User.objects.filter(id = request.user.id)
     
     if len(ch)>0:
            data = User.objects.get(id = request.user.id)
            context["data"]:data            
     if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
          user.set_password(new_pas)
          user.save()
          messages.success(request,'Password Change  Succeesfully!!!')
          user = User.objects.get(username=un)
          login(request,user)
        else:
          messages.success(request,'Current Password wrong!!!')
          return redirect("change_password")
     return render(request,'change-password.html')









