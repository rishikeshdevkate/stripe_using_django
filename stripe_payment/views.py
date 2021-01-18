import stripe
from django.conf import settings
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .models import PurchaseInfoModel
from .serializers import PurchaseInfoModelSerializer
from .utils import ResponseInfo

"""Setting up stripe secret kay"""
stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutAPiView(GenericAPIView):
    """
       Class for creating API view for Payment gateway Checkout.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = PurchaseInfoModelSerializer

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(CheckoutAPiView, self).__init__(**kwargs)

    def post(self, request, *args, **kwags):
        """
        Function for creating a charge.
        """
        print("reques",request.data)
        amount = request.data['amount']

        """Create a customer"""
        customer = stripe.Customer.create(
            email=request.data['stripeEmail'],
            source=request.data['stripeToken'],
        )

        """Create a Charge"""
        stripe.Charge.create(
            customer=customer.id,
            amount=str(amount) + '00',
            currency='inr',
            description='Payment Gateway',
        )
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["error"] = None
        self.response_format["message"] = "Payment completed successfully."
        return Response(self.response_format)


class WebHookApiView(GenericAPIView):
    """
           Class for creating API view for WebHook.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = PurchaseInfoModelSerializer

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(WebHookApiView, self).__init__(**kwargs)

    def post(self, request, *args, **kwags):
        """
            Function for WebHook
        """
        print("reee",request.data)
        payment_data = request.data.get('data')
        payment_object = payment_data.get('object')

        """Setting the transaction status"""
        if payment_object.get('balance_transaction'):
            pay_status = "S"
        else:
            pay_status = "F"

        """Customer payment info added"""
        PurchaseInfoModel.objects.create(customer_name=payment_object.get('billing_details').get('name'),
                                         email=payment_object.get('receipt_email'),
                                         total_amount=payment_object.get('amount')/100,
                                         transaction_id=payment_object.get('balance_transaction'),
                                         transaction_status=pay_status,
                                         address=payment_object.get('billing_details').get('address').get('line1'),
                                         country=payment_object.get('payment_method_details').get('card').get('country'),
                                         currency=payment_object.get('currency'),
                                         postal_code=payment_object.get('billing_details').get('address').get('postal_code'),
                                         receipt_url=payment_object.get('receipt_url'))

        return Response(self.response_format)



