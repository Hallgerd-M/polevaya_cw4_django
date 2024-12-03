from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from django.views.generic.edit import CreateView

from .forms import AddresseeForm, MailingForm, MessageForm
from .models import Addressee, Log, Mailing, Message
from .services.send_mail import EmailService


class AddresseeCreateView(LoginRequiredMixin, CreateView):
    model = Addressee
    form_class = AddresseeForm
    success_url = reverse_lazy("message_sending:addressee_list")

    def form_valid(self, form):
        addressee = form.save()
        user = self.request.user
        addressee.owner = user
        addressee.save()
        return super().form_valid(form)


class AddresseeUpdateView(LoginRequiredMixin, UpdateView):
    model = Addressee
    form_class = AddresseeForm
    success_url = reverse_lazy("message_sending:addressee_list")


@method_decorator(cache_page(60 * 15), name="dispatch")
class AddresseeListView(ListView):
    model = Addressee


@method_decorator(cache_page(60 * 15), name="dispatch")
class AddresseeDetailView(LoginRequiredMixin, DetailView):
    model = Addressee


class AddresseeDeleteView(LoginRequiredMixin, DeleteView):
    model = Addressee
    success_url = reverse_lazy("message_sending:addressee_list")


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("message_sending:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("message_sending:message_list")


@method_decorator(cache_page(60 * 15), name="dispatch")
class MessageListView(ListView):
    model = Message


@method_decorator(cache_page(60 * 15), name="dispatch")
class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("message_sending:message_list")


class MailingListView(ListView):
    model = Mailing
    template_name = "message_sending/mailing_list.html"


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("message_sending:mailing_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("message_sending:mailing_list")

    def post(self, request, *args, **kwargs):
        print(request.POST)
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class MailingDetailView(DetailView):
    model = Mailing


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("message_sending:mailing_list")


class LogListView(LoginRequiredMixin, ListView):
    model = Log


class SampleView(TemplateView):
    model = Mailing
    template_name = "message_sending/main.html"


def mailing_send_view(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    EmailService().send_message(pk)
    mailing.status = Mailing.COMPLETED
    mailing.save()
    return redirect(reverse("message_sending:mailing_list"))


class MailingStatusView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        if not request.user.has_perm("message_sending.can_change_status"):
            return HttpResponseForbidden("У вас нет прав для отключения рассылки.")

        mailing.is_active = False
        mailing.save()

        return redirect("message_sending:mailing_detail", pk=pk)
