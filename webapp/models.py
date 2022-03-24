# Django
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save


# Local Django

# Variables

REGISTRATION_STATUS = (
    ('Pending',  'Pending'),
    ('Approved', 'Approved'),
    ('Declined', 'Declined'),
)

NATIONAL_ID_TYPE = (
    ('Ghana Card',      'Ghana Card'),
    ('Drivers License', 'Driver License'),
    ('Passport',        'Passport'),
    ('voter ID',        'Voter ID'),
    ('other',           'Other'),
)


class CustomerDetails(models.Model):

    """ This model defines the customer registration detials """
    
    customer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=50)
    hobbies = models.CharField(max_length=50)
    national_id_type = models.CharField(max_length=50, choices=NATIONAL_ID_TYPE)
    national_id = models.CharField(max_length=50)
    username = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=20, null=True, blank=True)
    registration_status = models.CharField(max_length=50, choices=REGISTRATION_STATUS, default='Pending')
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    class Meta:
        verbose_name_plural = 'Customer Details'
        db_table = 'Customer Details'

    def __str__(self):
        return str(self.first_name + " " + self.last_name)


class Facilities(models.Model):    
    facility_id   = models.AutoField(primary_key=True)
    facility_name = models.CharField(max_length=80)

    class Meta:
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return str(self.facility_name)


class CustomerReservations(models.Model):

    """ This model defines the table that captures customer registration details """
    
    reservation_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, null=True)
    facility  = models.ForeignKey(Facilities, on_delete=models.CASCADE, null=True)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural  = 'Customer Reservations'
        db_table = 'Customer Reservations'

    def __str__(self):
        return str(self.reservation_id)


class CustomerPayments(models.Model):

    """ This model defines the table that captures customer refistration details """
    
    customer_id = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    amount_paid  = models.IntegerField()
    payment_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    class Meta:
        verbose_name_plural  = 'Customer Payments'
        db_table = 'Customer Payments'

    def __str__(self):
        return str(self.customer_id)


class CustomerFacility(models.Model):    
    customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, null=True, blank=True)
    facility = models.ForeignKey(Facilities, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural  = 'Customer Facility'
        db_table = 'Customer Facility'

    def __str__(self):
        return str(self.customer_id)