# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import EmailMessage
# from .models import JobApplication

# @receiver(post_save, sender=JobApplication)
# def send_status_update_email(sender, instance, created, **kwargs):
#     if created:
#         return  # Apply karte waqt mail views.py se gaya tha

#     user = instance.user
#     status = instance.status  # e.g. "Approved", "Rejected", "Shortlisted"
#     job = instance.job

#     subject = f"Update on Your Application for {job.title}"
#     if status == "Approved":
#         body = f"Dear {user.get_full_name() or user.email},\n\nCongratulations! Your application for {job.title} at {job.company} has been approved."
#     elif status == "Rejected":
#         body = f"Dear {user.get_full_name() or user.email},\n\nWe regret to inform you that your application for {job.title} at {job.company} has been rejected."
#     elif status == "Shortlisted":
#         body = f"Dear {user.get_full_name() or user.email},\n\nGood news! Your application for {job.title} at {job.company} has been shortlisted. Our team will contact you for the next steps."
#     else:
#         body = f"Dear {user.get_full_name() or user.email},\n\nYour application status for {job.title} has been updated: {status}."

#     email = EmailMessage(subject, body, to=[user.email])
#     if instance.resume:
#         email.attach(instance.resume.name, instance.resume.read(), 'application/pdf')

#     email.send()
