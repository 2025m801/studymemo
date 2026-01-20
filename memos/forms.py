from django import forms
from .models import Memo, Subject

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ["subject", "title", "content", "tags", "importance", "understanding", "next_action"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 6}),
            "tags": forms.TextInput(attrs={"placeholder": "#試験 #要復習"}),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name"]
