from django.contrib import admin
from app.models import Item, Post, ItemTransactionRecord, PostItemStatus
# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'quantity', 'time_created')
    fieldset = (
        (
            "Basic Info",
            {
                "fields": ['title', 'quantity', 'condition', 'owner']
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
    list_display = ('id', 'title', 'owner', 'area', 'time_created')
    fieldset = (
        (
            "Basic info",
            {
                "fields": ["id", "title", 'owner', 'area']
            }
        ),
        (
            "Detail",
            {
                "fields": ['item', "expiration_date", "items"]
            }
        )
    )


class PostItemStatusAdmin(admin.ModelAdmin):
    list_display = ('item', 'post')
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
                "fields": ['item_requesters'],
            }
        )
    )


admin.site.register(Item, ItemAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostItemStatus, PostItemStatusAdmin)
