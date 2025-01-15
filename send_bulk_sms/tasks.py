from celery import shared_task
from twilio.rest import Client
from sms_send.models import Recipients, SandBox, SmsConfiguration, SmsCompose

# bind=True, max_retries=3, default_retry_delay=3

@shared_task
def send_sms_task(body, sender_number, recipient_number, sms_compose_id, config_id):
    try:
        sms_config = SmsConfiguration.objects.get(id=config_id)
        client = Client(sms_config.account_sid, sms_config.auth_token)

        # Send SMS using Twilio
        message = client.messages.create(
            body=body,
            from_=sender_number,
            to=recipient_number,
           
        )

        # Log success
        Recipients.objects.create(
            phone_number=recipient_number,
            sms_compose_id=sms_compose_id,
            status='success',
            failed_reason="None"
        )
        SandBox.objects.create(
            sms_compose_id=sms_compose_id,
            sender_number=sender_number,
            recipient_number=recipient_number
        )
        return  {"recipient_number": recipient_number, "status": "success", "sid": message.sid}

    except Exception as e:
        # Log failure
        Recipients.objects.create(
            phone_number=recipient_number,
            sms_compose_id=sms_compose_id,
            status='failed',
            failed_reason=str(e)
        )
        return {"recipient_number": recipient_number, "status": "failed", "reason": str(e)}


