from django.shortcuts import render, redirect, get_object_or_404
from .forms import AdForm, ExchangeProposalForm
from django.contrib.auth.decorators import login_required
from .models import Ad, ExchangeProposal



# Create your views here.

def home(request):
    return render(request, 'ads/home.html')

def ads_list(request):
    ads = Ad.objects.all().order_by('-created_at')
    user_ads = Ad.objects.filter(user=request.user)
    return render(request, 'ads/ads_list.html', {'ads': ads, 'user_ads': user_ads})

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


@login_required
def create_proposal(request):
    ad_sender_id = request.GET.get('ad_sender')
    ad_receiver_id = request.GET.get('ad_receiver')

    ad_sender = get_object_or_404(Ad, id=ad_sender_id)
    ad_receiver = get_object_or_404(Ad, id=ad_receiver_id)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.sender = request.user
            proposal.ad_sender = ad_sender
            proposal.ad_receiver = ad_receiver
            proposal.status = 'pending'
            proposal.save()
            return redirect('ads_list')
    else:
        form = ExchangeProposalForm()

    return render(request, 'ads/create_proposal.html', {
        'form': form,
        'ad_sender': ad_sender,
        'ad_receiver': ad_receiver
    })


@login_required
def user_proposals(request):
    user = request.user
    user_ads = Ad.objects.filter(user=user)

    view_type = request.GET.get('type', 'all')

    if view_type == 'sent':
        proposals = ExchangeProposal.objects.filter(ad_sender__in=user_ads)
    elif view_type == 'received':
        proposals = ExchangeProposal.objects.filter(ad_receiver__in=user_ads)  
    else:
        sent = ExchangeProposal.objects.filter(ad_sender__in=user_ads)
        received = ExchangeProposal.objects.filter(ad_receiver__in=user_ads) 
        proposals = list(sent) + list(received)

    return render(request, 'ads/user_proposals.html', {'proposals': proposals, 'view_type': view_type})
