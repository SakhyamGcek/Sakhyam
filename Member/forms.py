# forms.py
from django import forms
from .models import Member, MemberRole

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone', 'branch','year']

class MemberRoleForm(forms.ModelForm):
    class Meta:
        model = MemberRole
        fields = ['role']