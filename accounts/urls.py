from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('reset-password/', views.reset_password_email, name='reset_password'),
    # path("resend-otp/", views.resend_otp, name="resend_otp")
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('new-password/', views.new_password, name='new_password'), 
    path('notes/', views.notes_view, name='notes'), 
    path('upload-notes/', views.upload_notes_view, name='upload_notes'),
    path('membership/', views.membership_view, name='membership'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('coin-transaction/', views.coin_transaction_view, name='coin_transaction'),
    path('submit-project/', views.submit_project, name='submit_project'),
    path('profile/', views.profile_view, name='profile'),
    path('add-coins/', views.add_coins, name='add_coins'),
    path('resume-builder/', views.resume_builder_view, name='resume_builder'),
    path('live-projects/', views.live_projects_view, name='live_projects'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('submit-project/', views.submit_project, name='submit_project'),
    path('add-coins/', views.add_coins, name='add_coins'),
    path('live-projects/', views.live_projects_view, name='live_projects'),
    path('resume-builder/', views.resume_builder_view, name='resume_builder'),
    path('featured/', views.featured, name='featured'),
    path('help/', views.help_view, name='help'),
    path('community/', views.community_view, name='community'),
    path('meet/', views.meet_view, name='meet'),
    path('livework/', views.livework_view, name='livework'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 
from django.urls import path
from . import views
