from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"

class Template(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(help_text="Use {{name}} placeholder for personalization")

    def __str__(self):
        return self.title

class Campaign(models.Model):
    name = models.CharField(max_length=100)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SentEmail(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email to {self.contact.email} for {self.campaign.name}"
