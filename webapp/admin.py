# Django
from django.contrib import admin

# Local Django apps
from .models import *


# Register your models here.

class CustomerDetailsAdmin(admin.ModelAdmin):

    list_display = (
        'customer_id',
        'user',
        'first_name',
        'last_name',
        'date_of_birth',
        'address',
        'hobbies',
        'registration_status',
        'date_created',
        'username',
        'password',
        'national_id',
    )


admin.site.register(CustomerDetails, CustomerDetailsAdmin)


class CustomerReservationsAdmin(admin.ModelAdmin):

    list_display = (
        'reservation_id',
        'customer_id',
        'facility',
        'reservation_date',
        'reservation_time',
        'date_created',
    )


admin.site.register(CustomerReservations, CustomerReservationsAdmin)


class CustomerPaymentsAdmin(admin.ModelAdmin):

    list_display = (
        'customer_id',
        'amount_paid',
        'payment_date',
        'date_created',
    )


admin.site.register(CustomerPayments, CustomerPaymentsAdmin)


class FacilitiesAdmin(admin.ModelAdmin):

    list_display = (
        'facility_id',
        'facility_name',
    )


admin.site.register(Facilities, FacilitiesAdmin)


class CustomerFacilityAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'facility',
    )


admin.site.register(CustomerFacility, CustomerFacilityAdmin)
