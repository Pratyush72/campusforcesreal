from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Note, CoinTransaction, MembershipTransaction, LiveWorkSubmission,LiveWorkProject,OTP, UserProfile
from django.contrib.admin.sites import AlreadyRegistered

# ---------------- CustomUser Admin ----------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'coins', 'membership_start_date', 'membership_end_date')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

# ---------------- Safe registration for other models ----------------
models = [Note, CoinTransaction, MembershipTransaction, LiveWorkProject, LiveWorkSubmission, OTP, UserProfile]

for model in models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass  # Agar already registered hai, ignore
