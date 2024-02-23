from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page
     path('slots/', views.slots_view, name='slots'),
    path('admin-login/', views.admin_login, name='admin_login'),  # Admin login page
    path('admin-logout/', views.admin_logout, name='admin_logout'),  # Admin logout page
    path('register/', views.register, name='register'),  # Registration page
    path('add-admin/', views.add_admin, name='add_admin'),  # Add admin page
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard page
    path('booking-management/<int:user_id>/', views.booking_management, name='booking_management'),  # Booking management page
    path('feedback-management/', views.feedback_management, name='feedback_management'),  # Feedback management page
    path('feedback/add/', views.add_feedback, name='add_feedback'),  # Add feedback page
    path('update_feedback/<int:feedback_id>/', views.update_feedback, name='update_feedback'),
    path('feedback/toggle/<int:fid>/', views.toggle_feedback_status, name='toggle_feedback_status'),  # Toggle feedback status
    path('feedback/delete/<int:fid>/', views.delete_feedback, name='delete_feedback'),  # Delete feedback
    path('rate-management/', views.rate_management, name='rate_management'),  # Rate management page
    path('add_rate/', views.add_rate, name='add_rate'),  # Add rate page
    path('rate_list/', views.rate_list, name='rate_list'),  # Add rate page
    path('update_rate/<int:rate_id>/', views.update_rate, name='update_rate'),
    path('delete_rate/<int:rate_id>/', views.delete_rate, name='delete_rate'),  # Delete rate
    path('admin/', views.AdminListCreate.as_view(), name='admin-list-create'),  # Admin list and create API
    path('admin/<int:pk>/', views.AdminRetrieveUpdateDestroy.as_view(), name='admin-retrieve-update-destroy'),  # Admin retrieve, update, and destroy API
    path('booking/', views.BookingListCreate.as_view(), name='booking-list-create'),  # Booking list and create API
    path('booking/<int:pk>/', views.BookingRetrieveUpdateDestroy.as_view(), name='booking-retrieve-update-destroy'),  # Booking retrieve, update, and destroy API
    path('feedback/', views.FeedbackListCreate.as_view(), name='feedback-list-create'),  # Feedback list and create API
    path('feedback/<int:pk>/', views.FeedbackRetrieveUpdateDestroy.as_view(), name='feedback-retrieve-update-destroy'),  # Feedback retrieve, update, and destroy API
    path('rate/', views.RateListCreate.as_view(), name='rate-list-create'),  # Rate list and create API
    path('rate/<int:pk>/', views.RateRetrieveUpdateDestroy.as_view(), name='rate-retrieve-update-destroy'),  # Rate retrieve, update, and destroy API
    path('slot/', views.SlotListCreate.as_view(), name='slot-list-create'),  # Slot list and create API
    path('slot/<int:pk>/', views.SlotRetrieveUpdateDestroy.as_view(), name='slot-retrieve-update-destroy'),  # Slot retrieve, update, and destroy API
    # Add URL patterns for other models' views here
]
