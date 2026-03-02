from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db.models import Q # Import this at the top
from django.contrib.auth import  login, get_user_model
from django.contrib import auth
from django.contrib.auth import logout
from final_app.models import AppliedJob, addjob, adminmodel, detail_of_jobseeker, usertables 
from django.shortcuts import  get_object_or_404
User = get_user_model()
import re


def about(request):
    return render (request,'about.html')


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('display')

def display(request):
    return render(request,'home.html')


def login_load_user(request):
    return render(request,'loginuser.html')


def signup_load_user(request):
    return render(request,'signupuser.html')



def login_load_admin(request):
    return render(request,'loginadmin.html')



def signup_load_admin(request):
    return render(request,'signupadmin.html')


def userfront_load(request):
    profile = usertables.objects.filter(jobseeker=request.user).first()
    return render(request, 'userfront.html', {'profile': profile})

def adminfront_load(request):
    return render (request,'adminfront.html')


def addjobadmin(request):
    return render (request,'addjobadmin.html')

def tracker_user(request):
    # 1. Get all jobs applied for by the logged-in user
    # 2. Use select_related to grab Job and Company names in one go
    user_apps = AppliedJob.objects.filter(user=request.user).order_by('-applied_at')
    
    # 3. Pass 'user_apps' to the template
    return render(request, 'tracker_user.html', {'user_apps': user_apps})


def job_applied_admin(request):
    # 1. Identify the recruiter
    current_admin = adminmodel.objects.get(jobadmin=request.user)
    
    # 2. Handle the Status Update
    if request.method == "POST":
        app_id = request.POST.get('app_id')
        new_status = request.POST.get('status') # This will be 'Accepted' or 'Declined'
        
        # Fetch the application linked to this admin for security
        application = get_object_or_404(AppliedJob, id=app_id, job__admin=current_admin)
        
        # Simple Logic: Directly update with the value from the button
        application.status = new_status
        application.save()
        
        color_msg = "approved" if new_status == "Accepted" else "rejected"
        messages.success(request, f"Application for {application.user.first_name} has been {color_msg}.")
        return redirect('job_applied_admin')

    # 3. Show applications for this admin's jobs
    applications = AppliedJob.objects.filter(job__admin=current_admin).order_by('-id')
    return render(request, 'jobappliedadmin.html', {'applications': applications})

def view_user_pro_admin(request):
    query = request.GET.get('search')
    # Default queryset
    jobseekers = detail_of_jobseeker.objects.all()

    if query:
        # Use Q objects for complex filtering across multiple fields
        jobseekers = jobseekers.filter(
            Q(f_name__icontains=query) | 
            Q(l_name__icontains=query) | 
            Q(email__icontains=query) |
            Q(skill__icontains=query) |
            Q(location__icontains=query) |
            Q(lat_quali__icontains=query) | # Added education to search
            Q(year_of_exp__icontains=query)
        ).distinct() # Use distinct to prevent duplicate rows if multiple Q matches
    
    return render(request, 'view_user_pro_admin.html', {
        'a': jobseekers,
        'search_query': query 
    })


def personal_detail_admin(request):
    ad=adminmodel.objects.get(jobadmin=request.user)
    return render (request,'personal_detail_admin.html',{'a':ad})

from .models import adminmodel, addjob # Ensure these are imported

def added_job_list(request):
    try:
        current_admin = adminmodel.objects.get(jobadmin=request.user)
    except adminmodel.DoesNotExist:
        return render(request, 'error.html', {'message': 'Admin profile not found'})

    # 2. Use that 'current_admin' instance to filter, NOT request.user
    ad = addjob.objects.filter(admin=current_admin)
    
    return render(request, 'added_job_list.html', {'a': ad})

def add_det_for_jobuser(request):
    # Check if details already exist
    exists = detail_of_jobseeker.objects.filter(user=request.user).exists()
    
    if exists:
        # Option A: Redirect them immediately
        messages.info(request, "You have already completed your profile.")
        return redirect('view_resume_user') 
    
    return render(request, 'add_det_for_jobuser.html', {'user': request.user})

def main_admin(request):
    return render (request,'main_admin.html')

def add_job_list_edit(request,pk):
    ad=addjob.objects.get(id=pk)
    return render (request,'added_job_list_edit.html',{'a':ad})


def add_job_list_delete(request,pk):
    ad=addjob.objects.get(id=pk)
    return render(request,'add_job_list_delete.html',{'ad':ad})



from django.db.models import Q # Ensure this is imported

from django.shortcuts import render
from .models import addjob, AppliedJob
from django.db.models import Q

def vac_of_job(request):
    query = request.GET.get('search')
    
    if query:
        ad = addjob.objects.filter(
            Q(job_name__icontains=query) | 
            Q(job_skill__icontains=query) |
            Q(job_qualification__icontains=query) |
            Q(admin__company_name__icontains=query)
        ).distinct()
    else:
        ad = addjob.objects.all()

    # Get the IDs of jobs the current user has already applied for
    applied_job_ids = []
    if request.user.is_authenticated:
        applied_job_ids = AppliedJob.objects.filter(user=request.user).values_list('job_id', flat=True)

    return render(request, 'vac_of_job.html', {
        'a': ad, 
        'query': query, 
        'applied_job_ids': applied_job_ids
    })


def view_resume_user(request):
    # .last() returns None if no record is found, instead of crashing
    us = detail_of_jobseeker.objects.filter(user=request.user).last()
    
    if not us:
        # Option A: Show a specific "No Resume" page
        # Option B: Pass 'us' as None and handle it in the same template
        messages.info(request, "You haven't created a resume yet. Please add your details.")
    
    return render(request, 'view_resume_user.html', {'a': us})


def user_detail_user(request):
    us=usertables.objects.filter(jobseeker=request.user).first()
    return render (request,'user_detail_user.html',{'a':us})



def usersignup_load(request):
    if request.method == 'POST':
        sfname = request.POST.get('fname')
        slname = request.POST.get('lname')
        semail = request.POST.get('email')
        susername = request.POST.get('username')
        spass = request.POST.get('pass')
        scpass = request.POST.get('cpass')
        pnumber = request.POST.get('pnumber')

        # 1. Password Match Check
        if spass != scpass:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signupuser.html')

        # 2. Password Strength Validation
        if len(spass) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'signupuser.html')
        elif not re.search('[A-Z]', spass):
            messages.error(request, 'Password must contain at least one uppercase letter (A-Z).')
            return render(request, 'signupuser.html')
        elif not re.search('[0-9]', spass):
            messages.error(request, 'Password must contain at least one digit (0-9).')
            return render(request, 'signupuser.html')
        elif not re.search(r'[@$!%*#?&]', spass):
            messages.error(request, 'Password must contain at least one special character (@, $, !, etc.).')
            return render(request, 'signupuser.html')

        # 3. Phone Number Validation (10 Digits)
        if not pnumber or len(pnumber) != 10 or not pnumber.isdigit():
            messages.error(request, 'Phone number must be exactly 10 digits.')
            return render(request, 'signupuser.html')

        # 4. Username Existence Check
        if User.objects.filter(username=susername).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'signupuser.html')

        # 5. Create User and Jobseeker Profile
        user = User.objects.create_user(
            first_name=sfname,
            last_name=slname,
            username=susername,
            email=semail,
            password=spass
        )
        
        jobseeker = usertables(
            phonenumber=pnumber,
            jobseeker=user
        )
        jobseeker.save()
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login_load_user')

    return render(request, 'signupuser.html')

       



def userlog_load(request):
    if request.method=='POST':
        susername=request.POST.get('username')
        spass=request.POST.get('pass')
        user=auth.authenticate(
            username=susername,
            password=spass
        )
        if user is not None:
            jobseeker=usertables.objects.filter(jobseeker=user.id).first()
            if jobseeker:
                auth.login(request,user)
                return redirect('userfront_load')
            else:
                messages.warning(request,"This account doesn't have a  profile.")
                return redirect('login_load_user')
        else:
            messages.error(request,"invalid email or password")
            return redirect('login_load_user')

    return redirect ('login_load_user')
            


def adminsignup_load(request):
    if request.method == 'POST':
        sfname = request.POST.get('fname')
        slname = request.POST.get('lname')
        eemail = request.POST.get('eemail')
        susername = request.POST.get('username')
        scompany = request.POST.get('company')
        spass = request.POST.get('pass')
        scpass = request.POST.get('cpass')

        # 1. Check if Passwords match
        if spass != scpass:
            messages.info(request, 'Passwords do not match')
            return render(request, 'signupadmin.html')

        # 2. Strong Password Validation
        if len(spass) < 8:
            messages.info(request, 'Password must be at least 8 characters long.')
            return render(request, 'signupadmin.html')
        
        elif not re.search('[A-Z]', spass):
            messages.info(request, 'Password must have at least one uppercase letter.')
            return render(request, 'signupadmin.html')
            
        elif not re.search('[0-9]', spass):
            messages.info(request, 'Password must have at least one number.')
            return render(request, 'signupadmin.html')

        elif not re.search('[@#$!%*?&]', spass):
            messages.info(request, 'Password must have at least one special character (@, #, $, etc.).')
            return render(request, 'signupadmin.html')

        # 3. Check if username already exists (Crucial step)
        if User.objects.filter(username=susername).exists():
            messages.info(request, 'Username already taken.')
            return render(request, 'signupadmin.html')

        # 4. Success Path: If all checks pass, create the user
        user = User.objects.create_user(
            first_name=sfname,
            last_name=slname,
            username=susername,
            email=eemail,
            password=spass
        )
        
        # 5. Create the Admin Profile
        job_profile = adminmodel(
            company_name=scompany,
            jobadmin=user
        )
        job_profile.save()
        
        messages.success(request, 'Account created successfully!')
        return redirect('login_load_admin')

    # If GET request, just show the page
    return render(request, 'signupadmin.html')



def adminlog_load(request):
    if request.method == 'POST':
        susername = request.POST.get('username')
        spass = request.POST.get('pass')
        user = auth.authenticate(username=susername, password=spass)

        if user is not None:
            if user.is_staff:
                auth.login(request, user)

                return render(request, 'main_admin.html')
            # 1. Look for the Admin/Employer profile linked to this user
            admin_profile = adminmodel.objects.filter(jobadmin=user.id).first()

            if admin_profile:
                # 2. Login and redirect to Admin dashboard
                auth.login(request, user)
                # messages.info(request, f"Welcome, {susername} ({admin_profile.company_name})")
                return redirect('adminfront_load')
            else:
                # 3. User exists, but isn't an Admin (maybe they are a Jobseeker)
                messages.error(request, "This account is not registered as an Admin.")
                return redirect('login_load_admin')
        else:
            # 4. Invalid credentials
            messages.error(request, 'Invalid username or password')
            return render(request, 'loginadmin.html')
            
    return render(request, 'loginadmin.html')


def add_job(request):
    if request.method=='POST':
        job=request.POST.get('job')
        salary=request.POST.get('salary')
        skill=request.POST.get('skill')
        quali=request.POST.get('quali')
        admin_profile = adminmodel.objects.get(jobadmin=request.user)
        add=addjob(
            admin=admin_profile,
            job_name=job,
            job_salary=salary,
            job_skill=skill,
            job_qualification=quali
        )
        add.save()

        return redirect ('addjobadmin')

def det_fo_jobuser_save(request):
    if request.method == 'POST':
        # Get data from POST
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('eemail')
        dob = request.POST.get('dob')
        ph = request.POST.get('pnumber')
        loc = request.POST.get('location')
        quali = request.POST.get('l_quali')
        skills = request.POST.get('skills')
        exp = request.POST.get('expe')
        img = request.FILES.get('image')

        # --- VALIDATION AND CLEANING ---
        
        # 1. Phone Number Validation
        if not ph or len(ph) != 10 or not ph.isdigit():
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect('add_det_for_jobuser')

        # 2. Integer/Date Fixes
        clean_dob = dob if dob else None
        clean_ph = int(ph) 
        clean_exp = int(exp) if exp and exp.strip() else 0

        # Check if the user already has a detail record
        if detail_of_jobseeker.objects.filter(user=request.user).exists():
            messages.warning(request, "You have already added your details.")
            return redirect('view_resume_user')

        # Create the record
        detail = detail_of_jobseeker(
            user=request.user,
            f_name=fname,
            l_name=lname,
            email=email,
            dob=clean_dob,
            phonenumber=clean_ph,
            location=loc,
            lat_quali=quali,
            skill=skills,
            year_of_exp=clean_exp,
            img=img
        )
        detail.save()
        
   
        return redirect('userfront_load')

    return redirect('add_det_for_jobuser')

def apply_now(request, pk):
    if request.user.is_authenticated:
        job_obj = addjob.objects.get(id=pk)
        # Check if already applied to prevent duplicates
        if AppliedJob.objects.filter(job=job_obj, user=request.user).exists():
            messages.warning(request, "You have already applied for this job.")
        else:
            AppliedJob.objects.create(job=job_obj, user=request.user)
        return redirect('vac_of_job')
    else:
        return redirect('login_load_user')




def add_job_list_edit_load(request,pk):
    if request.method=='POST':
        job=addjob.objects.get(id=pk)
        job.job_name=request.POST.get('name')
        job.job_salary=request.POST.get('salary')
        job.job_skill=request.POST.get('skill')
        job.job_qualification=request.POST.get('quali')
        job.save()
        return redirect ('added_job_list')
    return redirect('added_job_list')   



def add_job_list_delete_load(request,pk):
    job=addjob.objects.get(id=pk)
    job.delete()
    return redirect('added_job_list')

def personal_detail_admin_edit(request,pk):
    ad=adminmodel.objects.get(id=pk)
    return render(request,'personal_detail_admin_edit.html',{'a':ad})


def personal_detail_admin_edit_load(request,pk):
    if request.method=='POST':
        admi=adminmodel.objects.get(id=pk)
        use=admi.jobadmin
        use.first_name=request.POST.get('fname')
        use.last_name=request.POST.get('lname')
        use.email=request.POST.get('email')
        use.username=request.POST.get('usname')
        admi.company_name=request.POST.get('comname')
        use.save()
        admi.save()
        return redirect ('personal_detail_admin')
    return redirect('personal_detail_admin') 

def view_resume_user_edit (request,pk):
    us=detail_of_jobseeker.objects.get(id=pk)
    return render(request,'view_resume_user_edit.html',{'a':us})


def view_resume_user_edit_load (request,pk):
    if request.method=='POST':
        view=detail_of_jobseeker.objects.get(id=pk)
        if 'image' in request.FILES:
            view.img = request.FILES['image']
        view.f_name=request.POST.get('fname')
        view.l_name=request.POST.get('lname')
        view.email=request.POST.get('email')
        dob = request.POST.get('dob')
        view.dob = dob if dob else None
        view.phonenumber=request.POST.get('phnum')
        view.location=request.POST.get('loc')
        view.lat_quali=request.POST.get('qua')
        view.skill=request.POST.get('skill')
        view.year_of_exp=request.POST.get('yofexp')
        view.save()
        return redirect ('view_resume_user')



def recru_list_main(request):
    ad=adminmodel.objects.all()
    return render (request,'recru_list_main.html',{'a':ad})


def recru_list_main_edit (request,pk):
    ad=adminmodel.objects.get(id=pk)
    return render (request,'recru_list_main_edit.html',{'a':ad})


def recru_list_main_edit_load (request,pk):
    if request.method=='POST':
        admi=adminmodel.objects.get(id=pk)
        use=admi.jobadmin
        use.first_name=request.POST.get('fname')
        use.last_name=request.POST.get('lname')
        use.email=request.POST.get('email')
        use.username=request.POST.get('username')
        use.save()
        admi.company_name=request.POST.get('com_name')
        admi.save()
       
        return redirect ('recru_list_main')
    return redirect('recru_list_main')

def recru_list_main_delete (request,pk):
    ad=adminmodel.objects.get(id=pk)
    return render (request,'recru_list_main_delete.html',{'a':ad})

def recru_list_main_delete_load(request,pk):
    ad=adminmodel.objects.get(id=pk)
    ad.delete()
    return redirect ('recru_list_main')




def job_seeker_list_main (request):
    ad=usertables.objects.all()
    return render(request,'job_seeker_list_main.html',{'a':ad})



def job_seeker_list_main_edit(request, pk):
    ad = get_object_or_404(usertables, id=pk)
    
    if request.method == 'POST':
        phone = request.POST.get('phonenumber', '')
        
        # Validation: Check if it's numeric and exactly 10 digits
        if len(phone) == 10 and phone.isdigit():
            ad.phonenumber = phone
            ad.save()
            messages.success(request, "Phone number updated successfully!")
            return redirect('your_list_view_name') # Redirect back to the list
        else:
            messages.error(request, "Phone number must be exactly 10 digits.")
            
    return render(request, 'job_seeker_list_main_edit.html', {'a': ad})


def job_seeker_list_main_edit_load(request,pk):
    if request.method=='POST':
        ad=usertables.objects.get(id=pk)
        ad.jobseeker.first_name=request.POST.get('fname')
        ad.jobseeker.last_name=request.POST.get('lname')
        ad.jobseeker.email=request.POST.get('email')
        ad.jobseeker.username=request.POST.get('username')
        ad.phonenumber=request.POST.get('pnum')
        ad.jobseeker.save()
        ad.save()
        return redirect ('job_seeker_list_main')



def jobseeker_main_delete (request,pk):
    ad=usertables.objects.get(id=pk)
    return render (request,'jobseeker_main_delete.html',{'a':ad})


def jobseeker_main_delete_load(request,pk):
    ad=usertables.objects.get(id=pk)
    ad.delete()
    return redirect ('job_seeker_list_main')


def job_list_main(request):
    ad=addjob.objects.all().select_related('admin')
    return render (request,'job_list_main.html',{'a':ad})

def job_list_main_edit(request,pk):
    ad=addjob.objects.get(id=pk)
    return render (request,'job_list_main_edit.html',{'a':ad}  )


def job_list_main_edit_load(request,pk):
    if request.method=='POST':
        ad=addjob.objects.get(id=pk)
        ad.job_name=request.POST.get('name')
        ad.job_qualification=request.POST.get('quali')
        ad.job_skill=request.POST.get('skill')
        ad.job_salary=request.POST.get('salary')
        ad.save()
        return redirect ('job_list_main')

def job_list_main_delete(request, pk):  # Must match the name in urls.py
    job = addjob.objects.get(id=pk)
    job.delete()
    return redirect('job_list_main')


def user_detail_user_edit(request,pk):
    ad=usertables.objects.get(id=pk)
    return render (request,'user_detail_user_edit.html',{'a':ad})


def user_detail_user_edit_load(request,pk):
    if request.method=='POST':
        ad=usertables.objects.get(id=pk)
        ad.jobseeker.first_name=request.POST.get('fname')
        ad.jobseeker.last_name=request.POST.get('lname')
        ad.jobseeker.email=request.POST.get('email')
        ad.jobseeker.username=request.POST.get('username')
        ad.phonenumber=request.POST.get('phonum')
        ad.jobseeker.save()
        ad.save()
        return redirect ('user_detail_user')



def view_user_pro_admin_edit(request,pk):
    ad=detail_of_jobseeker.objects.get(id=pk)
    return render (request,'view_user_pro_admin_edit.html',{'i':ad})



def view_user_pro_admin_edit_load(request,pk):
    ad=detail_of_jobseeker.objects.get(id=pk)
    if request.method=='POST':
        ad.f_name=request.POST.get('fname')
        ad.l_name=request.POST.get('lname')
        ad.email=request.POST.get('email')
        ad.dob=request.POST.get('dob')
        ad.phonenumber=request.POST.get('phnum')
        ad.location=request.POST.get('loc')
        ad.lat_quali=request.POST.get('qua')
        ad.skill=request.POST.get('skill')
        ad.year_of_exp=request.POST.get('exp')
        ad.save()
        return redirect ('view_user_pro_admin')


def view_user_pro_admin_delete(request,pk):
    ad=detail_of_jobseeker.objects.get(id=pk)
    ad.delete()
    return redirect ('view_user_pro_admin')

# Create your views here.


# Create your views here.
