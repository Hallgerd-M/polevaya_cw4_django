from django import template

from message_sending.models import Addressee, Log, Mailing

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    else:
        return "#"


@register.simple_tag()
def count_all():
    mailings_count = Mailing.objects.all().count()
    return mailings_count


@register.simple_tag()
def count_active_mailings():
    active_mailings_count = Mailing.objects.filter(status="launched").count()
    return active_mailings_count


@register.simple_tag()
def count_unique_addressees():
    unique_addressees = Addressee.objects.all().count()
    return unique_addressees


@register.simple_tag()
def count_successfull_mailings():
    succesfull_mailings = Log.objects.filter(status="Successfully").count()
    return succesfull_mailings


@register.simple_tag()
def count_unsuccessfull_mailings():
    unsuccesfull_mailings = Log.objects.filter(status="Unsuccessfully").count()
    return unsuccesfull_mailings


@register.simple_tag()
def count_all_mailings():
    all_mailings = Log.objects.all().count()
    return all_mailings


@register.simple_tag()
def count_sent_mails():
    successfull_mailings = Log.objects.filter(status="Successfully")
    count = 0
    for log in successfull_mailings:
        mailing = log.mailing
        addressee = mailing.addressee.count()
        count += addressee
    return count
