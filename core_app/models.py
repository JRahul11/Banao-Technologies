from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    address_line1 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.address_line1
    
    class Meta:
        verbose_name_plural = "Address"
        db_table = "Address"

class UserModel(models.Model):
    USER_ROLE = (
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profilePictures', default=None, blank=True)
    email_id = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True, choices=USER_ROLE)
    last_login = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "User"
        db_table = "User"
    
    