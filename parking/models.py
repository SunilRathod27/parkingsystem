from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class Admin(AbstractUser):
    a_img = models.ImageField(upload_to='media/admin_images/', null=True, blank=True)
    a_lastseen = models.DateTimeField(null=True, blank=True)

class Booking(models.Model):
    b_id = models.AutoField(primary_key=True)
    b_u_id = models.ForeignKey(Admin, on_delete=models.CASCADE)
    b_t_id = models.IntegerField(null=True, blank=True)
    b_slot_id = models.CharField(max_length=20)
    b_vehicleno = models.CharField(max_length=20)
    b_contact = models.BigIntegerField()
    b_date = models.DateField()
    b_startdate = models.CharField(max_length=20)
    b_enddate = models.CharField(max_length=20)
    b_totaltime = models.IntegerField()
    b_amount = models.IntegerField()
    DURATION_CHOICES = [
        ('Hourly', 'Hourly'),
        ('Daily', 'Daily'),
        ('Monthly', 'Monthly'),
    ]
    duration_type = models.CharField(max_length=10, choices=DURATION_CHOICES)
    b_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirm', 'Confirm'), ('Complete', 'Complete')])
    b_udate = models.DateTimeField()


class Feedback(models.Model):
    fid = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=50)
    f_contact = models.BigIntegerField()
    f_message = models.TextField()
    f_status = models.CharField(max_length=20, choices=[('Show', 'Show'), ('Hide', 'Hide')])
    focdate = models.DateTimeField(default=datetime.now)

class Rate(models.Model):
    r_id = models.AutoField(primary_key=True)
    rtid = models.CharField(max_length=20)
    r_rate = models.IntegerField()
    r_cdate = models.DateTimeField()
    r_udate = models.DateTimeField()

class Slot(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_t_id = models.IntegerField()
    s_slot = models.CharField(max_length=20)
    s_cdate = models.DateTimeField()
    s_udate = models.DateTimeField()

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    hours_used = models.IntegerField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=datetime.now)


