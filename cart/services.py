# services.py
import os
import shutil
import zipfile
import cloudinary
import cloudinary.uploader
import requests
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils import timezone
from .models import WalletTransaction, Transaction

def create_wallet_transactions_from_cart(cart):
    cart_items = cart.cartItems.all()
    for cart_item in cart_items:
        transaction = Transaction.objects.get(merchant_reference=str(cart.id))
        amount = cart_item.quantity * cart_item.photo.price
        WalletTransaction.objects.create(
            user=cart_item.photo.owner,
            cart=cart,
            cart_item=cart_item,
            transaction=transaction,
            amount=amount,
            created_at=timezone.now()
        )

# def download_and_email_images(cart):
#     # Create a temporary directory to store downloaded images
#     temp_dir = os.path.join(settings.BASE_DIR, 'temp_images')
#     os.makedirs(temp_dir, exist_ok=True)
#     timestamp = timezone.now()

#     cart_items = cart.cartItems.all()
#     # Iterate through cart items
#     for cart_item in cart_items:
#         # Download image from Cloudinary
#         image_url = cart_item.photo.image.url
#         image_name = f"{cart_item.photo.title}.jpg"  # Assuming images are JPEG format
#         image_path = os.path.join(temp_dir, image_name)
#         cloudinary.uploader.download(image_url, image_path)

#     # Create a zip file containing the downloaded images
#     zip_folder = f"PS-{timestamp}.zip"
#     zip_file_path = os.path.join(settings.BASE_DIR, zip_folder)
#     with zipfile.ZipFile(zip_file_path, 'w') as zipf:
#         for root, dirs, files in os.walk(temp_dir):
#             for file in files:
#                 zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

#     # Get user's email
#     user_email = cart.user.email

#     # Send email with zip file attachment
#     subject = 'Your images from Picha Safari are Here'
#     message = 'Please find attached the images from your shopping cart. Thank you for shopping with us.'
#     from_email = settings.DEFAULT_FROM_EMAIL
#     to_email = [user_email]
#     send_mail(subject, message, from_email, to_email, fail_silently=False, attachments=[(os.path.basename(zip_file_path), open(zip_file_path, 'rb').read())])

#     # Clean up temporary directory and zip file
#     shutil.rmtree(temp_dir)
#     os.remove(zip_file_path)


def download_and_email_images(cart):
    # Create a temporary directory to store downloaded images
    timestamp = str(timezone.now())
    temp_folder = f'PS-{timestamp}'
    temp_dir = os.path.join(settings.BASE_DIR, temp_folder)
    os.makedirs(temp_dir, exist_ok=True)

    # Iterate through cart items
    for cart_item in cart.cartItems.all():
        # Retrieve the Cloudinary URL of the image
        image_url = cart_item.photo.image.url

        # Download the image using requests
        response = requests.get(image_url)

        # Ensure the request was successful
        if response.status_code == 200:
            # Construct the filename for the downloaded image
            image_name = f"{cart_item.photo.title}.jpg"  # Assuming images are JPEG format
            image_path = os.path.join(temp_dir, image_name)

            # Save the image to the local filesystem
            with open(image_path, 'wb') as f:
                f.write(response.content)

    # Create a zip file containing the downloaded images
    timestamp = str(timezone.now())
    zip_folder = f'PS-{timestamp}-images.zip'
    zip_file_path = os.path.join(settings.BASE_DIR, zip_folder)
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

    # Get user's email
    user_email = cart.user.email

    # Send email with zip file attachment
    subject = f'Order Details - Picha safari cart #{cart.id}'
    message = f' Hi {cart.user.first_name}, Your images from Picha Safari are here!!! Please find attached the images from your shopping cart.'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user_email]

    # Create EmailMessage object with the zip file attached
    email = EmailMessage(subject, message, from_email, to_email)
    email.attach_file(zip_file_path)
    email.send()

    # Clean up temporary directory and zip file
    shutil.rmtree(temp_dir)
    os.remove(zip_file_path)