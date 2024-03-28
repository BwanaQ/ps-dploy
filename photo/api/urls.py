from django.urls import path

from photo.api.views import PhototList, PhotoDetail 

urlpatterns = [
    path("photos/", PhototList.as_view(), name="api-photo-list"),
    path("photos/<int:pk>/", PhotoDetail.as_view(), name="api-photo-detail"),
]