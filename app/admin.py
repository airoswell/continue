from django.contrib import admin
from app.models import RegUser, Item, Post, PassEvent, ItemPostRelation
# Register your models here.


class RegUserAdmin(admin.ModelAdmin):
    fields = ['username', 'password', 'email']


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'quantity', 'time_created')
    fieldset = (
        (
            "Basic Info",
            {
                "fields": ['title', 'quantity', 'condition', 'current_owner']
            }
        ),
        (
            "Detail",
            {
                "fields": ['description', 'link', "time_created"]
            }
        ),
    )


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'zip_code', 'time_posted')
    fieldset = (
        (
            "Basic info",
            {
                "fields": ["id", "title", 'owner', 'zip_code']
            }
        ),
        (
            "Detail",
            {
                "fields": ['item', "expiration_date"]
            }
        )
    )


class ItemPostRelationAdmin(admin.ModelAdmin):
    list_display = ('item', 'post', 'item_status')
    fieldset = (
        (
            "Basic",
            {
                "fields": ['item', 'post'],
            }
        ),
        (
            "Detail",
            {
                "fields": ['item_status', 'item_request'],
            }
        )
    )

admin.site.register(RegUser, RegUserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ItemPostRelation, ItemPostRelationAdmin)
