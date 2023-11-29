from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Turf)
admin.site.register(Amenity)
admin.site.register(TurfBooking)
admin.site.register(PaymentHistoryModel)