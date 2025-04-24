from django.contrib import admin
from django.contrib.auth.models import User  # ✅ This is OK
from .models import EmailLog  # ✅ This is OK

admin.site.register(EmailLog)