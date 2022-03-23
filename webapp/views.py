# Django
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


# Local Django
from .forms         import *
from .models        import *
from .utils         import *
#from .decorators    import all_users, allowed_users, unauthenticated_user



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
        facility_reservations  = CustomerReservations.objects.all()
        new_registrations      = CustomerDetails.objects.filter(registration_status = "Pending")
        
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

        customer = CustomerDetails.objects.filter(customer_id=customer_id,)

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


        return redirect('admin_panel')
        
        #else:
        #    return HttpResponse('Restricted Access') 

    context = {'form':form}
    return render(request, 'register.html', context)

@login_required(login_url='login')
def customer_reservation_page(request):

    
    if request.user.is_superuser:
        return redirect('admin_panel')
    else:

        customer_id = request.user.customerdetails.customer_id
        print(customer_id)


        def form_type():

            form = CustomerReservationForm
            customer_payments = CustomerPayments.objects.filter(customer_id=customer_id)
            all_payments = customer_payments.aggregate(sum=Sum('amount_paid'))
            total_paid = all_payments['sum'] 

            subscription_cost = 1000  # This an assumed customer subscription cost
            
            if total_paid is not None:
                total_percentage_payment =  (total_paid / subscription_cost) * 100
            else:
                total_percentage_payment = 0
                
                #global form 
            #form = CustomerReservationForm
            return form


        if request.method =="POST":

            form = CustomerReservationForm(request.POST)
            if form.is_valid():

                facility = form.cleaned_data['facility'].facility_id
                customer_id = CustomerDetails.objects.get(customer_id=customer_id)
                customer_access = CustomerFacility.objects.filter(customer=customer_id).filter(facility=facility)

                if customer_access:
                    form.save()
                else:
                    #customer not eligible
                    print("not eligible")
                return redirect('sub')


    context = {'form':form_type()}

    return render(request, 'customer_page.html', context)

  
def customer_payments(request, customer_id):
    
    customers = CustomerDetails.objects.filter(customer_id=customer_id)

    customer_instance = customers.get(customer_id=customer_id)

    form = CustomerPaymentsForm(instance=customer_instance)
    

    if request.method == 'POST':
        form = CustomerPaymentsForm(request.POST)
        if form.is_valid():
            form.save()         

              
        return redirect('admin_panel')

    context = {'form':form}
    return render(request, 'payments.html', context)
