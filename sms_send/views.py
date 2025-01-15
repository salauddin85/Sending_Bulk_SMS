from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from twilio.rest import Client
from django.db import transaction
# from send_bulk_sms.tasks import send_sms_task

class SmsConfigurationView(APIView):
    def post(self, request):
        
        data = request.data
        print("Received data:", data) 

        serializer = SmsConfigurationSerializer(data=data)
        if serializer.is_valid():
            sms_config = serializer.save()
            return Response({
                "status": "success",
                "details": "Successfully added Twilio Configuration",
                "username": sms_config.username,
                "sms_config_id": sms_config.id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "failed",
                "errors": [serializer.errors]
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        all_configurations = SmsConfiguration.objects.all()
        serializer = SmsConfigurationSerializerForview(
            all_configurations, many=True)
        return Response(serializer.data)

        


class SmsComposeView(APIView):
    def post(self, request):
        print("Printing something")
        print(request.data)
        data = request.data
        body = data.get("body")
        config_id = data.get("config_id")
        recipients = data.get("recipients", None)

        print("data",data)
        # return Response("Ok")
        if not isinstance(recipients,list) or not recipients:
            return Response({
               "status": "failed",
                "message": "Recipients must be a non-empty list."
            },status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            sms_config=SmsConfiguration.objects.get(id=config_id)
        except SmsConfiguration.DoesNotExist:
            return Response({
                'status':"failed",
                "message":"Invalid Sms configaration id"
            },status=status.HTTP_404_NOT_FOUND)
        
        sms_compose = SmsCompose.objects.create(
            body=body,
            sms_configuration=sms_config,
            recipient_number=", ".join(recipients)
        )
        client = Client(sms_config.account_sid, sms_config.auth_token)

        response_data = []

        for recipient_number in recipients:
            try:
                # Send SMS using Twilio
                message = client.messages.create(
                    body=body,
                    from_=sms_config.sender_number,
                    to=recipient_number
                )

                recipient = Recipients.objects.create(
                    phone_number=recipient_number,
                    sms_compose=sms_compose,
                    status='success',
                    failed_reason="None"
                )

                SandBox.objects.create(
                    sms_compose=sms_compose,
                    sender_number=sms_config.sender_number,
                    recipient_number=recipient_number
                )

                response_data.append({
                    "recipient_number": recipient_number,
                    "status": "success",
                    "sid": message.sid
                })

            except Exception as e:
                Recipients.objects.create(
                    phone_number=recipient_number,
                    sms_compose=sms_compose,
                    status='failed',
                    failed_reason=str(e)
                )

                response_data.append({
                    "recipient_number": recipient_number,
                    "status": "failed",
                    "reason": str(e)
                })

        return Response({
            "status": "completed",
            "sms_compose_id": sms_compose.id,
            "recipients": response_data
        }, status=status.HTTP_201_CREATED)
    
    
    def get(self, request):
        sms_compose = SmsCompose.objects.all()
        serializer_data = SmsComposeSerializerForView(sms_compose, many=True).data
        return Response({
            "status": "success",
            "details": serializer_data  
        },status=status.HTTP_200_OK)
        

class SandboxView(APIView):
    def get (self,request):
        sandbox=SandBox.objects.all()
        serializer=SandboxSerializer(sandbox,many=True).data
        return Response({
            "status":"success",
            "details":serializer
        })
        

class RecipentsView(APIView):
    def get (self,request):
        recipents=Recipients.objects.all()
        serializer=RecipientsSerializer(recipents,many=True).data
        return Response({
            "status":"success",
            "details":serializer
        })



# class SmsComposeView(APIView):
#     def post(self, request):
#         data = request.data
#         body = data.get("body")
#         config_id = data.get("config_id")
#         recipients = data.get("recipients", None)

#         if not isinstance(recipients, list) or not recipients:
#             return Response({
#                 "status": "failed",
#                 "message": "Recipients must be a non-empty list."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             sms_config = SmsConfiguration.objects.get(id=config_id)
#         except SmsConfiguration.DoesNotExist:
#             return Response({
#                 "status": "failed",
#                 "message": "Invalid SMS configuration ID."
#             }, status=status.HTTP_404_NOT_FOUND)

#         # Create SmsCompose object
#         sms_compose = SmsCompose.objects.create(
#             body=body,
#             sms_configuration=sms_config,
#             recipient_number=", ".join(recipients)
#         )

#         # Asynchronously send SMS to each recipient
#         for recipient_number in recipients:
#             send_sms_task.delay(
#                 body=body,
#                 sender_number=sms_config.sender_number,
#                 recipient_number=recipient_number,
#                 sms_compose_id=sms_compose.id,
#                 config_id=sms_config.id
#             )

#         return Response({
#             "status": "processing",
#             "sms_compose_id": sms_compose.id,
#             "message": "SMS sending tasks have been queued."
#         }, status=status.HTTP_202_ACCEPTED)

#     def get(self, request):
#         sms_compose = SmsCompose.objects.all()
#         serializer_data = SmsComposeSerializerForView(sms_compose, many=True).data
#         return Response({
#             "status": "success",
#             "details": serializer_data
#         }, status=status.HTTP_200_OK)
