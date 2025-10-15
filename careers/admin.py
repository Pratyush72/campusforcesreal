from django.contrib import admin
from .models import Career, JobApplication

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'posted_at', 'plan_required')
    list_filter = ('plan_required',)
    search_fields = ('title', 'company', 'location')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'applied_at', 'rejection_reason')
    list_filter = ('status',)
    search_fields = ('user__email', 'job__title')
