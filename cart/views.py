from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum, F
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from decouple import config



from photo.models import Photo, Category, Tag
from .models import Cart, CartItem, Transaction, WalletTransaction
from .utils import PesaPalGateway
from .services import create_wallet_transactions_from_cart, download_and_email_images

import json
from paypal.standard.forms import PayPalPaymentsForm
import openpyxl as openpyxl
import time
import traceback
import uuid
import re
import requests

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .decorators import superuser_required
from .forms import NewsletterForm
from .models import NewsletterSubscription



payment_url = config("PESAPAL_PAYMENT_URL")
gateway = PesaPalGateway()



class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction_list.html'
    context_object_name = 'transactions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Pass the user object to the template context
        return context

    def get_queryset(self):
        return Transaction.objects.filter(payment_status_description="Completed")

def transaction_detail_view(request, merchant_reference):
    uuid_merchant_reference = uuid.UUID(merchant_reference)
    transaction = get_object_or_404(Transaction, merchant_reference=merchant_reference,payment_status_description="Completed")
    cart = get_object_or_404(Cart, id=uuid_merchant_reference)
    cart_items = cart.cartItems.all()
    context = {
        'transaction': transaction,
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/transaction_detail.html', context)


class WalletTransactionListView(LoginRequiredMixin, ListView):
    model = WalletTransaction
    template_name = 'cart/wallet_transaction_list.html'  # Update with your template name
    context_object_name = 'wallet_transactions'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            # Superadmins can see all wallet transactions
            return queryset.all()
        else:
            # Other users can only see their own wallet transactions
            return queryset.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Fetch wallet transactions queryset
        wallet_transactions = self.get_queryset()

        # Calculate total quantity
        if user.is_superuser:
            total_quantity = wallet_transactions.aggregate(total_quantity=Sum('cart_item__quantity'))['total_quantity'] or 0
        else:
            total_quantity = wallet_transactions.filter(user=user).aggregate(total_quantity=Sum('cart_item__quantity'))['total_quantity'] or 0

        # Calculate total amount
        total_amount = wallet_transactions.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        # Calculate total service charge and available amount
        total_service_charge = sum(transaction.service_charge for transaction in wallet_transactions)
        total_available_amount = total_amount - total_service_charge

        # Assign totals to context
        context['total_quantity'] = total_quantity
        context['total_amount'] = total_amount
        context['total_service_charge'] = total_service_charge
        context['total_available_amount'] = total_available_amount

        return context
# def my_transactions(request):
#     cart = Cart.objects
#     transactions = Transaction.objects



def home(request):
    if request.user.is_authenticated:
        return redirect('cart-home') 
    approved_photos = Photo.objects.filter(approval__is_approved=True)
    paginator = Paginator(approved_photos, 9)
    page_number = request.GET.get('page')
    try:
        photos = paginator.page(page_number)
    except PageNotAnInteger:
        photos=paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)


    tags = Tag.objects.all()
    categories = Category.objects.all()
    context = {"photos": photos, "tags": tags, "categories": categories}
    return render (request, "cart/home.html", context)
@login_required(login_url='login')
def index(request):
    approved_photos = Photo.objects.filter(approval__is_approved=True)
    paginator = Paginator(approved_photos, 9)
    page_number = request.GET.get('page')
    try:
        photos = paginator.page(page_number)
    except PageNotAnInteger:
        photos=paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)


    tags = Tag.objects.all()
    categories = Category.objects.all()
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    cart_items = cart.cartItems.all()
    context = {"photos": photos, "cart":cart, "cart_items":cart_items, "tags": tags, "categories": categories}
    return render (request, "cart/photo_list.html", context)

@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        cart = None
        cart_items = []
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cart_items = cart.cartItems.all()

    context = {"cart": cart, "items": cart_items}
    return render (request, "cart/cart.html", context)

@login_required(login_url='login')
def add_to_cart(request):
    response_data = {}
    data = json.loads(request.body)
    product_id = data["id"]
    product = Photo.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

        # Check if the item already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, photo=product)
        if not created:
            # If the item already exists, just increment the quantity
            cart_item.quantity += 1
            cart_item.save()

        tally = cart.tally
        cart_items = list(cart.cartItems.all().values())  # Convert QuerySet to a list of dictionaries
        response_data = {"tally": tally, "cart_items": cart_items}

        # Send success message to the client
        success_message = f"{product.title} was added to cart successfully!"
        response_data["success_message"] = success_message

    return JsonResponse(response_data, safe=False)

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    try:
        cart = Cart.objects.get(user=request.user, completed=False)
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
        cart_item.delete()
        messages.success(request,"Item removed from cart successfully.")
        if 'HTTP_REFERER' in request.META:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return redirect("cart-home")
    except Cart.DoesNotExist:
        messages.error(request,"Cart Does not Exist.")

        return redirect("cart-home")
    except CartItem.DoesNotExist:
        messages.error(request,"Cart Item Does not Exist.")

        return redirect("cart-home")

@login_required(login_url='login')
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    cart_items = cart.cartItems.all()
    phone_number = request.user.phone_number
    pattern = re.compile(r'(\d{3})(\d+)(\d{2})')
    reduced_number = pattern.sub(r'\1xxxxx\3', phone_number)
    print(f"!!!!!!!!!!!CART PRICE!!!!!!!!!!!!!!!! = {round(cart.final_price, 2)}")
    if request.method == 'POST':
        cart_id = str(cart.id)
        phonenumber = phone_number
        email = request.user.email
        amount = round(cart.final_price, 2)
        currency = "KES"
        callback_url = "https://www.pichasafari.co.ke/pesapal/callback" #Edit Accordingly

        try:
            res = gateway.make_payment(cart_id, phonenumber, email, amount, currency, callback_url)
            print(res)
            redirect_url = res['redirect_url']
            return redirect(redirect_url)

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return HttpResponse(error_message)

    context = {"cart":cart, "cart_items":cart_items, "reduced_number":reduced_number}
    return render (request, "cart/checkout.html", context)

@login_required(login_url='login')
def process_paypal_payment(request):
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    cart_items = cart.cartItems.all()
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': f'{cart.final_price}',
        'item_name': f'Order # {cart.id}',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("paypal-return")}',
        'cancel_url': f'http://{host}{reverse("paypal-cancel")}',
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'cart':cart,'cart_items':cart_items,'paypal_dict':paypal_dict,'form':form}
    return render(request,'cart/process_paypal_payment.html', context)

@csrf_exempt
def paypal_return(request):
    cart = Cart.objects.filter(user=request.user, completed=False).first()
    if cart:
        cart.completed = True
        cart.save()

    messages.success(request,"Payment was successfull.")
    return redirect("cart-home")

@csrf_exempt
def paypal_cancel(request):
    messages.error(request,"Failed! Payment was cancelled.")
    return redirect("cart-home")


def paymentIPN(request):
    orderTrackingId = request.GET.get("OrderTrackingId")
    orderMerchantReference = request.GET.get("OrderMerchantReference")
    orderNotificationType = request.GET.get("OrderNotificationType")


    payment_url = f"https://cybqa.pesapal.com/pesapalv3/api/Transactions/GetTransactionStatus?orderTrackingId={orderTrackingId}"

    token = gateway.getAuthorizationToken()

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % token,
        "Accepts": "application/json"
    }
    response = requests.get(payment_url, headers=headers)

    if response.status_code == 200:
        transaction_status = response.json()

        # Extract transaction data from response
        payment_method = transaction_status.get('payment_method')
        amount = transaction_status.get('amount')
        created_date = transaction_status.get('created_date')
        confirmation_code = transaction_status.get('confirmation_code')
        payment_status_description = transaction_status.get('payment_status_description')
        description = transaction_status.get('description')
        message = transaction_status.get('message')
        payment_account = transaction_status.get('payment_account')
        call_back_url = transaction_status.get('call_back_url')
        status_code = transaction_status.get('status_code')
        merchant_reference = transaction_status.get('merchant_reference')
        payment_status_code = transaction_status.get('payment_status_code')
        currency = transaction_status.get('currency')

        # Create transaction object and associate it with the cart
        transaction = Transaction.objects.create(
            payment_method=payment_method,
            amount=amount,
            created_date=created_date,
            confirmation_code=confirmation_code,
            payment_status_description=payment_status_description,
            description=description,
            message=message,
            payment_account=payment_account,
            call_back_url=call_back_url,
            status_code=status_code,
            merchant_reference=merchant_reference,
            payment_status_code=payment_status_code,
            currency=currency
        )



        return JsonResponse(response.json())
    else:
        return JsonResponse({'error': 'Failed to retrieve transaction status'}, status=400)


def callback(request):

    cart = Cart.objects.filter(user=request.user, completed=False).first()
    if cart:
        cart.completed = True
        cart.save()
    create_wallet_transactions_from_cart(cart)
    download_and_email_images(cart)
    messages.success(request,"Payment was successfull.")
    return redirect("cart-home")

def newsletter_signup(request):
    form = NewsletterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if the email is already subscribed
            if NewsletterSubscription.objects.filter(email=email).exists():
                # If already subscribed, you can handle this case
                # Redirect to a thank you page or display a message
                messages.info(request,"You are already Subscribed to our newsletter!.")
                return redirect('cart-home')
            else:
                # If not subscribed, create a new subscription
                subscription = NewsletterSubscription.objects.create(email=email)
                # Optionally, you can send a confirmation email here
                # Redirect to a thank you page or the homepage
                messages.success(request,"You are now subscribed to our newsletter.")
                return HttpResponseRedirect('cart-home')
    return render(request, 'cart/_base.html', {'form': form})



# @require_POST
# def ajax_search(request):
#     search_query = request.POST.get('search', '')
#     # Perform search query based on user input
#     results = Photo.objects.filter(name__icontains=search_query)
#     # Serialize the queryset to JSON
#     data = [{'title': photo.title,'description':photo.description, 'category':photo.category, 'tags': photo.tags, 'webp_image':photo.webp_image,'price': photo.price, 'owner':photo.owner} for photo in results]
#     return JsonResponse(data, safe=False)