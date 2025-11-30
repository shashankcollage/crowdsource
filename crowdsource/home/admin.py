from django.contrib import admin
from .models import *

admin.site.site_header="user dashboard"
admin.site.register(Issue)
admin.site.register(ActivityLog)
# admin.site.register(UserProfile)
