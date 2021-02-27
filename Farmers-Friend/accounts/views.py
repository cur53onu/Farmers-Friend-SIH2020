from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
import json
import urllib.request
import requests
from django.contrib import auth
import os
from django.contrib.auth.models import User
from .models import LoanSchemeForFarmers
from .models import CropInfo
from .models import extendeduser
import json
from .models import approvals
from .models import MarketPrices
from .models import PestControl
from .models import WillPlant
from django.contrib.auth.decorators import login_required
#import twilio
# from twilio.rest import Client
import threading
import datetime
user_data=extendeduser.objects.values('phone','town','user')
def printit():
    threading.Timer(10, printit).start()
    for i in user_data:
        city = i['town']
        src = 'http://api.openweathermap.org/data/2.5/weather?appid=e995a3bb90b825a2202b9786e17caa56&q='
        url = src + city
        list_of_data = requests.get(url).json()
        temp = list_of_data['main']['temp']
        newtmp = round(temp - 273.15, 3)
        condition = list_of_data['weather'][0]['description']
        humidity = list_of_data['main']['humidity']
        data = {
            "city": city,
            "temp": newtmp,
            "humidity": humidity,
            "condition": condition,
            "icon": str(list_of_data['weather'][0]['icon']),
        }
        print(data)
        if data['condition']=="overcast clouds":
            pass
            print('\n'+city,' user '+str(i['user'])+' overcast condition',end='\n')


# printit()
def index(request):
    return render(request, 'accounts/basic.html')

def Farmer(request):
    return render(request, 'accounts/FarmerPage.html')

def home(request):
    return render(request, 'accounts/basic.html')
def Admin(request):
    return render(request, 'accounts/AdminPage.html')


def userpage(request):
    return render(request, 'accounts/index.html')

def handlelogin(request):
         if request.method == "POST":
             uname1 = request.POST['uname1']
             pass3 = request.POST['pass3']
             user = auth.authenticate(username=uname1, password=pass3)
             if user is not None:
                auth.login(request, user)
                datas = extendeduser.objects.filter(user=request.user)
                messages.success(request, "Successfully logged in")
                if request.user.is_superuser:
                    return redirect("admin")
                data = str(datas[0].cat)
                if data == "Farmer":
                     return redirect('farmer')
                #return render(request,'accounts/FarmerPage.html')
                elif data == "Admin":
                    return redirect('admin')
                #return render(request, 'accounts/AdminPage.html')
             else:
                messages.error(request, "Invalid Credentials")
                return render(request, 'accounts/basic.html')
         else:
             return HttpResponse('NOT allowed')

def Addschemes(request):
    return render(request, 'accounts/AddSchemes.html')

def weather(request):
    try:
        if request.method == 'POST':
            city = request.POST['city']
            if len(city) == 0:
                messages.error(request, "Enter city name")
                return render(request, 'accounts/weather.html')
            src = 'http://api.openweathermap.org/data/2.5/weather?appid=e995a3bb90b825a2202b9786e17caa56&q='
            url = src + city
            list_of_data = requests.get(url).json()
            temp = list_of_data['main']['temp']
            newtmp = round(temp - 273.15, 3)
            condition = list_of_data['weather'][0]['description']
            humidity = list_of_data['main']['humidity']
            data = {
                "city": city,
                "temp": newtmp,
                "humidity": humidity,
                "condition": condition,
                "icon": str(list_of_data['weather'][0]['icon']),
            }
        return render(request, 'accounts/weather.html', data)
    except:
        messages.error(request, "Write city name correctly")
        return render(request, 'accounts/weather.html')
def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return render(request, 'accounts/basic.html')

def adminpanel(request):
    if request.method == 'POST':
        info = str(request.POST['dos'])
        name = str(request.POST['tos'])
        l = LoanSchemeForFarmers()
        l.info = info
        l.scheme_name = name
        l.save()
        euser=extendeduser.objects.values('phone','user')
        q=[]
        for j in euser:
            q.append(j['phone'])

        # url = "https://www.fast2sms.com/dev/bulk"
        # querystring = {"authorization": "ycJbOn8xXkgUB5j9ZTpM2hDHrYvFt4IzsNlSmAfLeaoGPiEKR7jiZe3wOzktNoFS8Ahr6TgQqvyPW9LV", "sender_id": "FarmerFriend", "message": info+"Scheme updated on FarmerFriend",
        #                "language": "english", "route": "p", "numbers":q}
        # headers = {
        #     'cache-control': "no-cache"
        # }
        # response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.text)

        #zerosms.sms(phno=9689914109, passwd=password, message='helloworld!!', receivernum=receiver mobilenumber)
        # #SMS Notification
        #     if p=='8830502656':
        #         account_sid = 'ACa522720e1d991ba02ac1afec621f3ed4'
        #         auth_token = 'f284dae9dfc1886dfe099fb75b0908a7'
        #         client = Client(account_sid, auth_token)
        #
        #         message = client.messages.create(
        #             body=l.scheme_name+"     Scheme Info:      "+l.info,
        #             from_='+12183166674',
        #             to='+918830502656'
        #         )
        #
        #         print(message.sid)

    return render(request, 'accounts/AdminPanel.html')
@login_required(login_url='/basic/')
def signup(request):
    try:
        if request.method == 'POST':
            uname = request.POST['uname']
            email = request.POST['email']
            fname = request.POST['fname']
            lname = request.POST['lname']
            phone = request.POST['phone']
            cat = request.POST['cat']
            town=request.POST['town']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            if len(uname)<6:
                messages.error(request, "Week Username")
                return render(request, 'accounts/basic.html')
            if pass1!=pass2:
                messages.error(request, "Passwords not Same")
                return render(request, 'accounts/basic.html')
            if len(pass1)<6:
                messages.error(request, "Password must be greater than 6 characters")
                return render(request, 'accounts/basic.html')
            user = User.objects.create_user(uname, email, pass1)
            user.first_name = fname
            user.last_name = lname
            user.save()
            newuser = extendeduser(phone=phone, cat=cat,town=town, user=user)
            newuser.save()
            messages.success(request, "Your FarmerFriend Account has been Created Successfully")
            euser = extendeduser.objects.values('phone', 'user')
            # url = "https://www.fast2sms.com/dev/bulk"
            # querystring = {
            #     "authorization": "ycJbOn8xXkgUB5j9ZTpM2hDHrYvFt4IzsNlSmAfLeaoGPiEKR7jiZe3wOzktNoFS8Ahr6TgQqvyPW9LV",
            #     "sender_id": "FarmerFriend", "message": "your Farmer Friend account has been created successfully\n Your Username is "+uname+"\nPassword is  "+pass1+"\n If you have any query call on below Number \nCustomerCare No:9689914109",
            #     "language": "english", "route": "p", "numbers": phone}
            # headers = {
            #     'cache-control': "no-cache"
            # }
            # response = requests.request("GET", url, headers=headers, params=querystring)
            # print(response.text)
            return render(request, 'accounts/basic.html')
    except:
        messages.error(request, "User with this information already exists")
        return render(request, 'accounts/basic.html')
def addcrop(request):
    if request.method == 'POST':
        cropinfo = str(request.POST['cropinfo'])
        cropname = str(request.POST['cropname'])
        cropimg = str(request.POST['cropimg'])
        c = CropInfo()
        c.crop_name = cropname
        c.crop_info = cropinfo
        c.img='accounts/images/'+cropimg
        c.save()
    return render(request, 'accounts/AdminPanel.html')

def getPrediction(district,c_season):
    x = approvals()
    x = x.predict(district, c_season)
    return x
def get_data():
    crops = CropInfo.objects.values('crop_name', 'crop_info')
    return crops


class my_dictionary(dict):

    # __init__ function
    def __init__(self):
        self = dict()

        # Function to add key:value

    def add(self, key, value):
        self[key] = value

def govtschemes(request):
    l=LoanSchemeForFarmers.objects.values('scheme_name','info')
    lis=[]
    for i in l:
        lis.append(i)
    dic={'dic':lis}
    print(dic)
    return render(request,'accounts/govschemes.html',dic)

def addPest(request):
    if request.method=='POST':
        pest=request.POST.get('pest')
        district=request.POST.get('district')
        crop=request.POST.get('crop')

        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' + district + '&appid=f90ba0f6ad9de2b73ce56962af45f62e').read()

        list_of_data = json.loads(source)
        temp=round(list_of_data['main']['temp']-273.15)
        rain=897
        humidity=(list_of_data['main']['humidity'])
        windspeed=(list_of_data['wind']['speed'])
        c=PestControl()
        c.AddPest(district,temp,rain,humidity,windspeed,crop,pest)
    return render(request, 'accounts/addpest.html')
def predictPest(request):
    data={}
    if request.method=='POST':
        district = request.POST.get('district')
        crop = request.POST.get('crop')
        crop=crop.capitalize()

        p = PestControl()
        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' + district + '&appid=f90ba0f6ad9de2b73ce56962af45f62e').read()

        list_of_data = json.loads(source)
        temp = round(list_of_data['main']['temp'] - 273.15)
        rain = 897
        humidity = (list_of_data['main']['humidity'])
        wind = (list_of_data['wind']['speed'])

        x = p.PredictPest(crop, district, temp, rain, humidity, wind)
        data['data']=x
    return render(request, 'accounts/predictpest.html',data)

def viewcrop(request):
    if request.method=='POST':
        data=''
        val=request.POST.get('crop-name')
        print(val)
        crop=CropInfo.objects.values('crop_name', 'crop_info','img')
        return render(request,'accounts/'+val+'.html')
        # for i in crop:
        #     if i['crop_name']==val:
        #         data=i['crop_info']
        #         data={'data':i}
        #         return render(request, 'accounts/viewcrop.html',data)
    else:
        return HttpResponse('NO CROP SELECTED')

def predictMPG(request):

    if request.method=='GET':
        context={'zz':1}
    if request.method == 'POST':
        w=WillPlant.objects.values('user','crop','town')
        temp3 = {}
        temp3['District'] = request.POST.get('District4')
        temp3['District'] = temp3['District'].upper()
        district=temp3['District']
        p = PestControl()
        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' + district + '&appid=f90ba0f6ad9de2b73ce56962af45f62e').read()

        list_of_data = json.loads(source)
        temp = round(list_of_data['main']['temp'] - 273.15)
        rain = 897
        humidity = (list_of_data['main']['humidity'])
        wind = (list_of_data['wind']['speed'])
        temp3['Season'] = (request.POST.get('Season1'))

        c_season = int(temp3['Season'])
        season = ''

        x = getPrediction(district, c_season)
        # if c_season == 0:
        #     season = "Current Season"
        crops = CropInfo.objects.values('crop_name', 'crop_info', 'img')
        crop_found = []
        pest_found = {}
        pest = []
        croppest = {}
        list_planted_crop=[]
        for i in w:
            if i['town']==district:
                list_planted_crop.append(i['crop'])
        print(list_planted_crop)
        if c_season == 1:
            season = 'Kharif'
        elif c_season == 2:
            season = 'Rabbi'
        elif c_season == 3:
            season = 'Whole Year'
        elif c_season == 4:
            season = 'No specific season'
        elif c_season == 5:
            season='All Seasons Without Previous Year Prod'
            for i in x[0]:
                for j in crops:
                    z = i
                    if j['crop_name'] == z:
                        count_of_crop = list_planted_crop.count(z)
                        j['count'] = count_of_crop
                        if count_of_crop > 1:
                            j['danger'] = 1
                        else:
                            j['safe']=1
                        t = p.PredictPest(z, district, temp, rain, humidity, wind)
                        n = len(crops)
                        pest.append(t)
                        pest_found[z] = t
                        crop_found.append(j)
                        croppest[z] = t

            context = {'crop': x[0], 'district': temp3['District'], 'season': season, 'predicted_crops': x[0],
                       'found': crop_found, 'pest': pest_found, 'croppest': croppest}
            return render(request, 'accounts/predict.html', context)

        for i in range(0,len(x[1])):
            for j in crops:
                z=(x[1][i][0])
                if j['crop_name']==z:
                    count_of_crop=list_planted_crop.count(z)
                    j['count']=count_of_crop
                    if count_of_crop>1:
                        j['danger']=1
                    else:
                        j['safe']=1
                    print(z,count_of_crop)
                    t = p.PredictPest(z, district, temp, rain, humidity, wind)
                    n = len(crops)
                    pest.append(t)
                    pest_found[z]=t
                    crop_found.append(j)
                    croppest[z]=t

        context = {'crop': x[1],'district':temp3['District'],'season':season,'predicted_crops':x[0],'found':crop_found,'pest':pest_found,'croppest':croppest}
        # context={}
    return render(request, 'accounts/predict.html', context)

def getPredictionNoPrevious(district,c_season):
    x = approvals()
    x = x.predict(district, c_season)
    return x

def predictwithoutprevious(request):
    context={}
    return render(request, 'accounts/predict.html', context)


def showweather(request):
    return render(request, 'accounts/weather.html')


def marketforuser(request):
    m_prices=MarketPrices.objects.values('town','crop','market','date','price')
    lis=[]
    for i in m_prices:
        print(i)
        lis.append(i)
    dic={'prices':lis}
    return render(request,'accounts/marketforuser.html',dic)

def willplant(request):
    if request.method=='POST':
        flg=0
        crop=request.POST.get('crop-name')
        dis=request.POST.get('district')
        # w=willplant()
        print(crop,dis,request.user)
        # w.user=reques t.user
        # w.town=''
        # w.crop=crop
    will_plant=WillPlant.objects.values('user','crop','town')

    for i in will_plant:
        print(i['user'],i['crop'],i['town'],request.user,crop,dis)
        if str(i['user'])==str(request.user) and str(i['crop']) == str(crop) and str(i['town']) == str(dis):
            flg=1
    if flg==0 or len(will_plant)==0:
        w = WillPlant()
        w.user = str(request.user)
        w.town = str(dis)
        w.crop = str(crop)
        w.save()
        print('added successfully')
    else:
        print('failed')
    print(will_plant)
    return render(request,'accounts/FarmerPage.html')

def userinfo(request):
    userdata=[]
    urs=extendeduser.objects.values('phone','cat','town','user')
    for i in urs:
        userdata.append(i)
    userdata={'userdata':userdata}
    return render(request,'accounts/userinfo.html',userdata)

def cropcountadminview(request):
    will_plant = WillPlant.objects.values('user', 'crop', 'town')
    lis=[]
    for i in will_plant:
        lis.append(i)
    croplist=[]
    for i in lis:
        croplist.append(i['crop'])
    croplist = list(set(croplist))
    citylist=[]
    for i in lis:
        croplist.append(i['crop'])
    citylist = list(set(citylist))
    lis2=[]
    cnt=0
    dic2={}
    # for i in range(0,len(croplist)):
    #     for j in range(1,len(lis)):
    #         if lis[j]['crop']==croplist[i] and lis[j]['town']==citylist[i]:
    #             dic2[croplist[j]]=croplist[i]
    # print(dic2)
    lis=sorted(lis, key=lambda i: i['town'])
    # lis=sorted(lis,key=lambda i: i['crop'])
    dic={'dic':lis}
    # print(dic)
    return render(request,'accounts/cropcountadminview.html',dic)

def adminmarketadd(request):
    print(request.user)
    z={'z':1}
    if request.method=='POST':
        dis = request.POST.get('District4')
        crop=request.POST.get('crop')
        market=request.POST.get('market')
        price=request.POST.get('price')
        date=datetime.datetime.now()
        print(dis,crop,market,date)
        marketprice=MarketPrices.objects.values('town','market','crop','price','date')
        for i in marketprice:
            if i['town']==dis and crop==i['crop'] and market==i['market']:
                i['price']=price
                item=MarketPrices.objects.get(town=dis,market=market,crop=crop)
                print(item)
                item.delete()
        marketpricenew=MarketPrices()
        marketpricenew.town=dis
        marketpricenew.market=market
        marketpricenew.crop=crop
        marketpricenew.price=price
        marketpricenew.date=date
        marketpricenew.save()

    return render(request,'accounts/adminmarketadd.html',z)

def schemepmkisan(request):
    if request.method=='POST':
        name=request.POST.get('schemename')
        print(name)
    return render(request,'accounts/'+name+'.html')

def pestinformation(request):
    return render(request,'accounts/pestinformation.html')
def LeafSpot(request):
    return render(request,'accounts/Leaf Spot or Sigatoka.html')
def PanamaWilt(request):
    return render(request,'accounts/Panama Wilt.html')
def AmricanBollWarm(request):
    return render(request, 'accounts/Amrican Boll  Warm.html')
def PinkBollWarm(request):
    return render(request, 'accounts/Pink Boll Warm.html')
def Leafhopper(request):
    return render(request, 'accounts/Leaf hopper.html')
def Cornworm(request):
    return render(request, 'accounts/Corn worm.html')
def PotatoLateBlightPhytophthorainfestans(request):
    return render(request, 'accounts/Potato Late Blight Phytophthora infestans.html')
def Earlyshootborer(request):
    return render(request, 'accounts/Early shoot borer.html')
