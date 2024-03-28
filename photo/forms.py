from django import forms
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField, CheckboxSelectMultiple

from .models import Photo, Tag, Category, Approval

class PhotoCreateForm(ModelForm):
    class Meta:
        model = Photo
        exclude = ['owner','webp_image']

class TagCreateForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class CategoryCreateForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ApprovalForm(ModelForm):
    class Meta:
        model = Approval
        exclude=['photo', 'approved_by', 'approved_time']
        fields = ['is_approved', 'comments']  