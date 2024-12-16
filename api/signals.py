from django.db.models.signals import post_save
from robots.models import Robot
from django.dispatch import receiver
from django.core.mail import send_mail


@receiver(post_save, sender=Robot)
def send_order_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'R4C: новое поступление!'
        message = (
            f'Добрый день!'
            f'Недавно вы интересовались нашим роботом модели {instance.model},'
            f' версии {instance.version}. Этот робот теперь в наличии.'
            f' Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'
        )
        from_email = 'no-replay@r4c.com'
        recipient_list = ['belyashnikova.tn@gmail.com']
        send_mail(subject, message, from_email, recipient_list)
