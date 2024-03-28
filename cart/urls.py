from django.urls import path
from cart.views import home, index, add_to_cart, cart, checkout, remove_from_cart, process_paypal_payment, paypal_return , paypal_cancel, paymentIPN, callback, newsletter_signup
""",payment_checkout"""
urlpatterns = [
    path('', home, name='home'),
    path('shop/', index, name='cart-home'),
    path('add_to_cart', add_to_cart, name='add'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove'),
    path('cart', cart, name='cart'),

    path('checkout', checkout, name='checkout'),
    # path('payment', payment_checkout, name='payment'),

    path('payment/paypal', process_paypal_payment, name='process-paypal-payment'),
    path('payment/return_url', paypal_return, name='paypal-return'),
    path('payment/cancel_url', paypal_cancel, name='paypal-cancel'),
    path('pesapal/payment-ipn/', paymentIPN, name="payment-ipn"),
    path('pesapal/callback/', callback, name='callback'),
    path('newsletter/signup/', newsletter_signup, name='newsletter_signup'),

]