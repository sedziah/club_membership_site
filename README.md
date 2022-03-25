# Club Membership Web Application

A club membership application that allows customers to register and reserve facilities. 


### Features

1. Signup New Customers
2. Admin approval
3. Username & password generation and creation
   - Username: Lastname + 2 numbers
   - Password: Alphanumeric characters

4. User Login
5. Facility Reservation
   - New customer: Gym only
   - 50% Payment : Gym & Swimming Pool
   - 100% Payment : All Facilities
6. User/Admin Logout

### Setting up and running the web application

1.	Clone or download the zipped repository from the GitHub link
2.	Extract all contents from the zipped folder
3.	Open your terminal and cd to project root $cd project_folder
4.	Create virtual environment and activate it by running
   	'$python -m venv venv'
ii.	 source venv/Scripts/activate
e.	Install all dependencies by executing:  $pip install -r requirements.txt
f.	Setup the application database by executing the following commands:
i.	$python manage.py makemigrations
ii.	$python manage.py migrate
g.	Run the application by executing: $python manage.py runserver
h.	For creating an admin-user execute: $python manage.py createsuperuser or use the login credentials below to access the system_admin
Admin credentials
username: admin
password: admin 
