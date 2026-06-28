from django.shortcuts import render,redirect
from .models import Contact
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('contact_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def contact_list(request):
    all_contacts = Contact.objects.filter(user=request.user)
    return render(request, 'contact/contact_list.html', {'contacts': all_contacts})

@login_required
def add_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        is_favourite = request.POST.get('is_favourite') == 'on'
        contact = Contact(name=name, email=email, phone=phone, address=address, is_favourite=is_favourite, user=request.user)
        contact.save()
        return render(request, 'contact/contact_list.html', {'contacts': Contact.objects.filter(user=request.user)})

@login_required
def get_contact(request,contact_id):
    contact = Contact.objects.get(id=contact_id, user=request.user)
    return render(request, 'contact/contact_detail.html', {'contact': contact})

def update_contact(request, contact_id):
    contact = Contact.objects.get(id=contact_id, user=request.user)
    if request.method == 'POST':
        contact.name = request.POST.get('name')
        contact.email = request.POST.get('email')
        contact.phone = request.POST.get('phone')
        contact.address = request.POST.get('address')
        contact.is_favourite = request.POST.get('is_favourite') == 'on'
        contact.save()
        return redirect('contact_list')
    return render(request, 'contact/contact_update.html', {'contact': contact})

def delete_contact(request,contact_id):
    contact = Contact.objects.get(id=contact_id, user=request.user)
    contact.delete()
    return redirect('contact_list')
