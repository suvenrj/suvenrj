from django.db import models

class Members(models.Model):

    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    DOB = models.DateField(blank=True)
    blood_group= models.CharField(max_length=255)
    email_id = models.EmailField(max_length=255)
    mobile_number = models.CharField(max_length=255)
    upcoming_appointment = models.DateTimeField(blank=True, null=True)
    sent_mail = models.BooleanField(default=True)
