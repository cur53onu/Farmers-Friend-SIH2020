from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.index,name='home'),
    path('basic/', views.home),
    path('index/', views.userpage,name='userpage'),
    path('weather', views.weather,name='weather'),
    path('adminpanel', views.adminpanel,name='admin-panel'),
    path('addcrop', views.addcrop,name='addcrop'),
    path('predictMPG', views.predictMPG,name='predict'),
    path('addpest', views.addPest,name='addpest'),
    path('predictpest', views.predictPest,name='predictpest'),
    path('signup',views.signup,name='signup'),
    path('login', views.handlelogin,name='handlelogin'),
    path('handlelogout', views.handlelogout, name='handlelogout'),
    path('Admin/', views.Admin,name='admin'),
    path('Farmer/', views.Farmer,name='farmer'),
    path('Weather/', views.showweather),
    path('Addschemes/', views.Addschemes),
    path('viewcrop', views.viewcrop,name='viewcrop'),
    path('predictwithoutprevious', views.predictwithoutprevious,name='predictwithoutprevious'),
    path('marketforuser', views.marketforuser,name='marketforuser'),
    path('willplant', views.willplant,name='willplant'),
    path('userinfo', views.userinfo,name='userinfo') ,
    path('cropcountadminview', views.cropcountadminview,name='cropcountadminview'),
    path('govtschemes', views.govtschemes,name='govtschemes'),
    path('adminmarketadd', views.adminmarketadd,name='adminmarketadd'),
    path('schemepmkisan', views.schemepmkisan,name='schemepmkisan'),
    path('pestinformation', views.pestinformation,name='pestinformation'),
    path('LeafSpotorSigatoka', views.LeafSpot,name='LeafSpot'),
    path('PanamaWilt', views.PanamaWilt,name='Panama Wilt'),
    path('AmricanBollWarm', views.AmricanBollWarm,name='AmricanBollWarm'),
    path('PinkBollWarm', views.PinkBollWarm,name='PinkBollWarm'),
    path('Leafhopper', views.Leafhopper,name='Leafhopper'),
    path('Cornworm', views.Cornworm,name='Cornworm'),
    path('PotatoLateBlightPhytophthorainfestans', views.PotatoLateBlightPhytophthorainfestans,name='PotatoLateBlightPhytophthorainfestans'),
    path('Earlyshootborer', views.Earlyshootborer,name='Earlyshootborer')
]