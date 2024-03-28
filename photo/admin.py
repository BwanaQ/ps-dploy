from django.contrib import admin
from .models import Photo,Tag,Category, Approval
admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Approval)
