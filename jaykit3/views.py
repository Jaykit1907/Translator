from django.shortcuts import render,redirect
from googletrans import Translator,LANGUAGES
from playsound import playsound
from gtts import gTTS
import os
import speech_recognition
import mysql.connector


final_result=''
def home(request):
    langguage=LANGUAGES
    
    try:
        if request.method=="POST":
            text1=request.POST['textarea1']
            lan=request.POST["selected_language"]
            if 'resultbtn' in request.POST:
                print("hii")
                result=Translator().translate(text1,src='en',dest=lan)
                final_result=result.text
                return render(request,"index.html",{"final_result":final_result,"text1":text1,"language":langguage})
            
            if 'speakbtn' in request.POST:
                print("Hellow")
                
                result=Translator().translate(text1,src='en',dest=lan)
                final_result=result.text
                audio_sound=gTTS(final_result,lang='en')
                audio_sound.save("voice.mp3")
                playsound("voice.mp3")
                os.remove("voice.mp3")
                return render(request,"index.html",{"final_result":final_result,"text1":text1,"language":langguage})

            
        
        
    except Exception as e:
        print(e)
        
            
            
    
    return render(request,"index.html",{"language":langguage})

def speak(request):
    language=LANGUAGES
    
    try:
        if request.method=="POST":
            sel1=request.POST["select1"]
            sel2=request.POST["select2"]
            
            recognizer=speech_recognition.Recognizer()
            with speech_recognition.Microphone() as source:
                
                print("Speak Anything :")
                audio=recognizer.listen(source)
                text=recognizer.recognize_google(audio,language=sel1)

                print(text)
            
                
                result=Translator().translate(text,dest=sel2)
                final_result=result.text
                print(final_result)
                pron=str(result.pronunciation)
                
                if pron=="None":
                    pron=final_result
                
                
                a=gTTS(final_result,lang=sel2)
                a.save("voice.mp3")
                playsound("voice.mp3")
                os.remove("voice.mp3")
            return render(request,'speak.html',{"language":language,"final_result":final_result,"text1":text,"pron":pron})
        
    except Exception as e:
        print(e)
        print(type(e))

    
        return render(request,'speak.html',{"error1":f"Network error:{e}"})
    
    return render(request,'speak.html',{'language':language})


def signup(request):
    
    try:
        if request.method=="POST":
            fname1=request.POST['fname']
            lname1=request.POST['lname']
            phone1=request.POST['phone']
            email1=request.POST['email']
            password1=request.POST['password']
            connection=mysql.connector.connect(host='localhost',user='root',database='jaykit4',password='pass123')
        
            con=connection.cursor()
            con.execute("insert into signup values (%s,%s,%s,%s,%s)",(fname1,lname1,phone1,email1,password1))
            connection.commit()
            print("data inserted")
            return redirect("/login/")
        
    except Exception as e:
        print(e)
        print("except block executed")
        
    
    
    
    
    return render(request,'signup.html')


def login(request):
    
    
    return redirect(request,"login.html")
