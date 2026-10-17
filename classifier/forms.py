from django import forms
from .models import Email


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ["sender", "subject", "body"]
        widgets = {
            "sender": forms.EmailInput(attrs={"placeholder": "sender@example.com (optional)"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "body": forms.Textarea(attrs={"rows": 6, "placeholder": "Paste the email body"}),
        }
