from django.shortcuts import render, redirect
from .forms import AdForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'ads/home.html')

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


def ad_success(request):
    return render(request, 'ads/success.html')


