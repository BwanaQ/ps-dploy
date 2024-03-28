from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Photo, Tag, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PhotoCreateForm, ApprovalForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

class PhotoListApprovalView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_list_approval.html'
    context_object_name = 'photos'
    
 


def photo_edit_approval(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    approval = photo.approval

    if request.method == 'POST':
        form = ApprovalForm(request.POST, instance=approval)
        if form.is_valid():
            approval = form.save(commit=False)
            approval.photo = photo
            approval.approved_by = request.user
            approval.save()
            messages.success(request, 'Approval updated successfully.')  # Add success message
            return redirect('photo_list_approval')
    else:
        form = ApprovalForm(instance=approval)
    return render(request, 'photo/approve_photo.html', {'form': form, 'photo': photo})

def photo_create_approval(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)

    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if form.is_valid():
            approval = form.save(commit=False)
            approval.photo = photo
            approval.approved_by = request.user
            approval.save()
            messages.success(request, 'Approval created successfully.')  # Add success message
            return redirect('photo_list_approval')
    else:
        form = ApprovalForm()
    return render(request, 'photo/approve_photo.html', {'form': form, 'photo': photo})


class PhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo_list.html'
    context_object_name = 'photos'
    
    def get_queryset(self):
        return Photo.objects.filter(owner=self.request.user)

class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photo/photo_detail.html'  
    context_object_name = 'photo'

class PhotoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Photo
    template_name = 'photo/photo_form.html'  
    fields = ['title', 'description', 'category', 'tags', 'image', 'price'] 
    success_url = reverse_lazy('photo_list')  
    success_message = "The Photo was created successfully!"
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        return response

class PhotoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Photo
    template_name = 'photo/photo_form.html'  
    fields = ['title', 'description', 'category', 'tags', 'price']
    success_url = reverse_lazy('photo_list')  
    success_message = "The Photo was updated successfully!"
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return response

class PhotoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Photo
    template_name = 'photo/photo_confirm_delete.html'  
    success_url = reverse_lazy('photo_list')  
    success_message = "The Photo was deleted successfully!"

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return response

# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.all()

class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'photo/category_detail.html'  
    context_object_name = 'category'

class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    template_name = 'photo/category_form.html'  
    fields = ['name'] 
    success_url = reverse_lazy('category_list')  
    success_message = "The Category was created successfully!"
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return response

class CategoryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    template_name = 'photo/category_form.html'  
    fields = ['name']
    success_url = reverse_lazy('category_list')  
    success_message = "The Category was updated successfully!"
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return response
    
class CategoryDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Category
    template_name = 'photo/category_confirm_delete.html'  
    success_url = reverse_lazy('category_list')  
    success_message = "The Category was deleted successfully!"

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return response


# Tag Views
class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'tag_list.html'
    context_object_name = 'tags'
    
    def get_queryset(self):
        return Tag.objects.all()

class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'photo/tag_detail.html'  
    context_object_name = 'tag'

class TagCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tag
    template_name = 'photo/tag_form.html'  
    fields = ['name'] 
    success_url = reverse_lazy('tag_list')  
    success_message = "The Tag was created successfully!"
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return response

class TagUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tag
    template_name = 'photo/tag_form.html'  
    fields = ['name']
    success_url = reverse_lazy('tag_list')  
    success_message = "The Tag was updated successfully!"
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return response
    
class TagDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Tag
    template_name = 'photo/tag_confirm_delete.html'  
    success_url = reverse_lazy('tag_list')  
    success_message = "The Tag was deleted successfully!"

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return response


