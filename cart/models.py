import uuid
from django.db import models
from django.conf import settings
from photo.models import Photo
from decimal import Decimal, ROUND_HALF_UP

class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        total=0
        cart_items = self.cartItems.all()
        total = sum([item.price for item in cart_items])
        return (round(float(total),2))
    @property
    def vat(self):
        total=0
        cart_items = self.cartItems.all()
        total = sum([item.price for item in cart_items])
        vat = 0.16 * float(total)
        return (round(vat, 2))

    @property
    def final_price(self):
        total=0
        cart_items = self.cartItems.all()
        total = sum([item.price for item in cart_items])
        vat = 0.16 * float(total)
        final_price = float(total)+vat
        return (round(final_price,2))

    @property
    def tally(self):
        cart_items = self.cartItems.all()
        total = sum([item.quantity for item in cart_items])
        return total
class CartItem(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='Items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartItems')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.quantity} x {self.photo.title} in cart # {self.cart.id}" )

    @property
    def price(self):
        new_price = self.photo.price * self.quantity
        return new_price

class Transaction(models.Model):
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    confirmation_code = models.CharField(max_length=100, blank=True, null=True)
    payment_status_description = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    payment_account = models.CharField(max_length=100, blank=True, null=True)
    call_back_url = models.URLField(blank=True, null=True)
    status_code = models.IntegerField(blank=True, null=True)
    merchant_reference = models.CharField(max_length=100, blank=True, null=True)
    payment_status_code = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return str(f"{self.payment_status_description} {self.payment_method} {self.amount}")

class WalletTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(CartItem, null=True, blank=True, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def service_charge(self):
        service_charge = float(self.amount) * 0.15
        service_charge = Decimal(str(service_charge)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return service_charge

    @property
    def available_amount(self):
        available_amount = float(self.amount) - (float(self.amount) * 0.15)
        return available_amount

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email