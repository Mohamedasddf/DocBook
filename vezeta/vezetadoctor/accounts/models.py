from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    SPECIALTY_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('pediatrics', 'Pediatrics'),
        ('orthopedics', 'Orthopedics'),
        ('dermatology', 'Dermatology'),
        ('dentistry', 'Dentistry'),
        ('psychiatry', 'Psychiatry'),
        ('general_surgery', 'General Surgery'),
        ('radiology', 'Radiology'),
        ('urology', 'Urology'),
    ]

    USER_TYPE_CHOICES = [
        ('doctor', 'دكتور'),
        ('user', 'مستخدم عادي'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='Default Name', blank=True)
    who_i = models.TextField(max_length=500, default='Default Discription', blank=True)
    city = models.CharField(max_length=100, default='City')
    address = models.TextField(max_length=500, default='Address')
    phone = models.CharField(max_length=15, default='Phone Number')
    working_hours = models.CharField(max_length=100, default='9:00 AM - 5:00 PM')
    available_times = models.TextField(default='')  # حقل نصي للطبيب لإدخال الأوقات
    waiting_time = models.IntegerField(default=15)
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES, default='general_surgery')
    services = models.TextField(max_length=500, null=True, blank=True)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', default='default_image.jpg')
    facebook = models.URLField(max_length=200, blank=True, null=True, default='') 
    twitter = models.URLField(max_length=200, blank=True, null=True, default='')   
    linkedin = models.URLField(max_length=200, blank=True, null=True, default='') 
    instagram = models.URLField(max_length=200, blank=True, null=True, default='') 
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    slug = models.SlugField(null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.name




# نموذج الموعد
class Appointment(models.Model):
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.appointment_time}"