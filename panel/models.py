from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone

class News(models.Model):
    title = models.CharField(max_length=100,default=None)
    detail = HTMLField()
    # image = models.ImageField(upload_to='media/',blank='true',null='true')

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField(default=None,null=True,blank=True)
# Create your models here.
class BloodRequest(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    location = models.CharField(max_length=255)
    disease = models.CharField(max_length=255)
    time_limit = models.DateTimeField()
    hospital = models.CharField(max_length=255)
    attendant_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    pick_drop_service = models.BooleanField(default=False)
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.blood_group} needed at {self.hospital}"
    
  
class ReadyDonors(models.Model):
    # Name and Address
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)

    # Personal Details
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    weight = models.FloatField()
    disease = models.CharField(max_length=255, blank=True, null=True)

    # Blood Group (Optional)
    blood_group = models.CharField(
        max_length=5,
        choices=[('A+', 'A+'), ('B+', 'B+'), ('O+', 'O+'), ('AB+', 'AB+'),
                 ('A-', 'A-'), ('B-', 'B-'), ('O-', 'O-'), ('AB-', 'AB-')],
        blank=True, null=True
    )

    # Contact Information
    phone = models.CharField(max_length=15)  # Ensure it's required in the form
    email = models.EmailField(blank=True, null=True)

    # Donation Time Preference (Now Optional)
    donation_time = models.CharField(
        max_length=20,
        choices=[('Urgent', 'Urgent'), ('Blood Bank', 'Donate to Blood Bank')],
        blank=True, null=True  # This prevents integrity errors when empty
    )

    # Date when donation was made or when form was submitted
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.blood_group if self.blood_group else 'No Blood Group'})"

    class Meta:
        verbose_name = 'Ready Donor'
        verbose_name_plural = 'Ready Donors'
