
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, OTPForm, NoteUploadForm
from .models import CustomUser, Note, CoinTransaction, MembershipTransaction, ProjectSubmission
import random
from django.contrib import messages  # For flash messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random

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
@login_required
def profile_view(request):
    from .models import CustomUser  # Ensure import at the top if not already
    user = CustomUser.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        # Make sure your HTML form uses 'first_name', 'mobile_number', and 'profile_picture' as field names
        user.username = request.POST.get('username', user.username)
        user.mobile_number = request.POST.get('mobile_number', user.mobile_number)
        # Remove membership_status update if not needed, or ensure the field exists
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





































































































#  -------------------------featured view ------------------------- #
def featured(request):
    return render (request ,'featured.html')


# ---------------------- Help View ---------------------- #
def help_view(request):
    return render(request, 'help.html')

# ---------------------- Community View ---------------------- #
def community_view(request):
    return render(request, 'community.html')

# ---------------------- meet View ---------------------- #
def meet_view(request):
    return render(request, 'meet.html')


# ---------------------- Add Coins View ---------------------- #
@login_required
def add_coins(request):
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        reason = request.POST.get('reason', 'Manual Add')
        
        if amount <= 0:
            messages.error(request, "Amount must be positive.")
            return redirect('add_coins')

        request.user.coins += amount
        request.user.save()

        CoinTransaction.objects.create(
            user=request.user,
            amount=amount,
            reason=reason
        )
        messages.success(request, f"{amount} coins added successfully!")
        return redirect('dashboard')

    return render(request, 'add_coins.html')


# ---------------------- Coin Transaction View ---------------------- #
# accounts/views.py

from django.shortcuts import render
from .models import CoinTransaction  # ensure yeh model hai tumhare paas

def coin_transaction_view(request):
    transactions = CoinTransaction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'coin_transaction.html', {'transactions': transactions})


# ---------------------- Live Projects View ---------------------- #
@login_required
def live_projects_view(request):
    projects = ProjectSubmission.objects.filter(user=request.user)
    return render(request, 'live_projects.html', {'projects': projects})

# ---------------------- Resume Builder View ---------------------- #
@login_required
def resume_builder_view(request):
    if request.method == 'POST':
        # Handle resume building logic here
        messages.success(request, "Resume built successfully!")
        return redirect('dashboard')
    return render(request, 'resume_builder.html')


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


from django.shortcuts import render, redirect
from .models import LiveProject
from .forms import LiveProjectForm
from django.contrib.auth.decorators import login_required

@login_required
def livework_view(request):
    user = request.user

    if request.method == 'POST':
        form = LiveProjectForm(request.POST)
        if form.is_valid():
            live_project = form.save(commit=False)
            live_project.user = user
            live_project.status = 'Pending'
            live_project.save()
            return redirect('livework')
    else:
        form = LiveProjectForm()

    # Fetch all live projects for display
    live_projects = LiveProject.objects.filter(status='Active').order_by('-created_at')

    context = {
        'form': form,
        'live_projects': live_projects
    }
    return render(request, 'livework.html', context)


# ---------------------- NOtes view ---------------------- #

# @login_required
# def upload_notes_view(request):
#     if request.method == 'POST':
#         form = NoteUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             note = form.save(commit=False)
#             note.user = request.user
#             note.save()
#             messages.success(request, 'Note uploaded successfully.')
#             return redirect('upload_notes')  # ya jahan redirect karna ho
#     else:
#         form = NoteUploadForm()
#     return render(request, 'upload_notes.html', {'form': form})


# ---------------------- Membership View ---------------------- #
# views.py (Full working Razorpay + coins backend logic)
import razorpay
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from .models import MembershipTransaction, CoinTransaction, UserProfile

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))


@login_required
def membership_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)  # ✅ FIXED: Always get/create safely

    if request.method == "POST":
        plan = request.POST.get("plan")
        use_coins = request.POST.get("use_coins") == "on"

        # Set plan amount
        amount_rupees = 199 if plan == "project" else 499
        coins_used = 0

        if use_coins:
            coins_used = min(profile.coins, amount_rupees * 10)  # Max coins allowed = price * 10
            discount_rupees = coins_used // 10
            amount_rupees -= discount_rupees

        amount_paise = amount_rupees * 100

        payment = razorpay_client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": "1"
        })

        MembershipTransaction.objects.create(
            user=user,
            plan=plan,
            razorpay_order_id=payment['id'],
            amount=amount_rupees,
            coins_used=coins_used,
            status="INITIATED"
        )

        context = {
            "order_id": payment['id'],
            "amount_rupees": amount_rupees,
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "user": user,
            "callback_url": "/payment-handler/"
        }
        return render(request, "payment_checkout.html", context)

    # 🟢 Render membership selection form (GET)
    coin_value = user.coins // 10  # 💰 10 coins = ₹1

    context = {
        "user_coins": user.coins,
        "coin_value": coin_value
    }
    return render(request, "membership.html", context)

@csrf_exempt
def payment_handler(request):
    if request.method == "POST":
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')

            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': signature
            }
            razorpay_client.utility.verify_payment_signature(params_dict)

            # Update transaction status
            transaction = MembershipTransaction.objects.get(razorpay_order_id=razorpay_order_id)
            transaction.status = "SUCCESS"
            transaction.razorpay_payment_id = razorpay_payment_id
            transaction.paid_at = timezone.now()
            transaction.save()

            # Update user profile
            profile = UserProfile.objects.get(user=transaction.user)
            if transaction.coins_used:
                profile.coins -= transaction.coins_used
                CoinTransaction.objects.create(
                    user=profile.user,
                    change=-transaction.coins_used,
                    reason="Used for membership purchase"
                )
            profile.membership_type = transaction.plan
            profile.membership_expiry = timezone.now() + timezone.timedelta(days=30)
            profile.save()

            messages.success(request, "Payment successful! Membership activated.")
            return redirect("membership")

        except Exception as e:
            print("Payment failed:", str(e))
            messages.error(request, "Payment failed or verification error. Try again.")
            return redirect("membership")

    return  redirect("membership")

# accounts/views.py

from django.shortcuts import render

def payment_success(request):
    return render(request, 'success.html')

def payment_failed(request):
    return render(request, 'failed.html')




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required




# ---------------------- Submit Project View ---------------------- #
@login_required
def submit_project(request):
    if request.method == 'POST':
        title = request.POST['title']
        github_link = request.POST['github_link']
        submission = ProjectSubmission(
            user=request.user,
            project_title=title,
            github_link=github_link
        )
        submission.save()
        messages.success(request, 'Project submitted successfully!')
        return redirect('dashboard')
    return render(request, 'accounts/submit_project.html')
