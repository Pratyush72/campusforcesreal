# admin_panel/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, FileResponse, HttpResponseForbidden, HttpResponse,HttpResponseNotAllowed
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
import os
# admin_panel/views.py
# sahi
from accounts.models import LiveWorkProject, Project, CustomUser, LiveWorkSubmission 
 

# Import models from accounts / careers (adjust if your apps named differently)
from accounts.models import Project, LiveWorkProject, CustomUser
from careers.models import JobApplication, Career

# Admin-only check
def admin_required(user):
    return user.is_active and (user.is_staff or user.is_superuser)

# -------------------------
# AUTH (simple admin login using Django auth)
# -------------------------
def admin_login(request):
    # if already logged in and admin -> redirect dashboard
    if request.user.is_authenticated and admin_required(request.user):
        return redirect('admin_panel:dashboard')

    error = None
    if request.method == 'POST':
        email = request.POST.get('email') or request.POST.get('username')  # support either field
        password = request.POST.get('password')
        # authenticate by username (AbstractUser uses username) or email; it depends on your AUTH config.
        user = authenticate(request, username=email, password=password)
        if user is None:
            # try authenticate by email if your AUTH backend supports it; fallback check:
            try:
                u = CustomUser.objects.filter(email=email).first()
                if u:
                    user = authenticate(request, username=u.username, password=password)
            except Exception:
                user = None

        if user and admin_required(user):
            login(request, user)
            return redirect('admin_panel:dashboard')
        else:
            error = "Invalid credentials or you don't have admin access."
    return render(request, 'admin_panel/login.html', {'error': error})

@login_required(login_url='admin_panel:login')
def admin_logout(request):
    logout(request)
    return redirect('admin_panel:login')

# -------------------------
# DASHBOARD
# -------------------------
@login_required(login_url='admin_panel:login')
@user_passes_test(admin_required, login_url='admin_panel:login')
def dashboard(request):
    stats = {
        'total_users': CustomUser.objects.count(),
        'total_projects': Project.objects.count(),
        'total_livework': LiveWorkProject.objects.count(),
        'total_job_apps': JobApplication.objects.count(),
    }
    # Recent entries
    recent_projects = Project.objects.order_by('-id')[:6]
    recent_live = LiveWorkProject.objects.order_by('-id')[:6]
    recent_jobs = JobApplication.objects.select_related('user','job').order_by('-applied_at')[:6]

    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'recent_projects': recent_projects,
        'recent_live': recent_live,
        'recent_jobs': recent_jobs,
    })

# -------------------------
# PROJECTS CRUD
# -------------------------
@login_required(login_url='admin_panel:login')
@user_passes_test(admin_required, login_url='admin_panel:login')
def manage_projects(request):
    projects = Project.objects.all().order_by('-id')
    return render(request, 'admin_panel/manage_projects.html', {'projects': projects})

@login_required(login_url='admin_panel:login')
@user_passes_test(admin_required, login_url='admin_panel:login')
def add_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image_url = request.POST.get('image_url')
        download_url = request.POST.get('download_url')
        is_free = request.POST.get('is_free') == 'on'
        plan_required = request.POST.get('plan_required') or None
        p = Project.objects.create(
            title=title, description=description, image_url=image_url,
            download_url=download_url, is_free=is_free, plan_required=plan_required
        )
        messages.success(request, 'Project created.')
        return redirect('admin_panel:manage_projects')
    return render(request, 'admin_panel/project_form.html', {'action': 'Add'})

@login_required(login_url='admin_panel:login')
@user_passes_test(admin_required, login_url='admin_panel:login')
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.image_url = request.POST.get('image_url')
        project.download_url = request.POST.get('download_url')
        project.is_free = request.POST.get('is_free') == 'on'
        project.plan_required = request.POST.get('plan_required') or None
        project.save()
        messages.success(request, 'Project updated.')
        return redirect('admin_panel:manage_projects')
    return render(request, 'admin_panel/project_form.html', {'action': 'Edit', 'project': project})

@login_required(login_url='admin_panel:login')
@user_passes_test(admin_required, login_url='admin_panel:login')
@require_POST
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    messages.success(request, 'Project deleted.')
    return redirect('admin_panel:manage_projects')

# -------------------------
# LIVEWORK CRUD
# -------------------------
@login_required(login_url='admin_panel:login')
@user_passes_test(admin_required, login_url='admin_panel:login')

# Manage LiveWork
def manage_livework(request):
    liveworks = LiveWorkProject.objects.all()  # yaha se sab LiveWorkProject fetch ho raha hai
    context = {
        'liveworks': liveworks
    }
    return render(request, 'admin_panel/manage_livework.html', context)

# Add LiveWork
def add_livework(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        plan_required = request.POST.get('plan_required')
        coins_reward = request.POST.get('coins_reward', 50)

        LiveWorkProject.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            plan_required=plan_required,
            coins_reward=coins_reward
        )
        messages.success(request, "LiveWork Project added successfully")
        return redirect('admin_panel:manage_livework')

    return render(request, 'admin_panel/add_livework.html')

# Edit LiveWork
from django.shortcuts import render, redirect, get_object_or_404
def edit_livework(request, pk):
    livework = get_object_or_404(LiveWorkProject, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        plan_required = request.POST.get('plan_required')
        coins_reward = request.POST.get('coins_reward') or 0

        # Validate date fields
        if not start_date or not end_date:
            error = "Start date and End date are required."
            return render(request, 'admin_panel/edit_livework.html', {
                'livework': livework,
                'action': 'Update',
                'error': error
            })

        # Update object
        livework.title = title
        livework.description = description
        livework.start_date = start_date
        livework.end_date = end_date
        livework.plan_required = plan_required
        livework.coins_reward = coins_reward
        livework.save()

        return redirect('admin_panel:manage_livework')

    # GET request
    return render(request, 'admin_panel/edit_livework.html', {
        'livework': livework,
        'action': 'Update'
    })


# Delete LiveWork
def delete_livework(request, pk):
    project = get_object_or_404(LiveWorkProject, pk=pk)
    project.delete()
    messages.success(request, "LiveWork Project deleted successfully")
    return redirect('admin_panel:manage_livework')

@login_required(login_url='admin_panel:login')
@user_passes_test(admin_required, login_url='admin_panel:login')
@require_POST
def delete_livework(request, pk):
    item = get_object_or_404(LiveWorkProject, pk=pk)
    item.delete()
    messages.success(request, 'LiveWork project deleted.')
    return redirect('admin_panel:manage_livework')

# -------------------------
# JOB APPLICATIONS (view, change status, download resume)
# -------------------------
@login_required(login_url='admin_panel:login')
@user_passes_test(admin_required, login_url='admin_panel:login')
def manage_jobs(request):
    apps = JobApplication.objects.select_related('user','job').order_by('-applied_at')
    return render(request, 'admin_panel/manage_jobs.html', {'apps': apps})

@login_required(login_url='admin_panel:login')
@user_passes_test(admin_required, login_url='admin_panel:login')
@require_POST
def update_job_status(request, pk):
    job_app = get_object_or_404(JobApplication, pk=pk)
    if request.method == "POST":
        status = request.POST.get("status")
        job_app.status = status

        # conditional fields
        if status == "shortlisted":
            job_app.assessment_link = request.POST.get("assessment_link", "")
            job_app.rejection_reason = ""  # clear rejection if previously rejected
        elif status == "rejected":
            job_app.rejection_reason = request.POST.get("rejection_reason", "")
            job_app.assessment_link = ""  # clear assessment if previously shortlisted
        else:
            job_app.assessment_link = ""
            job_app.rejection_reason = ""

        job_app.save()
        messages.success(request, "Job application updated successfully!")
        return redirect('admin_panel:manage_jobs')
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required(login_url='admin_panel:login')
@user_passes_test(admin_required, login_url='admin_panel:login')
def download_resume(request, pk):
    app = get_object_or_404(JobApplication, pk=pk)
    if not app.resume:
        return HttpResponse("No resume attached.", status=404)
    path = app.resume.path
    filename = os.path.basename(path)
    response = FileResponse(open(path, 'rb'), as_attachment=True, filename=filename)
    return response


# --------------------
# manage user details
# --------------------

from django.shortcuts import render
from accounts.models import CustomUser

def manage_users(request):
    users = CustomUser.objects.all()
    return render(request, 'admin_panel/manage_users.html', {'users': users})


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.mobile_number = request.POST.get('mobile_number')
        user.coins = request.POST.get('coins')

        # ✅ Handle subscription dates properly
        membership_start_date = request.POST.get('membership_start_date')
        membership_end_date = request.POST.get('membership_end_date')

        user.membership_start_date = (
            datetime.strptime(membership_start_date, '%Y-%m-%d').date()
            if membership_start_date else None
        )
        user.membership_end_date = (
            datetime.strptime(membership_end_date, '%Y-%m-%d').date()
            if membership_end_date else None
        )
        user.current_plan = request.POST.get('current_plan', user.current_plan)

        user.save()
        messages.success(request, "✅ User details updated successfully!")
        return redirect('admin_panel:manage_users')

    return render(request, 'admin_panel/edit_user.html', {'user': user})