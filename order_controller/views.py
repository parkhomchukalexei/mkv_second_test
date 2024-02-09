import json
from datetime import datetime, timezone, timedelta
from django.utils import timezone

import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from rest_framework import status
from rest_framework.views import Response, APIView

from order_controller.forms import OrderForm
from order_controller.models import Order
from order_controller.serializer import OrderSerializer


# Create your views here.

current_datetime = timezone.make_aware(datetime.now())

class OrderAPI(APIView):

    def post(self, request):

        start_timestamp = int(request.data['start_timestamp'])
        end_timestamp = int(request.data['end_timestamp'])

        user_data = json.loads(request.data['user_data'])

        start_datetime = convert_timestamp_to_datetime(start_timestamp)
        end_datetime = convert_timestamp_to_datetime(end_timestamp)

        data = {'start_timestamp': start_datetime, 'end_timestamp': end_datetime,
                'user_name':  user_data['name'],
                'user_email': user_data['email'],
                'cell_id': get_random_number()}

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            start_timestamp = serializer.validated_data['start_timestamp']
            end_timestamp = serializer.validated_data['end_timestamp']
            user_email = serializer.validated_data['user_email']
            user_name = serializer.validated_data['user_name']
            cell_id = serializer.validated_data['cell_id']

            if end_timestamp <= start_timestamp or end_timestamp - timedelta(hours=2) <= current_datetime:
                return Response({'error': 'Invalid end_timestamp'}, status=status.HTTP_400_BAD_REQUEST)

            if not serializer.validated_data['user_email']:
                return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            response = {
                "start_timestamp": start_timestamp - timedelta(hours=2),
                "end_timestamp": end_timestamp - timedelta(hours=2),
                "user_email": user_email,
                "user_name": user_name,
                "cell_id": cell_id
            }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderFormView(FormView):
    template_name = 'create_order.html'
    form_class = OrderForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        name = form.cleaned_data['name']
        start_date = form.cleaned_data['start_date'] + timedelta(hours=2)
        end_date = form.cleaned_data['end_date'] + timedelta(hours=2)

        data = {'start_timestamp': start_date, 'end_timestamp': end_date,
                'user_name': name, 'user_email': email, 'cell_id': get_random_number()}

        serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            start_timestamp = serializer.validated_data['start_timestamp']
            end_timestamp = serializer.validated_data['end_timestamp']

            if end_timestamp <= start_timestamp or end_timestamp - timedelta(hours=2) <= current_datetime:
                return Response({'error': 'Invalid end_timestamp'}, status=status.HTTP_400_BAD_REQUEST)

            if not serializer.validated_data['user_email']:
                return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            slug = serializer.instance.slug
            return redirect('order_detail_view', slug=slug)
        else:
            print(serializer.errors)

    def order_detail_view(request, slug):
        order = get_object_or_404(Order, slug=slug)

        return render(request, 'order_detail.html', {'order': order})


def get_random_number():
    try:
        url = 'https://csrng.net/csrng/csrng.php?min=1&max=50'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[0]['random']
    except requests.RequestException as e:
        print(f'An error occurred: {e}')
        return None
    except KeyError as e:
        print(f'Invalid JSON response: {e}')
        return None


def convert_timestamp_to_datetime(timestamp):
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return dt