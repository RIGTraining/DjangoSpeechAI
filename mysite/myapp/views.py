from django.shortcuts import render,redirect
from django.http import JsonResponse
from google import genai
import speech_recognition as sr
from .models import *
# Create your views here.
def homepage(request):
    chat_data = Chat.objects.all()
    return render(request, 'index.html', {'chat_data':chat_data})

def getsms(request):
    sms = request.GET['msg']
    client = genai.Client(api_key="AIzaSyBvTIhZ0ZfUn8-gIAddFchtyx-tvB5YkGY")

    response = client.models.generate_content(
    model="gemini-2.0-flash", contents=sms
    )
    
    print(response.text)
    chat = Chat.objects.create(question= sms, answer=response.text)
    return JsonResponse({'status':'success', 'answer':response.text})

def getvoice(request):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")
        try:
            print("Text: "+r.recognize_google(audio_text))
            sms = r.recognize_google(audio_text)
            # client = genai.Client(api_key="AIzaSyBvTIhZ0ZfUn8-gIAddFchtyx-tvB5YkGY")
            # response = client.models.generate_content(model="gemini-2.0-flash", contents=sms)
            # chat = Chat.objects.create(question= sms, answer=response.text)
            # print('success') 
            return JsonResponse({'sms':sms})           
            
        except:
            print("Sorry, I did not get that")
    return JsonResponse({'status':'success'})