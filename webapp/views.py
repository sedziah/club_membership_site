# Django
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Local Django
from .forms import *
from .models import *
from .utils import *



def index(request):

    ''' Homepage view'''
    return render(request, 'index.html')


def signup_page(request):

    '''New customer registration page'''
    
    form = CustomerProfilesForm

    if request.method =="POST":

        form = CustomerProfilesForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('first_name')
            messages.success(request, f"Hi {user} your account has been created successfully. Contact admin for your username and password")

        return redirect('index')

    context = {'form':form}
    return render(request, 'register.html', context)


def login_page(request):

    '''Existing customer login page'''

    form = LoginForm

    if request.method =="POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
                       
            if request.user.is_superuser:
                return redirect(admin_panel)
            else:
                return redirect('sub')
        else:
            messages.error(request, "Wrong username and password")

    context = {'form':form}
    return render(request, 'login.html', context)

def logoutUser(request):
    return redirect('index')

@login_required(login_url='login')
def admin_panel(request):
    """ 
    Admin panel for users with admin access to view and approve new users
    """

    if request.user.is_superuser:
    
        approved_customer      = CustomerDetails.objects.filter(registration_status = "Approved")
        new_registrations      = CustomerDetails.objects.filter(registration_status = "Pending")
        facility_reservations  = CustomerReservations.objects.all()
        
        print(approved_customer)

        context = {   

            'approved_customer'        : approved_customer,
            'new_registrations'        : new_registrations,
            'facility_reservations'    : facility_reservations 
        }
    else:
        return redirect('sub')

    return render(request, 'admin_panel.html', context)

@login_required(login_url='login')
def approve_registration(request, customer_id):
    
    form = CustomerApprovalForm
    customers = CustomerDetails.objects.get(customer_id=customer_id)

    
    if request.method == 'POST':
        form = CustomerApprovalForm(request.POST, instance=customers)
        if form.is_valid():
            form.save()         

        customer = CustomerDetails.objects.filter(customer_id=customer_id)

        for i in customer: 
            last_name = i.last_name 

        username = customer.update(username=username_generator(last_name))
        customer.update(password=password_generator())


        updated_customer = CustomerDetails.objects.filter(customer_id=customer_id,)

        for i in updated_customer: 
            username  = i.username
            password  = i.password

        ''' This function creates a new user in the user authentication table'''

        create_approved_user(username, password)

        user_instance = User.objects.get(username=username)
        user_customer = CustomerDetails.objects.filter(customer_id=customer_id)
        user_customer.update(user=user_instance)
        

        '''This function creates a new facility has been created in the facilities table'''
        
        

        update_customer_facility(customer_id=customer_id, facility_name='Gym')

        return redirect('admin_panel')

    context = {'form':form}
    return render(request, 'register.html', context)

@login_required(login_url='login')
def customer_reservation_page(request):
        
    if request.user.is_superuser:
        return redirect('admin_panel')
    else:

        form = CustomerReservationForm

        customer_id = request.user.customerdetails.customer_id

        
        if request.method =="POST":

            form = CustomerReservationForm(request.POST)
            if form.is_valid():

                facility = form.cleaned_data['facility'].facility_id
                customer_id = CustomerDetails.objects.get(customer_id=customer_id)
                facility_accessible = CustomerFacility.objects.filter(customer=customer_id).filter(facility=facility)

                if facility_accessible:
                    form.save()
                    CustomerReservations.objects.update(customer_id=customer_id)
                    messages.success(request, "Booking confirmed!")
                    
                else:
                    messages.error(request, "Your are not eligible to book this facility")
                return redirect('sub')


    context = {'form':form}

    return render(request, 'customer_page.html', context)

def customer_payments(request, customer_id):
    
    customers = CustomerDetails.objects.filter(customer_id=customer_id)

    customer_instance = customers.get(customer_id=customer_id)

    form = CustomerPaymentsForm(instance=customer_instance)
    

    if request.method == 'POST':
        form = CustomerPaymentsForm(request.POST)
        if form.is_valid():
            form.save()        

            payment_made = customer_percentage_paid(customer_id=customer_id)

            if payment_made >= 50 and payment_made < 100 :
                update_customer_facility(customer_id=customer_id, facility_name='Swimming Pool')

            elif payment_made >= 100:
                update_customer_facility(customer_id=customer_id, facility_name='Tennis Court')
                update_customer_facility(customer_id=customer_id, facility_name='Conference Room')
                update_customer_facility(customer_id=customer_id, facility_name='Swimming Pool')                
              
        return redirect('admin_panel')

    context = {'form':form}
    return render(request, 'payments.html', context)
