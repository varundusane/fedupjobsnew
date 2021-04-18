from django.contrib import admin
from django.contrib.auth.models import Group,User
# from admin_tools.dashboard.models import
from .models import JobCategory, WorkDetails, Job_keys
from django.utils.html import format_html

admin.site.unregister(Group)
admin.site.unregister(User)
# admin.site.unregister(LogEntry)
# admin.site.disable_action('Recent_action')
admin.site.register((JobCategory, Job_keys))

def make_verify(modeladmin, request, queryset):
    queryset.update(verify=True)
make_verify.short_description = "Verify selected jobs "

class work(admin.ModelAdmin):
    list_display = ('job_title', 'Verify_link','verify')
    actions = [make_verify]

    def Verify_link(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.verify_link)



admin.site.register(WorkDetails, work)

# admin.site.unregister(django_apscheduler)
