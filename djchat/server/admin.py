from django.contrib import admin
from .models import Category, Server, Channel


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Category, CategoryAdmin)


class ServerAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "category"]


admin.site.register(Server, ServerAdmin)


class ChannelAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "server"]


admin.site.register(Channel, ChannelAdmin)
