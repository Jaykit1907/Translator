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
    selected_option2=None
    final_result=""
    
    try:
        if request.method=="POST":
            text1=request.POST['textarea1']
            lan1=request.POST["selected_language1"]
            lan2=request.POST["selected_language2"]
            if 'resultbtn' in request.POST:
                print("hii")
                selected_option2=lan2
                result=Translator().translate(text1,src=lan1,dest=lan2)
                final_result=result.text
                print(final_result)
                return render(request,"index.html",{"final_result":final_result,"text1":text1,"language":langguage,"selected_option1":lan1,"selected_option2":lan2})
            
            if 'speakbtn' in request.POST:
                print("Hellow")
                
                result=Translator().translate(text1,src=lan1,dest=lan2)
                final_result=result.text
                audio_sound=gTTS(final_result,lang='en',tld='co.in')
                audio_sound.save("voice.mp3")
                playsound("voice.mp3")
                os.remove("voice.mp3")
                return render(request,"index.html",{"final_result":final_result,"text1":text1,"language":langguage,"selected_option1":lan1,"selected_option2":lan2})

            
        
        
    except Exception as e:
        print(e)
        # return render(request,"index.html",{"error":True,"message":"Network error"})

        
            
            
    
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
                absolute_path = os.path.abspath("voice.mp3")
                print(absolute_path)
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
            hashed_password = hash_password(password1)

        
            connection=mysql.connector.connect(host='localhost',user='root',database='jaykit4',password='pass123')
        
            con=connection.cursor()
            con.execute("insert into signup values (%s,%s,%s,%s,%s)",(fname1,lname1,phone1,email1,hashed_password))
            connection.commit()
            print("data inserted")
            con.close()
            # em=Signup(first_name=fname1,last_name=lname1,phone=phone1,email=email1,password=hashed_password)
            # em.save()
            return redirect("/login/")
            
        
    except Exception as e:
        print(e)
        print("except block executed")

    return render(request,'signup.html')



def hash_password(plain_text_password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed_password




def login(request):
    
    try:
        if request.method=="POST":
            email1=request.POST['email']
            password1=request.POST['password']

# Establish connection to the database
            conn = mysql.connector.connect(host='localhost',database='jaykit4',password="pass123",user="root")

            cursor = conn.cursor()

        # Username and password entered by the user
            username = email1
            entered_password =password1

        # Retrieve the stored hashed password for the given username
            select_query = "SELECT password FROM signup WHERE email = %s"
            cursor.execute(select_query, (username,))
            result = cursor.fetchone()

            if result:
                stored_hashed_password = result[0]

            # Verify the entered password against the stored hashed password
                if bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    print("Login successful!")
                    return redirect('/')
                else:
                    print("Incorrect password.")
                    return render(request,"login.html",{"error":True,"message":"Username or Password Invalid.Please try again"})
            else:
             print("Username not found.")
             return render(request,"login.html",{"error":True,"message":"User not found"})

        # Close the connection
        cursor.close()
        conn.close()

                
    except Exception as e:
        print("exception block")
        print(e)
        
        
    return render(request,"login.html")
        

def check_password(plain_text_password, hashed_password):
    
    hashed_password1 = bytes(hashed_password, 'utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password1)
