from django.db import models

from users.models import User


class Addressee(models.Model):
    email = models.CharField(
        max_length=100,
        verbose_name="E-mail адрес",
        help_text="Введите e-mail",
        unique=True,
    )
    name = models.CharField(
        max_length=150, verbose_name="Фамилия Имя Отчество", help_text="Введите Ф.И.О."
    )
    comment = models.TextField(
        null=True,
        blank=True,
        verbose_name="Комментарий",
        help_text="Введите комментарий",
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Введите владельца продукта",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "адресат"
        verbose_name_plural = "адресаты"
        ordering = ["email", "name"]
        permissions = [
            ("can_view_addressees", "Can view addressees"),
        ]


class Message(models.Model):
    subject = models.CharField(
        max_length=100, verbose_name="Тема письма", help_text="Введите тему письма"
    )
    body = models.TextField(verbose_name="Тело письма", help_text="Введите текст")
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Введите владельца продукта",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ["subject"]
        permissions = [
            ("can_view_messages", "Can view messages"),
        ]


class Mailing(models.Model):
    COMPLETED = "completed"
    CREATED = "created"
    LAUNCHED = "launched"

    STATUS_CHOISES = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (LAUNCHED, "Запущена"),
    ]

    start_mailing = models.DateField(auto_now_add=True)
    end_mailing = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOISES, default=CREATED, verbose_name="Статус"
    )
    message = models.ForeignKey(
        Message,
        verbose_name="Сообщение",
        help_text="Введите сообщение",
        on_delete=models.CASCADE,
    )
    addressee = models.ManyToManyField(
        Addressee,
        verbose_name="Получатель",
        help_text="Введите получателя",
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Введите владельца продукта",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Сообщение: {self.message.subject}"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["status"]
        permissions = [
            ("can_view_mailings", "Can view mailings"),
            ("can_change_status", "Can change status"),
        ]


class Log(models.Model):
    SUCCESSFULL = "Successfully"
    UNSUCCESSFULL = "Unsuccessfully"

    STATUS_CHOICES = [
        (SUCCESSFULL, "Успешно"),
        (UNSUCCESSFULL, "Не успешно"),
    ]

    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=UNSUCCESSFULL,
        verbose_name="Статус",
    )
    answer = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(
        Mailing, verbose_name="Рассылка", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Статус попытки рассылки: {self.status}"

    class Meta:
        verbose_name = "попытка"
        verbose_name_plural = "попытки"
        ordering = ["status"]
