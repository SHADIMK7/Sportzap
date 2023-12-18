from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

admin.site.register(Owner)
admin.site.register(Abstract)  

class TurfAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_per_page = 100
    list_display =['owner', 'name', 'location', 'price', 'image', 'description','latitude', 'longitude']
    # search_fields = ('price')
admin.site.register(Turf, TurfAdmin)
admin.site.register(Amenity)
# admin.site.register(TurfBooking)
admin.site.register(PaymentHistoryModel)
# admin.site.register(MatchModel)
admin.site.register(MatchRatingModel)
admin.site.register(Customer)
admin.site.register(Gallery)
admin.site.register(Profile)
admin.site.register(RewardPointModel)
admin.site.register(UserBookingHistory)
admin.site.register(RedeemRewardsModel)
# admin.site.register(TurfPriceUpdateModel)
admin.site.register(AiTurfBookModel)

class TurfBookingResource(resources.ModelResource):
    class Meta:
        model = TurfBooking

class TurfBookingAdmin(ImportExportModelAdmin):
    resource_class = TurfBookingResource

admin.site.register(TurfBooking, TurfBookingAdmin)
admin.site.register(TurfRating)

