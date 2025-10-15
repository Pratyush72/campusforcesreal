
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, OTPForm, NoteUploadForm
from .models import CustomUser, Note, CoinTransaction, MembershipTransaction, LiveWorkSubmission
import random
from django.contrib import messages  # For flash messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
import razorpay
from django.conf import settings
from .models import MembershipTransaction, CoinTransaction, UserProfile


# Store OTPs temporarily
otp_storage = {}


# ---------------------- Signup View ---------------------- #
# accounts/views.py
# Signup + Send OTP
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'User already exists!')
            return redirect('signup')

        otp = str(random.randint(100000, 999999))
        otp_storage[email] = {
            'otp': otp
        }
        # ✅ Send OTP to email
        send_mail(
            subject='CampusForces Signup OTP',
            message=f"""Hello {username},

        Thank you for signing up at CampusForce!

        Your One-Time Password (OTP) for completing your registration is: {otp}

        Please enter this OTP on the signup page to verify your email address.

        If you did not initiate this signup, please ignore this email.

        Best regards,
        CampusForces Team
        """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        # Store username and password in session for OTP verification
        request.session['email'] = email
        request.session['username'] = username
        request.session['password'] = password
        return redirect('otp_verify')

    return render(request, 'accounts/signup.html')

# OTP Verify
def otp_verify_view(request):
    email = request.session.get('email')
    username = request.session.get('username')
    password = request.session.get('password')
    if not email or email not in otp_storage or not username or not password:
        messages.error(request, 'Session expired or invalid email.')
        return redirect('signup')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        saved_otp = otp_storage[email]['otp']

        if entered_otp == saved_otp:
            # Create user and assign 50 coins
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Ensure you are using the correct user model with 'coins' field
            custom_user = CustomUser.objects.get(pk=user.pk)
            custom_user.coins = 50  # Assign coins to the custom user
            custom_user.save()
            # Clean up session and otp_storage
            del otp_storage[email]
            request.session.pop('username', None)
            request.session.pop('password', None)
            request.session.pop('email', None)
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP.')
            return redirect('otp_verify')
  
    return render(request, 'accounts/otp_verify.html')

# ---------------------- Login View ---------------------- #
def login_view(request): 
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Check if user exists with this email
        User = get_user_model()
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist. Please signup.')
            return render(request, 'accounts/login.html')

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'accounts/login.html')

# ---------------------- Login profile ---------------------- #
# ---------------------- Login profile ---------------------- #
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

@login_required
def profile_view(request):
    user = CustomUser.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        # Update username
        user.username = request.POST.get('username', user.username)
        # Update mobile number
        user.mobile_number = request.POST.get('mobile_number', user.mobile_number)
        # Update skills
        user.skills = request.POST.get('skills', user.skills)
        # Update profile picture if uploaded
        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']

        user.save()
        messages.success(request, "Profile updated successfully!")

    return render(request, 'profile.html', {'user': user})


# ---------------------- Profile Edit View ---------------------- #

# ---------------------- Logout View ---------------------- #
def logout_view(request):
    logout(request)
    return redirect('dashboard')

# ---------------------- Home View ---------------------- #
def home(request):
    return render(request, 'dashboard.html')

# ---------------------- Dashboard View ---------------------- #
def dashboard_view(request):
    return render(request, 'dashboard.html')
 
#------------------------- Reset Password View -------------------------#
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .forms import EmailForm, OTPForm, NewPasswordForm

User = get_user_model()

def reset_password_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                request.session['reset_email'] = email
                request.session['reset_otp'] = otp

                # ✅ Send OTP on email
                send_mail(
                    subject='CampusForces - Password Reset OTP',
                    message=f"""Hello,

                    We received a request to reset your CampusForces account password. 
                    Your One-Time Password (OTP) is: {otp}

                    Please use this OTP to reset your password. 
                    This OTP is valid for 5 minutes.

                    If you did not request a password reset, please ignore this message.

                    Thank you,
                    CampusForces Team
                    """,
                    from_email='your_email@gmail.com',
                    recipient_list=[email],
                    fail_silently=False,
                )
                return redirect('verify_otp')
            except User.DoesNotExist:
                messages.error(request, "User with this email does not exist.")
    else:
        form = EmailForm()
    return render(request, 'accounts/reset_password.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            real_otp = request.session.get('reset_otp')
            if entered_otp == real_otp:
                return redirect('new_password')
            else:
                messages.error(request, "Invalid OTP.")
    else:
        form = OTPForm()
    return render(request, 'accounts/verify_otp.html', {'form': form})

def new_password(request):
    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            email = request.session.get('reset_email') 
            new_password = form.cleaned_data['new_password']
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                # Clean session
                request.session.pop('reset_email', None)
                request.session.pop('reset_otp', None)
                messages.success(request, "Password reset successfully!")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "Something went wrong.")
    else:
        form = NewPasswordForm()
    return render(request, 'accounts/new_password.html', {'form': form})



# -------------------- News-Subscribe ------------

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from .models import Subscriber  # <-- make sure ye model hai

def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not email:
            messages.error(request, "Please enter a valid email!")
            return redirect(request.META.get('HTTP_REFERER'))

        # Save subscriber email to database
        Subscriber.objects.get_or_create(email=email)

        # Send welcome email
        subject = "Welcome to CAMPUSFORCES Community!"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]

        html_content = """
        <html>
        <body style="font-family: Arial, sans-serif; line-height:1.6; color:#333; text-align:center;">
            <h1 style="color:#4f46e5; font-size:30px; margin-bottom:20px; text-align:center;">CAMPUSFORCES</h1>
            <p style="font-size:18px;">Dear Student,</p>
            <p style="font-size:17px;">Welcome to the <strong>CAMPUSFORCES</strong> community! 🎉</p>
            <p style="font-size:16px;">By subscribing, you will receive:</p>
            <ul style="list-style:none; padding:0; text-align:left; display:inline-block;">
                <li>✅ Updates about live projects and coding challenges.</li>
                <li>🎓 Free resources to build your skills.</li>
                <li>💼 Notifications about internships and career opportunities.</li>
                <li>📘 Tips, tutorials, and guidance from industry experts.</li>
                <li>🏅 Special CampusCoins rewards for participation.</li>
            </ul>
            <p style="margin-top:20px;">We are committed to helping you grow and succeed in your career journey.</p>
            <p style="margin-top:30px; font-weight:bold;">Happy Learning,<br>The CAMPUSFORCES Team</p>
        </body>
        </html>
        """

        msg = EmailMultiAlternatives(subject, "", from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        messages.success(request, "Subscribed successfully! Check your inbox for a welcome email.")
        return redirect(request.META.get('HTTP_REFERER'))


#  -------------------------featured view ------------------------- #
def featured(request):
    return render (request ,'featured.html')


# ---------------------- Help View ---------------------- #
def help_view(request):
    return render(request, 'help.html')


# ---------------------- Project View ---------------------- #

from django.shortcuts import render
from .models import Project
@login_required
def projects_view(request):
    projects = Project.objects.all()  # fetch all projects from DB
    return render(request, 'projects.html', {'projects': projects})

# ---------------------- Community View ---------------------- #
def community_view(request):
    return render(request, 'community.html')


# ---------------------- Privacy Policy   ---------------------- #

def privacy_view(request):
    return render (request, 'privacy.html')

# ---------------------- Contact Us Page ---------------------- #
def contact_view(request):
    return render(request, 'contact.html')

# ---------------------- Form Submit ---------------------- #
def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Full message to send to admin
        full_message = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage:\n{message}"

        try:
            send_mail(
                subject=f"[Contact Form] {subject}",
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],  # Admin email
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Error sending message: {str(e)}")

    return redirect('contact')
# ---------------------- Term_condition  ---------------------- #

def term_condition_view(request):
    return render (request, 'term_condition.html')

# ---------------------- meet View ---------------------- #
def meet_view(request):
    return render(request, 'meet.html')


# ---------------------- Add Coins View ---------------------- #

# ---------------------- Coin Transaction View ---------------------- #
# accounts/views.py

from django.shortcuts import render
from .models import CoinTransaction  # ensure yeh model hai tumhare paas

# def coin_transaction_view(request):
#     transactions = CoinTransaction.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'coin_transaction.html', {'transactions': transactions})

# ---------------------- Upload Notes View ---------------------- #

@login_required
def upload_notes_view(request):
    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            # Determine coin reward
            if 'machine learning' in note.title.lower():
                reward_coins = 20
            else:
                reward_coins = 10

            # Update user coins
            request.user.coins += reward_coins
            request.user.save()

            # Log coin transaction
            CoinTransaction.objects.create(
                user=request.user,
                coins=reward_coins,
                reason="Note Upload"
            )

            messages.success(request, 'Note uploaded successfully!')
            return redirect('upload_notes')
    else:
        form = NoteUploadForm()

    # Fetch notes of current user
    user_notes = Note.objects.filter(user=request.user).order_by('-uploaded_at')

    return render(request, 'upload_notes.html', {
        'form': form,
        'notes': user_notes
    })

# ---------------------- Notes List View ---------------------- #
def notes_view(request):
    notes = Note.objects.all().order_by('-uploaded_at')
    return render(request, 'notes.html', {'notes': notes})


# -------------------- Project Related ----------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import LiveWorkProject, LiveWorkSubmission
from datetime import datetime

# ----------- Helper Emails -----------
def send_submission_email(user_email, project_title):
    send_mail(
        subject=f'Live Work Submission Received: {project_title}',
        message=f'Hello,\n\nYour submission for "{project_title}" has been received and is pending review.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )

def send_status_email(user_email, project_title, status, reason=None):
    msg = f'Hello,\n\nYour submission for "{project_title}" has been {status}.'
    if reason:
        msg += f'\nReason: {reason}'
    send_mail(
        subject=f'Live Work Submission {status}: {project_title}',
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )

# ----------- Live Work / Project View -----------

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import LiveWorkProject, LiveWorkSubmission

@login_required
def live_work_view(request):
    # Fetch all projects
    live_work = LiveWorkProject.objects.all().order_by('-start_date')

    # Fetch user's submissions
    submissions_qs = LiveWorkSubmission.objects.filter(user=request.user)
    submissions_dict = {sub.project.id: sub for sub in submissions_qs} if submissions_qs.exists() else {}

    return render(request, 'live_work.html', {
        'live_work': live_work,
        'submissions': submissions_dict,
        'user_plan': request.user.current_plan  # free / project / premium
    })

# ----------- Start Project / Code Editor -----------

@login_required
def start_project_view(request, project_id):
    project = get_object_or_404(LiveWorkProject, id=project_id)

    # Only premium users can start project
    if request.user.current_plan != 'premium':
        return redirect('livework')  # redirect free users

    return render(request, 'code_editor.html', {'project': project})


# ----------- Submit Live Work -----------
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import LiveWorkProject, LiveWorkSubmission


from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt  # Django CSRF token is already sent, so optional
@login_required

@login_required
def submit_code(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        code = request.POST.get("code")
        language = request.POST.get("language")

        project = get_object_or_404(LiveWorkProject, id=project_id)

        # Create submission
        submission = LiveWorkSubmission.objects.create(
            project=project,
            user=request.user,
            code=code,
            language=language,
            status="Pending"
        )

        # Send email to user
        try:
            subject = f"Code Submission Received for {project.title}"
            message = f"Hello {request.user.username},\n\n" \
                      f"Your code for the project '{project.title}' has been submitted successfully.\n" \
                      f"Status: {submission.status}\n" \
                      f"Submitted on: {submission.applied_at.strftime('%d-%m-%Y %H:%M:%S')}\n\n" \
                      "You will be notified once it is reviewed by admin.\n\nCampusForces Team"
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False
            )
        except Exception as e:
            print("Email sending error:", e)

        # Return JSON for JS redirect
        return JsonResponse({"success": True, "message": "Code submitted successfully."})

    return JsonResponse({"success": False, "message": "Invalid request."})
@login_required
def my_submissions_view(request):
    # Fetch all submissions of this user
    submissions = LiveWorkSubmission.objects.filter(user=request.user).order_by('-applied_at')

    return render(request, 'my_submissions.html', {
        'submissions': submissions
    })

# ------Razorpay use------
import razorpay
from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MembershipTransaction, CustomUser
from django.views.decorators.csrf import csrf_exempt


# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))


# ------------------ Membership Page ------------------ #
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.utils.timezone import now
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def membership_view(request):
    user = request.user
    today = date.today()
    coin_value = request.user.coins / 10  # 10 coins = 1 INR


    # Check if membership expired
    if user.membership_end_date and user.membership_end_date <= today:
        user.current_plan = 'free'
        user.membership_start_date = None
        user.membership_end_date = None
        user.save()

    return render(request, 'membership.html', {'user': user,'coin_value': coin_value})

# # ------------------ Checkout ------------------ #
@login_required
def checkout(request, plan):
    plans = {'project': {'name': 'Project Pass', 'price': 199},
             'premium': {'name': 'Premium Pass', 'price': 499}}
    
    coin_value = request.user.coins / 10

    plan_info = plans.get(plan)
    if not plan_info:
        messages.error(request, 'Invalid plan selected.')
        return redirect('membership')

    return render(request, 'checkout.html', {
        'plan': plan,
        'plan_name': plan_info['name'],
        'plan_price': plan_info['price'],
        'user': request.user,
        'coin_value': request.user.coins // 10,
        'coin_value':coin_value
    })


# # ------------------ Process Payment ------------------ #
# @login_required
# def process_payment(request):
#     if request.method != 'POST':
#         return redirect('membership')

#     user = request.user
#     plan = request.POST.get('plan')
#     used_coins = int(request.POST.get('used_coins', 0))

#     plan_prices = {'project': 199, 'premium': 499}
#     plan_price = plan_prices.get(plan, 0)
#     discount = used_coins / 10
#     final_amount = plan_price - discount
#     if final_amount < 0:
#         final_amount = 0

#     today = date.today()
#     end_date = today + timedelta(days=30 if plan == 'project' else 60)

#     # Fully paid by coins
#     if final_amount == 0:
#         tx = MembershipTransaction.objects.create(
#             user=user,
#             plan=plan,
#             price=0,
#             used_coins=used_coins,
#             status='Approved',
#             start_date=today,
#             end_date=end_date
#         )
#         # Update user membership info
#         user.current_plan = plan
#         user.membership_start_date = today
#         user.membership_end_date = end_date
#         user.save()

#         messages.success(request, f'Membership activated using coins! Plan: {plan}')
#         return redirect('membership')


#     # ------------------ Razorpay Payment ------------------ #
#     payment_amount = int(final_amount * 100)  # in paise
#     payment_receipt = f'{user.username}_{plan}_{today}'

#     razorpay_order = razorpay_client.order.create(dict(
#         amount=payment_amount,
#         currency='INR',
#         receipt=payment_receipt,
#         payment_capture='1'
#     ))

#     # Save transaction in DB
#     MembershipTransaction.objects.create(
#         user=user,
#         plan=plan,
#         price=final_amount,
#         used_coins=used_coins,
#         razorpay_order_id=razorpay_order['id'],
#         status='Pending',
#         start_date=today,
#         end_date=end_date
#     )

#     return render(request, 'razorpay_checkout.html', {
#         'order_id': razorpay_order['id'],
#         'final_amount': final_amount,
#         'razorpay_key_id': settings.RAZORPAY_KEY_ID,
#         'user': user,
#         'plan': plan,
#         'used_coins': used_coins
#     })


# ------------------ Process Payment ------------------ #
@login_required
def process_payment(request):
    if request.method != 'POST':
        return redirect('membership')

    user = request.user
    plan = request.POST.get('plan')
    used_coins = int(request.POST.get('used_coins', 0))

    plan_prices = {'project': 199, 'premium': 499}
    plan_price = plan_prices.get(plan, 0)

    discount = used_coins / 10
    final_amount = plan_price - discount
    if final_amount < 0:
        final_amount = 0

    today = date.today()
    end_date = today + timedelta(days=30 if plan == 'project' else 60)

    # ------------------ Fully paid by coins ------------------
    if final_amount == 0:
        if used_coins > user.coins:
            messages.error(request, "You don't have enough coins!")
            return redirect('membership')

        # Deduct coins and update user
        user.coins -= used_coins
        user.current_plan = plan
        user.membership_start_date = today
        user.membership_end_date = end_date
        user.save()

        # Save transaction
        MembershipTransaction.objects.create(
            user=user,
            plan=plan,
            price=0,
            used_coins=used_coins,
            status='Coins',  # Coins-only transaction
            start_date=today,
            end_date=end_date
        )

        messages.success(request, f'Membership activated using coins! Plan: {plan}')
        return render(request, 'success.html')

    # ------------------ Razorpay Payment ------------------
    payment_amount = int(final_amount * 100)
    payment_receipt = f'{user.username}_{plan}_{today}'

    try:
        razorpay_order = razorpay_client.order.create(dict(
            amount=payment_amount,
            currency='INR',
            receipt=payment_receipt,
            payment_capture='1'
        ))
    except Exception as e:
        print("⚠️ Payment Timeout or Error:", e)
        return render(request, 'timeout.html')

    MembershipTransaction.objects.create(
        user=user,
        plan=plan,
        price=final_amount,
        used_coins=used_coins,
        razorpay_order_id=razorpay_order['id'],
        status='Pending',
        start_date=today,
        end_date=end_date
    )

    return render(request, 'razorpay_checkout.html', {
        'order_id': razorpay_order['id'],
        'final_amount': final_amount,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'user': user,
        'plan': plan,
        'used_coins': used_coins
    })



# ------------------ Payment Timeout ------------------ #
def payment_timeout(request):
    return render(request, 'timeout.html')


# ------------------ Payment Success ------------------ #
from django.utils import timezone
from datetime import timedelta
from .models import MembershipTransaction, CustomUser
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

@login_required
@csrf_exempt
def payment_success(request):
    if request.method != "POST":
        return redirect('membership')

    payment_id = request.POST.get('razorpay_payment_id')
    order_id = request.POST.get('razorpay_order_id')

    tx = MembershipTransaction.objects.filter(razorpay_order_id=order_id).first()
    if tx:
        tx.payment_id = payment_id
        tx.status = 'Success'
        tx.start_date = timezone.now()

        # Set end_date based on plan
        if tx.plan == 'project':
            tx.end_date = timezone.now() + timedelta(days=30)
        elif tx.plan == 'premium':
            tx.end_date = timezone.now() + timedelta(days=60)
        tx.save()

        # Update user membership and coins
        user = tx.user
        user.current_plan = tx.plan
        user.membership_start_date = tx.start_date
        user.membership_end_date = tx.end_date

        # Deduct coins if any
        if tx.used_coins:
            user.coins -= tx.used_coins
            if user.coins < 0:
                user.coins = 0

        user.save()

        messages.success(request, f"{tx.plan.title()} Membership activated successfully!")

        return render(request, 'success.html')



# ------------------ Payment Failed ------------------ #
@login_required
@csrf_exempt
def payment_failed(request):
    if request.method == "POST":
        order_id = request.POST.get('razorpay_order_id')
        tx = MembershipTransaction.objects.filter(razorpay_order_id=order_id).first()
        if tx:
            tx.status = 'Rejected'
            tx.save()
        messages.error(request, 'Payment failed or cancelled.')
        return render(request, 'failed.html')
    else:
        # Agar GET request ho to bhi show page
        return render(request, 'failed.html')
    
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#  ------------------
#  view membership
# ----------------

from django.utils import timezone
from .models import MembershipTransaction

@login_required
def subscription_view(request):
    # coin info
    coin_value = request.user.coins / 10  # 10 coins = 1 INR

    # get latest active membership
    membership = MembershipTransaction.objects.filter(
        user=request.user,
        status='Approved',
        end_date__gte=timezone.now().date()
    ).order_by('-end_date').first()

    return render(request, 'accounts/subscription.html', {
        'coin_value': coin_value,
        'membership': membership,
    })

# -------------------- my_transactions_view ------------
# -------------------------------------------------------
@login_required
def my_transactions_view(request):
    transactions = MembershipTransaction.objects.filter(
        user=request.user,
        status__in=['Success', 'Faild', 'Coins']
    ).order_by('-created_at')

    # Total calculations
    total_paid = sum(tx.price for tx in transactions)
    total_coins_used = sum(tx.used_coins for tx in transactions)

    return render(request, 'my_transactions.html', {
        'transactions': transactions,
        'total_paid': total_paid,
        'total_coins_used': total_coins_used
    })


