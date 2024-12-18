from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import OrderSerializer
from orders.models import Order


class OrderRead(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/read.html'

    def get(self, request):
        orders = Order.objects.all()
        return Response({'orders': orders})


class OrderCreate(generics.CreateAPIView):
    serializer_class = OrderSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/create.html'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('orders:read')
        else:
            context = {'serializer': serializer}
            return Response(context, template_name=self.template_name)


class OrderEdit(generics.UpdateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/edit.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)
        return Response({'serializer': serializer, 'order': order})

    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('orders:read')
        else:
            context = {'serializer': serializer}
            return Response(context, template_name='orders/create.html')


class OrderDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        context = {'pk': pk}
        order.delete()
        return Response(context, template_name='orders/delete.html')
