from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Contact, Template, Campaign, SentEmail

def dashboard(request):
    campaigns = Campaign.objects.all().order_by('-created_at')
    return render(request, "campaigns/dashboard.html", {"campaigns": campaigns})

def contacts(request):
    if request.method == "POST":
        Contact.objects.create(name=request.POST['name'], email=request.POST['email'])
        return redirect('contacts')
    all_contacts = Contact.objects.all()
    return render(request, "campaigns/contacts.html", {"contacts": all_contacts})

def templates_view(request):
    if request.method == "POST":
        Template.objects.create(title=request.POST['title'], content=request.POST['content'])
        return redirect('templates')
    all_templates = Template.objects.all()
    return render(request, "campaigns/templates.html", {"templates": all_templates})

def campaigns_view(request):
    if request.method == "POST":
        template = Template.objects.get(id=request.POST['template'])
        Campaign.objects.create(name=request.POST['name'], template=template)
        return redirect('campaigns')
    all_campaigns = Campaign.objects.all()
    all_templates = Template.objects.all()
    return render(request, "campaigns/campaigns.html", {"campaigns": all_campaigns, "templates": all_templates})

def run_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    contacts = Contact.objects.all()

    for contact in contacts:
        personalized_content = campaign.template.content.replace("{{name}}", contact.name)
        SentEmail.objects.create(campaign=campaign, contact=contact, sent_at=timezone.now())
        print(f"[SIMULATED SEND] To: {contact.email}\n{personalized_content}\n")

    return redirect('dashboard')
