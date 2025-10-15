# careers/auto_mailer.py
import os
import django
import sys
import time
from django.core.mail import EmailMessage
import pymysql
pymysql.install_as_MySQLdb()

# ----------------------------
# Setup Django Environment
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('/Users/pratyush/Desktop/campusforce')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "campusforce.settings")
django.setup()

from careers.models import JobApplication

# ----------------------------
# Function to send professional email
# ----------------------------
def send_status_update(app):
    user = app.user
    job = app.job
    status = app.status
    username = user.get_username() or user.email

    # Subject & message based on status
    if status == "Applied":
        subject = f"Application Received: {job.title} at {job.company}"
        message = f"""
Dear {username},

Thank you for submitting your application for the position "{job.title}" at {job.company}.

We have successfully received your application along with the attached resume and cover letter. Our recruitment team will carefully review your submission and evaluate your qualifications.

You will receive an update regarding the status of your application in due course.

We appreciate your interest in joining {job.company} and wish you the best of luck.

Best regards,
{job.company} HR Team
"""
    elif status == "Rejected":
        subject = f"Application Update: {job.title} at {job.company}"
        message = f"""
Dear {username},

We appreciate the time and effort you invested in applying for the position "{job.title}" at {job.company}.

After careful consideration, we regret to inform you that your application has not been selected for further processing. 

Reason: {app.rejection_reason or 'Not specified'}

We encourage you to apply for future openings that match your profile and experience.

Thank you for your interest in {job.company}.

Best regards,
{job.company} HR Team
"""
    elif status == "Shortlisted":
        subject = f"Congratulations! You are Shortlisted for {job.title} at {job.company}"
        message = f"""
Dear {username},

We are pleased to inform you that your application for the position "{job.title}" at {job.company} has been shortlisted.

Next Steps:
Please complete the assessment using the following link: {app.assessment_link}

We wish you the best for the assessment and look forward to your participation.

Best regards,
{job.company} HR Team
"""
    elif status in ["Hired", "Approved"]:
        subject = f"Application Status: {job.title} at {job.company}"
        message = f"""
Dear {username},

Congratulations! Your application for the position "{job.title}" at {job.company} has been approved.

Our HR team will reach out to you with further instructions regarding joining formalities.

We are excited to have you on board and welcome you to {job.company}.

Best regards,
{job.company} HR Team
"""
    else:
        subject = f"Application Update: {job.title} at {job.company}"
        message = f"Dear {username},\n\nYour application status has been updated to '{status}'.\n\nBest regards,\n{job.company} HR Team"

    # Send Email with resume attached if available
    email = EmailMessage(subject, message, to=[user.email])
    if app.resume:
        email.attach(app.resume.name, app.resume.read(), 'application/pdf')
    email.send()

    # ✅ Track last status mailed
    app.mail_sent_status = status
    app.save()
    print(f"📩 Mail sent to {user.email} for status {status}")


# ----------------------------
# Auto Mailer Loop
# ----------------------------
def run_auto_mailer():
    print("🚀 Auto Mailer started (checking every 5 seconds)...")
    while True:
        try:
            # Sirf un applications fetch karo jinka status abhi mail nahi gaya
            pending_apps = JobApplication.objects.exclude(status=django.db.models.F('mail_sent_status'))
            for app in pending_apps:
                send_status_update(app)
            time.sleep(5)
        except Exception as e:
            print("❌ Error in auto_mailer:", e)
            time.sleep(5)


# ----------------------------
# Run the auto mailer
# ----------------------------
if __name__ == "__main__":
    run_auto_mailer()
