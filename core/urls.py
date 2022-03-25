# Django
from django.contrib import admin
from django.urls import path

# Local Django
from webapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name="index"),
    path('signup',views.signup_page, name="signup"),
    path('login',views.login_page, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('admin_panel',views.admin_panel,  name="admin_panel"),
    path('subscription', views.customer_reservation_page,  name="sub"),
    
    path('reg_approval/<str:customer_id>/', views.approve_registration,name="reg"),
    path('payments/<str:customer_id>/', views.customer_payments, name="payments")
]

