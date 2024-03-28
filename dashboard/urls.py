from django.urls import path
from .views import home_view
from photo.views import PhotoListView, PhotoDetailView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView, PhotoListApprovalView
from photo.views import TagListView, TagDetailView, TagCreateView, TagUpdateView, TagDeleteView
from photo.views import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, photo_edit_approval, photo_create_approval
from cart.views import TransactionListView, transaction_detail_view, WalletTransactionListView

urlpatterns = [
    path('', home_view, name='dashboard-home'),
    path('photos/', PhotoListView.as_view(), name='photo_list'),
    path('photos/approvals/', PhotoListApprovalView.as_view(), name='photo_list_approval'),
    path('photos/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photos/add/', PhotoCreateView.as_view(), name='photo_create'),
    path('photos/<int:pk>/edit/', PhotoUpdateView.as_view(), name='photo_edit'),
    path('photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
   
    path('photo/<int:photo_id>/approve/', photo_create_approval, name='photo_create_approval'),
    path('photo/<int:photo_id>/approve/edit/', photo_edit_approval, name='photo_edit_approval'),

    # category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    # tag URLs
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/<int:pk>/', TagDetailView.as_view(), name='tag_detail'),
    path('tags/add/', TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:pk>/edit/', TagUpdateView.as_view(), name='tag_edit'),
    path('tags/<int:pk>/delete/', TagDeleteView.as_view(), name='tag_delete'),
    #transaction URLs
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/<str:merchant_reference>/', transaction_detail_view, name='transaction_detail'),
    # Wallet Transactions
    path('wallet-transactions/', WalletTransactionListView.as_view(), name='wallet_transactions'),

]