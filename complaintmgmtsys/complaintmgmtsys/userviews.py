from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required

from cmsapp.models import CustomUser,UserReg,Category,Subcategory,State,Complaints,ComplaintRemark
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import json
from django.utils.timezone import now
from datetime import timedelta
from cmsapp.models import Complaints



@login_required(login_url='/')
def USERHOME(request):
    user_admin = request.user
    try:
        user_reg = UserReg.objects.get(admin=user_admin)
    except UserReg.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not registered.'})

    # Individual counts for display
    complaints_count = Complaints.objects.filter(userregid=user_reg).count()
    newcom_count = Complaints.objects.filter(status='0', userregid=user_reg).count()
    ipcom_count = Complaints.objects.filter(status='Inprocess', userregid=user_reg).count()
    closed_count = Complaints.objects.filter(status='Closed', userregid=user_reg).count()

    context = {
        'complaints_count': complaints_count,
        'newcom_count': newcom_count,
        'ipcom_count': ipcom_count,
        'closed_count': closed_count,
    }

    return render(request, 'user/userdashboard.html', context)

# def USERHOME(request):
#     user_admin = request.user
#     user_reg = UserReg.objects.get(admin=user_admin)
#     complaints_count = Complaints.objects.filter(userregid=user_reg).count()
#     newcom_count = Complaints.objects.filter(status='0',userregid=user_reg).count()
#     ipcom_count = Complaints.objects.filter(status='Inprocess',userregid=user_reg).count()
#     closed_count = Complaints.objects.filter(status='Closed',userregid=user_reg).count()
#     context = {
#     'complaints_count':complaints_count,
#     'newcom_count':newcom_count,
#     'ipcom_count':ipcom_count,
#     'closed_count':closed_count,        
#     }
#     return render(request,'user/userdashboard.html',context)

def USERSIGNUP(request):
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobno = request.POST.get('mobno', '').strip()        
        password = request.POST.get('password')
        password2 = request.POST.get('password2')  # New line

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('usersignup')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists')
            return redirect('usersignup')
        
        if not mobno:
            messages.error(request, 'Mobile number is required.')
            return redirect('usersignup')

        # Password confirmation check
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('usersignup')

        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            user_type=2,
            profile_pic=pic,
        )
        user.set_password(password)
        user.save()

        comuser = UserReg(
            admin=user,
            mobilenumber=mobno,
        )
        comuser.save()

        messages.success(request, 'Signup Successfully')
        return redirect('doLogin')

    return render(request, 'user/user_reg.html')

@login_required
def view_assigned_complaints(request):
    assigned_complaints = Complaints.objects.filter(assigned_to=request.user)
    
    return render(request, 'staff/assigned_complaints.html', {
        'complaints': assigned_complaints
    })



    return render(request,'user/user_reg.html')



@login_required(login_url='/')

def get_subcat(request):
    if request.method == 'GET':
        c_id = request.GET.get('c_id')
        subcat = Subcategory.objects.filter(cat_id=c_id)
        subcat_options = ''
        for subcategory in subcat:
            subcat_options += f'<option value="{subcategory.id}">{subcategory.subcatname}</option>'
        return JsonResponse({'subcat_options': subcat_options})



@login_required(login_url='/')

# def REGCOMPLAINT(request):
#     category = Category.objects.all()
#     state = State.objects.all()
#     if request.method == "POST":
#         cat_id = request.POST.get('cat_id')
#         subcategory_id_value = request.POST.get('subcategory_id')
#         complaint_number = random.randint(100000000, 999999999)
#         complainttype = request.POST.get('complainttype')
#         stateid = request.POST.get('stateid')
#         noc = request.POST.get('noc')
#         complaindetails = request.POST.get('complaindetails')
#         compfile = request.FILES.get('compfile')

#         cid = Category.objects.get(id=cat_id)
#         subcategory_id = Subcategory.objects.get(id=subcategory_id_value)
#         stateid_obj = State.objects.get(id=stateid)

#         # Accessing the UserReg instance associated with the logged-in user
#         userreg = request.user.userreg

#         complaint = Complaints(
#             cat_id=cid,
#             subcategory_id=subcategory_id,
#             complaint_number=complaint_number,
#             complainttype=complainttype,
#             stateid=stateid_obj,
#             noc=noc,
#             complaindetails=complaindetails,
#             compfile=compfile,
#             userregid=userreg  # Assigning the UserReg instance to userregid field
#         )
#         complaint.save()

#         messages.success(request, 'Complaint Lodged Successfully!!!')
#         return redirect("regcomplaint")
#     context = {
#         'category': category,
#         'state': state,
#     }    

#     return render(request, 'user/register-complaint.html', context)

def REGCOMPLAINT(request):
    category = Category.objects.all()
    state = State.objects.all()

    if request.method == "POST":
        try:
            # Extract form data
            cat_id = request.POST.get('cat_id')
            subcategory_id_value = request.POST.get('subcategory_id')
            complainttype = request.POST.get('complainttype')
            stateid = request.POST.get('stateid')
            noc = request.POST.get('noc')
            complaindetails = request.POST.get('complaindetails')
            compfile = request.FILES.get('compfile')
            # urgency = request.POST.get('urgency_level')

            # if not urgency:
            #     messages.error(request, "Please select an urgency level.")
            #     return redirect("regcomplaint")

            # Fetch related objects
            cid = Category.objects.get(id=cat_id)
            stateid_obj = State.objects.get(id=stateid)
            userreg = request.user.userreg  # Logged-in user

            # Fetch the Subcategory instance
            subcategory_id = None
            if subcategory_id_value:
                subcategory_id = Subcategory.objects.get(id=subcategory_id_value)

            # Generate a unique complaint number
            complaint_number = random.randint(100000000, 999999999)

            # Create Complaint instance
            complaint = Complaints(
                cat_id=cid,
                subcategory_id=subcategory_id,  # Assigning Subcategory instance now
                complaint_number=complaint_number,
                complainttype=complainttype,
                stateid=stateid_obj,
                noc=noc,
                complaindetails=complaindetails,
                compfile=compfile,
                userregid=userreg,
                # urgency=urgency,
            )
            complaint.save()

            messages.success(request, "Complaint Lodged Successfully!")
            return redirect("regcomplaint")

        except (Category.DoesNotExist, Subcategory.DoesNotExist, State.DoesNotExist):
            messages.error(request, "Invalid Category, Subcategory, or State selected.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    context = {
        'category': category,
        'state': state,
    }
    return render(request, 'user/register-complaint.html', context)

# from django.shortcuts import get_object_or_404

@login_required(login_url='/')
def COMPLAINTHISTORY(request):
    userreg = request.user.userreg
    # userreg = get_object_or_404(UserReg, admin=request.user)
    
    status = request.GET.get('status')

    # Debugging: print or log the status being filtered
    print(f"Filtering by status: {status}")

    # Filter based on status
    if status == '0':
        complaint_list = Complaints.objects.filter(userregid=userreg, status='0')
    elif status == 'Inprocess':
        complaint_list = Complaints.objects.filter(userregid=userreg, status='Inprocess')
    elif status == 'Closed':
        complaint_list = Complaints.objects.filter(userregid=userreg, status='Closed')
    else:
        complaint_list = Complaints.objects.filter(userregid=userreg)

    paginator = Paginator(complaint_list, 10)
    page_number = request.GET.get('page')
    try:
        complaints = paginator.page(page_number)
    except PageNotAnInteger:
        complaints = paginator.page(1)
    except EmptyPage:
        complaints = paginator.page(paginator.num_pages)

    context = {
        'complaints': complaints,
        'status_filter': status or 'all'
    }
    return render(request, 'user/complaint-history.html', context)

@login_required(login_url='/')

def COMPLAINTHISTORYDETAILS(request,id):
    complaints = Complaints.objects.get(id=id)
    complaintsremarks = ComplaintRemark.objects.filter(comp_id_id=id)
      
    context = {
         'complaints':complaints,
         'complaintsremarks':complaintsremarks,
    }
    return render(request,'user/complaint-details.html',context)
