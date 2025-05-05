import stripe
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from task.api.view_sets import *
from utils.response import ResponseNotOk

router = DefaultRouter()

urlpatterns = router.urls


class CreateCheckoutApiView(APIView):
    def post(self, request, *args, **kwargs):
        domain_url = settings.FRONT_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                # success_url=domain_url + 'payment/success?session_id={CHECKOUT_SESSION_ID}',
                success_url=domain_url + 'payment/confirm?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'payment/failed?session_id={CHECKOUT_SESSION_ID}',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'quantity': 1,
                        "price_data": {
                            'currency': 'usd',
                            'unit_amount': 500,
                            "product_data": {
                                'name': 'T-shirt',
                                'description': 'Comfortable cotton t-shirt',
                            }
                        }
                    }
                ]
            )
            return JsonResponse({'session_id': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class ConfirmCheckoutApiView(APIView):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session_id = request.data.get('session_id')
        if not session_id:
            return ResponseNotOk(reason='session_id not provided')
        try:
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            if checkout_session.get('payment_status') == "paid":
                return ResponseOk()
            else:
                return ResponseNotOk(reason='payment_status: ' + checkout_session.get('payment_status'))
        except Exception as e:
            return JsonResponse({'error': str(e)})


urlpatterns += [
    path('payment/create-checkout-session/', CreateCheckoutApiView.as_view()),  # new
    path('payment/confirm/', ConfirmCheckoutApiView.as_view()),  # new
]
