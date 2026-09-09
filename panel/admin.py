from django.contrib import admin
from panel.models import News,Contact,BloodRequest,ReadyDonors

class NewsAdmin(admin.ModelAdmin):
    list_display=(
        'title','detail',
    )
class ContactAdmin(admin.ModelAdmin):
    list_display=(
        'name','email','message'
    )
    def has_change_permission(self, request, obj=None):
        return False
class BloodRequestAdmin(admin.ModelAdmin):
    list_display=(
        'blood_group','location','disease','time_limit','hospital','attendant_name',
        'contact','pick_drop_service','created_at','is_solved'
    )
# class AboutAdmin(admin.ModelAdmin):
#     list_display=(
#         'title','description','members','reference','objectives','aims',
#         'mode_of_action','impacts'
#     )

class ReadyDonorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'blood_group', 'address', 'donation_time', 'created_at')
    list_filter = ('blood_group', 'donation_time', 'created_at', 'address')
    search_fields = ('name', 'phone', 'email', 'blood_group', 'address')
    
    # Make fields view-only
    readonly_fields = ('name', 'address', 'age', 'gender', 'weight', 'disease', 'blood_group', 'phone', 'email', 'donation_time')

    def has_change_permission(self, request, obj=None):
        # Disable editing permission
        return False

    def has_add_permission(self, request):
        # Disable adding permission
        return False
    # Optional: Add more customizations like ordering, inlines, etc.
admin.site.register(News,NewsAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(BloodRequest,BloodRequestAdmin)
# admin.site.register(About,AboutAdmin)
admin.site.register(ReadyDonors,ReadyDonorsAdmin)

# Register your models here.