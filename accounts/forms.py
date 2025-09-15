from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Note

# 1. Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')  # Add any fields you want

# 2. OTP Form
class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Enter OTP")

# 3. Note Upload Form
class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['pdf', 'title', 'tags'] 
        from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField()

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class NewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("new_password")
        p2 = cleaned_data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

from django import forms
from .models import LiveProject

class LiveProjectForm(forms.ModelForm):
    class Meta:
        model = LiveProject
        fields = ['project_title', 'description',]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

from django import forms

class MembershipPurchaseForm(forms.Form):
    plan = forms.ChoiceField(choices=[('project', 'Project Pass'), ('premium', 'Premium Pass')])
    use_coins = forms.BooleanField(required=False)
        