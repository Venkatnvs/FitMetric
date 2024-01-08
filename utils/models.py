from django.db import models

class ContactUs(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    phone_no = models.CharField(max_length=255,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    by_login_user = models.BooleanField(default=False)
    is_replyed = models.BooleanField(default=False)
    is_ignored = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.email}"