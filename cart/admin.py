from django.contrib import admin
from .models import Cart, CartItem, Transaction, WalletTransaction, NewsletterSubscription

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Transaction)
admin.site.register(WalletTransaction)
admin.site.register(NewsletterSubscription)