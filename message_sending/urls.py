from django.urls import path

from message_sending.apps import MessageSendingConfig
from message_sending.views import (AddresseeCreateView, AddresseeDeleteView,
                                   AddresseeDetailView, AddresseeListView,
                                   AddresseeUpdateView, LogListView,
                                   MailingCreateView, MailingDeleteView,
                                   MailingDetailView, MailingListView,
                                   MailingStatusView, MailingUpdateView,
                                   MessageCreateView, MessageDeleteView,
                                   MessageDetailView, MessageListView,
                                   MessageUpdateView, SampleView,
                                   mailing_send_view)

# from django.views.decorators.cache import cache_page


app_name = MessageSendingConfig.name

urlpatterns = [
    path("main/", SampleView.as_view(), name="main"),
    path("create_addressee/", AddresseeCreateView.as_view(), name="addressee_create"),
    path("create_message/", MessageCreateView.as_view(), name="message_create"),
    path("create_mailing/", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "addressee/<int:pk>/update/",
        AddresseeUpdateView.as_view(),
        name="addressee_update",
    ),
    path("addressee_list/", AddresseeListView.as_view(), name="addressee_list"),
    path("addressee/<int:pk>", AddresseeDetailView.as_view(), name="addressee_detail"),
    path(
        "addressee/<int:pk>/delete/",
        AddresseeDeleteView.as_view(),
        name="addressee_delete",
    ),
    path(
        "message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"
    ),
    path("message_list/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>", MessageDetailView.as_view(), name="message_detail"),
    path(
        "message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path(
        "mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path("mailing_list/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/<int:pk>", MailingDetailView.as_view(), name="mailing_detail"),
    path(
        "mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path("log_list/", LogListView.as_view(), name="log_list"),
    path("mailing/<int:pk>/send/", mailing_send_view, name="mailing_send"),
    path(
        "mailing/<int:pk>/unacivate/",
        MailingStatusView.as_view(),
        name="mailing_unactivate",
    ),
]
