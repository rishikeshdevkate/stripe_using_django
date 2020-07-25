import stripe

from django.conf import settings
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
stripe.api_key = settings.STRIPE_SECRET_KEY


class HomePageView(GenericAPIView):

    temp = '200'
    pay = temp
    template_name = 'home.html'

    def get(self, request, *args, **kwags):
        print("dataa",request.data.get('data'))
        return render(request, 'home.html', context={
            'temp': self.temp,
            'pay': self.pay,
            'key': settings.STRIPE_PUBLISHABLE_KEY
        })


def charge(request):
    temp = '200'
    print("dataa123", request.POST)

    if request.method == 'POST':
        customer = stripe.Customer.create(
            email=request.POST['stripeEmail'],
            source=request.POST['stripeToken'],
        )
        stripe.Charge.create(
            customer=customer.id,
            amount=temp,
            currency='inr',
            description='Inked Soul Payment Gateway',
        )

    return render(request, 'charge.html', {'temp': temp})
