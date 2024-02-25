# Import necessary modules and classes
from rest_framework import generics, status, serializers
from django.shortcuts import render, redirect, get_object_or_404
from .models import Admin, Booking, Feedback, Rate, Slot
from .serializers import AdminSerializer, BookingSerializer, FeedbackSerializer, RateSerializer, SlotSerializer
from django.contrib.auth import authenticate, login, logout , get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from rest_framework.response import Response
import requests
from django.utils import timezone
from django.core.exceptions import ValidationError
from django import forms
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.db.models import Subquery, OuterRef
# Define class for Admin registration
from .forms import LoginForm
import calendar
class AdminRegister(generics.CreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def get(self, request, *args, **kwargs):
        # Render the registration form for GET requests
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        # Handle form submission for POST requests
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Set the 'a_lastseen' field to the current timestamp
            serializer.validated_data['a_lastseen'] = timezone.now()
            # If form data is valid, save the user and display success message
            serializer.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')  # Redirect to login page
        else:
            # If form data is invalid, display error message and render the registration form again
            errors = serializer.errors
            messages.error(request, f'Registration failed. {errors}')
            return render(request, 'register.html', {'errors': errors})

# Define Serializer for Admin model
class AdminSerializer(serializers.ModelSerializer):
    a_img = serializers.ImageField(required=False)

    class Meta:
        model = Admin
        fields = ['a_id', 'a_username', 'a_password', 'a_img', 'a_lastseen']

# Define Form for Admin
class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['username', 'password', 'a_img']

# Define class for Admin List and Create operations
class AdminListCreate(generics.ListCreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

# Define class for Admin Retrieve, Update, and Destroy operations
class AdminRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

# Define class for Booking List and Create operations
class BookingListCreate(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# Define class for Booking Retrieve, Update, and Destroy operations
class BookingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# Define class for Feedback List and Create operations
class FeedbackListCreate(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

# Define class for Feedback Retrieve, Update, and Destroy operations
class FeedbackRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

# Define class for Rate List and Create operations
class RateListCreate(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

# Define class for Rate Retrieve, Update, and Destroy operations
class RateRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

# Define class for Slot List and Create operations
class SlotListCreate(generics.ListCreateAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

# Define Form for Login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['f_name', 'f_contact', 'f_message', 'f_status']

class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['rtid', 'r_rate']

# Define class for Slot Retrieve, Update, and Destroy operations
class SlotRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

# Define index view
def index(request):
    return render(request, 'index.html')

# Define admin_dashboard view
def admin_dashboard(request):
    # Fetch admin users data
    admin_users = Admin.objects.all()
    return render(request, 'admin_dashboard.html', {'admin_users': admin_users})

# Define feedback_management view
def feedback_management(request):
    # Fetch feedbacks data
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback_management.html', {'feedbacks': feedbacks})

# Define rate_management view
def rate_management(request):
    # Fetch rates data
    rates = Rate.objects.all()
    return render(request, 'rate_management.html', {'rates': rates})

# Define add_admin view

def add_admin(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to the appropriate page after registration
            return redirect('admin_login')  # Replace 'dashboard' with the desired URL name
    else:
        form = UserCreationForm()
    return render(request, 'admin_dashboard.html', {'form': form})

# Define register view
# def register(request):
    if request.method == 'POST':
        form = AdminForm(request.POST, request.FILES)
        if not form.is_valid():
            print(form.errors)  # Print form errors to console for debugging
            messages.error(request, 'Form is not valid.')
        else:
            try:
                admin_instance = Admin.objects.create(
                    # user=user,
                    a_username=form.cleaned_data['a_username'],
                    a_password=form.cleaned_data['a_password'],
                    a_img=form.cleaned_data['a_img']  # Assuming image is included in the form
                )

                # Update the last seen time for the admin user
                admin_instance.a_lastseen = timezone.now()
                admin_instance.save()

                messages.success(request, 'User added successfully.')
                return redirect('booking_management')  # Redirect to admin dashboard after adding admin
            except Exception as e:
                messages.error(request, f'Error: {e}')
    else:
        form = AdminForm()
    return render(request, 'register.html', {'form': form})
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm

class AdminCreationForm(UserCreationForm):
    a_img = forms.ImageField(required=False)  # Optional image field
    a_lastseen = forms.DateTimeField(required=False)  # Optional last seen field

    class Meta:
        model = Admin
        fields = ('username', 'a_img', 'a_lastseen', 'password1', 'password2')  # Include additional fields in the form
from .forms import AdminRegistrationForm , LoginForm
def register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.a_lastseen = timezone.now()  # Set a_lastseen to current date and time
            admin.save()
            return redirect('admin_login')  # Redirect to a success page
    else:
        form = AdminRegistrationForm()
    return render(request, 'register.html', {'form': form})


def admin_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('booking_management', user_id=user.id)  # Redirect to booking_management with user_id
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'admin_login.html', {'form': form})



def admin_logout(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('admin_login')




def booking_management(request, user_id):
    print("user_id", user_id)
    if request.method == 'POST':
        # Handling form submission for adding or updating booking
        booking_id = request.POST.get('booking_id')
        slot_id = request.POST.get('slot')
        duration_type = request.POST.get('duration_type')

        # Calculate total time based on duration type
        if duration_type == 'Hourly':
            total_time = int(request.POST.get('b_totaltime'))
        elif duration_type == 'Daily':
            total_time = int(request.POST.get('b_totaltime'))
        elif duration_type == 'Monthly':
            current_month = datetime.now().month
            days_in_current_month = calendar.monthrange(datetime.now().year, current_month)[1]
            total_time = int(request.POST.get('b_totaltime')) * days_in_current_month

        # Get the Admin instance corresponding to the user_id
        admin_instance = User.objects.get(pk=user_id)

        # Calculate amount based on duration type and total time
        amount = calculate_parking_amount(duration_type, total_time)

        if booking_id:  # For updating existing booking
            existing_booking = Booking.objects.get(pk=booking_id)
            if existing_booking.b_slot_id != slot_id and Booking.objects.filter(b_slot_id=slot_id).exists():
                return HttpResponseBadRequest("The selected slot is already booked.")

            # Update existing booking fields
            existing_booking.b_slot_id = slot_id
            existing_booking.b_vehicleno = request.POST.get('vehicle_number')
            existing_booking.b_contact = request.POST.get('contact')
            existing_booking.duration_type = request.POST.get('duration_type')
            existing_booking.b_amount = amount
            existing_booking.b_totaltime=total_time
            existing_booking.b_u_id = admin_instance
            existing_booking.b_udate = datetime.now()
            existing_booking.save()
        else:  # For adding new booking
            new_booking = Booking.objects.create(
                b_slot_id=slot_id,
                b_vehicleno=request.POST.get('vehicle_number'),
                b_contact=request.POST.get('contact'),
                duration_type=request.POST.get('duration_type'),
                b_u_id=admin_instance,
                b_amount=amount,
                b_date=datetime.today().date(),
                b_totaltime=total_time,
                b_udate=datetime.now(),
            )

        return redirect('booking_management', user_id=user_id)

    else:
        # Fetch bookings data for listing
        bookings = Booking.objects.filter(b_u_id=user_id)
        # Extract the IDs of slots booked by the user
        booked_slot_ids = bookings.values_list('b_slot_id', flat=True)

        # Fetch slots corresponding to the booked slot IDs
        slots = Slot.objects.filter(s_id__in=booked_slot_ids)

        # Create a dictionary to map slot IDs to slot names
        slot_names = {slot.s_id: slot.s_slot for slot in slots}

        # Print bookings along with corresponding slot names
        for booking in bookings:
            print(slot_names)
            slot_id = int(booking.b_slot_id)
            slot_name = slot_names.get(slot_id)
            booking.slot_name = slot_name

        # Pass bookings to the template context for rendering

        # Fetch bookings data for listing
        # Fetch slots data
        slots = Slot.objects.all()
        context = {
            'bookings': bookings,
            'slots': slots,
        }
        return render(request, 'booking_management.html', context)



def calculate_parking_amount(duration_type, total_time):
    # Fetch rate from Rate model based on duration type
    if duration_type == 'Hourly':
        rate_obj = Rate.objects.get(rtid='Hourly')  # Assuming hourly rate has rtid=1
    elif duration_type == 'Daily':
        rate_obj = Rate.objects.get(rtid='Daily')  # Assuming daily rate has rtid=2
    elif duration_type == 'Monthly':
        rate_obj = Rate.objects.get(rtid='Monthly')  # Assuming monthly rate has rtid=3

    # Calculate amount using fetched rate
    amount = total_time * rate_obj.r_rate

    return amount

def slots_view(request):
    slots = Slot.objects.all()
    return render(request, 'slots.html', {'slots': slots})
# Define home_view
def home_view(request):
    return render(request, 'home.html')

# Define add_feedback view
def add_feedback(request):
    if request.method == 'POST':
        # Handle form submission for adding new feedback
        f_name = request.POST.get('f_name')
        f_contact = request.POST.get('f_contact')
        f_message = request.POST.get('f_message')
        f_status = 'Show'  # Assuming new feedbacks are initially shown
        # Create new feedback entry
        feedback = Feedback.objects.create(
            f_name=f_name,
            f_contact=f_contact,
            f_message=f_message,
            f_status=f_status
        )
        return redirect('feedback_management')
    else:
        return render(request, 'feedback_management.html')

def update_feedback(request, feedback_id):
    if request.method == 'POST':
        # Retrieve the feedback object
        feedback = Feedback.objects.get(fid=feedback_id)  # Use 'fid' instead of 'id'

        # Update feedback data based on the form submission
        feedback.f_name = request.POST.get('f_name')
        feedback.f_contact = request.POST.get('f_contact')
        feedback.f_message = request.POST.get('f_message')

        # Save the updated feedback
        feedback.save()

        # Redirect to a success page or back to the feedback list
        return redirect('feedback_management')  # Replace 'feedback_list' with the name of your feedback list URL pattern

    else:
        return HttpResponse("Method not allowed")
# Define toggle_feedback_status view
def toggle_feedback_status(request, fid):
    feedback = Feedback.objects.get(pk=fid)
    # Toggle the status
    if feedback.f_status == 'Show':
        feedback.f_status = 'Hide'
    else:
        feedback.f_status = 'Show'
    feedback.save()
    return redirect('feedback_management')

# Define delete_feedback view
def delete_feedback(request, fid):
    feedback = Feedback.objects.get(pk=fid)
    feedback.delete()
    return redirect('feedback_management')


# View for adding a new rate
def add_rate(request):
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.r_cdate = datetime.today()  # Set creation date to today's date
            rate.r_udate = datetime.today()
            rate.save()
            messages.success(request, 'Rate added successfully!')
            return redirect('rate_management')
        else:
            messages.error(request, 'Failed to add rate. Please check the form data.')
    else:
        form = RateForm()

    return render(request, 'rate_management.html', {'form': form})

# View for updating an existing rate
def update_rate(request, rate_id):
    rate = Rate.objects.get(pk=rate_id)
    if request.method == 'POST':
        form = RateForm(request.POST, instance=rate)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.r_udate =datetime.today()
            rate.save()
            return redirect('rate_list')  # Redirect to the rate list page
    else:
        form = RateForm(instance=rate)
    return redirect('rate_list')

# View for deleting a rate
def delete_rate(request, rate_id):
    rate = get_object_or_404(Rate, pk=rate_id)
    rate.delete()
    return redirect('rate_list')

# View for listing rates
def rate_list(request):
    rates = Rate.objects.all()
    return render(request, 'rate_management.html', {'rates': rates})





