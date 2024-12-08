from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.views import (PasswordResetConfirmView,
                                       PasswordResetView)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, UpdateView, View
from django.views.generic.edit import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import (UserForgotPasswordForm, UserForm,
                         UserRegistrationForm, UserSetNewPasswordForm)
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    @staticmethod
    def send_welcome_email(user_email):
        subject = f"Добро пожаловать, {user_email}!"
        message = "Спасибо, что зарегистрировались! Теперь Ваш аккаунт активирован"
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
        )


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("message_sending:main")
    permission_required = 'users.change_user'


@method_decorator(cache_page(60 * 15), name="dispatch")
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("message_sending:main")
    permission_required = 'users.change_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


@method_decorator(cache_page(60 * 15), name="dispatch")
class UserListView(ListView):
    model = User


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """

    form_class = UserForgotPasswordForm
    template_name = "users/user_password_reset.html"
    success_url = reverse_lazy("message_sending:main")
    success_message = (
        "Письмо с инструкцией по восстановлению пароля отправлена на ваш email"
    )
    subject_template_name = "users/email/password_subject_reset_mail.txt"
    email_template_name = "users/email/password_reset_mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Запрос на восстановление пароля"
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """

    form_class = UserSetNewPasswordForm
    template_name = "users/user_password_set_new.html"
    success_url = reverse_lazy("users:login")
    success_message = "Пароль успешно изменен. Можете авторизоваться на сайте."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Установить новый пароль"
        return context


class BlockUsersView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)

        if not request.user.has_perm("users.can_view_users"):
            return HttpResponseForbidden("У вас нет прав для блокировки пользователя.")

        user.is_active = False
        user.save()

        return redirect("users:user_detail", pk=pk)
