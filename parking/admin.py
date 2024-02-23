from django.contrib import admin
from .models import Admin, Booking, Feedback, Rate, Slot
admin.site.site_header = "SMART PARKING"
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Admin._meta.fields]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Booking._meta.fields]

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Feedback._meta.fields]

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Rate._meta.fields]

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Slot._meta.fields]
