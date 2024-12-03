from django.forms import ModelForm

from message_sending.models import Addressee, Mailing, Message


class AddresseeForm(ModelForm):
    class Meta:
        model = Addressee
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(AddresseeForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите Ф.И.О."}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите email"}
        )
        self.fields["comment"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Добавьте комментарий"}
        )


class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["subject"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите тему письма"}
        )
        self.fields["body"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите информацию"}
        )


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        exclude = (
            "start_mailing",
            "end_mailing",
            "status",
            "owner",
        )

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields["message"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберите сообщение"}
        )
        self.fields["addressee"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Добавьте получателей"}
        )
