# careers/apps.py
from django.apps import AppConfig
import threading, time
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class CareersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'careers'

    started = False  # ✅ flag to prevent multiple threads

    def ready(self):
        if CareersConfig.started:  # agar already start ho chuka hai to dobara mat chalao
            return
        CareersConfig.started = True

        from careers.models import JobApplication  

        def background_mailer():
            while True:
                try:
                    pending = JobApplication.objects.filter(mail_sent=False)
                    for app in pending:
                        subject, text_message, html_message = "", "", ""

                        if app.status == "Rejected":
                            subject = f"Update on Your Application for {app.job.title}"
                            text_message = f"""
Dear {app.user.username},

Thank you for applying for the position of {app.job.title} at {app.job.company}.  

Unfortunately, your application was not successful at this stage.  

Reason: {app.rejection_reason if app.rejection_reason else "Not specified"}  

We appreciate your interest and encourage you to apply for future opportunities.

Best Regards,  
HR Team – {app.job.company}
                            """
                            html_message = f"""
<p>Dear {app.user.username},</p>
<p>Thank you for applying for the position of <b>{app.job.title}</b> at <b>{app.job.company}</b>.</p>
<p>Unfortunately, your application was <b>not successful</b> at this stage.</p>
<p><b>Reason Provided:</b> {app.rejection_reason if app.rejection_reason else "Not specified"}</p>
<p>We truly appreciate your interest and encourage you to apply again for future opportunities with us.</p>
<br>
<p>Best Regards,<br><b>HR Team – {app.job.company}</b></p>
                            """

                        elif app.status == "Shortlisted":
                            subject = f"Congratulations! You’ve Been Shortlisted for {app.job.title}"
                            text_message = f"""
Dear {app.user.first_name},

You have been shortlisted for {app.job.title} at {app.job.company}.

Complete your assessment here: {app.assessment_link}

Best Regards,
HR Team – {app.job.company}
                            """
                            html_message = f"""
<p>Dear {app.user.username},</p>
<p>We are excited to inform you that you have been <b>shortlisted</b> for the position of <b>{app.job.title}</b> at <b>{app.job.company}</b>. 🎉</p>
<p>Please complete your assessment here:<br>
<a href="{app.assessment_link}">{app.assessment_link}</a></p>
<p>We wish you the best of luck for the next stage.</p>
<br>
<p>Best Regards,<br><b>HR Team – {app.job.company}</b></p>
                            """

                        elif app.status == "Hired":
                            subject = f"🎉 Welcome to {app.job.company} – {app.job.title}"
                            text_message = f"""
Dear {app.user.username},

Congratulations! You are hired for {app.job.title} at {app.job.company}!

Our HR team will contact you shortly with onboarding details.

Best Regards,
HR Team – {app.job.company}
                            """
                            html_message = f"""
<p>Dear {app.user.username},</p>
<p><b>Congratulations!</b> 🎉 You have been selected for the role of <b>{app.job.title}</b> at <b>{app.job.company}</b>.</p>
<p>Our HR team will contact you shortly with onboarding details and formalities.</p>
<p>Welcome aboard, we look forward to working with you 🚀</p>
<br>
<p>Best Regards,<br><b>HR Team – {app.job.company}</b></p>
                            """

                        if subject:
                            email = EmailMultiAlternatives(
                                subject,
                                text_message,
                                settings.DEFAULT_FROM_EMAIL,
                                [app.user.email]
                            )
                            email.attach_alternative(html_message, "text/html")
                            email.send()

                            app.mail_sent = True
                            app.save()

                except Exception as e:
                    print("Mailer error:", e)

                time.sleep(5)  # check every 5 sec

        threading.Thread(target=background_mailer, daemon=True).start()
