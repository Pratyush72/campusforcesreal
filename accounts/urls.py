from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from .views import newsletter_subscribe
from django.views.generic import TemplateView





urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('reset-password/', views.reset_password_email, name='reset_password'),
    path('newsletter/subscribe/', newsletter_subscribe, name='newsletter_subscribe'),
    # path("resend-otp/", views.resend_otp, name="resend_otp")
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('new-password/', views.new_password, name='new_password'), 
    path('notes/', views.notes_view, name='notes'), 
    path('upload-notes/', views.upload_notes_view, name='upload_notes'),
    path('membership/', views.membership_view, name='membership'),
    path('checkout/<str:plan>/', views.checkout, name='checkout'),
    path('projects/', views.projects_view, name='projects'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('payment-timeout/', views.payment_timeout, name='payment_timeout'),
    # path('coin-transaction/', views.coin_transaction_view, name='coin_transaction'),
    path('my_transactions/', views.my_transactions_view, name='my_transactions'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path("careers/", include("careers.urls", namespace="careers")),
    path('featured/', views.featured, name='featured'),
    path('help/', views.help_view, name='help'),
    path('community/', views.community_view, name='community'),
    path('meet/', views.meet_view, name='meet'),
    path('submit_code/', views.submit_code, name='submit_code'),
    path('my_submissions/', views.my_submissions_view, name='my_submissions'),
    path('livework/start/<int:project_id>/', views.start_project_view, name='start_project'),
    path('live_work/', views.live_work_view, name='live_work'),
    path('start_project/<int:project_id>/', views.start_project_view, name='start_project'),
    path('submit_code/', views.submit_code, name='submit_code'),
    path('privacy/', views.privacy_view,name='privacy'),
    path('term_condition/', views.term_condition_view,name='term_condition'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('admin/', admin.site.urls),
    path('chat/', include('realtime_chat.urls', namespace='realtime_chat')),  # Chat app
    path('admin-panel/', include('admin_panel.urls', namespace='admin_panel')),




   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 
from django.urls import path
from . import views
