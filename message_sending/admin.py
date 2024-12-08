from django.contrib import admin

from message_sending.models import Addressee, Log, Mailing, Message


@admin.register(Addressee)
class AddresseeAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "comment")
    list_filter = ("email",)
    search_fields = ("email", "name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
    list_filter = ("subject",)
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "status",
        "message",
    )
    list_filter = ("status",)
    search_fields = ("status", "message")


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("status", "answer", "mailing", "datetime")
    list_filter = ("status",)
    search_fields = ("status", "answer")
