from django.db import models
from accounts.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import MySQLdb

class Career(models.Model):
    JOB_TYPE_CHOICES = [
        ('full-time','Full Time'),
        ('part-time','Part Time'),
        ('internship','Internship'),
    ]
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    plan_required = models.CharField(max_length=20, choices=[('project','Project Pass'),('premium','Premium Pass')], blank=True, null=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full-time')

    def __str__(self):
        return f"{self.title} at {self.company}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Applied','Applied'),
        ('Shortlisted','Shortlisted'),
        ('Rejected','Rejected'),
        ('Hired','Hired'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Career, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    rejection_reason = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    assessment_link = models.URLField(blank=True, null=True)
    mail_sent = models.BooleanField(default=False)  # ✅ Track if mail sent


    def __str__(self):
        return f"{self.user.email} - {self.job.title}"

# ---------------- SIGNAL ----------------
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import JobApplication

@receiver(post_save, sender=JobApplication)
def send_status_email(sender, instance, created, **kwargs):
    user_email = instance.user.email
    job_title = instance.job.title
    company = instance.job.company
    username = instance.user.username  # ❌ Remove ()

    if created:
        # Student applied
        subject = f"Application Received: {job_title} at {company}"
        message = f"""
Dear {username or user_email},

Thank you for submitting your application for the position "{job_title}" at {company}.
We have received your application along with your resume and cover letter. Our recruitment team will review it and update you soon regarding the next steps.

Best regards,
{company} HR Team
"""
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])

    else:
        # Status updated by admin
        status = instance.status
        if status == 'Rejected':
            subject = f"Application Update: {job_title} at {company}"
            message = f"""
Dear {username or user_email},

Thank you for applying for "{job_title}" at {company}.
After careful consideration, we regret to inform you that your application has been rejected.

Reason: {instance.rejection_reason or 'Not specified'}

We encourage you to apply for future opportunities.

Best regards,
{company} HR Team
"""
        elif status == 'Shortlisted':
            subject = f"Congratulations! Shortlisted for {job_title} at {company}"
            message = f"""
Dear {username or user_email},

We are pleased to inform you that your application for "{job_title}" at {company} has been shortlisted.
Please complete the assessment at the following link: {instance.assessment_link}

Best regards,
{company} HR Team
"""
        elif status in ['Hired', 'Approved']:
            subject = f"Application Approved: {job_title} at {company}"
            message = f"""
Dear {username or user_email},

Congratulations! Your application for "{job_title}" at {company} has been approved.
Our HR team will contact you for next steps.

Best regards,
{company} HR Team
"""
        else:
            subject = f"Application Update: {job_title} at {company}"
            message = f"Dear {username or user_email},\n\nYour application status is now '{status}'.\n\nBest regards,\n{company} HR Team"

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
