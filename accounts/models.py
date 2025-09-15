from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User
from django.conf import settings

from django.db import models
from django.conf import settings

# ------------------------------
# 1. Custom User Model
# ------------------------------
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    coins = models.IntegerField(default=0)
    mobile_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    membership_status = models.CharField(max_length=50, default='Free')  # Optional



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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
# ------------------------------
class ProjectSubmission(models.Model):  
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=255)
    github_link = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.project_title} - {self.status}"

# ------------------------------
# 5. Coin Transaction Model
# ------------------------------
class CoinTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount} coins"

# ------------------------------
# 6. Membership Model
# ------------------------------
from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

class CoinWallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user}'s Wallet: {self.coins} Coins"

# ------------------------------
# 5. Coin Transaction Model
# ------------------------------
class CoinTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coins = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} coins for {self.reason}"

class MembershipTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    used_coins = models.IntegerField(default=0)
    razorpay_order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Created')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def activate_membership(self):
        self.status = 'Success'
        if self.plan == 'project':
            self.end_date = timezone.now() + timedelta(days=30)
        elif self.plan == 'premium':
            self.end_date = timezone.now() + timedelta(days=90)
        self.save()

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return str(self.user)


# ------------------------------
# 6. LIve Projects Model
# ------------------------------
class LiveProject(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, default='Active')  # e.g., Active, Completed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project_title} - {self.status}"