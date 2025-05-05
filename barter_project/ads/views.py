from django.shortcuts import render, redirect, get_object_or_404
from .forms import AdForm
from django.contrib.auth.decorators import login_required
from .models import Ad


# Create your views here.

def home(request):
    return render(request, 'ads/home.html')

def ads_list(request):
    ads = Ad.objects.all().order_by('-created_at')
    return render(request, 'ads/ads_list.html', {'ads': ads})

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_success')
    else:
        form = AdForm()
    
    return render(request, 'ads/create_ad.html', {'form': form})

def update_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return render(request, 'ads/permission_denied.html')
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ads_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/update_ad.html', {'form': form})

def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return render(request, 'ads/permission_denied.html')
    
    if request.method == 'POST':
        ad.delete()
        return redirect('ads_list')
    
    return render(request, 'ads/delete_ad.html', {'ad': ad})

def ad_success(request):
    return render(request, 'ads/success.html')


