from django.db import models
from django.utils import timezone

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    branch = models.CharField(max_length=15, blank=True, null=True)
    year = models.CharField(max_length=15, blank=True, null=True)
    #photo = models.ImageField(upload_to='members/', blank=True, null=True)
    #bio = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(blank=True, null=True)  # Add this field

    def save(self, *args, **kwargs):
        if self.is_approved and self.approval_date is None:
            self.approval_date = timezone.now()
        super(Member, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class MemberRole(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='roles')
    role = models.CharField(max_length=50)
    photo_url = models.TextField(blank=True, null=True)
    assigned_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.member.name} - {self.role}"