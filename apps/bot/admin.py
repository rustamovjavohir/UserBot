from django.contrib import admin
from apps.bot.models import User, Group, Message


# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "message", "image", "message_id", "is_deleted", "created_at"]
    list_display_links = ["user", "message"]
    # list_editable = ["balance", "payment_date"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["id", "group_id"]
    # list_editable = ["balance", "payment_date"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "user_telegram_id", "username", "full_name", "is_deleted", "created_at"]
