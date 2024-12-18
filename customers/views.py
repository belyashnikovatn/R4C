from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CustomerSerializer
from customers.models import Customer


class CustomerRead(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customers/read.html'

    def get(self, request):
        customers = Customer.objects.all()
        return Response({'customers': customers})


class CustomerCreate(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customers/create.html'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('customers:read')
        else:
            context = {'serializer': serializer}
            return Response(context, template_name=self.template_name)


class CustomerEdit(generics.UpdateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customers/edit.html'

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer)
        return Response({'serializer': serializer, 'customer': customer})

    def post(self, request, pk, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('customers:read')
        else:
            context = {'serializer': serializer}
            return Response(context, template_name='customers/create.html')


class CustomerDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        context = {'pk': pk}
        customer.delete()
        return Response(context, template_name='customers/delete.html')
