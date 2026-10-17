from django.contrib import admin
from .models import Email

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "priority", "confidence", "corrected", "created")
    list_filter = ("priority", "corrected")
