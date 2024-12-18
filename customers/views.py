from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CustomerSerializer

from customers.models import Customer



def render_html_response(context, template_name):
    """
    Render HTML response using the provided serializer and template name.
    """
    return Response(context, template_name=template_name)


class CustomerCreate(generics.ListAPIView):
    serializer_class = CustomerSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer_form.html'

    def post(self, request, *args, **kwargs):
        # message = "Congratulations! your contact has been added successfully."
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            # if request.accepted_renderer.format == 'html':
                # messages.success(request, message)
            return redirect('customers:read')

            # else:
            #     # Return JSON response with success message and serialized data
            #     return Response(
            #         status_code=status.HTTP_201_CREATED,
            #         message=message,
            #         data=serializer.data)
        else:
            # if request.accepted_renderer.format == 'html':
                # Render the HTML template with invalid serializer data
            context = {'serializer':serializer}
            return render_html_response(context, self.template_name)
            # else:   
            #     # Return JSON response with error message
            #     return Response(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         message="We apologize for the inconvenience, but please review the below information.",
            #         data=(serializer.errors))


# class CustomerCreate(generics.ListAPIView):
#     """
#     View to get the listing of all contacts.
#     Supports both HTML and JSON response formats.
#     """
#     serializer_class = CustomerSerializer
#     renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
#     template_name = 'customer_form.html'

#     def get(self, request, *args, **kwargs):
#         queryset = Customer.objects.all()

#         if request.accepted_renderer.format == 'html':
#             serializer = self.serializer_class()  # Create an instance of the serializer
#             context = {'customers': queryset, 'serializer': serializer}
#             return render_html_response(context, self.template_name)
#         else:
#             # Return a JSON response if the format is not HTML
#             serializer = self.serializer_class(queryset, many=True)
#             return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         """
#         Handle POST request to add or update a contact.
#         """
#         message = "Congratulations! your contact has been added successfully."
#         serializer = self.serializer_class(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()

#             if request.accepted_renderer.format == 'html':
#                 messages.success(request, message)
#                 return redirect('customers:read')

#             else:
#                 # Return JSON response with success message and serialized data
#                 return Response(
#                     status_code=status.HTTP_201_CREATED,
#                     message=message,
#                     data=serializer.data)
#         else:
#             # Invalid serializer data
#             if request.accepted_renderer.format == 'html':
#                 # Render the HTML template with invalid serializer data
#                 context = {'serializer':serializer}
#                 return render_html_response(context, self.template_name)
#             else:   
#                 # Return JSON response with error message
#                 return Response(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     message="We apologize for the inconvenience, but please review the below information.",
#                     data=(serializer.errors))
    
# class CustomerAdd(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'customer_form.html'

#     # def get(self, request):
#     #     customers = Customer.objects.all()
#     #     return Response({'customers': customers})

#     def post(self, request):
#         serializer = CustomerSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         customers = Customer.objects.all()
#         return Response({'customers': customers})
#         # return Response(serializer.data)


class CustomerRead(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer_list.html'

    def get(self, request):
        customers = Customer.objects.all()
        return Response({'customers': customers})

    # def post(self, request):
    #     serializer = CustomerSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'customer_list.html'

    # def get(self, request):
    #     queryset = Customer.objects.all()
    #     return Response({'customers': queryset})

    # def post(self, request):
    #     serializer = CustomerSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return redirect('customers:list')


class CustomerDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer_list.html'

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        # serializer = RobotPostSerializer(robot)
        # return Response({'serializer': serializer, 'robot': robot})
        return Response({'customer': Customer.objects.all()}, template_name='customer_list.html') 



class CustomerEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer_detail.html'
    # template_name = 'customer_form.html'

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer)
        return Response({'serializer': serializer, 'customer': customer})

    def post(self, request, pk=None):
        if pk:
            customer = get_object_or_404(Customer, pk=pk)
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return redirect('customers:read')
        else:
            serializer = CustomerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # return redirect('student_add')
        # customer = get_object_or_404(Customer, pk=pk)
        # serializer = CustomerSerializer(customer, data=request.data)
        # if not serializer.is_valid():
            # return Response({'serializer': serializer, 'customer': customer})
        # serializer.save()
        # return redirect('customers:list')