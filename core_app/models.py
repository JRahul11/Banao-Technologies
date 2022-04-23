from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


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
        return self.user.username
    
    class Meta:
        verbose_name_plural = "User"
        db_table = "User"


class BlogModel(models.Model):
    CATEGORIES = (
        ('Mental Health', 'Mental Health'),
        ('Heart Disease', 'Heart Disease'),
        ('Covid19', 'Covid19'),
        ('Immunization ', 'Immunization')
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='blogPictures', default=None, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORIES, null=True, blank=True)
    summary = models.CharField(max_length=500, null=True, blank=True)
    content = models.TextField(max_length=5000, null=True, blank=True)
    isdraft = models.BooleanField(default=False, null=True, blank=True)
    date = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = "Blog"
        db_table = "Blog"


class Appointment(models.Model):
    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="patient")
    doctor = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="doctor")
    speciality = models.CharField(max_length=100, null=True, blank=True)
    date = models.CharField(max_length=100, null=True, blank=True)
    start_time = models.CharField(max_length=100, null=True, blank=True)
    end_time = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.patient.first_name + ' ' + self.doctor.first_name
    
    class Meta:
        verbose_name_plural = "Appointment"
        db_table = "Appointment"