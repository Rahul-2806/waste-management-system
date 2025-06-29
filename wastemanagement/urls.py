"""wastemanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wasteapp.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
# from scipy import stats



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('index/',index,name="index"),  
    path('customer/',customer,name="customer"),
    path('login/',login,name="login"),
    path('category/',category,name="category"),
    path('product/',product,name="product"),
    path('location/',location,name="location"),
    path('custaction/',custaction,name="custaction"),
    path('prodaction/',prodaction,name="prodaction"),
    path('cataction/',cataction,name="cataction"),
    path('locaction/',locaction,name="locaction"),
    path('loginaction/',loginaction,name="loginaction"),
    path('adminhome/',adminhome,name="adminhome"),
    path('customerhome/',customerhome, name="customerhome"),
    path('viewcustomer/', viewcustomer, name="viewcustomer"),
    path('staff/', staff, name="staff"), 
    path('staffaction/', staffaction, name="staffaction"),
    path('viewstaff/', viewstaff, name="viewstaff"),
    path('deletestaff/', deletestaff, name="deletestaff"),
    path('deletecustomer/', deletecustomer, name="deletecustomer"),
    path('viewproduct/', viewproduct, name="viewproduct"),
    path('viewcategory/', viewcategory, name="viewcategory"),
    path('viewlocation/', viewlocation, name="viewlocation"),
    path('deleteproduct/', deleteproduct, name="deleteproduct"),
    path('deletecategory/', deletecategory, name="deletecategory"),
    path('deletelocation/', deletelocation, name="deletelocation"),
    path('updateproduct/', updateproduct, name="updateproduct"),
    path('updateproductaction/', updateproductaction, name="updateproductaction"),
    path('application/', application, name="application"),
    path('viewapplication/', viewapplication, name="viewapplication"),
    path('applicationaction/', applicationaction, name="applicationaction"),
    path('updatecustomeraction/', updatecustomeraction, name="updatecustomeraction"),
    path('updatecustomer/', updatecustomer, name="updatecustomer"),
    path('updatestaff/', updatestaff, name="updatestaff"),
    path('updatestaffingaction/', updatestaffingaction, name="updatestaffingaction"),
    path('updatecategory/', updatecategory, name="updatecategory"),
    path('updatecategoryaction/', updatecategoryaction, name="updatecategoryaction"),
    path('updatelocation/', updatelocation, name="updatelocation"),
    path('updatelocationaction/', updatelocationaction, name="updatelocationaction"),
    path('approveapplication/', approveapplication, name="approveapplication"),
    path('rejectapplication/', rejectapplication, name="rejectapplication"),
    path('managerate/', managerate, name="managerate"),
    path('viewmanagerateaction/', viewmanagerateaction, name="viewmanagerateaction"),
    path('viewmanagerate/', viewmanagerate, name="viewmanagerate"),
    path('updatemanagerate/', updatemanagerate, name="updatemanagerate"),
    path('updatemanagerateaction/', updatemanagerateaction, name="updatemanagerateaction"),
    path('deletemanagerate/', deletemanagerate, name="deletemanagerate"),
    path('subcategory/', subcategory, name="subcategory"),
    path('viewsubcataction/', viewsubcataction, name="viewsubcataction"),
    path('viewratedetails/',viewratedetails,name="viewratedetails"),
    path('viewcustpro/', viewcustpro, name="viewcustpro"),
    path('pdetails/', pdetails, name="pdetails"),
    path('addtocart/', addtocart, name="addtocart"),
    path('viewcart/', viewcart, name="viewcart"),
    path('deletecart/', deletecart, name="deletecart"),
    path('updatecart/', updatecart, name="updatecart"),
    path('orders/', orders, name="orders"),    
    path('assignlocation/', assignlocation, name="assignlocation"),
    path('assignlocationaction/', assignlocationaction, name="assignlocationaction"),
    path('viewassignlocation',viewassignlocation,name="viewassignlocation"),
    path('viewassignedloc', viewassignedloc, name="viewassignedloc"),
    path('payment/', payment, name="payment"),
    path('paymentaction/', paymentaction, name="paymentaction"),
    path('myorders/', myorders, name="myorders"),
    path('orderaction/', orderaction, name="orderaction"),
    path('payment_success/', payment_success, name="payment_success"),
    path('payment_error/', payment_error, name="payment_error"),
    # path('viewcustloc/', viewcustloc, name="viewcustloc"),
    path('wastestats/', wastestats, name="wastestats"),
    path('staffeedback/', staffeedback, name="staffeedback"),
    path('reports/', reports, name="reports"),
    path('customercare/', customercare, name="customercare"),
    path('wastecollectingusers/', wastecollectingusers, name="wastecollectingusers"),
 
    path('staffprofile/', staffprofile, name="staffprofile"),
    path('staffhome/', staffhome, name="staffhome"),
    path('collectionteams/', collectionteams, name="collectionteams"),
    path('recyclinginsights/', recyclinginsights, name="recyclinginsights"),
    path('ekmmap/', ekmmap, name="ekmmap"),
    path('reductionplan/', reductionplan, name="reductionplan"),
    path('energy/', energy, name="energy"),
    path('wheather/', wheather, name="wheather"),
    path('biogasmonitoring/', biogasmonitoring, name="biogasmonitoring"),
    path('fleet/', fleet, name="fleet"),
    path('adminbiomon/', adminbiomon, name="adminbiomon"),
    path('viewcollectionmap/', viewcollectionmap, name="viewcollectionmap"),
    
    path('agent/', agent, name="agent"),
    path('view_application_status/', view_application_status, name="view_application_status"),
    path('rejectorder/', rejectorder, name="rejectorder"),
    path('updateStaffAct/', updateStaffAct, name="updateStaffAct"),
    path('trashview/', trashview, name="trashview"),
    path('paybill/', paybill, name="paybill"),
    path('paybillAct/', paybillAct, name="paybillAct"),
    path('viewpayment/', viewpayment, name="viewpayment"),
    path('feedback/', feedback, name="feedback"),
    path('feedbackaction/', feedbackaction, name="feedbackaction"),
    path('status/', status, name="status"),
    path('viewFeedback/', viewFeedback, name="viewFeedback"),
    path('viewAllAssign/', viewAllAssign, name="viewAllAssign"),
    path('customerprofile/', customerprofile, name="customerprofile"),
    path('updateCustomerAction/', updateCustomerAction, name="updateCustomerAction"),
    path('wastecategory/', wastecategory, name="wastecategory"),
    path('smartwaste/', smartwaste, name="smartwaste"),
    path('recycling/', recycling, name="recycling"),
    path('office/', office, name="office"),
    path('future/', future, name="future"),
    path('guide/', guide, name="guide"),
    path('insta/', insta, name="insta"),
   

    

    
    
    



    
    path('wasteinfo/', wasteinfo, name="wasteinfo"),
    path('service/', service, name="service"),
    path('service1/', service1, name="service1"),
    path('service2/', service2, name="service2"),
    path('service3/', service3, name="service3"),
    path('about/', about, name="about"),
    
    
    
    
   




    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns() 
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+= staticfiles_urlpatterns()
