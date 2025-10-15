from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# ------------------------------
# 1. Custom User Model
# ------------------------------
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    coins = models.IntegerField(default=0)
    mobile_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    current_plan = models.CharField(max_length=50, default='free')  # free / project / premium
    membership_start_date = models.DateField(blank=True, null=True)
    membership_end_date = models.DateField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True, help_text="Enter your skills separated by commas, e.g., Python, Django, SQL")


    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_active_membership(self):
        if self.membership_end_date and self.membership_end_date >= timezone.now().date():
            return True
        return False

    def __str__(self):
        return self.email



# ------------------------------
# 2. OTP Model (For Signup Verification)
# ------------------------------
class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - OTP: {self.code}"


# ------------------------------
# 3. Notes Model
# ------------------------------
class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ------------------------------
# 4. Project Submission Model
from django.db import models
from django.conf import settings

# ---------------- Live Work Project ----------------
class LiveWorkProject(models.Model):
    PLAN_CHOICES = [
        ("free", "Free"),
        ("project", "Project"),
        ("premium", "Premium")
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    plan_required = models.CharField(max_length=50, choices=PLAN_CHOICES, default='premium')
    coins_reward = models.IntegerField(default=50)

    def __str__(self):
        return self.title

# ---------------- Live Work Submission ----------------
class LiveWorkSubmission(models.Model):
    project = models.ForeignKey(LiveWorkProject, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='Pending')  # Pending / Approved / Rejected
    rejection_reason = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.project.title} ({self.status})"

# ----
# ------------------------------
# 5. Coin Transaction Model
# ------------------------------
class CoinTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coins = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.coins} coins for {self.reason}"


# ------------------------------
# 6. Membership Transaction Model
# ------------------------------
class MembershipTransaction(models.Model):
    PLAN_CHOICES = [
        ('project', 'Project Pass'),
        ('premium', 'Premium Pass'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    price = models.IntegerField()
    used_coins = models.IntegerField(default=0)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')  # Pending / Success / Failed
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan} - {self.status}"
    
    def activate_membership(self):
        """Call this after payment is successful to activate membership."""
        self.status = 'Success'
        self.start_date = timezone.now()

        # Set end date based on plan
        if self.plan == 'project':
            self.end_date = timezone.now() + timedelta(days=30)
        elif self.plan == 'premium':
            self.end_date = timezone.now() + timedelta(days=90)
        self.save()

        # Update user membership & coins
        user = self.user
        user.membership_status = self.plan.capitalize()
        user.coins -= self.used_coins
        if user.coins < 0:
            user.coins = 0
        user.save()


# ------------------------------
# 7. User Profile Model
# ------------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return str(self.user)


# ------------------------------
# 8. Live Projects Model
# ------------------------------
class LiveProject(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, default='Active')  # e.g., Active, Completed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project_title} - {self.status}"


# ------------------------------
# 9. Clone Projects Model
# ------------------------------

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.CharField(max_length=255)  # Image path or URL
    download_url = models.CharField(max_length=255)  # File path or URL
    is_free = models.BooleanField(default=False)
    plan_required = models.CharField(
        max_length=20,
        choices=[('project', 'Project Pass'), ('premium', 'Premium Pass')],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


# ------------------------------
# 10. Subscribe_user
# ------------------------------

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email