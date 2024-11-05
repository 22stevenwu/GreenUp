from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse

from .forms import UserProfileForm, CampaignForm
from .models import User, Campaign

@login_required 
def get_user(request):
  return User.objects.filter(email=request.user.email).first()

@login_required 
def supervisor_check(request):
  user = get_user(request)
  if user is None or not user.supervisor:
    return redirect('supervisor_alert')  

  return None

def supervisor_alert(request):
  return render(request, 'supervisor_alert.html')

def logout_view(request):
  logout(request)
  return redirect("home")

def home_view(request):
  return render(request, 'home.html')

def actions_view(request):
  return render(request, 'actions.html')

def rewards_view(request):
  return render(request, 'rewards.html')


def profile_view(request):
  user = get_object_or_404(User, email=request.user.email)
  context = {
        'user': user
  }
  return render(request, 'profile.html', context)

def profile_create_view(request):
  email = request.user.email

  if request.method == 'POST':
    form = UserProfileForm(request.POST)

    if form.is_valid():
      profile = form.save(commit=False)
      profile.email = email
      profile.profile_completed = True
      profile.save() 
      return redirect('profile') 
  else:
    form = UserProfileForm(initial={'email': email})

    context = {
      'form': form
    }
    return render(request, "profile_create.html", context)

def check(request):
    google_email = request.user.email

    if User.objects.filter(email=google_email).exists():
        return redirect('profile')  
    else:
        return redirect('profile_create')  

@login_required
def campaign_list_view(request):
  current_date = timezone.now().date()

  user = get_user(request)

  expired_campaigns = Campaign.objects.filter(enddate__lt=current_date)
  active_campaigns = Campaign.objects.filter(enddate__gte=current_date)

  return render(request, 'campaign_list.html', {
    'user': user,
    'expired_campaigns': expired_campaigns,
    'active_campaigns': active_campaigns
  })

def create_campaign(request):
    if supervisor_check(request):
      return supervisor_check(request)
    
    user = get_user(request)

    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('campaign_list') 
    else:
        form = CampaignForm()

    return render(request, 'campaign_create.html', {
        'form': form,
        'user': user 
    })

@login_required
def complete_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    user = get_user(request)

    if campaign not in user.completed_campaigns.all():
        user.completed_campaigns.add(campaign)
        user.update_points()
        user.save()
        return redirect('campaign_list')
    else:
        messages.info(request, f"Error: Campaign '{campaign.name}' is already completed.")

@login_required
def campaign_detail(request, campaign_id):
    # Retrieve the specific campaign
    campaign = get_object_or_404(Campaign, id=campaign_id)
    
    # Collect participating users and their details
    participating_users = []
    non_supervisor_users = User.objects.filter(supervisor=False)

    for user in non_supervisor_users:
        if campaign in user.completed_campaigns.all():
            # Collect participation details
            participation = {
                'name': user.name,  # Adjust 'name' if User model has a different field for names
                'day': timezone.now().date(),  # Replace with actual participation date if tracked
                'time': timezone.now().time(),  # Replace with actual participation time if tracked
                'location': campaign.location,  # Assumes Campaign model has a 'location' field
                'points': user.total_points,  # Adjust if points are tracked differently
            }
            participating_users.append(participation)
    
    # Render the campaign detail template with campaign and participating users
    return render(request, 'campaign_detail.html', {
        'campaign': campaign,
        'participating_users': participating_users,
    })


def landing_view(request):
    top_users = User.objects.order_by('-total_points')[:5]
    
    return render(request, 'landing.html', {'top_users': top_users})