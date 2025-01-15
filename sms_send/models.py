from django.db import models

class SmsConfiguration(models.Model):
    username = models.CharField(max_length=100)
    account_sid = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=100)
    sender_number = models.CharField(max_length=20)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.sender_number})"

class SmsCompose(models.Model):
    body = models.TextField()
    sms_configuration = models.ForeignKey(SmsConfiguration, on_delete=models.SET_NULL, null=True, blank=True)
    recipient_number = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.recipient_number

STATUS_CHOICES = [
    ('success', 'Success'),
    ('failed', 'Failed'),
    ('pending', 'Pending'),
]

class Recipients(models.Model):
    phone_number = models.CharField(max_length=100)
    sms_compose = models.ForeignKey(SmsCompose, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    failed_reason = models.CharField(max_length=500, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.phone_number} - Status: {self.status}"



class SandBox(models.Model):
    sms_compose = models.ForeignKey(SmsCompose, on_delete=models.CASCADE)
    sender_number = models.CharField(max_length=100)
    recipient_number = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Sender: {self.sender_number} to Recipient: {self.recipient_number}"
