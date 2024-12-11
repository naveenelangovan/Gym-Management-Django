from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app.views  import  admin_dashboard,add_user,add_workout,admin_login,edit_user,edit_workout,delete_user,delete_workout,user_details,user_login,user_profile,check_in,check_out, home,logout_user, calculate_bmi


urlpatterns = [
    
    path('admin/', admin.site.urls),
        
    # Home page
    path('', home, name='home'),
    path('logout/', logout_user, name='logout'),

    # Admin routes
    path('admin-login/', admin_login, name='admin_login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),

    # User routes
    path('user-login/', user_login, name='user_login'),
    path('user-profile/<int:id>/', user_profile, name='user_profile'),

    # User management (admin)
    path('add-user/', add_user, name='add_user'),
    path('edit-user/<int:id>/', edit_user, name='edit_user'),
    path('delete-user/<int:id>/', delete_user, name='delete_user'),
    
    # View user details (admin)
    path('user-details/<int:id>/', user_details, name='user_details'),

    # Workout management
    path('add-workout/<int:user_id>/', add_workout, name='add_workout'),
    path('edit-workout/<int:id>/', edit_workout, name='edit_workout'),
    path('delete-workout/<int:id>/', delete_workout, name='delete_workout'),

    # Check-in and check-out
    path('check-in/<int:id>/', check_in, name='check_in'),
    path('check-out/<int:id>/', check_out, name='check_out'),
    
    path('bmi-calculator/', calculate_bmi, name='calculate_bmi'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
