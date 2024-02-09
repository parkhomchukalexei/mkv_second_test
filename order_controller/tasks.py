from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils import timezone

from order_controller.models import Order


@shared_task
def send_order_email(order_id):

    order = Order.objects.get(id=order_id)
    html_content = render_to_string('order_email_template.html', {'order': order, 'slug': str(order.slug)})

    try:
        send_mail(
            f'Замовлення #{order.cell_id}',
            '',
            'probaby35@gmail.com',
            [order.user_email],
            html_message=html_content
        )
    except BadHeaderError:
        return 'Invalid header found.'
    except Exception as e:
        return f'An error occurred: {e}'
    else:
        return 'Email sent successfully.'



@shared_task
def send_rental_reminder_email():
    thirty_minutes_from_now = timezone.now() + timedelta(hours= 2, minutes=30)
    orders_to_remind = Order.objects.filter(end_timestamp__lte=thirty_minutes_from_now, reminded=False)

    for order in orders_to_remind:
        html_content = render_to_string('reminder_email_template.html', {'order': order, 'slug': str(order.slug)})
        send_mail(
            f'Заказ #{order.id}',
            '',
            'index@example.com',
            [order.user_email],
            html_message=html_content
        )
        order.reminded = True
        order.save()