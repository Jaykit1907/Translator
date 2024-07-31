from django.shortcuts import render,redirect
from Signup.models import Signup
from googletrans import Translator,LANGUAGES
from playsound import playsound
from gtts import gTTS
import os
import speech_recognition
import mysql.connector
import bcrypt


final_result=''
def home(request):
    langguage=LANGUAGES
    selected_option=None
    
    try:
        if request.method=="POST":
            text1=request.POST['textarea1']
            lan=request.POST["selected_language"]
            if 'resultbtn' in request.POST:
                print("hii")
                selected_option=lan
                result=Translator().translate(text1,src='en',dest=lan)
                final_result=result.text
                return render(request,"index.html",{"final_result":final_result,"text1":text1,"language":langguage,"selected_option":lan})
            
            if 'speakbtn' in request.POST:
                print("Hellow")
                
                result=Translator().translate(text1,src='en',dest=lan)
                final_result=result.text
                audio_sound=gTTS(final_result,lang='en')
                audio_sound.save("voice.mp3")
                playsound("voice.mp3")
                os.remove("voice.mp3")
                return render(request,"index.html",{"final_result":final_result,"text1":text1,"language":langguage,"selected_option":lan})

            
        
        
    except Exception as e:
        print(e)
        
            
            
    
    return render(request,"index.html",{"language":langguage})

def speak(request):
    language=LANGUAGES
    selected_option1=None
    selected_option2=None
    
    try:
        if request.method=="POST":
            sel1=request.POST["select1"]
            sel2=request.POST["select2"]
            
            recognizer=speech_recognition.Recognizer()
            with speech_recognition.Microphone() as source:
                
                selected_option1=sel1
                selected_option2=sel2
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
            return render(request,'speak.html',{"language":language,"final_result":final_result,"text1":text,"pron":pron,"selected_option1":selected_option1,"selected_option2":selected_option2})
        
    except Exception as e:
        print(e)
        print(type(e))

    
        return render(request,'speak.html',{"error1":f"Error:{e}","language":language,'selected_option1':selected_option1,"selected_option2":selected_option2})
    
    return render(request,'speak.html',{'language':language})


def signup(request):
    
    try:
        if request.method=="POST":
            fname1=request.POST['fname']
            lname1=request.POST['lname']
            phone1=request.POST['phone']
            email1=request.POST['email']
            password1=request.POST['password']
        
            # connection=mysql.connector.connect(host='localhost',user='root',database='jaykit4',password='pass123')
        
            # con=connection.cursor()
            # con.execute("insert into signup values (%s,%s,%s,%s,%s)",(fname1,lname1,phone1,email1,password1))
            # connection.commit()
            # print("data inserted")
            # con.close()
            em=Signup(first_name=fname1,last_name=lname1,phone=phone1,email=email1,password=password1)
            em.save()
            return redirect("/login/")
            
        
    except Exception as e:
        print(e)
        print("except block executed")

    return render(request,'signup.html')


def login(request):
    
    try:
        if request.method=="POST":
            email1=request.POST['email']
            password1=request.POST['password']
            
            connection=mysql.connector.connect(host='localhost',database='jaykit4',password="pass123",user="root")
            cur=connection.cursor()
            cur.execute("select password from signup where email=%s",(email1,))
            verify=cur.fetchone()
            verify=str(verify)
            print(type(verify))
            print("database password:"+verify)
            print(type(password1))
            password1=tuple(password1)
            print("login passord:"+password1)
            if verify == password1:
               print("login successufl")
                
            else:
               print("invalid user")
            
            
            
            
        
        
    except Exception as e:
        print(e)
        print("dont' have an account")
    
    
    return render(request,"login.html")
