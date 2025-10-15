from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .models import Career, JobApplication

# ------------------------------
# 1. List + Search + Filter Jobs
# ------------------------------
def career_list(request):
    qs = Career.objects.all().order_by("-posted_at")
    q = request.GET.get("q")
    plan_required = request.GET.get("plan_required")  # optional filter
    job_type = request.GET.get("job_type")  # optional filter

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(company__icontains=q) |
            Q(location__icontains=q)
        )

    if plan_required and plan_required != "all":
        qs = qs.filter(plan_required=plan_required)

    if job_type and job_type != "all":
        qs = qs.filter(job_type=job_type)

    return render(request, "career_list.html", {"careers": qs})


# ------------------------------
# 2. Career Detail + Apply
# ------------------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Career, JobApplication

@login_required
def career_detail(request, pk):
    career = get_object_or_404(Career, pk=pk)
    existing_application = JobApplication.objects.filter(job=career, user=request.user).first()

    if request.method == "POST":
        if existing_application:
            messages.warning(request, "You have already applied for this job.")
        else:
            app = JobApplication.objects.create(
                job=career,
                user=request.user,
                resume=request.FILES.get("resume"),
                cover_letter=request.POST.get("cover_letter"),
            )
            messages.success(request, "Application submitted successfully! You will receive a confirmation email shortly.")
            return redirect("careers:my_applications")

    applications = JobApplication.objects.filter(job=career)

    return render(request, "career_detail.html", {
        "career": career,
        "existing_application": existing_application,
        "applications": applications
    })



# ------------------------------
# 3. Show My Applications
# ------------------------------
@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(user=request.user).select_related("job")
    return render(request, "my_applications.html", {"applications": applications})


from django.http import FileResponse, Http404

@login_required
def view_resume(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if not application.resume:
        raise Http404("Resume not found.")

    return FileResponse(application.resume.open('rb'), content_type='application/pdf', filename=f"{application.user.email}_resume.pdf")
