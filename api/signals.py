from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def send_order_notification(instance, **kwargs):
    """
    Сигнал при сохранении робота (post + put + patch):
    если в заказах есть такие роботы, то делаем рассылку.
    """
    if recipient_list := Order.objects.filter(
                robot_serial=instance.serial).distinct().values_list(
                'customer__email', flat=True):
        subject = f'Something new in R4C: {instance.serial}'
        message = render_to_string('new_robot.html', {'robot': instance})
        mail = EmailMessage(
            subject=subject,
            body=message,
            from_email='no-replay@r4c.com',
        )
        mail.content_subtype = 'html'

        for client in recipient_list:
            mail.to = [client]
            mail.send()
