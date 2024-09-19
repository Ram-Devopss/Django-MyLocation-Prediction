from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from requests import request
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import random

import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#import the sklearn libraries
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score


account={}
otp_number = str(random.randint(100000, 999999))
detection ={}



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def main(request):
    return render(request,"main.html")


def index(request):
    # If the login was unsuccessful or it's not a POST request, render the login page
    return render(request, 'login.html')


@csrf_protect   
def welcome(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
            
        user=authenticate(username=username,password=password)
        print(username,password)
        if user is not None:
           login(request,user)
           messages.success(request,"Welcome,You are Successfully Logged in!!!")
           return render(request,"dashboard.html")
        else:
            messages.error(request,"Username or Password is incorrect.Please try again..")
            return render(request,"error.html")
    
    return render(request,"index.html")

# Creating a Account
def register(request):
            
 return render(request,"signup.html")
        


def detect(request):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error
    from sklearn.preprocessing import StandardScaler

    # Sample dataset (replace this with your actual dataset)
    ## Replace Here Your Datas In The Correct Format
    data = {
        'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3],
        'timestamp': ['2022-01-01 08:00', '2022-01-01 12:00', '2022-01-01 18:00',
                    '2022-01-02 09:30', '2022-01-02 14:00', '2022-01-02 19:45',
                    '2022-01-03 07:15', '2022-01-03 13:30', '2022-01-03 20:00'],
        'latitude': [37.7749, 37.7837, 37.7749, 34.0522, 34.0522, 34.1014, 40.7128, 40.7213, 40.7128],
        'longitude': [-122.4194, -122.4224, -122.4194, -118.2437, -118.2437, -118.3257, -74.0060, -73.9901, -74.0060],
    }

    df = pd.DataFrame(data)

    # Feature engineering
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek

    # Features and target variables
    X = df[['latitude', 'longitude', 'hour', 'day_of_week']]
    y = df[['latitude', 'longitude']]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train a Random Forest Regressor
    regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    regressor.fit(X_train_scaled, y_train)

    # Make predictions on the test set
    y_pred = regressor.predict(X_test_scaled)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse:.6f}')

    # Example usage: Predict next location for a new data point
    new_data_point = pd.DataFrame({'latitude': [37.7550], 'longitude': [-122.4085], 'hour': [12], 'day_of_week': [1]})
    new_data_point_scaled = scaler.transform(new_data_point)
    predicted_location = regressor.predict(new_data_point_scaled)
    print(f'Predicted Next Latitude: {predicted_location[0][0]:.6f}')
    print(f'Predicted Next Longitude: {predicted_location[0][1]:.6f}')
    
    data={}
    data['mean'] = f'{mse:.6f}'
    data['lat'] = f'{predicted_location[0][0]:.6f}'
    data['long'] = f'{predicted_location[0][1]:.6f}'

    data['final'] = f"{ predicted_location}"

    print(f"Final Decision { predicted_location}")
    print('################### --------------- Code Was Succeffully Executed!')
    return render(request,"dashboard.html",data)

def send_otp(request):
    if request.method == 'POST':

        account['user'] = request.POST.get("username")
        account['email']  = request.POST.get("email")
        account['mobile'] = request.POST.get("mobile")
        account['password'] = request.POST.get("password")
        account['repassword'] = request.POST.get("confirmPassword")
        account['method'] = request.POST.get('Verification')

        credential = {'name':account['user'],'email':account['email'],'mobile':account['mobile'],'password':account['password'],'repassword':account['repassword'],'method':account['method']}
        # Open the file in write mode
        with open('credential.txt', 'w') as file:
        # Write the content to the file
            file.write(str(credential))
        
        if account['method'] == 'email':
            # Your email credentials
            fromaddr = "ramdevops2005@gmail.com"
            toaddr = request.POST.get("email")
            smtp_password = "rcau rkir ffiw megr"

            # Create a MIMEMultipart object
            msg = MIMEMultipart()

            # Set the sender and recipient email addresses
            msg['From'] = fromaddr
            msg['To'] = toaddr
            
            # Set the subject
            msg['Subject'] = "Otp Verification"

            # Set the email body
            body = f"Your OTP is: {otp_number}"
            msg.attach(MIMEText(body, 'plain'))

            try:
                # Connect to the SMTP server
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    # Start TLS for security
                    server.starttls()

                    # Log in to the email account
                    server.login(fromaddr, smtp_password)

                    # Send the email
                    server.sendmail(fromaddr, toaddr, msg.as_string())

                # Email sent successfully, render a template
                return render(request, 'verification_otp.html')

            except Exception as e:
                # An error occurred while sending email, redirect with an error message
                messages.error(request, f"Error sending OTP email: {e}")
                return render(request,'signup.html')  # You need to replace 'verify_it' with the appropriate URL name
        else:
            # Invalid method, redirect with an error message
            messages.error(request, "Invalid verification method")
            return render(request,'signup.html')  # You need to replace 'verify_it' with the appropriate URL name

    # If the request method is not POST, redirect with an error message
    messages.error(request, "Invalid request method")
    return render(request,'signup.html') # You need to replace 'verify_it' with the appropriate URL name


def verify_it(request):
    
    if request.method=="POST":


       

        verifi_otp1 = request.POST.get("otp1")
        verifi_otp2 = request.POST.get("otp2")
        verifi_otp3 = request.POST.get("otp3")
        verifi_otp4 = request.POST.get("otp4")
        verifi_otp5 = request.POST.get("otp5")
        verifi_otp6 = request.POST.get("otp6")

        six_digits=f"{verifi_otp1}{verifi_otp2}{verifi_otp3}{verifi_otp4}{verifi_otp5}{verifi_otp6}"
        if six_digits==otp_number:

         my_user=User.objects.create_user(account['user'],account['email'],account['password'])
         my_user.save() 
         messages.success(request,"Your account has been Created Successfully!!!")
         redirect(index)


        # else:
        #     messages.success(request,"Registration Failed!!")
        #     return render(request, 'success.html',six_digits)
        
    return render(request,"login.html")  

