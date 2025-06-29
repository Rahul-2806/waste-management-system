from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect,redirect
from django.db import connection
from wasteapp.forms import pform
from wasteapp.models import pmodel
import datetime
today_date = datetime.date.today()
today = today_date.strftime("%Y-%m-%d")

# < code by Rahul >
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

# < end >

def index(request):
    return render(request,'index.html')
def customer(request):
    return render(request,'customer.html')
from .forms import CustomerForm  # Assuming the CustomerForm is imported correctly
from .models import Customer  # Assuming the Customer model is imported
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse

def custaction(request, customer_id=None):
    cursor = connection.cursor()

    if request.method == "POST":
        # Bind the form with POST and FILES data
        customer_form = CustomerForm(request.POST, request.FILES)

        if customer_form.is_valid():
            # Get the email from the form
            email = customer_form.cleaned_data["email"]

            # If a customer ID is provided, try to fetch the customer to update
            if customer_id:
                try:
                    customer = Customer.objects.get(Cid=customer_id)
                except Customer.DoesNotExist:
                    return create_paper_notification(
                        "Customer Not Found", 
                        "We couldn't locate the customer profile in our records",
                        "error",
                        "/viewcustomer/"
                    )

            # If no customer ID is provided, create a new one
            else:
                customer = Customer()

            # Check if the email already exists (excluding the current customer, if updating)
            cursor.execute("SELECT COUNT(*) FROM customer WHERE email = %s AND Cid != %s", [email, customer.Cid if customer_id else 0])
            email_exists = cursor.fetchone()[0]

            if email_exists > 0:
                # If the email exists, show a notification
                return create_paper_notification(
                    "Email Already Registered", 
                    "This email address is already being used by another customer",
                    "warning",
                    "/viewcustomer/"
                )

            # Update or create the customer instance
            customer.Name = customer_form.cleaned_data["name"]
            customer.Gender = customer_form.cleaned_data["gender"]
            customer.Address = customer_form.cleaned_data["address"]
            customer.Phone = customer_form.cleaned_data["phone"]
            customer.Email = customer_form.cleaned_data["email"]
            customer.Img = customer_form.cleaned_data["Img"]

            # Save the customer instance to the database
            customer.save()
            
            # Get the newly added customer's ID
            cursor.execute("SELECT MAX(cid) AS cid FROM customer")
            staff_id = cursor.fetchone()[0]

            # Insert into login table with the 'customer' user type
            cursor.execute(
                "INSERT INTO login(uid, uname, upass, utype) VALUES (%s, %s, %s, %s)",
                (staff_id, email, request.POST['password'], 'customer')
            )

            # Success message with paper notification
            action = "updated" if customer_id else "created"
            return create_paper_notification(
                f"Customer {action.capitalize()}", 
                f"The customer profile has been successfully {action}",
                "success",
                "/customer/"
            )
        else:
            # Print errors if form is invalid, for debugging purposes
            print(customer_form.errors)
            # Optionally: Return errors to the template
            return render(request, "customer.html", {"customer_form": customer_form, "errors": customer_form.errors})
    
    else:
        if customer_id:
            try:
                customer = Customer.objects.get(Cid=customer_id)
                customer_form = CustomerForm(initial={
                    'name': customer.Name,
                    'address': customer.Address,
                    'phone': customer.Phone,
                    'gender': customer.Gender,
                    'email': customer.Email,
                    'img': customer.Img,
                })
            except Customer.DoesNotExist:
                return create_paper_notification(
                    "Customer Not Found", 
                    "We couldn't locate the customer profile in our records",
                    "error",
                    "/viewcustomer/"
                )
        else:
            customer_form = CustomerForm()  # Show an empty form if not a POST request

    return render(request, "customer.html", {"customer_form": customer_form})

def create_paper_notification(title, message, notification_type, redirect_url):
    """
    Create a handwritten paper note notification with enhanced animations and design
    
    Args:
        title: The notification title
        message: The notification message
        notification_type: 'success', 'warning', or 'error'
        redirect_url: Where to redirect after notification
    """
    # Set stamps and colors based on notification type
    if notification_type == "success":
        stamp_text = "APPROVED"
        stamp_color = "#2e7d32"
        ink_color = "#1b5e20"
    elif notification_type == "warning":
        stamp_text = "ATTENTION"
        stamp_color = "#f57f17"
        ink_color = "#e65100"
    else:  # error
        stamp_text = "DECLINED"
        stamp_color = "#c62828"
        ink_color = "#b71c1c"
    
    html_response = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&family=Indie+Flower&family=Permanent+Marker&display=swap" rel="stylesheet">
        <style>
            :root {{
                --stamp-color: {stamp_color};
                --ink-color: {ink_color};
                --paper-color: #fffdf0;
                --paper-shadow: rgba(0, 0, 0, 0.4);
            }}
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Indie Flower', cursive;
                background-color: rgba(0, 0, 0, 0.5);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                perspective: 1200px;
                overflow: hidden;
            }}
            
            .backdrop {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(5px);
                z-index: 10;
                opacity: 0;
                animation: fadeIn 0.5s ease forwards;
            }}
            
            .paper-container {{
                width: 350px;
                height: 450px;
                position: relative;
                transform-style: preserve-3d;
                z-index: 20;
                transform: translateY(100vh) rotateX(-20deg) rotateY(5deg);
                animation: slideUp 0.8s cubic-bezier(0.22, 0.61, 0.36, 1) forwards;
            }}
            
            .paper {{
                position: absolute;
                width: 100%;
                height: 100%;
                background: var(--paper-color);
                border-radius: 2px;
                padding: 25px;
                box-shadow: 0 20px 40px var(--paper-shadow);
                overflow: hidden;
                transform-origin: top center;
                transform: rotateX(-90deg);
                animation: unfold 1s cubic-bezier(0.22, 0.61, 0.36, 1) forwards 0.4s;
                backface-visibility: hidden;
            }}
            
            /* Torn paper edges with SVG */
            .paper::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: url('data:image/svg+xml;utf8,<svg width="350" height="450" xmlns="http://www.w3.org/2000/svg"><path fill="none" stroke="rgba(0,0,0,0.07)" stroke-width="2" d="M0,0 Q5,10 8,5 T15,12 T22,5 T30,10 T40,2 T50,8 T60,0 T70,5 T80,0 T90,8 T100,0 T110,5 T120,0 T130,10 T140,2 T150,8 T160,0 T170,4 T180,0 T190,9 T200,1 T210,6 T220,0 T230,5 T240,0 T250,4 T260,0 T270,7 T280,2 T290,6 T300,0 T310,8 T320,0 T330,5 T340,0 T350,7" /><path fill="none" stroke="rgba(0,0,0,0.07)" stroke-width="2" d="M0,450 Q5,440 8,445 T15,438 T22,445 T30,440 T40,448 T50,442 T60,450 T70,445 T80,450 T90,442 T100,450 T110,445 T120,450 T130,440 T140,448 T150,442 T160,450 T170,446 T180,450 T190,441 T200,449 T210,444 T220,450 T230,445 T240,450 T250,446 T260,450 T270,443 T280,448 T290,444 T300,450 T310,442 T320,450 T330,445 T340,450 T350,443" /><path fill="none" stroke="rgba(0,0,0,0.07)" stroke-width="2" d="M0,0 Q10,5 5,8 T12,15 T5,22 T10,30 T2,40 T8,50 T0,60 T5,70 T0,80 T8,90 T0,100 T5,110 T0,120 T10,130 T2,140 T8,150 T0,160 T4,170 T0,180 T9,190 T1,200 T6,210 T0,220 T5,230 T0,240 T4,250 T0,260 T7,270 T2,280 T6,290 T0,300 T8,310 T0,320 T5,330 T0,340 T7,350 T0,360 T6,370 T0,380 T8,390 T0,400 T5,410 T0,420 T7,430 T0,440 T5,450" /><path fill="none" stroke="rgba(0,0,0,0.07)" stroke-width="2" d="M350,0 Q340,5 345,8 T338,15 T345,22 T340,30 T348,40 T342,50 T350,60 T345,70 T350,80 T342,90 T350,100 T345,110 T350,120 T340,130 T348,140 T342,150 T350,160 T346,170 T350,180 T341,190 T349,200 T344,210 T350,220 T345,230 T350,240 T346,250 T350,260 T343,270 T348,280 T344,290 T350,300 T342,310 T350,320 T345,330 T350,340 T343,350 T350,360 T344,370 T350,380 T342,390 T350,400 T345,410 T350,420 T343,430 T350,440 T345,450" /></svg>');
                pointer-events: none;
                z-index: 5;
            }}
            
            .paper-texture {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: url('data:image/svg+xml;utf8,<svg width="300" height="300" xmlns="http://www.w3.org/2000/svg"><filter id="noise" x="0" y="0"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="5" stitchTiles="stitch" seed="42"/><feBlend mode="soft-light" in="SourceGraphic"/></filter><rect width="300" height="300" filter="url(%23noise)" opacity="0.3"/></svg>');
                background-repeat: repeat;
                pointer-events: none;
                z-index: 5;
                mix-blend-mode: multiply;
            }}
            
            .paper-lines {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: linear-gradient(#bbb 1px, transparent 1px);
                background-size: 100% 25px;
                background-position: 0 20px;
                pointer-events: none;
                opacity: 0.1;
                z-index: 1;
            }}
            
            /* Paper fold creases */
            .paper-crease {{
                position: absolute;
                top: 0;
                left: 15%;
                width: 1px;
                height: 100%;
                background: linear-gradient(90deg, 
                    transparent, 
                    rgba(0,0,0,0.05) 45%, 
                    rgba(0,0,0,0.1) 50%,
                    rgba(0,0,0,0.05) 55%, 
                    transparent);
                width: 10px;
                opacity: 0;
                animation: showCrease 0.5s ease-in forwards 1.2s;
                transform: rotate(1deg);
                z-index: 2;
            }}
            
            .paper-crease-2 {{
                left: 65%;
                animation-delay: 1.3s;
                transform: rotate(-1deg);
            }}
            
            .paper-crease-horizontal {{
                top: 33%;
                left: 0;
                width: 100%;
                height: 10px;
                background: linear-gradient(0deg, 
                    transparent, 
                    rgba(0,0,0,0.05) 45%, 
                    rgba(0,0,0,0.1) 50%,
                    rgba(0,0,0,0.05) 55%, 
                    transparent);
                animation-delay: 1.4s;
            }}
            
            .stamp {{
                position: absolute;
                top: 20px;
                right: 20px;
                width: 100px;
                height: 100px;
                display: flex;
                justify-content: center;
                align-items: center;
                opacity: 0;
                animation: stampAppear 0.6s ease-out forwards 1.7s;
                transform-origin: center;
            }}
            
            .stamp::before {{
                content: '{stamp_text}';
                position: absolute;
                transform: rotate(25deg);
                font-family: 'Permanent Marker', cursive;
                font-size: 14px;
                font-weight: bold;
                color: white;
                text-align: center;
                line-height: 1;
                z-index: 30;
                text-shadow: 1px 1px 1px rgba(0,0,0,0.3);
                letter-spacing: 1px;
            }}
            
            .stamp::after {{
                content: '';
                position: absolute;
                width: 90px;
                height: 90px;
                background: var(--stamp-color);
                border-radius: 50%;
                transform: rotate(25deg);
                box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1);
                z-index: 20;
                background-image: url('data:image/svg+xml;utf8,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><filter id="texturizer"><feTurbulence type="turbulence" baseFrequency="0.1" numOctaves="2" seed="2"/><feDisplacementMap in="SourceGraphic" scale="8"/></filter><rect width="100" height="100" fill="none" filter="url(%23texturizer)"/></svg>');
                background-blend-mode: overlay;
            }}
            
            .stamp-impression {{
                position: absolute;
                width: 100%;
                height: 100%;
                border-radius: 50%;
                box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
                z-index: 21;
                background-image: url('data:image/svg+xml;utf8,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><filter id="emboss"><feGaussianBlur in="SourceAlpha" stdDeviation="2"/><feOffset dx="1" dy="1"/><feComposite in2="SourceGraphic" operator="arithmetic" k1="0" k2="1" k3="1" k4="0"/></filter><circle cx="50" cy="50" r="45" fill="none" stroke="black" stroke-width="2" filter="url(%23emboss)"/></svg>');
                opacity: 0.2;
            }}
            
            .stamp-border {{
                position: absolute;
                width: 100%;
                height: 100%;
                border: 2px dashed var(--stamp-color);
                border-radius: 50%;
                opacity: 0.5;
            }}
            
            .content {{
                position: relative;
                z-index: 10;
                padding-top: 30px;
            }}
            
            .header {{
                display: flex;
                align-items: flex-start;
                margin-bottom: 25px;
                animation: fadeIn 0.5s ease-out forwards 1.3s;
                opacity: 0;
            }}
            
            .date {{
                font-size: 14px;
                color: #666;
                margin-left: auto;
                transform: rotate(-2deg);
                position: relative;
            }}
            
            .date::after {{
                content: '';
                position: absolute;
                bottom: -3px;
                left: 0;
                width: 100%;
                height: 1px;
                background: #666;
                opacity: 0.3;
            }}
            
            .title {{
                position: relative;
                font-size: 32px;
                font-weight: bold;
                color: var(--ink-color);
                margin-bottom: 20px;
                transform: rotate(-1deg);
                opacity: 0;
                padding-right: 50px; /* Space for stamp */
                text-shadow: 1px 1px 1px rgba(0,0,0,0.1);
            }}
            
            .title-container {{
                position: relative;
                overflow: hidden;
            }}
            
            .title-underline {{
                position: absolute;
                bottom: -5px;
                left: 0;
                width: 0;
                height: 2px;
                background: var(--ink-color);
                animation: drawLine 0.6s ease-out forwards 1.8s;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                opacity: 0.7;
            }}
            
            .message {{
                font-size: 20px;
                color: #333;
                line-height: 1.5;
                margin-bottom: 30px;
                opacity: 0;
                position: relative;
                text-shadow: 0.5px 0.5px 0.5px rgba(0,0,0,0.1);
            }}
            
            .signature {{
                position: absolute;
                bottom: 30px;
                right: 30px;
                font-family: 'Caveat', cursive;
                font-size: 24px;
                font-weight: bold;
                color: var(--ink-color);
                transform: rotate(-5deg) translateY(20px);
                opacity: 0;
                z-index: 10;
                text-shadow: 1px 1px 1px rgba(0,0,0,0.15);
                position: relative;
            }}
            
            .signature-dash {{
                position: absolute;
                bottom: -5px;
                left: -10px;
                width: 0;
                height: 2px;
                background: var(--ink-color);
                opacity: 0.6;
                animation: signatureDash 0.4s ease-out forwards 3.2s;
            }}
            
            .ink-splatter {{
                position: absolute;
                background-repeat: no-repeat;
                background-size: contain;
                z-index: 1;
                opacity: 0;
                mix-blend-mode: multiply;
            }}
            
            .splatter-1 {{
                top: 10%;
                left: 5%;
                width: 90px;
                height: 90px;
                background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path fill="{stamp_color}" fill-opacity="0.2" d="M81.5,45.3C80.7,43.9,79.5,44.4,78,45.3C76.5,46.2,75.6,47.1,76.3,48.3C77.1,49.5,77.6,49.5,79.5,48.1C81.4,46.7,82.3,46.7,81.5,45.3z M76.4,39.3c0.3-1.5-0.4-2.2-2-1.7C73,38,71.5,39.3,71.8,40.7C72,42.1,73.3,42.4,74.8,41.3C76.3,40.3,76.1,40.8,76.4,39.3z M42.2,69.2c-1-1.7-2-1.3-3.5-0.3C37.2,69.8,36,71,37,72.7C38,74.4,39.1,74,40.6,72.9C42.1,71.8,43.1,70.9,42.2,69.2z M29.8,55.9c0.8-2.2-0.9-3.1-3.5-2.1C24.5,54.4,22,57.4,22.5,59C22.9,60.6,25.1,60,27.3,58.2C29.5,56.4,29.3,57.2,29.8,55.9z M55.2,68.5c2.7-0.2,4.7-3.4,4.4-6.9c-0.3-3.5-2.8-6.1-5.5-5.9c-2.7,0.2-4.7,3.4-4.4,6.9C50,66.1,52.5,68.7,55.2,68.5z M17.1,53.5c1.2-0.1,2-2,1.9-4.1c-0.1-2.1-1.2-3.8-2.4-3.7c-1.2,0.1-2,2-1.9,4.1C14.8,51.9,15.9,53.6,17.1,53.5z M56.4,41.8c1.4-0.1,2.4-2.2,2.3-4.6c-0.1-2.4-1.4-4.3-2.8-4.2c-1.4,0.1-2.4,2.2-2.3,4.6C53.8,40,55.1,41.9,56.4,41.8z M18.7,64.6c0.7-0.1,1.3-1.2,1.2-2.5c-0.1-1.3-0.7-2.3-1.5-2.2c-0.7,0.1-1.3,1.2-1.2,2.5C17.3,63.7,18,64.7,18.7,64.6z M60.5,76c1.1-0.1,1.9-1.8,1.8-3.7c-0.1-1.9-1.1-3.4-2.2-3.3c-1.1,0.1-1.9,1.8-1.8,3.7C58.4,74.6,59.4,76.1,60.5,76z M75.2,60.3c1.5-0.1,2.7-2.6,2.5-5.3c-0.1-2.8-1.5-4.9-3.1-4.8c-1.5,0.1-2.7,2.6-2.5,5.3C72.3,58.3,73.7,60.4,75.2,60.3z"/></svg>');
                animation: fadeInSplatter 0.4s ease-out forwards 2.1s;
                filter: hue-rotate(5deg);
            }}
            
            .splatter-2 {{
                bottom: 15%;
                right: 8%;
                width: 110px;
                height: 110px;
                transform: rotate(180deg);
                background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path fill="{stamp_color}" fill-opacity="0.15" d="M38.2,73.2c0.2-0.9-0.8-1.2-1.8-0.8c-1,0.4-1.9,1.3-1.6,2.1c0.3,0.8,1.2,0.7,2.2,0.1C37.9,74,38,74.1,38.2,73.2z M58.1,84.3c-0.5-1-1.3-0.9-2.3-0.2c-1,0.7-1.8,1.8-1.3,2.7c0.5,0.9,1.6,0.8,2.6,0C58.1,86,58.6,85.2,58.1,84.3z M41.9,30.7c-0.2-1-1.2-1-2.3-0.2c-1.1,0.8-1.9,2.1-1.7,3.1c0.2,1,1.4,0.8,2.5,0C41.5,32.9,42.1,31.7,41.9,30.7z M65.3,27.5c-0.5-1.2-1.7-1.2-3.3-0.1c-1.6,1.1-2.7,2.9-2.2,4.1c0.5,1.2,1.9,1,3.6-0.1C65,30.3,65.7,28.7,65.3,27.5z M27.4,55.8c1.5-0.4,2.1-2.5,1.2-4.6c-0.9-2.1-2.8-3.6-4.3-3.2c-1.5,0.4-2.1,2.5-1.2,4.6C24,54.7,25.9,56.2,27.4,55.8z M37.6,68.8c0.8-0.2,1.1-1.3,0.7-2.5c-0.5-1.2-1.5-2-2.3-1.8c-0.8,0.2-1.1,1.3-0.7,2.5C35.8,68.2,36.8,69,37.6,68.8z M39.8,47.9c0.9-0.2,1.3-1.6,0.8-3c-0.5-1.4-1.7-2.3-2.6-2.1c-0.9,0.2-1.3,1.6-0.8,3C37.7,47.2,38.9,48.1,39.8,47.9z M54.2,68.5c0.5-0.1,0.7-0.9,0.5-1.7c-0.3-0.8-0.9-1.3-1.4-1.2c-0.5,0.1-0.7,0.9-0.4,1.7C53.1,68.1,53.8,68.6,54.2,68.5z M69.2,59.8c0.7-0.2,1-1.2,0.6-2.3c-0.4-1.1-1.3-1.8-2-1.6c-0.7,0.2-1,1.2-0.6,2.3C67.6,59.3,68.5,60,69.2,59.8z M65.3,43.1c0.9-0.2,1.3-1.7,0.8-3.2c-0.4-1.5-1.6-2.6-2.6-2.4c-0.9,0.2-1.3,1.7-0.8,3.2C63.2,42.2,64.3,43.3,65.3,43.1z M75,83.9c-0.5-0.1-1,0.5-1.1,1.5c-0.1,0.9,0.3,1.8,0.8,1.9c0.5,0.1,1-0.5,1.1-1.5C75.9,84.9,75.5,84,75,83.9z M78.4,65.1c-0.8-0.1-1.5,0.8-1.7,2.1c-0.2,1.3,0.4,2.5,1.2,2.6c0.8,0.1,1.5-0.8,1.7-2.1C79.7,66.4,79.2,65.2,78.4,65.1z M83.3,46.3c-0.3-1.2-1.4-1.8-2.6-1.5c-1.2,0.3-1.9,1.6-1.6,2.8c0.3,1.2,1.4,1.8,2.6,1.5C82.9,48.8,83.6,47.5,83.3,46.3z"/></svg>');
                animation: fadeInSplatter 0.4s ease-out forwards 2.3s;
                filter: hue-rotate(-5deg);
            }}

            .splatter-3 {{
                top: 60%;
                left: 15%;
                width: 80px;
                height: 80px;
                transform: rotate(45deg);
                background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path fill="{stamp_color}" fill-opacity="0.1" d="M50.9,26.2c-1.9-2.3-4.4-1.2-7.1,1.7c-2.8,2.9-4.7,6.5-2.8,8.8c1.9,2.3,5.1,1.1,7.9-1.8C51.7,32,52.8,28.5,50.9,26.2z M57.9,39.9c2.7-0.3,4.3-3.2,3.6-6.5c-0.7-3.3-3.5-5.8-6.2-5.5c-2.7,0.3-4.3,3.2-3.6,6.5C52.4,37.7,55.2,40.2,57.9,39.9z M47.6,39.9c-2.3-2.3-5.6-2.3-7.5,0c-1.9,2.3-1.6,6,0.7,8.3c2.3,2.3,5.6,2.3,7.5,0C50.2,45.9,49.9,42.2,47.6,39.9z M40.8,64.9c-1.1-1.2-3.2-0.9-4.7,0.7c-1.5,1.6-1.9,3.9-0.7,5.1c1.1,1.2,3.2,0.9,4.7-0.7C41.5,68.4,41.9,66.1,40.8,64.9z M55.6,64.4c-2.1-1.1-4.9,0.3-6.3,3.2c-1.3,2.9-0.7,6.1,1.4,7.2c2.1,1.1,4.9-0.3,6.3-3.2C58.3,68.7,57.7,65.5,55.6,64.4z"/></svg>');
                animation: fadeInSplatter 0.4s ease-out forwards 2.5s;
                filter: hue-rotate(15deg);
            }}
            
            /* 3D paper floating effect */
            @keyframes paperFloat {{
                0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
                25% {{ transform: translateY(-2px) rotate(0.3deg); }}
                75% {{ transform: translateY(2px) rotate(-0.3deg); }}
            }}
            
            /* Animations */
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            
            @keyframes fadeOut {{
                from {{ opacity: 1; }}
                to {{ opacity: 0; }}
            }}
            
            @keyframes slideUp {{
                from {{ transform: translateY(100vh) rotateX(-20deg) rotateY(5deg); }}
                to {{ transform: translateY(0) rotateX(0deg) rotateY(0deg); }}
            }}
            
            @keyframes unfold {{
                0% {{ transform: rotateX(-90deg); box-shadow: 0 5px 15px var(--paper-shadow); }}
                40% {{ box-shadow: 0 15px 25px var(--paper-shadow); }}
                100% {{ transform: rotateX(0deg); box-shadow: 0 20px 40px var(--paper-shadow); animation-timing-function: cubic-bezier(0.22, 0.61, 0.36, 1); }}
            }}
            
            @keyframes drawLine {{
                0% {{ width: 0; opacity: 0.4; }}
                50% {{ opacity: 0.7; }}
                100% {{ width: 100%; opacity: 0.5; }}
            }}
            
            @keyframes showCrease {{
                from {{ opacity: 0; }}
                to {{ opacity: 0.6; }}
            }}
            
            @keyframes stampAppear {{
                0% {{ opacity: 0; transform: scale(1.5) rotate(10deg); filter: blur(5px); }}
                40% {{ opacity: 0.9; transform: scale(1.2) rotate(15deg); filter: blur(1px); }}
                60% {{ opacity: 0.8; transform: scale(1.1) rotate(25deg); filter: blur(0); }}
                80% {{ opacity: 0.8; transform: scale(0.9) rotate(20deg); }}
                100% {{ opacity: 0.8; transform: scale(1) rotate(25deg); }}
            }}
            
            @keyframes fadeInSplatter {{
                from {{ opacity: 0; transform: scale(0.8) rotate(var(--rotation, 0deg)); }}
                to {{ opacity: 1; transform: scale(1) rotate(var(--rotation, 0deg)); }}
            }}
            
            @keyframes fadeOutPaper {{
                0% {{ transform: rotateX(0deg); opacity: 1; }}
                100% {{ transform: rotateX(90deg); opacity: 0; }}
            }}
            
            @keyframes slideDown {{
                from {{ transform: translateY(0) rotateX(0deg) rotateY(0deg); }}
                to {{ transform: translateY(100vh) rotateX(20deg) rotateY(-5deg); }}
            }}
            
            @keyframes signatureDash {{
                from {{ width: 0; }}
                to {{ width: calc(100% + 20px); }}
            }}
            
            /* Handwriting animation for text */
            @keyframes handwriting {{
                0% {{ clip-path: polygon(0 0, 0 0, 0 100%, 0 100%); }}
                100% {{ clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }}
            }}
        </style>
    </head>
    <body>
        <div class="backdrop"></div>
        
        <div class="paper-container">
            <div class="paper">
                <div class="paper-texture"></div>
                <div class="paper-lines"></div>
                <div class="paper-crease"></div>
                <div class="paper-crease paper-crease-2"></div>
                <div class="paper-crease paper-crease-horizontal"></div>
                
                <div class="content">
                    <div class="header">
                        <div class="date" id="current-date"></div>
                    </div>
                    
                    <div class="title-container">
                        <div class="title" id="title-text">{title}</div>
                        <div class="title-underline"></div>
                    </div>
                    
                    <div class="message" id="message-text">{message}</div>
                    
                    <div class="signature">
                        System
                        <div class="signature-dash"></div>
                    </div>
                </div>
                
                <div class="stamp">
                    <div class="stamp-border"></div>
                    <div class="stamp-impression"></div>
                </div>
                
                <div class="ink-splatter splatter-1"></div>
                <div class="ink-splatter splatter-2"></div>
                <div class="ink-splatter splatter-3"></div>
            </div>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                // Set current date
                const now = new Date();
                const options = {{ month: 'short', day: 'numeric', year: 'numeric' }};
                document.getElementById('current-date').textContent = now.toLocaleDateString('en-US', options);
                
                // Apply floating animation to paper after it unfolds
                setTimeout(() => {{
                    document.querySelector('.paper').style.animation = 'paperFloat 8s ease-in-out infinite';
                }}, 1400);
                
                // Animate text appearing with improved typewriter effect
                const titleEl = document.getElementById('title-text');
                const messageEl = document.getElementById('message-text');
                
                setTimeout(() => {{
                    typeWriter(titleEl, titleEl.textContent, 0, 40, 0.85);
                }}, 1300);
                
                setTimeout(() => {{
                    typeWriter(messageEl, messageEl.textContent, 0, 25, 0.9);
                }}, 1800);
                
                // Animate signature with handwriting effect
                setTimeout(() => {{
                    document.querySelector('.signature').style.animation = 'fadeIn 0.5s ease-out forwards';
                    document.querySelector('.signature').style.transform = 'rotate(-5deg) translateY(0)';
                }}, 2800);
                
                // Add subtle paper movement on hover
                document.querySelector('.paper').addEventListener('mousemove', function(e) {{
                    const xPos = (e.clientX / window.innerWidth) - 0.5;
                    const yPos = (e.clientY / window.innerHeight) - 0.5;
                    
                    this.style.transform = `rotateY(${{xPos * 5}}deg) rotateX(${{-yPos * 5}}deg)`;
                }});
                
                document.querySelector('.paper').addEventListener('mouseleave', function() {{
                    this.style.transform = 'rotateY(0deg) rotateX(0deg)';
                    this.style.animation = 'paperFloat 8s ease-in-out infinite';
                }});
                
                // Set timeout for redirect
                setTimeout(() => {{
                    document.querySelector('.paper').style.animation = 'fadeOutPaper 0.8s cubic-bezier(0.22, 0.61, 0.36, 1) forwards';
                    document.querySelector('.paper-container').style.animation = 'slideDown 0.8s cubic-bezier(0.22, 0.61, 0.36, 1) forwards 0.4s';
                    document.querySelector('.backdrop').style.animation = 'fadeOut 0.5s ease-out forwards 0.8s';
                    
                    setTimeout(() => {{
                        window.location = '{redirect_url}';
                    }}, 1300);
                }}, 5000); // Increased display time so users can see all animations
            }});
            
            function typeWriter(element, text, index, speed, randomness = 0.5) {{
                if (index < text.length) {{
                    element.textContent = text.substring(0, index + 1);
                    element.style.opacity = '1';
                    
                    // Add randomness to typing speed for more natural effect
                    const randomSpeed = speed * (1 - randomness + Math.random() * randomness * 2);
                    
                    setTimeout(() => {{
                        typeWriter(element, text, index + 1, speed, randomness);
                    }}, randomSpeed);
                }}
            }}
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def login(request):
    return render(request,'login.html')

def category(request):
    return render(request,'category.html')

def cataction(request):
    cursor=connection.cursor()
    cat=request.GET['category']
    desc=request.GET['description']
    sql="INSERT INTO category(Cname,Description)VALUES('%s','%s')"%(cat,desc)
    cursor.execute(sql)
    
    # Create a simple light blue notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Category Added</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #64B5F6, #2196F3);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-check"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Category Added</div>
                <div class="notification-subtext">Category has been successfully added</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/category/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def product(request):
    cursor=connection.cursor()
    sql="select * from subcategory"
    cursor.execute(sql)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Subid':row[0], 'Subcategoryname':row[1],'Category':row[2],'Description':row[3]}
        tt.append(q)
    return render(request,'product.html',{'tt':tt})

    
def prodaction(request):
    if request.method == "POST":
        MyProfileForm = pform(request.POST, request.FILES)
        if MyProfileForm.is_valid():
            profile = pmodel()
            profile.Item = request.POST["Item"]
            profile.Category = request.POST["category"]
            profile.Subcategory = request.POST["subcat"]
            profile.Des = request.POST["description"]
            profile.Amnt = request.POST["amount"]
            profile.Stock = request.POST["stock"]
            profile.Img = MyProfileForm.cleaned_data["Img"]
            profile.save()
            
            # Create HTML response with animated notification in LIGHT BLUE
            html_response = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Product Added</title>
                <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
                <style>
                    * { margin: 0; padding: 0; box-sizing: border-box; }
                    body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
                    .notification-wrapper {
                        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                        display: flex; justify-content: center; align-items: center;
                        background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                        z-index: 1000;
                    }
                    .notification-container {
                        position: relative; background: rgba(255, 255, 255, 0.95);
                        border-radius: 24px; padding: 2rem;
                        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                        animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                        max-width: 90%; width: 400px;
                    }
                    .icon-circle {
                        width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                        border-radius: 50%; display: flex; align-items: center;
                        justify-content: center; margin: 0 auto 1.5rem;
                        position: relative; overflow: hidden;
                        animation: popIn 0.5s ease-out forwards;
                        transform: scale(0);
                    }
                    .icon-circle i {
                        color: white; font-size: 32px;
                        transform: scale(0) rotate(-180deg);
                        animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
                    }
                    .ripple {
                        position: absolute; width: 100%; height: 100%;
                        border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                        animation: rippleEffect 1.5s linear infinite;
                    }
                    .notification-text, .notification-subtext {
                        text-align: center; opacity: 0;
                        animation: textFadeIn 0.5s ease 0.6s forwards;
                    }
                    .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
                    .notification-subtext { color: #666; font-size: 1rem; }
                    .progress-bar {
                        position: absolute; bottom: 0; left: 0; height: 4px;
                        background: linear-gradient(to right, #64B5F6, #2196F3);
                        width: 100%; animation: progress 2s linear forwards;
                    }

                    /* Animations */
                    @keyframes popIn {
                        0% { transform: scale(0); }
                        80% { transform: scale(1.2); }
                        100% { transform: scale(1); }
                    }
                    @keyframes tickBounce {
                        0% { transform: scale(0) rotate(-180deg); }
                        80% { transform: scale(1.2) rotate(10deg); }
                        100% { transform: scale(1) rotate(0deg); }
                    }
                    @keyframes rippleEffect {
                        0% { width: 0; height: 0; opacity: 0.5; }
                        100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
                    }
                    @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                    @keyframes progress { from { width: 100%; } to { width: 0%; } }
                    @keyframes fadeOut { to { opacity: 0; } }
                </style>
            </head>
            <body>
                <div class="notification-wrapper">
                    <div class="notification-container">
                        <div class="icon-circle">
                            <i class="fas fa-check"></i>
                            <div class="ripple"></div>
                        </div>
                        <div class="notification-text">Product Added</div>
                        <div class="notification-subtext">Your product has been successfully added</div>
                        <div class="progress-bar"></div>
                    </div>
                </div>
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        setTimeout(() => {
                            document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                            setTimeout(() => { window.location = '/product/'; }, 500);
                        }, 2000);
                    });
                </script>
            </body>
            </html>
            """
            return HttpResponse(html_response)
        else:
            # If form is invalid, keep light blue for consistency but use X icon
            error_html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Error</title>
                <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
                <style>
                    * { margin: 0; padding: 0; box-sizing: border-box; }
                    body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
                    .notification-wrapper {
                        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                        display: flex; justify-content: center; align-items: center;
                        background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                        z-index: 1000;
                    }
                    .notification-container {
                        position: relative; background: rgba(255, 255, 255, 0.95);
                        border-radius: 24px; padding: 2rem;
                        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                        animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                        max-width: 90%; width: 400px;
                    }
                    .icon-circle {
                        width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                        border-radius: 50%; display: flex; align-items: center;
                        justify-content: center; margin: 0 auto 1.5rem;
                        position: relative; overflow: hidden;
                        animation: popIn 0.5s ease-out forwards;
                        transform: scale(0);
                    }
                    .icon-circle i {
                        color: white; font-size: 32px;
                        transform: scale(0);
                        animation: errorBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
                    }
                    .ripple {
                        position: absolute; width: 100%; height: 100%;
                        border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                        animation: rippleEffect 1.5s linear infinite;
                    }
                    .notification-text, .notification-subtext {
                        text-align: center; opacity: 0;
                        animation: textFadeIn 0.5s ease 0.6s forwards;
                    }
                    .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
                    .notification-subtext { color: #666; font-size: 1rem; }
                    .progress-bar {
                        position: absolute; bottom: 0; left: 0; height: 4px;
                        background: linear-gradient(to right, #64B5F6, #2196F3);
                        width: 100%; animation: progress 2s linear forwards;
                    }

                    /* Animations */
                    @keyframes popIn {
                        0% { transform: scale(0); }
                        80% { transform: scale(1.2); }
                        100% { transform: scale(1); }
                    }
                    @keyframes errorBounce {
                        0% { transform: scale(0); }
                        80% { transform: scale(1.2); }
                        100% { transform: scale(1); }
                    }
                    @keyframes rippleEffect {
                        0% { width: 0; height: 0; opacity: 0.5; }
                        100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
                    }
                    @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                    @keyframes progress { from { width: 100%; } to { width: 0%; } }
                    @keyframes fadeOut { to { opacity: 0; } }
                </style>
            </head>
            <body>
                <div class="notification-wrapper">
                    <div class="notification-container">
                        <div class="icon-circle">
                            <i class="fas fa-exclamation"></i>
                            <div class="ripple"></div>
                        </div>
                        <div class="notification-text">Form Error</div>
                        <div class="notification-subtext">Please check your inputs and try again</div>
                        <div class="progress-bar"></div>
                    </div>
                </div>
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        setTimeout(() => {
                            document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                            setTimeout(() => { window.location = '/product/'; }, 500);
                        }, 2000);
                    });
                </script>
            </body>
            </html>
            """
            return HttpResponse(error_html)
    else:
        MyProfileForm = pform()
        # Return a basic form or redirect to the product page
        return HttpResponseRedirect('/product/')
   

def location(request):
    cursor=connection.cursor()
    sql="select * from location"
    cursor.execute(sql)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Locid':row[0], 'Location':row[1],'Area': row[2],'Rate':row[3],'Corate':row[4]}
        tt.append(q)
    return render(request,'location.html',{'tt':tt}) 
    
def locaction(request):
    cursor=connection.cursor()
    loc=request.GET['location']
    area=request.GET['address']
    rate=request.GET['rate']
    corate=request.GET['comrate']
    sql="INSERT INTO location(Location,Area,Rate,Corate)VALUES('%s','%s','%s','%s')"%(loc,area,rate,corate)
    cursor.execute(sql)
    
    # Create animated notification with light blue color
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Location Added</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #64B5F6, #2196F3);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-check"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Location Added</div>
                <div class="notification-subtext">Location has been successfully added</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewlocation/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def loginaction(request):
    cursor = connection.cursor()
    un = request.GET['login']
    up = request.GET['password']
    s = "SELECT * FROM login WHERE Uname='%s' AND Upass='%s'" % (un, up)
    cursor.execute(s)
    if (cursor.rowcount) > 0:
        rs = cursor.fetchall()
        for row in rs:
            request.session['Uid'] = row[1]
            request.session['Uname'] = row[2]
            request.session['Upass'] = row[3]
            request.session['Utype'] = row[4]
        
        # Get user data for personalization
        user_type = request.session['Utype']
        user_name = request.session['Uname']
        
        # Enhanced theme configurations with gradients and expanded colors
        theme_config = {
            'admin': {
                'primary': '#6366F1',
                'primary_dark': '#4F46E5',
                'secondary': '#A78BFA',
                'accent': '#C4B5FD',
                'light': '#EEF2FF',
                'icon': 'fa-crown',
                'greeting': 'Welcome back, Administrator',
                'pattern': 'radial',
                'gradient': 'linear-gradient(135deg, #6366F1 0%, #4F46E5 50%, #4338CA 100%)',
                'accent_gradient': 'linear-gradient(135deg, #C4B5FD 0%, #A78BFA 100%)',
                'font': "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                'highlights': ['#818CF8', '#8B5CF6', '#6D28D9']
            },
            'customer': {
                'primary': '#0EA5E9',
                'primary_dark': '#0284C7',
                'secondary': '#38BDF8',
                'accent': '#BAE6FD',
                'light': '#F0F9FF',
                'icon': 'fa-user',
                'greeting': 'Welcome back',
                'pattern': 'wave',
                'gradient': 'linear-gradient(135deg, #0EA5E9 0%, #0284C7 50%, #0369A1 100%)',
                'accent_gradient': 'linear-gradient(135deg, #BAE6FD 0%, #38BDF8 100%)',
                'font': "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                'highlights': ['#7DD3FC', '#38BDF8', '#0284C7']
            },
            'employee': {
                'primary': '#10B981',
                'primary_dark': '#059669',
                'secondary': '#34D399',
                'accent': '#A7F3D0',
                'light': '#ECFDF5',
                'icon': 'fa-briefcase',
                'greeting': 'Welcome back, Staff Member',
                'pattern': 'hex',
                'gradient': 'linear-gradient(135deg, #10B981 0%, #059669 50%, #047857 100%)',
                'accent_gradient': 'linear-gradient(135deg, #A7F3D0 0%, #34D399 100%)',
                'font': "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                'highlights': ['#6EE7B7', '#34D399', '#059669']
            }
        }
        
        # Get theme based on user type (default to customer)
        theme = theme_config.get(user_type, theme_config['customer'])
        
        # Generate sophisticated background pattern SVG
        pattern_svg = ""
        if theme['pattern'] == 'wave':
            pattern_svg = f"""url("data:image/svg+xml,%3Csvg width='100' height='50' viewBox='0 0 100 50' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 25C20 25 20 0 40 0C60 0 60 25 80 25C100 25 100 0 120 0V50H0V25Z' fill='{theme['accent'].replace('#', '%23')}'/%3E%3C/svg%3E")"""
        elif theme['pattern'] == 'hex':
            pattern_svg = f"""url("data:image/svg+xml,%3Csvg width='56' height='100' viewBox='0 0 56 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M28 0L56 25V75L28 100L0 75V25L28 0Z' stroke='{theme['accent'].replace('#', '%23')}' fill='none' stroke-width='1'/%3E%3C/svg%3E")"""
        else:  # radial
            pattern_svg = f"""url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='50' cy='50' r='25' stroke='{theme['accent'].replace('#', '%23')}' fill='none' stroke-width='1.5'/%3E%3C/svg%3E")"""
        
        # Generate particle colors JavaScript array with highlights
        particle_colors = theme['highlights'] + [theme['primary'], theme['secondary'], theme['accent']]
        particle_colors_js = str(particle_colors).replace("'", '"')
        
        success_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome {user_name}</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                :root {{
                    --primary: {theme['primary']};
                    --primary-dark: {theme['primary_dark']};
                    --secondary: {theme['secondary']};
                    --accent: {theme['accent']};
                    --light: {theme['light']};
                    --text-primary: #1E293B;
                    --text-secondary: #64748B;
                    --bg-main: #F8FAFC;
                    --bg-card: #FFFFFF;
                    --shadow-xs: 0 1px 2px rgba(16, 24, 40, 0.05);
                    --shadow-sm: 0 1px 3px rgba(16, 24, 40, 0.1), 0 1px 2px rgba(16, 24, 40, 0.06);
                    --shadow-md: 0 4px 8px -2px rgba(16, 24, 40, 0.1), 0 2px 4px -2px rgba(16, 24, 40, 0.06);
                    --shadow-lg: 0 12px 16px -4px rgba(16, 24, 40, 0.08), 0 4px 6px -2px rgba(16, 24, 40, 0.03);
                    --shadow-xl: 0 20px 24px -4px rgba(16, 24, 40, 0.08), 0 8px 8px -4px rgba(16, 24, 40, 0.03);
                    --shadow-2xl: 0 24px 48px -12px rgba(16, 24, 40, 0.25);
                    --shadow-inner: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
                    --easing: cubic-bezier(0.22, 1, 0.36, 1);
                    --primary-rgb: 0, 0, 0; /* Will be set by JS */
                    --gradient: {theme['gradient']};
                    --accent-gradient: {theme['accent_gradient']};
                    --font-family: {theme['font']};
                }}
                
                * {{ 
                    margin: 0; 
                    padding: 0; 
                    box-sizing: border-box; 
                }}
                
                body {{ 
                    font-family: var(--font-family);
                    background-color: var(--bg-main);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    overflow: hidden;
                    color: var(--text-primary);
                    position: relative;
                }}
                
                /* Enhanced morphing background */
                .bg-morphing {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: -2;
                    background: 
                        radial-gradient(circle at 15% 50%, rgba(var(--primary-rgb), 0.08) 0%, transparent 40%),
                        radial-gradient(circle at 85% 30%, rgba(var(--primary-rgb), 0.05) 0%, transparent 40%),
                        radial-gradient(circle at 50% 80%, rgba(var(--primary-rgb), 0.07) 0%, transparent 50%);
                    filter: blur(50px);
                    animation: morphBackground 20s ease-in-out infinite alternate;
                }}
                
                @keyframes morphBackground {{
                    0% {{ 
                        background-position: 0% 0%, 100% 0%, 50% 100%;
                        background-size: 70% 70%, 50% 50%, 60% 60%;
                    }}
                    50% {{ 
                        background-position: 10% 20%, 90% 40%, 40% 80%;
                        background-size: 60% 60%, 70% 70%, 50% 50%;
                    }}
                    100% {{ 
                        background-position: 0% 40%, 100% 30%, 50% 90%;
                        background-size: 50% 50%, 60% 60%, 70% 70%;
                    }}
                }}
                
                /* Background patterns */
                .bg-pattern {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: -1;
                    opacity: 0.25;
                    background-image: {pattern_svg};
                    background-size: 800px 800px;
                    animation: patternFloat 120s linear infinite;
                }}
                
                @keyframes patternFloat {{
                    0% {{ background-position: 0 0; }}
                    100% {{ background-position: 800px 800px; }}
                }}
                
                .login-success {{
                    position: relative;
                    width: 550px;
                    background-color: var(--bg-card);
                    border-radius: 32px;
                    box-shadow: var(--shadow-xl), 0 0 0 1px rgba(16, 24, 40, 0.06);
                    overflow: hidden;
                    transform: translateY(30px);
                    opacity: 0;
                    animation: slideUpFadeIn 1s var(--easing) forwards;
                    backdrop-filter: blur(10px);
                    background: rgba(255, 255, 255, 0.85);
                }}
                
                @keyframes slideUpFadeIn {{
                    0% {{ transform: translateY(30px) scale(0.97); opacity: 0; filter: blur(5px); }}
                    60% {{ transform: translateY(-5px) scale(1.02); opacity: 0.9; filter: blur(0px); }}
                    100% {{ transform: translateY(0) scale(1); opacity: 1; filter: blur(0px); }}
                }}
                
                .success-header {{
                    background: var(--gradient);
                    height: 200px;
                    position: relative;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    overflow: hidden;
                }}
                
                /* Enhanced background layers with 3D parallax effect */
                .bg-layer {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    opacity: 0.8;
                    will-change: transform;
                }}
                
                .layer-1 {{
                    background: radial-gradient(circle at 20% 50%, var(--secondary) 0%, transparent 50%);
                    animation: parallaxLayer 15s ease-in-out infinite alternate;
                }}
                
                .layer-2 {{
                    background: radial-gradient(circle at 80% 30%, var(--accent) 0%, transparent 50%);
                    animation: parallaxLayer 12s ease-in-out 2s infinite alternate-reverse;
                }}
                
                .layer-3 {{
                    background: radial-gradient(circle at 50% 80%, var(--primary-dark) 0%, transparent 40%);
                    animation: parallaxLayer 10s ease-in-out 1s infinite alternate;
                }}
                
                @keyframes parallaxLayer {{
                    0% {{ opacity: 0.4; transform: translateX(-5px) translateY(-5px) scale(1); }}
                    50% {{ opacity: 0.6; transform: translateX(5px) translateY(5px) scale(1.1); }}
                    100% {{ opacity: 0.4; transform: translateX(-5px) translateY(-5px) scale(1); }}
                }}
                
                /* Advanced animated particles with varied sizes and shapes */
                .particles-container {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    overflow: hidden;
                    z-index: 2;
                }}
                
                .particle {{
                    position: absolute;
                    pointer-events: none;
                    will-change: transform;
                }}
                
                /* Glow effect with dynamic shadows */
                .glow-effect {{
                    position: absolute;
                    width: 300px;
                    height: 300px;
                    background: radial-gradient(circle, var(--accent) 0%, transparent 70%);
                    border-radius: 50%;
                    opacity: 0.4;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    z-index: 1;
                    filter: blur(20px);
                    animation: pulsateGlow 6s ease-in-out infinite;
                }}
                
                @keyframes pulsateGlow {{
                    0% {{ transform: translate(-50%, -50%) scale(0.8); opacity: 0.3; }}
                    50% {{ transform: translate(-50%, -50%) scale(1.4); opacity: 0.5; }}
                    100% {{ transform: translate(-50%, -50%) scale(0.8); opacity: 0.3; }}
                }}
                
                .logo-container {{
                    position: relative;
                    z-index: 3;
                    width: 110px;
                    height: 110px;
                    background: rgba(255, 255, 255, 0.9);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: var(--shadow-lg), 0 0 0 8px rgba(255, 255, 255, 0.15), 0 0 30px 5px rgba(0, 0, 0, 0.1);
                    animation: logoRevealEnhanced 1.2s var(--easing) forwards;
                    opacity: 0;
                    transform: scale(0.5) translateY(20px);
                    backdrop-filter: blur(5px);
                }}
                
                @keyframes logoRevealEnhanced {{
                    0% {{ opacity: 0; transform: scale(0.5) translateY(20px) rotate(-10deg); }}
                    40% {{ opacity: 0.8; transform: scale(1.15) translateY(-10px) rotate(5deg); }}
                    60% {{ opacity: 1; transform: scale(0.95) translateY(-5px) rotate(0deg); }}
                    80% {{ transform: scale(1.05) translateY(2px); }}
                    100% {{ opacity: 1; transform: scale(1) translateY(0); }}
                }}
                
                /* Logo ring animation */
                .logo-ring {{
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    border-radius: 50%;
                    border: 2px solid rgba(255, 255, 255, 0.5);
                    animation: ringPulse 3s ease-in-out infinite;
                }}
                
                .logo-ring-1 {{
                    animation-delay: 0s;
                }}
                
                .logo-ring-2 {{
                    animation-delay: 1s;
                }}
                
                @keyframes ringPulse {{
                    0% {{ transform: scale(0.95); opacity: 0.5; }}
                    50% {{ transform: scale(1.15); opacity: 0; }}
                    100% {{ transform: scale(0.95); opacity: 0.5; }}
                }}
                
                .logo-container i {{
                    font-size: 42px;
                    background: var(--gradient);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    animation: iconPopEnhanced 0.6s ease-out 0.9s forwards;
                    opacity: 0;
                    transform: scale(0);
                    filter: drop-shadow(0 0 2px rgba(var(--primary-rgb), 0.2));
                }}
                
                @keyframes iconPopEnhanced {{
                    0% {{ opacity: 0; transform: scale(0) rotate(-45deg); filter: blur(10px); }}
                    40% {{ opacity: 0.8; transform: scale(1.2) rotate(15deg); filter: blur(0px); }}
                    60% {{ opacity: 1; transform: scale(0.9) rotate(-5deg); }}
                    80% {{ transform: scale(1.1) rotate(2deg); }}
                    100% {{ opacity: 1; transform: scale(1) rotate(0deg); }}
                }}
                
                .success-body {{
                    padding: 40px 35px 40px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    position: relative;
                }}
                
                .verified-badge {{
                    position: absolute;
                    top: -22px;
                    background: var(--gradient);
                    color: white;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 10px 20px;
                    border-radius: 40px;
                    box-shadow: var(--shadow-md), 0 0 0 4px rgba(255, 255, 255, 0.9);
                    animation: badgeSlideInEnhanced 0.6s var(--easing) 0.3s forwards, 
                               badgePulseEnhanced 3s ease-in-out 1.5s infinite;
                    opacity: 0;
                    transform: translateY(20px);
                    backdrop-filter: blur(4px);
                }}
                
                @keyframes badgeSlideInEnhanced {{
                    0% {{ opacity: 0; transform: translateY(20px) scale(0.8); filter: blur(5px); }}
                    70% {{ opacity: 1; transform: translateY(-5px) scale(1.05); filter: blur(0px); }}
                    100% {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0px); }}
                }}
                
                @keyframes badgePulseEnhanced {{
                    0% {{ box-shadow: var(--shadow-md), 0 0 0 4px rgba(255, 255, 255, 0.9), 0 0 0 0 rgba(var(--primary-rgb), 0.5); }}
                    50% {{ box-shadow: var(--shadow-md), 0 0 0 4px rgba(255, 255, 255, 0.9), 0 0 25px 8px rgba(var(--primary-rgb), 0.3); }}
                    100% {{ box-shadow: var(--shadow-md), 0 0 0 4px rgba(255, 255, 255, 0.9), 0 0 0 0 rgba(var(--primary-rgb), 0.5); }}
                }}
                
                .welcome-message {{
                    margin-top: 15px;
                    text-align: center;
                }}
                
                .welcome-title {{
                    font-size: 28px;
                    font-weight: 700;
                    margin-bottom: 8px;
                    background: var(--gradient);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    text-fill-color: transparent;
                    opacity: 0;
                    animation: fadeUpTitleEnhanced 0.8s ease 0.5s forwards;
                }}
                
                @keyframes fadeUpTitleEnhanced {{
                    0% {{ opacity: 0; transform: translateY(15px); filter: blur(8px); }}
                    60% {{ opacity: 0.9; transform: translateY(-5px); filter: blur(0px); }}
                    100% {{ opacity: 1; transform: translateY(0); filter: blur(0px); }}
                }}
                
                .welcome-subtitle {{
                    color: var(--text-secondary);
                    font-size: 16px;
                    font-weight: 400;
                    opacity: 0;
                    animation: fadeUpEnhanced 0.6s ease 0.7s forwards;
                }}
                
                @keyframes fadeUpEnhanced {{
                    0% {{ opacity: 0; transform: translateY(15px); filter: blur(4px); }}
                    60% {{ opacity: 0.9; transform: translateY(-3px); filter: blur(0px); }}
                    100% {{ opacity: 1; transform: translateY(0); filter: blur(0px); }}
                }}
                
                .status-card {{
                    margin-top: 35px;
                    background-color: rgba(255, 255, 255, 0.7);
                    border-radius: 24px;
                    padding: 25px;
                    width: 100%;
                    box-shadow: var(--shadow-sm), 0 0 0 1px rgba(226, 232, 240, 0.6);
                    opacity: 0;
                    transform: translateY(15px) scale(0.98);
                    animation: cardRevealEnhanced 0.8s var(--easing) 0.9s forwards;
                    backdrop-filter: blur(10px);
                    border-top: 1px solid rgba(255, 255, 255, 0.8);
                    border-left: 1px solid rgba(255, 255, 255, 0.8);
                }}
                
                @keyframes cardRevealEnhanced {{
                    0% {{ opacity: 0; transform: translateY(15px) scale(0.98); filter: blur(5px); }}
                    60% {{ opacity: 0.9; transform: translateY(-5px) scale(1.01); filter: blur(0px); }}
                    100% {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0px); }}
                }}
                
                .status-item {{
                    display: flex;
                    align-items: center;
                    margin-bottom: 20px;
                    opacity: 0;
                    animation-name: statusItemFadeEnhanced;
                    animation-duration: 0.6s;
                    animation-fill-mode: forwards;
                    animation-timing-function: var(--easing);
                    transform-origin: left center;
                }}
                
                .status-item:nth-child(1) {{
                    animation-delay: 1.2s;
                }}
                
                .status-item:nth-child(2) {{
                    animation-delay: 1.4s;
                }}
                
                .status-item:last-child {{
                    margin-bottom: 0;
                }}
                
                @keyframes statusItemFadeEnhanced {{
                    0% {{ opacity: 0; transform: translateX(-15px) scale(0.95); filter: blur(4px); }}
                    60% {{ opacity: 0.9; transform: translateX(5px) scale(1.02); filter: blur(0px); }}
                    100% {{ opacity: 1; transform: translateX(0) scale(1); filter: blur(0px); }}
                }}
                
                .status-icon {{
                    width: 52px;
                    height: 52px;
                    border-radius: 16px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 20px;
                    position: relative;
                    overflow: hidden;
                }}
                
                .status-icon::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: var(--gradient);
                    opacity: 0.9;
                    z-index: 1;
                }}
                
                /* Enhanced shimmer effect */
                .status-icon::after {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 200%;
                    height: 100%;
                    background: linear-gradient(90deg, 
                        transparent 0%, 
                        rgba(255, 255, 255, 0.1) 20%, 
                        rgba(255, 255, 255, 0.3) 50%, 
                        rgba(255, 255, 255, 0.1) 80%, 
                        transparent 100%);
                    animation: shimmerEnhanced 2.5s infinite;
                    z-index: 2;
                }}
                
                @keyframes shimmerEnhanced {{
                    0% {{ transform: translateX(-100%) skewX(-15deg); }}
                    100% {{ transform: translateX(50%) skewX(-15deg); }}
                }}
                
                .status-icon i {{
                    color: white;
                    font-size: 20px;
                    position: relative;
                    z-index: 3;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                
                .status-text {{
                    flex: 1;
                }}
                
                .status-label {{
                    font-size: 16px;
                    font-weight: 600;
                    margin-bottom: 3px;
                    color: var(--text-primary);
                }}
                
                .status-value {{
                    font-size: 15px;
                    color: var(--text-secondary);
                }}
                
                .progress-container {{
                    margin-top: 35px;
                    width: 100%;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    opacity: 0;
                    animation: fadeUpEnhanced 0.6s ease 1.6s forwards;
                }}
                
                .progress-label {{
                    font-size: 14px;
                    color: var(--text-secondary);
                    margin-bottom: 12px;
                    display: flex;
                    width: 100%;
                    justify-content: space-between;
                    font-weight: 500;
                }}
                
                .progress-time {{
                    font-weight: 600;
                    color: var(--primary);
                    position: relative;
                }}
                
                /* Countdown highlight effect */
                .progress-time::before {{
                    content: '';
                    position: absolute;
                    top: -4px;
                    left: -6px;
                    right: -6px;
                    bottom: -4px;
                    background-color: var(--accent);
                    border-radius: 10px;
                    opacity: 0.3;
                    z-index: -1;
                    animation: pulseBg 2s infinite;
                }}
                
                @keyframes pulseBg {{
                    0% {{ opacity: 0.2; transform: scale(0.95); }}
                    50% {{ opacity: 0.4; transform: scale(1.05); }}
                    100% {{ opacity: 0.2; transform: scale(0.95); }}
                }}
                
                .progress-bar {{
                    width: 100%;
                    height: 10px;
                    background-color: #E2E8F0;
                    border-radius: 8px;
                    overflow: hidden;
                    position: relative;
                    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
                }}
                
                .progress-fill {{
                    height: 100%;
                    width: 100%;
                    background: var(--gradient);
                    border-radius: 8px;
                    animation: progressShrinkEnhanced 2.5s linear forwards;
                    position: relative;
                    transform-origin: right center;
                }}
                
                /* Enhanced shimmering effect on progress bar */
                .progress-fill::after {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 50%;
                    height: 100%;
                    background: linear-gradient(90deg, 
                        transparent 0%, 
                        rgba(255, 255, 255, 0.2) 20%, 
                        rgba(255, 255, 255, 0.5) 50%, 
                        rgba(255, 255, 255, 0.2) 80%, 
                        transparent 100%);
                    animation: progressShimmerEnhanced 1.5s infinite;
                }}
                
                @keyframes progressShimmerEnhanced {{
                    0% {{ transform: translateX(0%) skewX(-20deg); }}
                    100% {{ transform: translateX(300%) skewX(-20deg); }}
                }}
                
                @keyframes progressShrinkEnhanced {{
                    0% {{ transform: scaleX(1); }}
                    10% {{ transform: scaleX(0.95); }}
                    25% {{ transform: scaleX(0.85); }}
                    50% {{ transform: scaleX(0.6); }}
                    75% {{ transform: scaleX(0.3); }}
                    90% {{ transform: scaleX(0.15); }}
                    100% {{ transform: scaleX(0); }}
                }}
                
                /* Advanced 3D confetti animation */
                .confetti-container {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    z-index: 100;
                    perspective: 700px;
                }}
                
                .confetti {{
                    position: absolute;
                    width: 10px;
                    height: 10px;
                    opacity: 0;
                    will-change: transform, opacity;
                }}
                
                @keyframes fallAndFade3D {{
                    0% {{ transform: rotateX(0deg) rotateY(0deg) translateZ(0) translateY(-100vh); opacity: 1; }}
                    25% {{ transform: rotateX(45deg) rotateY(45deg) translateZ(100px) translateY(-50vh); opacity: 1; }}
                    50% {{ transform: rotateX(90deg) rotateY(90deg) translateZ(50px) translateY(0vh); opacity: 0.8; }}
                    75% {{ transform: rotateX(180deg) rotateY(135deg) translateZ(150px) translateY(50vh); opacity: 0.5; }}
                    100% {{ transform: rotateX(360deg) rotateY(180deg) translateZ(0) translateY(100vh); opacity: 0; }}
                }}
                
                @keyframes fallAndSwirl3D {{
                    0% {{ transform: rotateX(0deg) rotateZ(0deg) translateY(-100vh) translateX(0); opacity: 1; }}
                    25% {{ transform: rotateX(45deg) rotateZ(90deg) translateY(-25vh) translateX(50px); opacity: 1; }}
                    50% {{ transform: rotateX(90deg) rotateZ(180deg) translateY(0vh) translateX(-30px); opacity: 0.8; }}
                    75% {{ transform: rotateX(180deg) rotateZ(270deg) translateY(50vh) translateX(30px); opacity: 0.5; }}
                    100% {{ transform: rotateX(360deg) rotateZ(360deg) translateY(100vh) translateX(0); opacity: 0; }}
                }}
                
                /* Enhanced particle movement with 3D rotation */
                @keyframes moveParticle3D {{
                    0% {{ transform: translate3d(0, 0, 0) rotateX(0deg) rotateY(0deg); }}
                    25% {{ transform: translate3d(25px, -15px, 20px) rotateX(45deg) rotateY(30deg); }}
                    50% {{ transform: translate3d(-10px, 20px, -10px) rotateX(90deg) rotateY(60deg); }}
                    75% {{ transform: translate3d(15px, 10px, 5px) rotateX(45deg) rotateY(90deg); }}
                    100% {{ transform: translate3d(0, 0, 0) rotateX(0deg) rotateY(0deg); }}
                }}
                
                /* Floating orbs in background */
                .floating-orbs {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: -2;
                    pointer-events: none;
                }}
                
                .orb {{
                    position: absolute;
                    border-radius: 50%;
                    background: var(--accent-gradient);
                    filter: blur(40px);
                    opacity: 0.3;
                    will-change: transform;
                }}
            </style>
        </head>
        <body>
            <div class="bg-morphing"></div>
            <div class="bg-pattern"></div>
            <div class="floating-orbs" id="floatingOrbs"></div>
            
            <div class="login-success">
                <div class="success-header">
                    <div class="bg-layer layer-1"></div>
                    <div class="bg-layer layer-2"></div>
                    <div class="bg-layer layer-3"></div>
                    <div class="glow-effect"></div>
                    
                    <!-- Particles in the header -->
                    <div class="particles-container" id="particles"></div>
                    
                    <div class="logo-container">
                        <div class="logo-ring logo-ring-1"></div>
                        <div class="logo-ring logo-ring-2"></div>
                        <i class="fas {theme['icon']}"></i>
                    </div>
                </div>
                
                <div class="success-body">
                    <div class="verified-badge">
                        <i class="fas fa-check" style="margin-right: 6px;"></i> Authentication Successful
                    </div>
                    
                    <div class="welcome-message">
                        <div class="welcome-title">{theme['greeting']}</div>
                        <div class="welcome-subtitle">Hello {user_name}, you've successfully logged in</div>
                    </div>
                    
                    <div class="status-card">
                        <div class="status-item">
                            <div class="status-icon">
                                <i class="fas fa-user-shield"></i>
                            </div>
                            <div class="status-text">
                                <div class="status-label">Account Type</div>
                                <div class="status-value">{user_type.capitalize()}</div>
                            </div>
                        </div>
                        
                        <div class="status-item">
                            <div class="status-icon">
                                <i class="fas fa-clock"></i>
                            </div>
                            <div class="status-text">
                                <div class="status-label">Login Time</div>
                                <div class="status-value">Just now</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="progress-container">
                        <div class="progress-label">
                            <span>Redirecting to dashboard</span>
                            <span class="progress-time">2.5s</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="confetti-container" id="confetti-container"></div>
            
            <script>
                // Extract RGB from primary color for glow effect
                const primaryHex = '{theme['primary']}';
                const r = parseInt(primaryHex.substring(1,3), 16);
                const g = parseInt(primaryHex.substring(3,5), 16);
                const b = parseInt(primaryHex.substring(5,7), 16);
                document.documentElement.style.setProperty('--primary-rgb', `${{r}}, ${{g}}, ${{b}}`);
                
                // Enhanced particle animation in header with varied shapes
                function createParticles() {{
                    const particlesContainer = document.getElementById('particles');
                    const colors = {particle_colors_js};
                    const shapes = ['circle', 'square', 'triangle', 'diamond', 'ring'];
                    
                    for (let i = 0; i < 40; i++) {{
                        const particle = document.createElement('div');
                        particle.className = 'particle';
                        
                        // Random styling
                        const size = Math.random() * 6 + 2;
                        const color = colors[Math.floor(Math.random() * colors.length)];
                        const shape = shapes[Math.floor(Math.random() * shapes.length)];
                        
                        particle.style.width = `${{size}}px`;
                        particle.style.height = `${{size}}px`;
                        
                        // Apply different shapes
                        if (shape === 'circle') {{
                            particle.style.borderRadius = '50%';
                            particle.style.backgroundColor = color;
                        }} else if (shape === 'square') {{
                            particle.style.borderRadius = '2px';
                            particle.style.backgroundColor = color;
                            particle.style.transform = `rotate(${{Math.random() * 45}}deg)`;
                        }} else if (shape === 'triangle') {{
                            particle.style.width = '0';
                            particle.style.height = '0';
                            particle.style.borderLeft = `${{size/2}}px solid transparent`;
                            particle.style.borderRight = `${{size/2}}px solid transparent`;
                            particle.style.borderBottom = `${{size}}px solid ${{color}}`;
                            particle.style.backgroundColor = 'transparent';
                        }} else if (shape === 'diamond') {{
                            particle.style.width = `${{size}}px`;
                            particle.style.height = `${{size}}px`;
                            particle.style.backgroundColor = color;
                            particle.style.transform = `rotate(45deg)`;
                        }} else if (shape === 'ring') {{
                            particle.style.width = `${{size}}px`;
                            particle.style.height = `${{size}}px`;
                            particle.style.borderRadius = '50%';
                            particle.style.border = `1px solid ${{color}}`;
                            particle.style.backgroundColor = 'transparent';
                        }}
                        
                        particle.style.boxShadow = `0 0 ${{size/2}}px ${{color}}`;
                        
                        // Random position
                        particle.style.left = `${{Math.random() * 100}}%`;
                        particle.style.top = `${{Math.random() * 100}}%`;
                        
                        // 3D particle movement
                        const duration = Math.random() * 25 + 10;
                        const delay = Math.random() * 5;
                        
                        particle.style.animation = `moveParticle3D ${{duration}}s ease-in-out ${{delay}}s infinite`;
                        particle.style.transform = 'translate3d(0, 0, 0)';
                        
                        particlesContainer.appendChild(particle);
                    }}
                }}
                
                // Create floating background orbs
                function createFloatingOrbs() {{
                    const orbsContainer = document.getElementById('floatingOrbs');
                    const colors = {particle_colors_js};
                    
                    for (let i = 0; i < 8; i++) {{
                        const orb = document.createElement('div');
                        orb.className = 'orb';
                        
                        // Random size
                        const size = Math.random() * 200 + 100;
                        orb.style.width = `${{size}}px`;
                        orb.style.height = `${{size}}px`;
                        
                        // Random position
                        orb.style.left = `${{Math.random() * 100}}%`;
                        orb.style.top = `${{Math.random() * 100}}%`;
                        
                        // Random color from theme
                        const colorIndex = Math.floor(Math.random() * colors.length);
                        orb.style.background = colors[colorIndex];
                        
                        // Animation
                        const duration = Math.random() * 40 + 20;
                        const delay = Math.random() * 10;
                        
                        orb.style.animation = `moveParticle ${{duration}}s ease-in-out ${{delay}}s infinite`;
                        
                        orbsContainer.appendChild(orb);
                    }}
                }}
                
                // Create advanced 3D confetti elements
                function createConfetti() {{
                    const container = document.getElementById('confetti-container');
                    const colors = {particle_colors_js};
                    const shapes = ['circle', 'square', 'triangle', 'line', 'star', 'cross', 'heart'];
                    
                    for (let i = 0; i < 100; i++) {{
                        const confetti = document.createElement('div');
                        confetti.className = 'confetti';
                        
                        // Random styling
                        const size = Math.random() * 12 + 6;
                        const shape = shapes[Math.floor(Math.random() * shapes.length)];
                        const color = colors[Math.floor(Math.random() * colors.length)];
                        
                        // Set size
                        confetti.style.width = `${{size}}px`;
                        confetti.style.height = `${{size}}px`;
                        
                        // Set shape
                        if (shape === 'circle') {{
                            confetti.style.borderRadius = '50%';
                            confetti.style.background = color;
                        }} else if (shape === 'square') {{
                            confetti.style.background = color;
                        }} else if (shape === 'triangle') {{
                            confetti.style.width = '0';
                            confetti.style.height = '0';
                            confetti.style.borderLeft = `${{size/2}}px solid transparent`;
                            confetti.style.borderRight = `${{size/2}}px solid transparent`;
                            confetti.style.borderBottom = `${{size}}px solid ${{color}}`;
                            confetti.style.background = 'transparent';
                        }} else if (shape === 'line') {{
                            confetti.style.width = `${{size * 2}}px`;
                            confetti.style.height = `${{size/4}}px`;
                            confetti.style.background = color;
                        }} else if (shape === 'star') {{
                            confetti.style.width = '0';
                            confetti.style.height = '0';
                            confetti.style.borderRight = `${{size/2}}px solid transparent`;
                            confetti.style.borderBottom = `${{size/3}}px solid ${{color}}`;
                            confetti.style.borderLeft = `${{size/2}}px solid transparent`;
                            confetti.style.transform = `rotate(35deg)`;
                            
                            // Create star shape with pseudo-element
                            const afterStyles = `
                                .star-${{i}}::before {{
                                    content: '';
                                    position: absolute;
                                    top: 0;
                                    left: -${{size/2}}px;
                                    width: 0;
                                    height: 0;
                                    border-bottom: ${{size/3}}px solid ${{color}};
                                    border-left: ${{size/2}}px solid transparent;
                                    border-right: ${{size/2}}px solid transparent;
                                    transform: rotate(-70deg);
                                }}
                            `;
                            
                            const styleSheet = document.createElement('style');
                            styleSheet.textContent = afterStyles;
                            document.head.appendChild(styleSheet);
                            
                            confetti.classList.add(`star-${{i}}`);
                            confetti.style.background = 'transparent';
                        }} else if (shape === 'cross') {{
                            confetti.style.width = `${{size}}px`;
                            confetti.style.height = `${{size/4}}px`;
                            confetti.style.background = color;
                            confetti.style.position = 'relative';
                            
                            const afterStyles = `
                                .cross-${{i}}::before {{
                                    content: '';
                                    position: absolute;
                                    top: -${{size*3/8}}px;
                                    left: ${{size*3/8}}px;
                                    width: ${{size/4}}px;
                                    height: ${{size}}px;
                                    background-color: ${{color}};
                                }}
                            `;
                            
                            const styleSheet = document.createElement('style');
                            styleSheet.textContent = afterStyles;
                            document.head.appendChild(styleSheet);
                            
                            confetti.classList.add(`cross-${{i}}`);
                        }} else if (shape === 'heart') {{
                            confetti.style.width = `${{size}}px`;
                            confetti.style.height = `${{size}}px`;
                            confetti.style.background = color;
                            confetti.style.transform = 'rotate(-45deg)';
                            confetti.style.borderRadius = `${{size/4}}px`;
                            
                            const afterStyles = `
                                .heart-${{i}}::before,
                                .heart-${{i}}::after {{
                                    content: '';
                                    position: absolute;
                                    width: ${{size}}px;
                                    height: ${{size}}px;
                                    background-color: ${{color}};
                                    border-radius: 50%;
                                }}
                                .heart-${{i}}::before {{
                                    top: -${{size/2}}px;
                                    left: 0;
                                }}
                                .heart-${{i}}::after {{
                                    top: 0;
                                    left: -${{size/2}}px;
                                }}
                            `;
                            
                            const styleSheet = document.createElement('style');
                            styleSheet.textContent = afterStyles;
                            document.head.appendChild(styleSheet);
                            
                            confetti.classList.add(`heart-${{i}}`);
                        }}
                        
                        // Add glossy effect
                        confetti.style.boxShadow = `inset 0 0 ${{size/3}}px rgba(255, 255, 255, 0.5), 0 0 ${{size/4}}px rgba(0, 0, 0, 0.1)`;
                        
                        // Random position
                        confetti.style.left = `${{Math.random() * 100}}%`;
                        
                        // Random animation
                        const animationDuration = Math.random() * 2.5 + 2;
                        const animationDelay = Math.random() * 0.7;
                        
                        // Use advanced 3D animations
                        const animationType = Math.random() > 0.5 ? 'fallAndFade3D' : 'fallAndSwirl3D';
                        
                        confetti.style.animation = `${{animationType}} ${{animationDuration}}s var(--easing) ${{animationDelay}}s forwards`;
                        
                        container.appendChild(confetti);
                    }}
                }}
                
                // Initialize everything with proper timing
                document.addEventListener('DOMContentLoaded', function() {{
                    // Create floating orbs
                    createFloatingOrbs();
                    
                    // Initialize particles with slight delay
                    setTimeout(createParticles, 200);
                    
                    // Create confetti with a slight delay
                    setTimeout(createConfetti, 800);
                    
                    // Update countdown timer with smooth animation
                    const progressTimeEl = document.querySelector('.progress-time');
                    let timeLeft = 2.5;
                    
                    const interval = setInterval(() => {{
                        timeLeft -= 0.1;
                        if (timeLeft <= 0) {{
                            clearInterval(interval);
                            timeLeft = 0;
                        }}
                        progressTimeEl.textContent = timeLeft.toFixed(1) + 's';
                    }}, 100);
                    
                    // Redirect after animation completes with fade transition
                    setTimeout(() => {{
                        const successCard = document.querySelector('.login-success');
                        
                        // Add sophisticated exit animation
                        successCard.style.animation = 'exitAnimation 1s var(--easing) forwards';
                        
                        // Add @keyframes for exit animation
                        const styleSheet = document.createElement('style');
                        styleSheet.textContent = `
                            @keyframes exitAnimation {{
                                0% {{ opacity: 1; transform: translateY(0) scale(1) rotate(0); filter: blur(0); }}
                                30% {{ opacity: 0.9; transform: translateY(-20px) scale(1.02) rotate(0); filter: blur(0); }}
                                100% {{ opacity: 0; transform: translateY(-50px) scale(0.95) rotate(1deg); filter: blur(15px); }}
                            }}
                        `;
                        document.head.appendChild(styleSheet);
                        
                        // Final celebration effect before redirect
                        setTimeout(() => {{
                            // Create a flash effect before redirect
                            const flash = document.createElement('div');
                            flash.style.position = 'fixed';
                            flash.style.top = '0';
                            flash.style.left = '0';
                            flash.style.width = '100%';
                            flash.style.height = '100%';
                            flash.style.backgroundColor = 'white';
                            flash.style.opacity = '0';
                            flash.style.zIndex = '1000';
                            flash.style.transition = 'opacity 0.5s ease-in-out';
                            document.body.appendChild(flash);
                            
                            setTimeout(() => {{
                                flash.style.opacity = '0.7';
                                setTimeout(() => {{
                                    // Redirect to dashboard
                                    window.location = '/{user_type}home/';
                                }}, 300);
                            }}, 50);
                        }}, 600);
                    }}, 2500);
                }});
            </script>
        </body>
        </html>
        """
        
        return HttpResponse(success_html)
    else:
        # Create a modernized error animation with enhanced 3D effects
        error_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Authentication Failed</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                :root {
                    --primary: #EF4444;
                    --primary-dark: #B91C1C;
                    --secondary: #F87171;
                    --accent: #FEE2E2;
                    --light: #FEF2F2;
                    --text-primary: #1E293B;
                    --text-secondary: #64748B;
                    --bg-main: #F8FAFC;
                    --bg-card: #FFFFFF;
                    --shadow-xs: 0 1px 2px rgba(16, 24, 40, 0.05);
                    --shadow-sm: 0 1px 3px rgba(16, 24, 40, 0.1), 0 1px 2px rgba(16, 24, 40, 0.06);
                    --shadow-md: 0 4px 8px -2px rgba(16, 24, 40, 0.1), 0 2px 4px -2px rgba(16, 24, 40, 0.06);
                    --shadow-lg: 0 12px 16px -4px rgba(16, 24, 40, 0.08), 0 4px 6px -2px rgba(16, 24, 40, 0.03);
                    --shadow-xl: 0 20px 24px -4px rgba(16, 24, 40, 0.08), 0 8px 8px -4px rgba(16, 24, 40, 0.03);
                    --easing: cubic-bezier(0.22, 1, 0.36, 1);
                    --error-gradient: linear-gradient(135deg, #EF4444 0%, #B91C1C 100%);
                    --primary-rgb: 239, 68, 68;
                }
                
                * { 
                    margin: 0; 
                    padding: 0; 
                    box-sizing: border-box; 
                }
                
                body { 
                    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background-color: var(--bg-main);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    overflow: hidden;
                    color: var(--text-primary);
                    perspective: 1000px;
                }
                
                /* Modernized animated background with 3D effect */
                .bg-animation {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: -1;
                    overflow: hidden;
                }
                
                .bg-circle {
                    position: absolute;
                    border-radius: 50%;
                    background: var(--accent);
                    opacity: 0.4;
                    filter: blur(60px);
                    transform-style: preserve-3d;
                    will-change: transform, opacity;
                    animation: moveAndPulse3D var(--duration) var(--easing) infinite;
                }
                
                .circle-1 {
                    width: 700px;
                    height: 700px;
                    top: 30%;
                    left: -300px;
                    --duration: 25s;
                    background: radial-gradient(circle at 30% 50%, var(--accent) 0%, var(--secondary) 70%);
                }
                
                .circle-2 {
                    width: 600px;
                    height: 600px;
                    top: -200px;
                    right: 10%;
                    --duration: 30s;
                    background: radial-gradient(circle at 70% 50%, var(--accent) 0%, var(--primary) 70%);
                }
                
                .circle-3 {
                    width: 400px;
                    height: 400px;
                    bottom: -100px;
                    right: 20%;
                    --duration: 20s;
                    background: radial-gradient(circle at 50% 50%, var(--secondary) 0%, var(--primary-dark) 70%);
                }
                
                @keyframes moveAndPulse3D {
                    0% { transform: translateY(0) translateZ(0) scale(1); opacity: 0.4; }
                    25% { transform: translateY(50px) translateZ(50px) scale(1.05); opacity: 0.5; }
                    50% { transform: translateY(100px) translateZ(0) scale(1.1); opacity: 0.5; }
                    75% { transform: translateY(50px) translateZ(-50px) scale(1.05); opacity: 0.4; }
                    100% { transform: translateY(0) translateZ(0) scale(1); opacity: 0.4; }
                }
                
                /* Animated geometric shapes in background */
                .geometric-shapes {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: -2;
                    opacity: 0.3;
                }
                
                .shape {
                    position: absolute;
                    opacity: 0.2;
                    filter: blur(1px);
                    transform-style: preserve-3d;
                    will-change: transform;
                }
                
                .shape-1 {
                    top: 20%;
                    left: 10%;
                    width: 120px;
                    height: 120px;
                    border: 2px solid var(--primary);
                    transform: rotate(45deg);
                    animation: rotateShape 20s linear infinite;
                }
                
                .shape-2 {
                    top: 60%;
                    right: 15%;
                    width: 80px;
                    height: 80px;
                    border-radius: 50%;
                    border: 2px solid var(--secondary);
                    animation: floatShape 15s ease-in-out infinite alternate;
                }
                
                .shape-3 {
                    bottom: 15%;
                    left: 20%;
                    border-left: 70px solid transparent;
                    border-right: 70px solid transparent;
                    border-bottom: 120px solid var(--primary-dark);
                    opacity: 0.15;
                    animation: floatShape 18s ease-in-out 2s infinite alternate-reverse;
                }
                
                @keyframes rotateShape {
                    0% { transform: rotate(0deg) translateZ(0); }
                    100% { transform: rotate(360deg) translateZ(50px); }
                }
                
                @keyframes floatShape {
                    0% { transform: translateY(0) rotate(0) translateZ(0); }
                    50% { transform: translateY(-40px) rotate(10deg) translateZ(30px); }
                    100% { transform: translateY(40px) rotate(-10deg) translateZ(-30px); }
                }
                
                .error-container {
                    position: relative;
                    width: 450px;
                    background-color: rgba(255, 255, 255, 0.85);
                    border-radius: 32px;
                    box-shadow: var(--shadow-xl), 0 0 0 1px rgba(16, 24, 40, 0.06);
                    overflow: hidden;
                    animation: appearWithShake3D 1s var(--easing) both;
                    transform-style: preserve-3d;
                    backdrop-filter: blur(10px);
                    border-top: 1px solid rgba(255, 255, 255, 0.8);
                    border-left: 1px solid rgba(255, 255, 255, 0.8);
                }
                
                @keyframes appearWithShake3D {
                    0% { transform: translateY(30px) translateZ(-50px) scale(0.95) rotateX(10deg); opacity: 0; filter: blur(10px); }
                    40% { transform: translateY(0) translateZ(0) scale(1) rotateX(0deg); opacity: 0.9; filter: blur(0); }
                    50% { transform: translateX(-15px) rotateY(-5deg); }
                    60% { transform: translateX(15px) rotateY(5deg); }
                    70% { transform: translateX(-10px) rotateY(-3deg); }
                    80% { transform: translateX(10px) rotateY(3deg); }
                    90% { transform: translateX(-5px) rotateY(-1deg); }
                    100% { transform: translateX(0) rotateY(0deg); opacity: 1; }
                }
                
                .error-header {
                    padding: 50px 0;
                    position: relative;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                
                /* Enhanced pulsing ring animation around the error icon */
                .error-icon-wrapper {
                    position: relative;
                    transform-style: preserve-3d;
                    perspective: 800px;
                }
                
                .error-ring {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 100px;
                    height: 100px;
                    border-radius: 50%;
                    border: 2px solid var(--primary);
                    animation: ringPulse3D 2s ease-out infinite;
                    opacity: 0.7;
                }
                
                .error-ring-2 {
                    animation-delay: 0.5s;
                }
                
                .error-ring-3 {
                    animation-delay: 1s;
                }
                
                @keyframes ringPulse3D {
                    0% { width: 80px; height: 80px; opacity: 0.7; transform: translate(-50%, -50%) translateZ(0); }
                    50% { opacity: 0.4; transform: translate(-50%, -50%) translateZ(20px); }
                    100% { width: 180px; height: 180px; opacity: 0; transform: translate(-50%, -50%) translateZ(0); }
                }
                
                .error-icon {
                    width: 100px;
                    height: 100px;
                    background: var(--error-gradient);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                    box-shadow: 0 0 40px rgba(239, 68, 68, 0.4), inset 0 0 15px rgba(255, 255, 255, 0.3);
                    animation: iconAppear3D 0.6s var(--easing) 0.3s backwards, iconPulse3D 2s ease-in-out 0.9s infinite;
                    transform-style: preserve-3d;
                }
                
                @keyframes iconAppear3D {
                    0% { transform: scale(0.6) translateY(20px) translateZ(-30px) rotateX(20deg); opacity: 0; filter: blur(10px); }
                    60% { transform: scale(1.1) translateY(-10px) translateZ(20px) rotateX(-10deg); opacity: 0.9; filter: blur(0); }
                    80% { transform: scale(0.95) translateY(5px) translateZ(10px) rotateX(5deg); }
                    100% { transform: scale(1) translateY(0) translateZ(0) rotateX(0deg); opacity: 1; }
                }
                
                @keyframes iconPulse3D {
                    0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.6), inset 0 0 15px rgba(255, 255, 255, 0.3); transform: translateZ(0); }
                    50% { box-shadow: 0 0 25px 5px rgba(239, 68, 68, 0.4), inset 0 0 20px rgba(255, 255, 255, 0.5); transform: translateZ(15px); }
                    100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0), inset 0 0 15px rgba(255, 255, 255, 0.3); transform: translateZ(0); }
                }
                
                /* Enhanced animated lock icon with 3D effect */
                .error-icon i {
                    color: white;
                    font-size: 40px;
                    animation: lockShake3D 4s ease-in-out 1s infinite;
                    text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                    transform-style: preserve-3d;
                }
                
                @keyframes lockShake3D {
                    0%, 40%, 100% { transform: rotate(0) translateZ(0); }
                    5%, 15%, 25% { transform: rotate(-5deg) translateZ(10px); }
                    10%, 20%, 30% { transform: rotate(5deg) translateZ(5px); }
                    35% { transform: rotate(-3deg) translateZ(15px); }
                    37% { transform: rotate(0) translateZ(20px); }
                    38% { transform: rotate(3deg) translateZ(15px); }
                }
                
                .error-body {
                    padding: 15px 35px 45px;
                    text-align: center;
                }
                
                .error-title {
                    font-size: 26px;
                    font-weight: 700;
                    background: var(--error-gradient);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    text-fill-color: transparent;
                    margin-bottom: 16px;
                    animation: fadeUp3D 0.5s ease 0.5s backwards;
                    text-shadow: 0 5px 15px rgba(239, 68, 68, 0.1);
                }
                
                @keyframes fadeUp3D {
                    0% { opacity: 0; transform: translateY(15px) translateZ(-10px); filter: blur(5px); }
                    60% { opacity: 0.8; transform: translateY(-5px) translateZ(10px); filter: blur(0); }
                    100% { opacity: 1; transform: translateY(0) translateZ(0); }
                }
                
                .error-message {
                    color: var(--text-secondary);
                    font-size: 16px;
                    line-height: 1.6;
                    margin-bottom: 35px;
                    animation: fadeUp3D 0.5s ease 0.7s backwards;
                }
                
                .error-fields {
                    display: flex;
                    align-items: center;
                    background-color: rgba(254, 226, 226, 0.7);
                    padding: 18px 22px;
                    border-radius: 20px;
                    margin-bottom: 30px;
                    border: 1px solid var(--accent);
                    box-shadow: var(--shadow-sm), 0 0 15px rgba(239, 68, 68, 0.1);
                    animation: fieldAppear3D 0.5s ease 0.9s backwards;
                    backdrop-filter: blur(5px);
                    position: relative;
                    overflow: hidden;
                }
                
                /* Field background animation */
                .error-fields::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
                    animation: fieldGlimmer 2s infinite;
                    z-index: 0;
                }
                
                @keyframes fieldGlimmer {
                    0% { transform: translateX(-100%); }
                    100% { transform: translateX(100%); }
                }
                
                @keyframes fieldAppear3D {
                    0% { opacity: 0; transform: translateY(15px) translateZ(-20px) scale(0.95); filter: blur(5px); }
                    60% { opacity: 0.9; transform: translateY(-5px) translateZ(10px) scale(1.02); filter: blur(0); }
                    100% { opacity: 1; transform: translateY(0) translateZ(0) scale(1); }
                }
                
                .error-fields i {
                    color: var(--primary);
                    margin-right: 14px;
                    font-size: 20px;
                    animation: errorIconPulse 1.5s ease-in-out infinite;
                    position: relative;
                    z-index: 1;
                }
                
                @keyframes errorIconPulse {
                    0%, 100% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.2); opacity: 0.8; }
                }
                
                .error-text {
                    font-size: 16px;
                    color: var(--primary-dark);
                    font-weight: 600;
                    position: relative;
                    z-index: 1;
                }
                
                .retry-button {
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                    padding: 14px 36px;
                    background: var(--error-gradient);
                    color: white;
                    font-weight: 600;
                    font-size: 16px;
                    border: none;
                    border-radius: 50px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
                    position: relative;
                    overflow: hidden;
                    animation: buttonAppear3D 0.5s ease 1.1s backwards;
                    transform-style: preserve-3d;
                }
                
                @keyframes buttonAppear3D {
                    0% { opacity: 0; transform: translateY(15px) translateZ(-20px); filter: blur(5px); }
                    60% { opacity: 0.9; transform: translateY(-5px) translateZ(10px); filter: blur(0); }
                    100% { opacity: 1; transform: translateY(0) translateZ(0); }
                }
                
                .retry-button:hover {
                    transform: translateY(-3px) scale(1.02);
                    box-shadow: 0 8px 20px rgba(239, 68, 68, 0.4);
                }
                
                .retry-button:active {
                    transform: translateY(1px) scale(0.98);
                }
                
                .retry-button i {
                    font-size: 16px;
                    animation: spinIcon3D 2s linear infinite;
                }
                
                @keyframes spinIcon3D {
                    0% { transform: rotate(0deg) translateZ(0); }
                    50% { transform: rotate(180deg) translateZ(5px); }
                    100% { transform: rotate(360deg) translateZ(0); }
                }
                
                /* Enhanced ripple effect with 3D */
                .ripple {
                    position: absolute;
                    border-radius: 50%;
                    background: radial-gradient(circle, rgba(255, 255, 255, 0.7) 0%, rgba(255, 255, 255, 0) 70%);
                    transform: scale(0) translateZ(0);
                    animation: ripple3D 0.8s cubic-bezier(0.11, 0.65, 0.33, 1);
                }
                
                @keyframes ripple3D {
                    to {
                        transform: scale(2.5) translateZ(20px);
                        opacity: 0;
                    }
                }
                
                /* Enhanced particle effects with 3D */
                .particle-container {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    perspective: 1000px;
                    z-index: 100;
                }
                
                .particle {
                    position: absolute;
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background-color: var(--primary);
                    opacity: 0.6;
                    pointer-events: none;
                    transform-style: preserve-3d;
                    will-change: transform, opacity;
                }
                
                @keyframes particleFade3D {
                    0% { transform: translate3d(0, 0, 0) scale(1); opacity: 0.6; }
                    50% { transform: translate3d(calc(var(--tx) * 0.5), calc(var(--ty) * 0.5), 20px) scale(1.2); opacity: 0.8; }
                    100% { transform: translate3d(var(--tx), var(--ty), 0) scale(0); opacity: 0; }
                }
                
                /* Add glitch effect on error */
                @keyframes glitchText {
                    0% { transform: translate(0); }
                    20% { transform: translate(-3px, 3px); }
                    40% { transform: translate(-3px, -3px); }
                    60% { transform: translate(3px, 3px); }
                    80% { transform: translate(3px, -3px); }
                    100% { transform: translate(0); }
                }
                
                /* Screen glitch effect */
                .screen-glitch {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    z-index: 1000;
                    opacity: 0;
                    mix-blend-mode: overlay;
                    display: none;
                }
                
                .glitch-line {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 2px;
                    background-color: rgba(239, 68, 68, 0.5);
                    transform: translateY(var(--offset));
                }
            </style>
        </head>
        <body>
            <div class="bg-animation">
                <div class="bg-circle circle-1"></div>
                <div class="bg-circle circle-2"></div>
                <div class="bg-circle circle-3"></div>
            </div>
            
            <div class="geometric-shapes">
                <div class="shape shape-1"></div>
                <div class="shape shape-2"></div>
                <div class="shape shape-3"></div>
            </div>
            
            <div class="error-container">
                <div class="error-header">
                    <div class="error-icon-wrapper">
                        <div class="error-ring"></div>
                        <div class="error-ring error-ring-2"></div>
                        <div class="error-ring error-ring-3"></div>
                        <div class="error-icon">
                            <i class="fas fa-lock"></i>
                        </div>
                    </div>
                </div>
                
                <div class="error-body">
                    <div class="error-title">Authentication Failed</div>
                    <div class="error-message">
                        We couldn't verify your credentials. Please check your username and password and try again.
                    </div>
                    
                    <div class="error-fields">
                        <i class="fas fa-exclamation-circle"></i>
                        <div class="error-text">Invalid username or password</div>
                    </div>
                    
                    <button class="retry-button" id="retry-button">
                        <i class="fas fa-sync-alt"></i>
                        Try Again
                    </button>
                </div>
            </div>
            
            <div class="particle-container" id="particle-container"></div>
            <div class="screen-glitch" id="screen-glitch"></div>
            
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    // Create screen glitch effect
                    function createGlitchEffect() {
                        const glitchContainer = document.getElementById('screen-glitch');
                        glitchContainer.style.display = 'block';
                        
                        // Create random glitch lines
                        for (let i = 0; i < 10; i++) {
                            const line = document.createElement('div');
                            line.className = 'glitch-line';
                            const offset = Math.random() * 100 + 'vh';
                            line.style.setProperty('--offset', offset);
                            line.style.height = (Math.random() * 2 + 1) + 'px';
                            line.style.opacity = Math.random() * 0.5 + 0.5;
                            glitchContainer.appendChild(line);
                        }
                        
                        // Animate glitch
                        setTimeout(() => {
                            glitchContainer.style.opacity = '1';
                            
                            setTimeout(() => {
                                glitchContainer.style.opacity = '0';
                                
                                setTimeout(() => {
                                    glitchContainer.style.opacity = '0.8';
                                    
                                    setTimeout(() => {
                                        glitchContainer.style.opacity = '0';
                                        glitchContainer.innerHTML = '';
                                    }, 100);
                                }, 50);
                            }, 100);
                        }, 100);
                    }
                    
                    // Create glitch effect occasionally
                    setInterval(createGlitchEffect, 4000);
                    
                    // Add enhanced ripple effect to button
                    document.getElementById('retry-button').addEventListener('mousedown', function(e) {
                        const button = e.currentTarget;
                        const ripple = document.createElement('span');
                        const rect = button.getBoundingClientRect();
                        
                        const size = Math.max(rect.width, rect.height) * 2.5;
                        const x = e.clientX - rect.left - size / 2;
                        const y = e.clientY - rect.top - size / 2;
                        
                        ripple.style.width = ripple.style.height = `${size}px`;
                        ripple.style.left = `${x}px`;
                        ripple.style.top = `${y}px`;
                        ripple.className = 'ripple';
                        
                        button.appendChild(ripple);
                        
                        // Create particles on click
                        createParticles(e.clientX, e.clientY);
                        
                        // Create glitch effect on button click
                        createGlitchEffect();
                        
                        setTimeout(() => {
                            ripple.remove();
                        }, 800);
                        
                        // Redirect to login page with delay
                        setTimeout(() => {
                            // Create flash transition before redirect
                            const flash = document.createElement('div');
                            flash.style.position = 'fixed';
                            flash.style.top = '0';
                            flash.style.left = '0';
                            flash.style.width = '100%';
                            flash.style.height = '100%';
                            flash.style.backgroundColor = 'rgba(239, 68, 68, 0.05)';
                            flash.style.opacity = '0';
                            flash.style.zIndex = '1000';
                            flash.style.transition = 'opacity 0.3s ease-in-out';
                            document.body.appendChild(flash);
                            
                            setTimeout(() => {
                                flash.style.opacity = '1';
                                
                                setTimeout(() => {
                                    window.location.href = '/login/';
                                }, 300);
                            }, 50);
                        }, 400);
                    });
                    
                    // Create 3D particles function
                    function createParticles(x, y) {
                        const container = document.getElementById('particle-container');
                        const colors = ['#EF4444', '#F87171', '#FCA5A5', '#FECACA'];
                        const shapes = ['circle', 'square', 'triangle'];
                        
                        for (let i = 0; i < 20; i++) {
                            const particle = document.createElement('div');
                            particle.className = 'particle';
                            
                            // Random styling and shape
                            const size = Math.random() * 6 + 4;
                            const color = colors[Math.floor(Math.random() * colors.length)];
                            const shape = shapes[Math.floor(Math.random() * shapes.length)];
                            
                            // Apply different shapes
                            if (shape === 'circle') {
                                particle.style.borderRadius = '50%';
                            } else if (shape === 'square') {
                                particle.style.borderRadius = '2px';
                            } else if (shape === 'triangle') {
                                particle.style.width = '0';
                                particle.style.height = '0';
                                particle.style.borderLeft = `${size/2}px solid transparent`;
                                particle.style.borderRight = `${size/2}px solid transparent`;
                                particle.style.borderBottom = `${size}px solid ${color}`;
                                particle.style.background = 'transparent';
                            }
                            
                            if (shape !== 'triangle') {
                                particle.style.width = `${size}px`;
                                particle.style.height = `${size}px`;
                                particle.style.backgroundColor = color;
                            }
                            
                            // Position at click point
                            particle.style.left = `${x}px`;
                            particle.style.top = `${y}px`;
                            
                            // Random direction and distance with 3D effect
                            const tx = (Math.random() - 0.5) * 100;
                            const ty = (Math.random() - 0.5) * 100;
                            particle.style.setProperty('--tx', `${tx}px`);
                            particle.style.setProperty('--ty', `${ty}px`);
                            
                            // Animation with 3D effect
                            const duration = Math.random() * 0.6 + 0.6;
                            particle.style.animation = `particleFade3D ${duration}s cubic-bezier(0.21, 0.94, 0.64, 0.99) forwards`;
                            
                            container.appendChild(particle);
                            
                            // Clean up
                            setTimeout(() => {
                                particle.remove();
                            }, duration * 1000);
                        }
                    }
                    
                    // Add slight glitch to error text occasionally
                    const errorText = document.querySelector('.error-text');
                    setInterval(() => {
                        errorText.style.animation = 'glitchText 0.3s ease';
                        setTimeout(() => {
                            errorText.style.animation = 'none';
                        }, 300);
                    }, 3000);
                });
            </script>
        </body>
        </html>
        """
        
        return HttpResponse(error_html)
    
def adminhome(request):
        return render(request, 'adminhome.html')
    
def customerhome(request):
        return render(request, 'customerhome.html')
      

def viewcustomer(request):
    cursor=connection.cursor()
    sql="select * from customer"
    cursor.execute(sql)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Cid':row[0], 'Name':row[1],'Address': row[2],'Phone':row[3],'Gender':row[4],'Email':row[5],'Img':row[6]}
        tt.append(q)    
    return render(request,'viewcustomer.html',{'tt':tt})   

def staff(request):
    return render(request, 'staff.html')

from .forms import StaffForm
from .models import Staff

# from django.shortcuts import render
# from django.http import HttpResponse
# from .forms import StaffForm  # Assuming the form is imported correctly
# from .models import Staff  # Assuming the Staff model is imported
# from django.db import connection

def staffaction(request):
    cursor = connection.cursor()
    
    if request.method == "POST":
        staffform = StaffForm(request.POST, request.FILES)
        
        if staffform.is_valid():
            # Get the email from the form
            email = staffform.cleaned_data["email"]
            
            # Check if the email already exists in the login table
            cursor.execute("SELECT COUNT(*) FROM login WHERE uname = %s", [email])
            email_exists = cursor.fetchone()[0]  # Fetch the count of records with the same email
            
            if email_exists > 0:
                # If the email exists, show an error notification
                error_html = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Email Already Exists</title>
                    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
                    <style>
                        * { margin: 0; padding: 0; box-sizing: border-box; }
                        body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
                        .notification-wrapper {
                            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                            display: flex; justify-content: center; align-items: center;
                            background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                            z-index: 1000;
                        }
                        .notification-container {
                            position: relative; background: rgba(255, 255, 255, 0.95);
                            border-radius: 24px; padding: 2rem;
                            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                            animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                            max-width: 90%; width: 400px;
                        }
                        .icon-circle {
                            width: 80px; height: 80px; background: linear-gradient(45deg, #FF8A80, #FF5252);
                            border-radius: 50%; display: flex; align-items: center;
                            justify-content: center; margin: 0 auto 1.5rem;
                            position: relative; overflow: hidden;
                            animation: popIn 0.5s ease-out forwards;
                            transform: scale(0);
                        }
                        .icon-circle i {
                            color: white; font-size: 32px;
                            transform: scale(0) rotate(-180deg);
                            animation: iconBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
                        }
                        .ripple {
                            position: absolute; width: 100%; height: 100%;
                            border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                            animation: rippleEffect 1.5s linear infinite;
                        }
                        .notification-text, .notification-subtext {
                            text-align: center; opacity: 0;
                            animation: textFadeIn 0.5s ease 0.6s forwards;
                        }
                        .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
                        .notification-subtext { color: #666; font-size: 1rem; }
                        .progress-bar {
                            position: absolute; bottom: 0; left: 0; height: 4px;
                            background: linear-gradient(to right, #FF8A80, #FF5252);
                            width: 100%; animation: progress 2s linear forwards;
                        }

                        /* Animations */
                        @keyframes floatIn {
                            from { transform: translateY(20px); opacity: 0; }
                            to { transform: translateY(0); opacity: 1; }
                        }
                        @keyframes popIn {
                            0% { transform: scale(0); }
                            80% { transform: scale(1.2); }
                            100% { transform: scale(1); }
                        }
                        @keyframes iconBounce {
                            0% { transform: scale(0) rotate(-180deg); }
                            80% { transform: scale(1.2) rotate(10deg); }
                            100% { transform: scale(1) rotate(0deg); }
                        }
                        @keyframes rippleEffect {
                            0% { width: 0; height: 0; opacity: 0.5; }
                            100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
                        }
                        @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                        @keyframes progress { from { width: 100%; } to { width: 0%; } }
                        @keyframes fadeOut { to { opacity: 0; } }
                    </style>
                </head>
                <body>
                    <div class="notification-wrapper">
                        <div class="notification-container">
                            <div class="icon-circle">
                                <i class="fas fa-exclamation-triangle"></i>
                                <div class="ripple"></div>
                            </div>
                            <div class="notification-text">Email Already Exists</div>
                            <div class="notification-subtext">Please use a different email address</div>
                            <div class="progress-bar"></div>
                        </div>
                    </div>
                    <script>
                        document.addEventListener('DOMContentLoaded', function() {
                            setTimeout(() => {
                                document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                                setTimeout(() => { window.location = '/viewstaff/'; }, 500);
                            }, 2000);
                        });
                    </script>
                </body>
                </html>
                """
                return HttpResponse(error_html)
            
            # If the email doesn't exist, proceed to create the staff record
            staff = Staff()
            staff.name = staffform.cleaned_data["name"]
            staff.gender = staffform.cleaned_data["gender"]
            staff.dob = staffform.cleaned_data["dob"]
            staff.address = staffform.cleaned_data["address"]
            staff.place = staffform.cleaned_data["place"]
            staff.phone = staffform.cleaned_data["phone"]
            staff.adhaar = staffform.cleaned_data["adhaar"]
            staff.email = staffform.cleaned_data["email"]
            staff.img = staffform.cleaned_data["img"]  # Save the image (if provided)
            
            # Save the staff instance to the database
            staff.save()

            # Get the newly added staff's ID (assuming auto-incrementing Sid)
            cursor.execute("SELECT MAX(Sid) AS Sid FROM staff")  # Ensure this is the correct table
            staff_id = cursor.fetchone()[0]

            # Insert into login table with the 'staff' user type
            cursor.execute(
                "INSERT INTO login(uid, uname, upass, utype) VALUES (%s, %s, %s, %s)",
                (staff_id, email, request.POST['password'], 'staff')
            )

            # Success animation for staff added successfully
            success_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Staff Added</title>
                <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
                    
                    * {{ 
                        margin: 0; 
                        padding: 0; 
                        box-sizing: border-box; 
                    }}
                    
                    :root {{
                        --primary: #4CAF50;        /* Green */
                        --primary-dark: #388E3C;
                        --primary-light: #A5D6A7;
                        --success: #4CAF50;
                        --text-dark: #333333;
                        --text-light: #666666;
                        --bg: #F8F9FA;
                        --white: #FFFFFF;
                        --shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                    }}
                    
                    body {{ 
                        font-family: 'Poppins', sans-serif;
                        background-color: var(--bg);
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        color: var(--text-dark);
                    }}
                    
                    .success-container {{
                        width: 90%;
                        max-width: 500px;
                        position: relative;
                    }}
                    
                    .success-card {{
                        background: var(--white);
                        border-radius: 20px;
                        box-shadow: var(--shadow);
                        overflow: hidden;
                        transform: translateY(20px);
                        opacity: 0;
                        animation: slideUp 0.5s ease forwards;
                    }}
                    
                    .card-header {{
                        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
                        color: white;
                        padding: 30px;
                        position: relative;
                    }}
                    
                    .card-header-icon {{
                        position: absolute;
                        top: -30px;
                        right: -30px;
                        width: 100px;
                        height: 100px;
                        background: rgba(255, 255, 255, 0.1);
                        border-radius: 50%;
                    }}
                    
                    .card-title {{
                        font-size: 24px;
                        font-weight: 700;
                        margin-bottom: 10px;
                    }}
                    
                    .card-subtitle {{
                        font-size: 16px;
                        opacity: 0.9;
                    }}
                    
                    .profile-image {{
                        width: 110px;
                        height: 110px;
                        border-radius: 50%;
                        border: 5px solid white;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                        position: absolute;
                        left: 30px;
                        bottom: -55px;
                        background: white;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        z-index: 10;
                    }}
                    
                    .profile-image i {{
                        font-size: 50px;
                        color: var(--primary);
                    }}
                    
                    .card-body {{
                        padding: 70px 30px 30px;
                    }}
                    
                    .info-box {{
                        padding: 20px;
                        background: #F5F7FA;
                        border-radius: 12px;
                        margin-bottom: 25px;
                        opacity: 0;
                        animation: fadeIn 0.5s ease 0.3s forwards;
                    }}
                    
                    .info-label {{
                        font-size: 13px;
                        color: var(--text-light);
                        margin-bottom: 5px;
                    }}
                    
                    .info-value {{
                        font-size: 16px;
                        font-weight: 600;
                        color: var(--text-dark);
                    }}
                    
                    .info-row {{
                        display: flex;
                        gap: 15px;
                        margin-bottom: 15px;
                    }}
                    
                    .info-row:last-child {{
                        margin-bottom: 0;
                    }}
                    
                    .info-item {{
                        flex: 1;
                    }}
                    
                    .success-badge {{
                        display: inline-flex;
                        align-items: center;
                        gap: 8px;
                        background: var(--primary-light);
                        color: var(--primary-dark);
                        padding: 8px 15px;
                        border-radius: 50px;
                        font-size: 14px;
                        font-weight: 600;
                        margin-bottom: 20px;
                        box-shadow: 0 3px 10px rgba(76, 175, 80, 0.15);
                        opacity: 0;
                        animation: fadeIn 0.5s ease 0.2s forwards;
                    }}
                    
                    .success-badge i {{
                        font-size: 16px;
                    }}
                    
                    .action-buttons {{
                        display: grid;
                        grid-template-columns: 1fr;
                        gap: 15px;
                        opacity: 0;
                        animation: fadeIn 0.5s ease 0.5s forwards;
                    }}
                    
                    .action-button {{
                        padding: 12px;
                        border-radius: 10px;
                        font-size: 15px;
                        font-weight: 600;
                        border: none;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        transition: all 0.3s ease;
                    }}
                    
                    .button-primary {{
                        background: var(--primary);
                        color: white;
                        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
                    }}
                    
                    .button-primary:hover {{
                        transform: translateY(-3px);
                        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
                    }}
                    
                    .button-primary i {{
                        margin-right: 8px;
                    }}
                    
                    /* Overlay checkmark */
                    .checkmark-overlay {{
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: rgba(0,0,0,0.5);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        z-index: 9999;
                        opacity: 1;
                        animation: fadeCheckmark 0.5s ease 2s forwards;
                    }}
                    
                    .checkmark-circle {{
                        width: 90px;
                        height: 90px;
                        background: white;
                        border-radius: 50%;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }}
                    
                    .checkmark-icon {{
                        color: var(--success);
                        font-size: 40px;
                        animation: scaleCheckmark 0.5s cubic-bezier(0.54, 1.82, 0.54, 0.86);
                    }}
                    
                    /* Animations */
                    @keyframes slideUp {{
                        from {{ transform: translateY(20px); opacity: 0; }}
                        to {{ transform: translateY(0); opacity: 1; }}
                    }}
                    
                    @keyframes fadeIn {{
                        from {{ opacity: 0; }}
                        to {{ opacity: 1; }}
                    }}
                    
                    @keyframes scaleCheckmark {{
                        0% {{ transform: scale(0); }}
                        50% {{ transform: scale(1.2); }}
                        100% {{ transform: scale(1); }}
                    }}
                    
                    @keyframes fadeCheckmark {{
                        to {{ opacity: 0; visibility: hidden; }}
                    }}
                </style>
            </head>
            <body>
                <!-- Initial checkmark overlay -->
                <div class="checkmark-overlay">
                    <div class="checkmark-circle">
                        <i class="fas fa-check checkmark-icon"></i>
                    </div>
                </div>
                
                <div class="success-container">
                    <div class="success-card">
                        <div class="card-header">
                            <div class="card-header-icon"></div>
                            <h1 class="card-title">Staff Added</h1>
                            <p class="card-subtitle">Staff member has been successfully added</p>
                            <div class="profile-image">
                                <i class="fas fa-user-tie"></i>
                            </div>
                        </div>
                        
                        <div class="card-body">
                            <div class="success-badge">
                                <i class="fas fa-check-circle"></i>
                                <span>Successfully Added</span>
                            </div>
                            
                            <div class="info-box">
                                <div class="info-row">
                                    <div class="info-item">
                                        <div class="info-label">Name</div>
                                        <div class="info-value">{staff.name}</div>
                                    </div>
                                    <div class="info-item">
                                        <div class="info-label">Email</div>
                                        <div class="info-value">{staff.email}</div>
                                    </div>
                                </div>
                                
                                <div class="info-row">
                                    <div class="info-item">
                                        <div class="info-label">Phone</div>
                                        <div class="info-value">{staff.phone}</div>
                                    </div>
                                    <div class="info-item">
                                        <div class="info-label">Place</div>
                                        <div class="info-value">{staff.place}</div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="action-buttons">
                                <button class="action-button button-primary" id="viewStaffBtn">
                                    <i class="fas fa-users"></i>View All Staff
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        // Button click handler
                        document.getElementById('viewStaffBtn').addEventListener('click', function() {{
                            window.location.href = '/viewstaff/';
                        }});
                        
                        // Auto redirect after 5 seconds
                        setTimeout(function() {{
                            window.location.href = '/viewstaff/';
                        }}, 5000);
                    }});
                </script>
            </body>
            </html>
            """
            return HttpResponse(success_html)
        else:
            # Print errors if form is invalid, for debugging purposes
            print(staffform.errors)
            # Optionally: Return errors to the template
            return render(request, "viewstaff.html", {"staffform": staffform, "errors": staffform.errors})
    else:
        staffform = StaffForm()  # Show an empty form if not a POST request

    return render(request, "viewstaff.html", {"staffform": staffform})



def viewstaff(request):
    cursor=connection.cursor()
    sql="select * from staff"
    cursor.execute(sql)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Sid':row[0], 'Name':row[1],'Gender': row[2],'Dob':row[3],'Address':row[4],'Place':row[5],'Phone':row[6],'Adhaar':row[7],'Email':row[8],'img':row[9]}
        tt.append(q)
    return render(request, 'viewstaff.html', {'tt':tt})


def deletestaff(request):
    cursor=connection.cursor()
    dlid=request.GET['id']
    s="delete from staff where Sid='%s'"%(dlid)  
    cursor.execute(s)
    
    # Create light red notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Staff Deleted</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #FF8A80, #FF5252);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #FF8A80, #FF5252);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-user-slash"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Staff Deleted</div>
                <div class="notification-subtext">Staff record has been successfully deleted</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewstaff/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def deletecustomer(request):
    cursor=connection.cursor()
    dlid=request.GET['id']
    s="delete from customer where Cid='%s'"%(dlid)  
    cursor.execute(s)
    
    # Create light red notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Customer Deleted</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #FF8A80, #FF5252);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #FF8A80, #FF5252);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-user-minus"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Customer Deleted</div>
                <div class="notification-subtext">Customer record has been successfully deleted</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewcustomer/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def viewproduct(request):
    cursor=connection.cursor()
    sql="select * from product"
    cursor.execute(sql)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Pid':row[0], 'Item':row[1],'Category': row[2],'Subcategory':row[3],'Des':row[4],'Amnt':row[5],'Stock':row[6],'Img':row[7]}
        tt.append(q)
    return render(request, 'viewproduct.html', {'tt':tt})

def viewcategory(request):
    cursor=connection.cursor()
    sql="select * from category"
    cursor.execute(sql)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Catid':row[0], 'Cname':row[1],'Description':row[2]}
        tt.append(q)
    return render(request, 'viewcategory.html', {'tt':tt})

def viewlocation(request):
    cursor=connection.cursor()
    sql="select * from location"
    cursor.execute(sql)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Locid':row[0], 'Location':row[1],'Area': row[2],'Rate':row[3],'Corate':row[4]}
        tt.append(q)
    return render(request, 'viewlocation.html', {'tt':tt})

def deleteproduct(request):
    try:
        cursor = connection.cursor()
        dlid = request.GET['id']
        s = "delete from product where Pid='%s'" % (dlid)
        cursor.execute(s)
        
        # Create HTML response with animated notification in LIGHT RED
        html_response = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Product Deleted</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
                .notification-wrapper {
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    display: flex; justify-content: center; align-items: center;
                    background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                    z-index: 1000;
                }
                .notification-container {
                    position: relative; background: rgba(255, 255, 255, 0.95);
                    border-radius: 24px; padding: 2rem;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                    animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                    max-width: 90%; width: 400px;
                }
                .icon-circle {
                    width: 80px; height: 80px; background: linear-gradient(45deg, #FF8A80, #E57373);
                    border-radius: 50%; display: flex; align-items: center;
                    justify-content: center; margin: 0 auto 1.5rem;
                    position: relative; overflow: hidden;
                    animation: popIn 0.5s ease-out forwards;
                    transform: scale(0);
                }
                .icon-circle i {
                    color: white; font-size: 32px;
                    transform: scale(0) rotate(-180deg);
                    animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
                }
                .ripple {
                    position: absolute; width: 100%; height: 100%;
                    border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                    animation: rippleEffect 1.5s linear infinite;
                }
                .notification-text, .notification-subtext {
                    text-align: center; opacity: 0;
                    animation: textFadeIn 0.5s ease 0.6s forwards;
                }
                .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
                .notification-subtext { color: #666; font-size: 1rem; }
                .progress-bar {
                    position: absolute; bottom: 0; left: 0; height: 4px;
                    background: linear-gradient(to right, #FF8A80, #E57373);
                    width: 100%; animation: progress 2s linear forwards;
                }

                /* Animations */
                @keyframes popIn {
                    0% { transform: scale(0); }
                    80% { transform: scale(1.2); }
                    100% { transform: scale(1); }
                }
                @keyframes tickBounce {
                    0% { transform: scale(0) rotate(-180deg); }
                    80% { transform: scale(1.2) rotate(10deg); }
                    100% { transform: scale(1) rotate(0deg); }
                }
                @keyframes rippleEffect {
                    0% { width: 0; height: 0; opacity: 0.5; }
                    100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
                }
                @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                @keyframes progress { from { width: 100%; } to { width: 0%; } }
                @keyframes fadeOut { to { opacity: 0; } }
            </style>
        </head>
        <body>
            <div class="notification-wrapper">
                <div class="notification-container">
                    <div class="icon-circle">
                        <i class="fas fa-check"></i>
                        <div class="ripple"></div>
                    </div>
                    <div class="notification-text">Product Deleted</div>
                    <div class="notification-subtext">The product has been successfully removed</div>
                    <div class="progress-bar"></div>
                </div>
            </div>
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    setTimeout(() => {
                        document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                        setTimeout(() => { window.location = '/viewproduct/'; }, 500);
                    }, 2000);
                });
            </script>
        </body>
        </html>
        """
        return HttpResponse(html_response)
        
    except Exception as e:
        # Error notification
        error_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
                .notification-wrapper {
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    display: flex; justify-content: center; align-items: center;
                    background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                    z-index: 1000;
                }
                .notification-container {
                    position: relative; background: rgba(255, 255, 255, 0.95);
                    border-radius: 24px; padding: 2rem;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                    animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                    max-width: 90%; width: 400px;
                }
                .icon-circle {
                    width: 80px; height: 80px; background: linear-gradient(45deg, #F44336, #D32F2F);
                    border-radius: 50%; display: flex; align-items: center;
                    justify-content: center; margin: 0 auto 1.5rem;
                    position: relative; overflow: hidden;
                    animation: popIn 0.5s ease-out forwards;
                    transform: scale(0);
                }
                .icon-circle i {
                    color: white; font-size: 32px;
                    transform: scale(0);
                    animation: errorBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
                }
                .ripple {
                    position: absolute; width: 100%; height: 100%;
                    border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                    animation: rippleEffect 1.5s linear infinite;
                }
                .notification-text, .notification-subtext {
                    text-align: center; opacity: 0;
                    animation: textFadeIn 0.5s ease 0.6s forwards;
                }
                .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
                .notification-subtext { color: #666; font-size: 1rem; }
                .progress-bar {
                    position: absolute; bottom: 0; left: 0; height: 4px;
                    background: linear-gradient(to right, #F44336, #D32F2F);
                    width: 100%; animation: progress 2s linear forwards;
                }

                /* Animations */
                @keyframes popIn {
                    0% { transform: scale(0); }
                    80% { transform: scale(1.2); }
                    100% { transform: scale(1); }
                }
                @keyframes errorBounce {
                    0% { transform: scale(0); }
                    80% { transform: scale(1.2); }
                    100% { transform: scale(1); }
                }
                @keyframes rippleEffect {
                    0% { width: 0; height: 0; opacity: 0.5; }
                    100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
                }
                @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                @keyframes progress { from { width: 100%; } to { width: 0%; } }
                @keyframes fadeOut { to { opacity: 0; } }
            </style>
        </head>
        <body>
            <div class="notification-wrapper">
                <div class="notification-container">
                    <div class="icon-circle">
                        <i class="fas fa-exclamation"></i>
                        <div class="ripple"></div>
                    </div>
                    <div class="notification-text">Deletion Failed</div>
                    <div class="notification-subtext">Unable to delete the product</div>
                    <div class="progress-bar"></div>
                </div>
            </div>
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    setTimeout(() => {
                        document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                        setTimeout(() => { window.location = '/viewproduct/'; }, 500);
                    }, 2000);
                });
            </script>
        </body>
        </html>
        """
        return HttpResponse(error_html)

def deletecategory(request):
    cursor=connection.cursor()
    dlid=request.GET['id']
    s="delete from category where Catid='%s'"%(dlid)
    cursor.execute(s)
    
    # Create a simple light red notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Category Deleted</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #FF8A80, #FF5252);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #FF8A80, #FF5252);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-trash-alt"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Category Deleted</div>
                <div class="notification-subtext">Category has been successfully deleted</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewcategory/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)


def deletelocation(request):
    cursor=connection.cursor()
    dlid=request.GET['id']
    s="delete from location where Locid='%s'"%(dlid)
    cursor.execute(s)
    
    # Create a simple light red notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Location Deleted</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #FF8A80, #FF5252);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #FF8A80, #FF5252);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-trash-alt"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Location Deleted</div>
                <div class="notification-subtext">Location has been successfully deleted</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewlocation/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def updateproduct(request):
    cursor=connection.cursor()
    upid=request.GET['id']
    s="select * from product where Pid='%s'"%(upid)
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Pid':row[0],'Item':row[1],'Category':row[2],'Subcategory':row[3],'Des':row[4],'Amnt':row[5],'Stock':row[6],'Img':row[7]}
        tt.append(q)
    return render(request, 'updateproduct.html', {'tt':tt})

def updateproductaction(request):
    try:
        cursor = connection.cursor()
        pid = request.GET['id']
        na = request.GET['name']
        cat = request.GET['category']
        subcat = request.GET['subcat']
        des = request.GET['description']
        amnt = request.GET['amount']
        stock = request.GET['stock']
        img = request.GET['Img']
        
        sql = "update product set Item='%s', Category='%s', Subcategory='%s', Des='%s',  Amnt='%s', Stock='%s', Img='%s' where Pid='%s'" % (na, cat, subcat, des, amnt, stock, img, pid)
        cursor.execute(sql)
        
        # Create HTML response with animated notification in LIGHT BLUE
        html_response = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Product Updated</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
                .notification-wrapper {
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    display: flex; justify-content: center; align-items: center;
                    background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                    z-index: 1000;
                }
                .notification-container {
                    position: relative; background: rgba(255, 255, 255, 0.95);
                    border-radius: 24px; padding: 2rem;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                    animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                    max-width: 90%; width: 400px;
                }
                .icon-circle {
                    width: 80px; height: 80px; background: linear-gradient(45deg, #90CAF9, #64B5F6);
                    border-radius: 50%; display: flex; align-items: center;
                    justify-content: center; margin: 0 auto 1.5rem;
                    position: relative; overflow: hidden;
                    animation: popIn 0.5s ease-out forwards;
                    transform: scale(0);
                }
                .icon-circle i {
                    color: white; font-size: 32px;
                    transform: scale(0) rotate(-180deg);
                    animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
                }
                .ripple {
                    position: absolute; width: 100%; height: 100%;
                    border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                    animation: rippleEffect 1.5s linear infinite;
                }
                .notification-text, .notification-subtext {
                    text-align: center; opacity: 0;
                    animation: textFadeIn 0.5s ease 0.6s forwards;
                }
                .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
                .notification-subtext { color: #666; font-size: 1rem; }
                .progress-bar {
                    position: absolute; bottom: 0; left: 0; height: 4px;
                    background: linear-gradient(to right, #90CAF9, #64B5F6);
                    width: 100%; animation: progress 2s linear forwards;
                }

                /* Animations */
                @keyframes popIn {
                    0% { transform: scale(0); }
                    80% { transform: scale(1.2); }
                    100% { transform: scale(1); }
                }
                @keyframes tickBounce {
                    0% { transform: scale(0) rotate(-180deg); }
                    80% { transform: scale(1.2) rotate(10deg); }
                    100% { transform: scale(1) rotate(0deg); }
                }
                @keyframes rippleEffect {
                    0% { width: 0; height: 0; opacity: 0.5; }
                    100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
                }
                @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                @keyframes progress { from { width: 100%; } to { width: 0%; } }
                @keyframes fadeOut { to { opacity: 0; } }
            </style>
        </head>
        <body>
            <div class="notification-wrapper">
                <div class="notification-container">
                    <div class="icon-circle">
                        <i class="fas fa-check"></i>
                        <div class="ripple"></div>
                    </div>
                    <div class="notification-text">Product Updated</div>
                    <div class="notification-subtext">Your changes have been saved successfully</div>
                    <div class="progress-bar"></div>
                </div>
            </div>
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    setTimeout(() => {
                        document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                        setTimeout(() => { window.location = '/viewproduct/'; }, 500);
                    }, 2000);
                });
            </script>
        </body>
        </html>
        """
        return HttpResponse(html_response)
        
    except Exception as e:
        # Error notification
        error_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
                .notification-wrapper {
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    display: flex; justify-content: center; align-items: center;
                    background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                    z-index: 1000;
                }
                .notification-container {
                    position: relative; background: rgba(255, 255, 255, 0.95);
                    border-radius: 24px; padding: 2rem;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                    animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                    max-width: 90%; width: 400px;
                }
                .icon-circle {
                    width: 80px; height: 80px; background: linear-gradient(45deg, #F44336, #D32F2F);
                    border-radius: 50%; display: flex; align-items: center;
                    justify-content: center; margin: 0 auto 1.5rem;
                    position: relative; overflow: hidden;
                    animation: popIn 0.5s ease-out forwards;
                    transform: scale(0);
                }
                .icon-circle i {
                    color: white; font-size: 32px;
                    transform: scale(0);
                    animation: errorBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
                }
                .ripple {
                    position: absolute; width: 100%; height: 100%;
                    border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                    animation: rippleEffect 1.5s linear infinite;
                }
                .notification-text, .notification-subtext {
                    text-align: center; opacity: 0;
                    animation: textFadeIn 0.5s ease 0.6s forwards;
                }
                .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
                .notification-subtext { color: #666; font-size: 1rem; }
                .progress-bar {
                    position: absolute; bottom: 0; left: 0; height: 4px;
                    background: linear-gradient(to right, #F44336, #D32F2F);
                    width: 100%; animation: progress 2s linear forwards;
                }

                /* Animations */
                @keyframes popIn {
                    0% { transform: scale(0); }
                    80% { transform: scale(1.2); }
                    100% { transform: scale(1); }
                }
                @keyframes errorBounce {
                    0% { transform: scale(0); }
                    80% { transform: scale(1.2); }
                    100% { transform: scale(1); }
                }
                @keyframes rippleEffect {
                    0% { width: 0; height: 0; opacity: 0.5; }
                    100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
                }
                @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                @keyframes progress { from { width: 100%; } to { width: 0%; } }
                @keyframes fadeOut { to { opacity: 0; } }
            </style>
        </head>
        <body>
            <div class="notification-wrapper">
                <div class="notification-container">
                    <div class="icon-circle">
                        <i class="fas fa-exclamation"></i>
                        <div class="ripple"></div>
                    </div>
                    <div class="notification-text">Update Failed</div>
                    <div class="notification-subtext">Unable to update the product</div>
                    <div class="progress-bar"></div>
                </div>
            </div>
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    setTimeout(() => {
                        document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                        setTimeout(() => { window.location = '/viewproduct/'; }, 500);
                    }, 2000);
                });
            </script>
        </body>
        </html>
        """
        return HttpResponse(error_html)

def application(request):
    cursor=connection.cursor()
    sql="select * from location"
    cursor.execute(sql)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Locid':row[0], 'Location':row[1],'Area': row[2],'Rate':row[3],'Corate':row[4]}
        tt.append(q)
    return render(request, 'application.html' ,{'tt':tt})

def applicationaction(request):
    cursor = connection.cursor()
    name = request.GET['name']
    addr = request.GET['address']
    area = request.GET['area']
    loc = request.GET['location']
    house = request.GET['house']
    ph = request.GET['phone']
    date = today
    type = request.GET['type']
    uid = request.session['Uid']
    
    # Check if the user has already submitted an application
    check_sql = "SELECT COUNT(*) FROM application WHERE Uid = %s"
    cursor.execute(check_sql, [uid])
    result = cursor.fetchone()
    
    if result[0] > 0:  # If count is greater than 0, the user has already submitted an application
        # Create already submitted notification with light blue theme
        already_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Application Already Exists</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
                .notification-wrapper {
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    display: flex; justify-content: center; align-items: center;
                    background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                    z-index: 1000;
                }
                .notification-container {
                    position: relative; background: rgba(255, 255, 255, 0.95);
                    border-radius: 24px; padding: 2rem;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                    animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                    max-width: 90%; width: 400px;
                }
                .icon-circle {
                    width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                    border-radius: 50%; display: flex; align-items: center;
                    justify-content: center; margin: 0 auto 1.5rem;
                    position: relative; overflow: hidden;
                    animation: popIn 0.5s ease-out forwards;
                    transform: scale(0);
                }
                .icon-circle i {
                    color: white; font-size: 32px;
                    transform: scale(0) rotate(-180deg);
                    animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
                }
                .ripple {
                    position: absolute; width: 100%; height: 100%;
                    border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                    animation: rippleEffect 1.5s linear infinite;
                }
                .notification-text, .notification-subtext {
                    text-align: center; opacity: 0;
                    animation: textFadeIn 0.5s ease 0.6s forwards;
                }
                .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
                .notification-subtext { color: #666; font-size: 1rem; }
                .progress-bar {
                    position: absolute; bottom: 0; left: 0; height: 4px;
                    background: linear-gradient(to right, #64B5F6, #2196F3);
                    width: 100%; animation: progress 2s linear forwards;
                }

                /* Animations */
                @keyframes floatIn {
                    from { transform: translateY(20px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
                @keyframes popIn {
                    0% { transform: scale(0); }
                    80% { transform: scale(1.2); }
                    100% { transform: scale(1); }
                }
                @keyframes tickBounce {
                    0% { transform: scale(0) rotate(-180deg); }
                    80% { transform: scale(1.2) rotate(10deg); }
                    100% { transform: scale(1) rotate(0deg); }
                }
                @keyframes rippleEffect {
                    0% { width: 0; height: 0; opacity: 0.5; }
                    100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
                }
                @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                @keyframes progress { from { width: 100%; } to { width: 0%; } }
                @keyframes fadeOut { to { opacity: 0; } }
            </style>
        </head>
        <body>
            <div class="notification-wrapper">
                <div class="notification-container">
                    <div class="icon-circle">
                        <i class="fas fa-info"></i>
                        <div class="ripple"></div>
                    </div>
                    <div class="notification-text">Application Exists</div>
                    <div class="notification-subtext">You have already submitted an application</div>
                    <div class="progress-bar"></div>
                </div>
            </div>
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    setTimeout(() => {
                        document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                        setTimeout(() => { window.location = '/application/'; }, 500);
                    }, 2000);
                });
            </script>
        </body>
        </html>
        """
        return HttpResponse(already_html)
    
    # If no application is found, insert the new application
    sql = """
    INSERT INTO application(Name, Address, Area, Location, Houseno, Phone, Uid, Status, Date, type)
    VALUES(%s, %s, %s, %s, %s, %s, %s, 'pending', %s, %s)
    """
    cursor.execute(sql, [name, addr, area, loc, house, ph, uid, date, type])
    
    # Create success notification with light blue theme
    success_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Application Submitted</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #64B5F6, #2196F3);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-file-alt"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Application Submitted</div>
                <div class="notification-subtext">Your application has been successfully submitted</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/application/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(success_html)

def viewapplication(request):
    cursor=connection.cursor()
    sql="select * from application"
    cursor.execute(sql)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Appno':row[0], 'Name':row[1],'Address': row[2],'Area':row[3],'Houseno':row[5],'Phone':row[6],'Status':row[8],'Date':row[9]}
        tt.append(q)
    return render(request, 'viewapplication.html', {'tt':tt})



def updatecustomer(request):
    cursor=connection.cursor()
    upid=request.GET['id']
    s="select * from customer where Cid='%s'"%(upid)
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Cid':row[0],'Name':row[1],'Address':row[2],'Phone':row[3],'Gender':row[4],'Email':row[5]}
        tt.append(q)
    return render(request, 'updatecustomer.html', {'tt':tt})


def updatecustomeraction(request):
    cursor=connection.cursor()
    cid=request.GET['id']
    na=request.GET['name']
    addr=request.GET['address']
    ph=request.GET['phone']
    gen=request.GET['gender']
    mail=request.GET['email']
    sql="update customer set Name='%s', Address='%s', Phone='%s', Gender='%s', Email='%s' where Cid='%s'"%(na, addr, ph, gen, mail, cid)
    cursor.execute(sql)
    
    # Create light blue notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Customer Updated</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #64B5F6, #2196F3);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-user-edit"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Customer Updated</div>
                <div class="notification-subtext">Customer information has been successfully updated</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewcustomer/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def updatestaff(request):
    cursor=connection.cursor()
    upid=request.GET['id']
    s="select * from staff where Sid='%s'"%(upid)
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Sid':row[0],'Name':row[1],'Gender':row[2],'Dob':row[3],'Address':row[4],'Place':row[5],'Phone':row[6],'Adhaar':row[7],'Email':row[8]}
        tt.append(q)
    return render(request, 'updatestaff.html', {'tt':tt})


def updatestaffingaction(request):
    cursor=connection.cursor()
    sid=request.GET['id']
    na=request.GET['staffname']
    gen=request.GET['gender']
    dob=request.GET['date']
    addr=request.GET['address']
    plc=request.GET['place']
    phn=request.GET['phone']
    adhr=request.GET['adhaar']
    email=request.GET['email']
    sql="update staff set Name='%s', Gender='%s', Dob='%s', Address='%s', Place='%s', Phone='%s', Adhaar='%s', Email='%s' where Sid='%s'"%(na, gen, dob, addr, plc, phn, adhr, email, sid)
    cursor.execute(sql)
    
    # Create light blue notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Staff Updated</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #64B5F6, #2196F3);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-user-edit"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Staff Updated</div>
                <div class="notification-subtext">Staff information has been successfully updated</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewstaff/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def updatecategory(request):
    cursor=connection.cursor()
    upid=request.GET['id']
    s="select * from category where Catid='%s'"%(upid)
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Catid':row[0],'Cname':row[1],'Description':row[2]}
        tt.append(q)
    return render(request, 'updatecategory.html', {'tt':tt})

def updatecategoryaction(request):
    cursor=connection.cursor()
    cid=request.GET['id']
    cat=request.GET['category']
    des=request.GET['des']
    sql="update category set Cname='%s', Description='%s' where Catid='%s'"%(cat,des,cid)
    cursor.execute(sql)
    
    # Create a light blue notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Category Updated</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #64B5F6, #2196F3);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-check"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Category Updated</div>
                <div class="notification-subtext">The category has been successfully updated</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewcategory/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def updatelocation(request):
    cursor=connection.cursor()
    upid=request.GET['id']
    s="select * from location where Locid='%s'"%(upid)
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Locid':row[0],'Location':row[1],'Area':row[2],'Rate':row[3],'Corate':row[4]}
        tt.append(q)
    return render(request, 'updatelocation.html', {'tt':tt})

def updatelocationaction(request):
    cursor=connection.cursor()
    lid=request.GET['id']
    loc=request.GET['location']
    area=request.GET['address']
    rate=request.GET['rate']
    corate=request.GET['corate']
    sql="update location set Location='%s', Area='%s', Rate='%s', Corate='%s' where Locid='%s'"%(loc, area, rate, corate, lid)
    cursor.execute(sql)
    
    # Create light blue notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Location Updated</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #64B5F6, #2196F3);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-pencil-alt"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Location Updated</div>
                <div class="notification-subtext">Your location has been successfully updated</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewlocation/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def approveapplication(request):
    cursor=connection.cursor()
    upid=request.GET['id']
    s="update application set Status='approved' where Appno='%s'"%(upid)
    cursor.execute(s)
    
    # Create light blue notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Application Approved</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #64B5F6, #2196F3);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-check-double"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Application Approved</div>
                <div class="notification-subtext">Application has been successfully approved</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewapplication/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def rejectapplication(request):
    cursor=connection.cursor()
    upid=request.GET['id']
    s="update application set Status='rejected' where Appno='%s'"%(upid)
    cursor.execute(s)
    
    # Create light red notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Application Rejected</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #FF8A80, #FF5252);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #FF8A80, #FF5252);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-times"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Application Rejected</div>
                <div class="notification-subtext">Application has been rejected</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewapplication/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def managerate(request):
    return render(request, 'managerate.html')



def viewmanagerateaction(request):
    try:
        cursor = connection.cursor()
        
        # Get request parameters safely
        mpc = request.GET.get('municipality', '')
        rate = request.GET.get('rate', '')
        type_ = request.GET.get('type', '')
        district = request.GET.get('district', '')

        # Use parameterized query to prevent SQL injection
        sql = "INSERT INTO managerate (Mpc, Rate, Type, District) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, [mpc, rate, type_, district])

        html_response = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Update Notification</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
                .notification-wrapper {
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    display: flex; justify-content: center; align-items: center;
                    background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                    z-index: 1000;
                }
                .notification-container {
                    position: relative; background: rgba(255, 255, 255, 0.95);
                    border-radius: 24px; padding: 2rem;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                    animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                    max-width: 90%; width: 400px;
                }
                .icon-circle {
                    width: 80px; height: 80px; background: linear-gradient(45deg, #2196F3, #1976D2);
                    border-radius: 50%; display: flex; align-items: center;
                    justify-content: center; margin: 0 auto 1.5rem;
                    position: relative; overflow: hidden;
                    animation: popIn 0.5s ease-out forwards;
                    transform: scale(0);
                }
                .icon-circle i {
                    color: white; font-size: 32px;
                    transform: scale(0) rotate(-180deg);
                    animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
                }
                .ripple {
                    position: absolute; width: 100%; height: 100%;
                    border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                    animation: rippleEffect 1.5s linear infinite;
                }
                .notification-text, .notification-subtext {
                    text-align: center; opacity: 0;
                    animation: textFadeIn 0.5s ease 0.6s forwards;
                }
                .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
                .notification-subtext { color: #666; font-size: 1rem; }
                .progress-bar {
                    position: absolute; bottom: 0; left: 0; height: 4px;
                    background: linear-gradient(to right, #2196F3, #1976D2);
                    width: 100%; animation: progress 2s linear forwards;
                }

                /* Animations */
                @keyframes popIn {
                    0% { transform: scale(0); }
                    80% { transform: scale(1.2); }
                    100% { transform: scale(1); }
                }
                @keyframes tickBounce {
                    0% { transform: scale(0) rotate(-180deg); }
                    80% { transform: scale(1.2) rotate(10deg); }
                    100% { transform: scale(1) rotate(0deg); }
                }
                @keyframes rippleEffect {
                    0% { width: 0; height: 0; opacity: 0.5; }
                    100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
                }
                @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                @keyframes progress { from { width: 100%; } to { width: 0%; } }
                @keyframes fadeOut { to { opacity: 0; } }
            </style>
        </head>
        <body>
            <div class="notification-wrapper">
                <div class="notification-container">
                    <div class="icon-circle">
                        <i class="fas fa-check"></i>
                        <div class="ripple"></div>
                    </div>
                    <div class="notification-text">Successfully Updated</div>
                    <div class="notification-subtext">Your changes have been saved</div>
                    <div class="progress-bar"></div>
                </div>
            </div>
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    setTimeout(() => {
                        document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                        setTimeout(() => { window.location = '/viewmanagerate/'; }, 500);
                    }, 2000);
                });
            </script>
        </body>
        </html>
        """
        return HttpResponse(html_response)

    except Exception as e:
        print(f"Error: {e}")  # Log error for debugging
        return HttpResponse("<h3>Update Failed</h3>")  # Simple error message


def viewmanagerate(request):
    cursor=connection.cursor()
    sql="select * from managerate"
    cursor.execute(sql)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Mrid':row[0],'Mpc':row[1],'Rate':row[2],'Type':row[3],'District':row[4]}
        tt.append(q)
    return render(request, 'viewmanagerate.html', {'tt':tt})

def updatemanagerate(request):
    cursor=connection.cursor()
    upid=request.GET['id']
    s="select * from managerate where Mrid='%s'"%(upid)
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Mrid':row[0],'Mpc':row[1],'Rate':row[2],'Type':row[3],'District':row[4]}
        tt.append(q)
    return render(request, 'updatemanagerate.html', {'tt':tt})

def updatemanagerateaction(request):
    try:
        cursor = connection.cursor()
        mid = request.GET['id']
        mpc = request.GET['mpc']
        rate = request.GET['rate']
        type = request.GET['type']
        district = request.GET['district']
        
        sql = "update managerate set Mpc='%s', Rate='%s', Type='%s', District='%s' where Mrid='%s'" % (mpc, rate, type, district, mid)
        cursor.execute(sql)
        
        html_response = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update Notification</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #f5f5f5;
        }

        .notification-wrapper {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(8px);
            z-index: 1000;
        }

        .notification-container {
            position: relative;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            transform: translateY(20px);
            animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
            max-width: 90%;
            width: 400px;
        }

        .icon-circle {
            width: 80px;
            height: 80px;
            background: linear-gradient(45deg, #00E676, #00C853);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.5rem;
            position: relative;
            animation: iconPop 0.6s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.2s forwards;
            transform: scale(0);
        }

        .icon-circle i {
            color: white;
            font-size: 32px;
            animation: iconRotate 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.4s forwards;
            transform: scale(0) rotate(-180deg);
        }

        .notification-text {
            text-align: center;
            color: #333;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            opacity: 0;
            animation: textFadeIn 0.5s ease 0.6s forwards;
        }

        .notification-subtext {
            text-align: center;
            color: #666;
            font-size: 1rem;
            opacity: 0;
            animation: textFadeIn 0.5s ease 0.7s forwards;
        }

        .progress-bar {
            position: absolute;
            bottom: 0;
            left: 0;
            height: 4px;
            background: linear-gradient(to right, #2196F3, #1976D2);
            border-radius: 0 0 24px 24px;
            width: 100%;
            animation: progress 2s linear forwards;
        }

        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.4);
            animation: ripple 1s linear infinite;
            top: 50%;
            left: 50%;
        }

        @keyframes floatIn {
            0% {
                opacity: 0;
                transform: translateY(20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes iconPop {
            0% {
                transform: scale(0);
            }
            100% {
                transform: scale(1);
            }
        }

        @keyframes iconRotate {
            0% {
                transform: scale(0) rotate(-180deg);
            }
            100% {
                transform: scale(1) rotate(0);
            }
        }

        @keyframes textFadeIn {
            0% {
                opacity: 0;
                transform: translateY(10px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes progress {
            0% {
                width: 100%;
            }
            100% {
                width: 0%;
            }
        }

        @keyframes ripple {
            0% {
                width: 0;
                height: 0;
                opacity: 0.5;
            }
            100% {
                width: 150px;
                height: 150px;
                opacity: 0;
                transform: translate(-50%, -50%);
            }
        }

        @keyframes fadeOut {
            to {
                opacity: 0;
            }
        }
    </style>
</head>
<body>
    <div class="notification-wrapper">
        <div class="notification-container">
            <div class="icon-circle">
                <i class="fas fa-check"></i>
                <div class="ripple"></div>
            </div>
            <div class="notification-text">Successfully Updated</div>
            <div class="notification-subtext">Your changes have been saved</div>
            <div class="progress-bar"></div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const wrapper = document.querySelector('.notification-wrapper');
            
            setTimeout(() => {
                wrapper.style.animation = 'fadeOut 0.5s ease forwards';
                
                setTimeout(() => {
                    window.location = '/viewmanagerate/';
                }, 500);
            }, 2000);
        });
    </script>
</body>
</html>
        """
        return HttpResponse(html_response)
        
    except Exception as e:
        error_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Same head and styles as above -->
</head>
<body>
    <div class="notification-wrapper">
        <div class="notification-container">
            <div class="icon-circle" style="background: linear-gradient(45deg, #FF5252, #D50000);">
                <i class="fas fa-exclamation-triangle"></i>
                <div class="ripple"></div>
            </div>
            <div class="notification-text">Update Failed</div>
            <div class="notification-subtext">Could not save your changes</div>
            <div class="progress-bar" style="background: linear-gradient(to right, #FF5252, #D50000);"></div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const wrapper = document.querySelector('.notification-wrapper');
            setTimeout(() => {
                wrapper.style.animation = 'fadeOut 0.5s ease forwards';
                setTimeout(() => {
                    window.location = '/viewmanagerate/';
                }, 500);
            }, 2000);
        });
    </script>
</body>
</html>
        """
        return HttpResponse(error_html)

def deletemanagerate(request):
    try:
        cursor = connection.cursor()
        dlid = request.GET['id']
        sql = "delete from managerate where Mrid='%s'" % (dlid)
        cursor.execute(sql)
        
        html_response = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Notification</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #f5f5f5;
        }

        .notification-wrapper {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(8px);
            z-index: 1000;
        }

        .notification-container {
            position: relative;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            transform: translateY(20px);
            animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
            max-width: 90%;
            width: 400px;
        }

        .icon-circle {
            width: 80px;
            height: 80px;
            background: linear-gradient(45deg, #FF5252, #FF1744);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.5rem;
            position: relative;
            animation: iconPop 0.6s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.2s forwards;
            transform: scale(0);
        }

        .icon-circle.error {
            background: linear-gradient(45deg, #FF5252, #D50000);
        }

        .icon-circle i {
            color: white;
            font-size: 32px;
            animation: iconRotate 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.4s forwards;
            transform: scale(0) rotate(-180deg);
        }

        .notification-text {
            text-align: center;
            color: #333;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            opacity: 0;
            animation: textFadeIn 0.5s ease 0.6s forwards;
        }

        .notification-subtext {
            text-align: center;
            color: #666;
            font-size: 1rem;
            opacity: 0;
            animation: textFadeIn 0.5s ease 0.7s forwards;
        }

        .progress-bar {
            position: absolute;
            bottom: 0;
            left: 0;
            height: 4px;
            background: linear-gradient(to right, #00E676, #00C853);
            border-radius: 0 0 24px 24px;
            width: 100%;
            animation: progress 2s linear forwards;
        }

        .progress-bar.error {
            background: linear-gradient(to right, #FF5252, #D50000);
        }

        /* Ripple effect */
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.4);
            animation: ripple 1s linear infinite;
            top: 50%;
            left: 50%;
        }

        @keyframes floatIn {
            0% {
                opacity: 0;
                transform: translateY(20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes iconPop {
            0% {
                transform: scale(0);
            }
            100% {
                transform: scale(1);
            }
        }

        @keyframes iconRotate {
            0% {
                transform: scale(0) rotate(-180deg);
            }
            100% {
                transform: scale(1) rotate(0);
            }
        }

        @keyframes textFadeIn {
            0% {
                opacity: 0;
                transform: translateY(10px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes progress {
            0% {
                width: 100%;
            }
            100% {
                width: 0%;
            }
        }

        @keyframes ripple {
            0% {
                width: 0;
                height: 0;
                opacity: 0.5;
            }
            100% {
                width: 150px;
                height: 150px;
                opacity: 0;
                transform: translate(-50%, -50%);
            }
        }

        @keyframes fadeOut {
            to {
                opacity: 0;
            }
        }
    </style>
</head>
<body>
    <div class="notification-wrapper">
        <div class="notification-container">
            <div class="icon-circle">
                <i class="fas fa-check"></i>
                <div class="ripple"></div>
            </div>
            <div class="notification-text">Successfully Deleted</div>
            <div class="notification-subtext">Redirecting you back...</div>
            <div class="progress-bar"></div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const wrapper = document.querySelector('.notification-wrapper');
            
            // Fade out the entire notification
            setTimeout(() => {
                wrapper.style.animation = 'fadeOut 0.5s ease forwards';
                
                // Redirect after fade out
                setTimeout(() => {
                    window.location = '/viewmanagerate/';
                }, 500);
            }, 2000);
        });
    </script>
</body>
</html>
        """
        return HttpResponse(html_response)
        
    except Exception as e:
        # In case of error, show error notification
        error_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Same head and style content as above -->
</head>
<body>
    <div class="notification-container">
        <div class="notification error">
            <div class="success-icon">
                <i class="fas fa-exclamation-triangle"></i>
            </div>
            <div class="message">Error: Could not delete record</div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(function() {
                const notification = document.querySelector('.notification-container');
                notification.style.animation = 'slideOut 0.5s ease forwards';
                
                setTimeout(function() {
                    window.location = '/viewmanagerate/';
                }, 500);
            }, 2000);
        });
    </script>
</body>
</html>
        """
        return HttpResponse(error_html)
    




def subcategory(request):
    cursor=connection.cursor()
    s="SELECT * FROM category"
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Catid':row[0], 'Cname':row[1], 'Description':row[2]}
        tt.append(q)
    return render(request,'viewsubcategory.html',{'tt':tt})

def viewsubcataction(request):
    cursor=connection.cursor()
    subname=request.GET['catname']
    cat=request.GET['category']
    des=request.GET['description']
    sql="INSERT INTO subcategory(Subcategoryname,Category,Description)VALUES('%s','%s','%s')"%(subname, cat, des)
    cursor.execute(sql)
    
    # Create a simple light blue notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Subcategory Added</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #64B5F6, #2196F3);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-folder-plus"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Subcategory Added</div>
                <div class="notification-subtext">Subcategory has been successfully added</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/subcategory/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)




def viewratedetails(request):
    cursor=connection.cursor()
    s="SELECT * FROM managerate"
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Mrid':row[0], 'Mpc':row[1], 'Rate':row[2],'Type':row[3],'District':row[4]}
        tt.append(q)
    return render(request,'viewratedetails.html',{'tt':tt})

def viewcustpro(request):
    cursor=connection.cursor()
    s="SELECT * FROM product"
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
         q={'Pid':row[0],'Item':row[1],'Category':row[2],'Subcategory':row[3],'Des':row[4],'Amnt':row[5],'Stock':row[6],'Img':row[7]}
         tt.append(q)
    return render(request, 'viewcustpro.html', {'tt':tt})



def pdetails(request):
    cursor=connection.cursor()
    s="SELECT * from product where  Pid='%s'" %(request.GET['id'])
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Pid':row[0],'Item':row[1],'Category':row[2],'Subcategory':row[3],'Des':row[4],'Amnt':row[5],'Stock':row[6],'Img':row[7]}
        tt.append(q)
    return render(request,'pdetails.html',{'tt':tt})    


def addtocart(request):
    cursor = connection.cursor()
    bi = request.GET['bi']
    qty = request.GET['qty']
    uid = request.session['Uid']

    sql2 = "SELECT * FROM cart WHERE Pid = %s AND Uid = %s"
    cursor.execute(sql2, [bi, uid])
    result = cursor.fetchall()

    if cursor.rowcount > 0:
        success_message = "Already Exists in Cart"
        icon_class = "fas fa-info-circle"
    else:
        sql1 = "INSERT INTO cart (Pid, Uid, Cqty) VALUES (%s, %s, %s)"
        cursor.execute(sql1, [bi, uid, qty])
        success_message = "Added to Cart"
        icon_class = "fas fa-shopping-cart"

    # HTML animation response with unique purple/orange gradient theme
    success_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cart Update</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #f5f5f5; }}
            
            /* Unique vibrant gradient theme - purple to orange */
            :root {{
                --gradient-start: #9C27B0;  /* Vibrant purple */
                --gradient-end: #FF9800;    /* Vibrant orange */
                --accent-light: #E1BEE7;    /* Light purple */
            }}
            
            .notification-wrapper {{
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px); z-index: 1000;
            }}
            
            .notification-container {{
                background: rgba(255, 255, 255, 0.95); 
                border-radius: 24px; 
                padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1); 
                transform: translateY(20px);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; 
                width: 400px; 
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            
            /* Decorative corner element */
            .notification-container::before {{
                content: '';
                position: absolute;
                width: 150px;
                height: 150px;
                background: linear-gradient(45deg, var(--gradient-start), var(--gradient-end));
                opacity: 0.1;
                border-radius: 50%;
                top: -75px;
                right: -75px;
            }}
            
            /* Main circular icon with gradient */
            .icon-circle {{
                width: 80px; 
                height: 80px; 
                background: linear-gradient(45deg, var(--gradient-start), var(--gradient-end));
                border-radius: 50%; 
                display: flex; 
                align-items: center; 
                justify-content: center;
                margin: 0 auto 1.5rem; 
                animation: iconPop 0.6s ease-out 0.2s forwards;
                transform: scale(0);
                position: relative;
                box-shadow: 0 10px 20px rgba(156, 39, 176, 0.2);
            }}
            
            /* Pulsing effect behind the icon */
            .icon-circle::before {{
                content: '';
                position: absolute;
                width: 100%;
                height: 100%;
                border-radius: 50%;
                background: linear-gradient(45deg, var(--gradient-start), var(--gradient-end));
                opacity: 0.6;
                z-index: -1;
                animation: pulse 2s infinite;
            }}
            
            .icon-circle i {{
                color: white; 
                font-size: 32px; 
                animation: iconRotate 0.5s ease-out 0.4s forwards;
                transform: scale(0) rotate(-180deg);
            }}
            
            .notification-text {{
                color: #333; 
                font-size: 1.5rem; 
                font-weight: 600; 
                margin-bottom: 0.5rem;
                opacity: 0; 
                animation: textFadeIn 0.5s ease 0.6s forwards;
                background: linear-gradient(45deg, var(--gradient-start), var(--gradient-end));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .notification-subtext {{
                color: #666; 
                font-size: 1rem; 
                opacity: 0; 
                animation: textFadeIn 0.5s ease 0.7s forwards;
            }}
            
            /* Animated confetti particles */
            .confetti {{
                position: absolute;
                width: 10px;
                height: 10px;
                background-color: var(--accent-light);
                opacity: 0;
                animation: confettiFall 3s ease-out forwards;
            }}
            
            .progress-bar {{
                position: absolute; 
                bottom: 0; 
                left: 0; 
                height: 4px;
                background: linear-gradient(to right, var(--gradient-start), var(--gradient-end));
                width: 100%; 
                animation: progress 2s linear forwards;
            }}
            
            /* Animations */
            @keyframes floatIn {{ 
                from {{ opacity: 0; transform: translateY(20px); }} 
                to {{ opacity: 1; transform: translateY(0); }} 
            }}
            
            @keyframes iconPop {{ 
                from {{ transform: scale(0); }} 
                to {{ transform: scale(1); }} 
            }}
            
            @keyframes iconRotate {{ 
                from {{ transform: scale(0) rotate(-180deg); }} 
                to {{ transform: scale(1) rotate(0); }} 
            }}
            
            @keyframes textFadeIn {{ 
                from {{ opacity: 0; transform: translateY(10px); }} 
                to {{ opacity: 1; transform: translateY(0); }} 
            }}
            
            @keyframes progress {{ 
                from {{ width: 100%; }} 
                to {{ width: 0%; }} 
            }}
            
            @keyframes fadeOut {{ 
                to {{ opacity: 0; }} 
            }}
            
            @keyframes pulse {{
                0% {{ transform: scale(1); opacity: 0.6; }}
                50% {{ transform: scale(1.1); opacity: 0.3; }}
                100% {{ transform: scale(1); opacity: 0.6; }}
            }}
            
            @keyframes confettiFall {{
                0% {{ transform: translateY(-100px) rotate(0deg); opacity: 1; }}
                100% {{ transform: translateY(400px) rotate(360deg); opacity: 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="{icon_class}"></i>
                </div>
                <div class="notification-text">{success_message}</div>
                <div class="notification-subtext">Check your cart for details</div>
                <div class="progress-bar"></div>
            </div>
        </div>

        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                const wrapper = document.querySelector('.notification-wrapper');
                const container = document.querySelector('.notification-container');
                
                // Create confetti effect
                for (let i = 0; i < 15; i++) {{
                    const confetti = document.createElement('div');
                    confetti.classList.add('confetti');
                    
                    // Random position, size, and delay
                    confetti.style.left = Math.random() * 100 + '%';
                    confetti.style.width = Math.random() * 8 + 4 + 'px';
                    confetti.style.height = Math.random() * 8 + 4 + 'px';
                    confetti.style.animationDelay = Math.random() * 1.5 + 's';
                    
                    // Random colors
                    const colors = ['#9C27B0', '#FF9800', '#E1BEE7', '#FFE0B2'];
                    confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                    
                    // Random shapes
                    if (Math.random() > 0.6) {{
                        confetti.style.borderRadius = '50%';
                    }}
                    
                    container.appendChild(confetti);
                }}

                // Fade out the notification and redirect
                setTimeout(() => {{
                    wrapper.style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => {{
                        window.location = '/viewcustpro/';
                    }}, 500);
                }}, 2000);
            }});
        </script>
    </body>
    </html>
    """
    
    return HttpResponse(success_html)



def viewcart(request):
    cursor = connection.cursor()
    uid = request.session.get('Uid')  
    if not uid:
        return render(request, 'viewcart.html', {'tt': [], 'total': 0})
    q = """SELECT product.Pid, product.Item, product.Des, product.Amnt, product.Stock, product.Img, cart.Cqty, cart.Cartid FROM product INNER JOIN cart ON product.Pid = cart.Pid WHERE cart.Uid = %s"""
    cursor.execute(q, [uid])  
    rs = cursor.fetchall()
    tt = []
    total = 0
    for row in rs:
        Cqty = int(row[6])
        Amnt = int(row[3])
        item_total = Cqty * Amnt  
        total += item_total
        q = {'Pid': row[0],'Item': row[1],'Des': row[2],'Amnt': row[3],'Stock': row[4],'Img': row[5],'Cqty': row[6],'Cartid': row[7],'item_total': item_total  
        }
        tt.append(q)
    return render(request, 'viewcart.html', {'tt': tt, 'total': total})


def deletecart(request):
    cursor=connection.cursor()
    bi=request.GET['id']
    sql="delete from cart where Cartid='%s'"%(bi)
    cursor.execute(sql)
    
    # Create light red notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Item Removed</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #FF8A80, #FF5252);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #FF8A80, #FF5252);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-shopping-cart"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Item Removed</div>
                <div class="notification-subtext">Item has been removed from your cart</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewcart/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)


def updatecart(request):
    cursor=connection.cursor()
    bi=request.GET['bi']
    qty=request.GET['qty']
    sql="update cart set Cqty='%s' where Cartid='%s'"%(qty, bi)
    print(sql)
    cursor.execute(sql)
    
    # Create light blue notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cart Updated</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #64B5F6, #2196F3);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-sync-alt"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Cart Updated</div>
                <div class="notification-subtext">Quantity has been successfully updated</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/viewcart/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)



# from django.shortcuts import render
# from django.db import connection

def orders(request):
    cursor = connection.cursor()

    # Join orders, customer, and product tables to get all necessary details
    s = """
        SELECT 
            orders.Oid, orders.Odate, orders.Pid, orders.Uid, orders.Qnty, orders.Tamnt, 
            orders.Status, orders.Pstatus, 
            customer.Name, customer.Address, customer.Phone, customer.Gender, customer.Email, 
            product.Item
        FROM 
            orders
        INNER JOIN customer ON orders.Uid = customer.Cid
        INNER JOIN product ON orders.Pid = product.Pid
    """

    cursor.execute(s)
    rs = cursor.fetchall()

    # Prepare the data to be passed to the template
    tt = []
    for row in rs:
        order_details = {
            'Oid': row[0],
            'Odate': row[1],
            'Pid': row[2],
            'Uid': row[3],
            'Qnty': row[4],
            'Tamnt': row[5],
            'Status': row[6],
            'Pstatus': row[7],
            'Name': row[8],  # Customer Name
            'Address': row[9],  # Customer Address
            'Phone': row[10],  # Customer Phone
            'Gender': row[11],  # Customer Gender
            'Email': row[12],  # Customer Email
            'Product_Name': row[13]  # Product Name
        }
        tt.append(order_details)

    # Render the template with the orders data
    return render(request, 'orders.html', {'tt': tt})


def status(request):
    cursor = connection.cursor()
    oid=request.GET['oid']
    sts=request.GET['s']
    sql="update orders set Status='%s' WHERE Oid='%s'"%(sts,oid)
    cursor.execute(sql)
    
    # Create light blue notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Status Updated</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #64B5F6, #2196F3);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-exchange-alt"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Status Updated</div>
                <div class="notification-subtext">Order status has been changed to """ + sts + """</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/orders/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)




def payment(request):
    return render(request, 'payment.html')


def assignlocation(request):
    cursor = connection.cursor()
    
    # Fetch all staff details
    sql = "SELECT * FROM staff"
    cursor.execute(sql)
    rs = cursor.fetchall()
    tt = []
    for row in rs:
        q = {'Sid': row[0], 'Name': row[1], 'Gender': row[2], 'Dob': row[3], 'Address': row[4], 'Place': row[5], 'Phone': row[6], 'Adhaar': row[7], 'Email': row[8]}
        tt.append(q)
    
    # Fetch locations not assigned in the assignloc table
    s = """
    SELECT * 
    FROM location
    WHERE Locid NOT IN (SELECT Locationid FROM assignloc)
    """
    cursor.execute(s)
    sr = cursor.fetchall()
    ttt = []
    for row in sr:
        r = {'Locid': row[0], 'Location': row[1], 'Area': row[2], 'Rate': row[3], 'Corate': row[4]}
        ttt.append(r)

    return render(request, 'assignlocation.html', {'tt': tt, 'ttt': ttt})



def assignlocationaction(request):
    cursor=connection.cursor()
    staff=request.GET['staff']
    loc=request.GET['location']
    sql="INSERT INTO assignloc(Staffid,Locationid)VALUES('%s','%s')"%(staff, loc)
    cursor.execute(sql)
    
    # Create light blue notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Location Assigned</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #64B5F6, #2196F3);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #64B5F6, #2196F3);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-map-marker-alt"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Location Assigned</div>
                <div class="notification-subtext">Staff has been successfully assigned to location</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/assignlocation/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)


def viewassignedloc(request):
    cursor=connection.cursor()
    uid=request.session['Uid']
    s="SELECT assignloc.Aid, staff.Name, location.Location,location.Area FROM assignloc INNER JOIN staff ON assignloc.Staffid = staff.Sid INNER JOIN location ON assignloc.Locationid = location.Locid where assignloc.staffid='%s'"%uid
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Aid':row[0], 'Name':row[1],'Location': row[2],'Area':row[3]}
        tt.append(q)
    return render(request, 'viewassignedloc.html',{'tt':tt})


def viewassignlocation(request):
    cursor=connection.cursor()
    s="SELECT assignloc.Alocid, staff.Name, location.Location FROM assignloc INNER JOIN staff ON assignloc.Staffid = staff.Sid INNER JOIN location ON assignloc.Locationid = location.Locid"
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Alocid':row[0], 'Name':row[1],'Location': row[2]}
        tt.append(q)
    return render(request, 'viewassignlocation.html', {'tt':tt})




# from django.shortcuts import redirect
# from django.http import HttpResponse
# from django.db import connection, transaction
# import datetime

def paymentaction(request):
    uid = request.session.get('Uid')
    if not uid:
        return redirect('/login/')

    cursor = connection.cursor()

    # Fetch cart items
    cursor.execute("SELECT * FROM cart WHERE Uid = %s", [uid])
    cart_items = cursor.fetchall()

    if not cart_items:
        return redirect('/viewcart/')

    total_amount = 0  # Initialize total amount

    # Start transaction
    with transaction.atomic():
        for row in cart_items:
            pid = row[1]
            qty = int(row[3])

            # Fetch product details
            cursor.execute("SELECT Amnt, Stock, Category FROM product WHERE Pid = %s", [pid])
            product = cursor.fetchone()

            if not product:
                return redirect('/viewcart/')

            amnt, stock, category = product
            stock = int(stock)
            amnt = int(amnt)

            # Check if stock is available
            if qty > stock:
                return redirect('/viewcart/')

            total_amount += amnt * qty
            stock -= qty

            # Insert into orders
            cursor.execute("""
                INSERT INTO orders (Odate, Pid, Uid, Qnty, Tamnt, Status, Pstatus)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, [today, pid, uid, qty, amnt * qty, 'ordered', 'paid'])  # Here 'paid' can be dynamic

            # Update product stock
            cursor.execute("UPDATE product SET Stock = %s WHERE Pid = %s", [stock, pid])

        # Clear the cart after order completion
        cursor.execute("DELETE FROM cart WHERE Uid = %s", [uid])

    # Create unique payment success animation (exactly as provided)
    success_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Payment Successful</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
            
            * {{ 
                margin: 0; 
                padding: 0; 
                box-sizing: border-box; 
            }}
            
            :root {{
                --primary: #00D09C;        /* Mint Green */
                --primary-dark: #00AA7E;
                --primary-light: #7AEFD1;
                --accent: #835AF1;         /* Purple */
                --accent-dark: #6A46C2;
                --text: #263238;
                --text-light: #546E7A;
                --bg: #F5F9FC;
                --white: #FFFFFF;
            }}
            
            body {{ 
                font-family: 'Poppins', sans-serif;
                background-color: var(--bg);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: var(--text);
                overflow: hidden;
            }}
            
            .payment-container {{
                position: relative;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                width: 100vw;
                height: 100vh;
                background-color: var(--bg);
            }}
            
            /* Loader Styles */
            .loader {{
                position: absolute;
                width: 120px;
                height: 120px;
                opacity: 0;
                visibility: hidden;
                transition: all 0.2s;
            }}
            
            .loader.active {{
                opacity: 1;
                visibility: visible;
            }}
            
            .loader-circle {{
                border: 4px solid rgba(0, 208, 156, 0.2);
                border-left-color: var(--primary);
                border-radius: 50%;
                width: 100%;
                height: 100%;
                animation: loader-spin 1s linear infinite;
            }}
            
            .loader-text {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 0.85rem;
                font-weight: 500;
                color: var(--text-light);
                letter-spacing: 0.5px;
            }}
            
            /* Success Animation Styles */
            .success-animation {{
                position: absolute;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 2.5rem;
                background: var(--white);
                border-radius: 24px;
                box-shadow: 0 20px 60px rgba(131, 90, 241, 0.1);
                transform: translateY(40px);
                opacity: 0;
                visibility: hidden;
                transition: all 0.5s cubic-bezier(0.22, 1, 0.36, 1);
                max-width: 90%;
                width: 460px;
            }}
            
            .success-animation.active {{
                transform: translateY(0);
                opacity: 1;
                visibility: visible;
            }}
            
            .success-checkmark {{
                width: 110px;
                height: 110px;
                position: relative;
                margin-bottom: 1.5rem;
            }}
            
            .check-circle {{
                stroke-dasharray: 166;
                stroke-dashoffset: 166;
                stroke-width: 6;
                stroke-miterlimit: 10;
                stroke: var(--primary);
                fill: none;
                animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
            }}
            
            .check-circle-bg {{
                stroke-dasharray: 166;
                stroke-dashoffset: 166;
                stroke-width: 6;
                stroke-miterlimit: 10;
                stroke: var(--primary-light);
                fill: none;
                opacity: 0.2;
                animation: stroke-bg 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
            }}
            
            .check {{
                transform-origin: 50% 50%;
                stroke-dasharray: 48;
                stroke-dashoffset: 48;
                stroke: var(--white);
                animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.6s forwards;
            }}
            
            .success-spark {{
                position: absolute;
                width: 15px;
                height: 15px;
                background: var(--accent);
                border-radius: 50%;
                opacity: 0;
            }}
            
            .spark-1 {{
                top: 10px;
                right: 10px;
                animation: sparkle 0.4s ease 1s forwards;
            }}
            
            .spark-2 {{
                bottom: 10px;
                left: 10px;
                animation: sparkle 0.4s ease 1.1s forwards;
            }}
            
            .spark-3 {{
                top: 50%;
                left: 0;
                animation: sparkle 0.4s ease 1.2s forwards;
            }}
            
            .spark-4 {{
                top: 30%;
                right: 0;
                animation: sparkle 0.4s ease 1.3s forwards;
            }}
            
            .success-message {{
                text-align: center;
                margin-bottom: 1.5rem;
            }}
            
            .success-title {{
                font-size: 1.8rem;
                font-weight: 700;
                color: var(--text);
                margin-bottom: 0.5rem;
                opacity: 0;
                transform: translateY(10px);
                animation: fadeUp 0.5s ease 0.8s forwards;
            }}
            
            .success-description {{
                font-size: 1rem;
                color: var(--text-light);
                opacity: 0;
                transform: translateY(10px);
                animation: fadeUp 0.5s ease 1s forwards;
            }}
            
            .amount-card {{
                background: linear-gradient(135deg, var(--primary-light), var(--primary));
                border-radius: 16px;
                padding: 1.5rem;
                width: 100%;
                margin-bottom: 1.2rem;
                position: relative;
                overflow: hidden;
                opacity: 0;
                transform: translateY(10px);
                animation: fadeUp 0.5s ease 1.2s forwards;
            }}
            
            .amount-label {{
                font-size: 0.9rem;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 0.3rem;
            }}
            
            .amount-value {{
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--white);
                display: flex;
                align-items: center;
            }}
            
            .amount-value i {{
                margin-right: 8px;
                font-size: 1.2rem;
            }}
            
            .currency {{
                font-size: 1rem;
                margin-right: 4px;
            }}
            
            .amount-card::after {{
                content: '';
                position: absolute;
                width: 200px;
                height: 200px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                bottom: -100px;
                right: -100px;
            }}
            
            .redirect-button {{
                background: linear-gradient(135deg, var(--accent), var(--accent-dark));
                color: var(--white);
                border: none;
                border-radius: 50px;
                padding: 1rem 2rem;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                width: 100%;
                transition: all 0.3s;
                margin-top: 0.5rem;
                position: relative;
                overflow: hidden;
                opacity: 0;
                transform: translateY(10px);
                animation: fadeUp 0.5s ease 1.4s forwards;
            }}
            
            .redirect-button::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(to right, transparent, rgba(255,255,255,0.2), transparent);
                transform: translateX(-100%);
            }}
            
            .redirect-button:hover::before {{
                animation: shimmer 1.5s infinite;
            }}
            
            .redirect-button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(131, 90, 241, 0.2);
            }}
            
            /* Animations */
            @keyframes loader-spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            
            @keyframes stroke {{
                100% {{ stroke-dashoffset: 0; }}
            }}
            
            @keyframes stroke-bg {{
                100% {{ 
                    stroke-dashoffset: 0; 
                    opacity: 0.2;
                }}
            }}
            
            @keyframes fadeUp {{
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            @keyframes sparkle {{
                0% {{ 
                    transform: scale(0); 
                    opacity: 0; 
                }}
                50% {{ 
                    transform: scale(1.5); 
                    opacity: 1; 
                }}
                100% {{ 
                    transform: scale(1); 
                    opacity: 0.8; 
                }}
            }}
            
            @keyframes shimmer {{
                to {{ transform: translateX(100%); }}
            }}
            
            /* Background decoration elements */
            .decoration-circle {{
                position: fixed;
                border-radius: 50%;
                background: linear-gradient(135deg, var(--primary-light), var(--primary));
                opacity: 0.05;
                z-index: -1;
            }}
            
            .circle-1 {{
                width: 300px;
                height: 300px;
                top: -100px;
                left: -100px;
            }}
            
            .circle-2 {{
                width: 500px;
                height: 500px;
                bottom: -200px;
                right: -200px;
            }}
            
        </style>
    </head>
    <body>
        <div class="payment-container">
            <!-- Background decoration -->
            <div class="decoration-circle circle-1"></div>
            <div class="decoration-circle circle-2"></div>
            
            <!-- Payment Processing Loader -->
            <div class="loader active" id="payment-loader">
                <div class="loader-circle"></div>
                <div class="loader-text">Processing Payment...</div>
            </div>
            
            <!-- Success Animation -->
            <div class="success-animation" id="success-animation">
                <div class="success-checkmark">
                    <svg width="110" height="110" viewBox="0 0 52 52">
                        <circle class="check-circle-bg" cx="26" cy="26" r="25"></circle>
                        <circle class="check-circle" cx="26" cy="26" r="25"></circle>
                        <path class="check" d="M14.1 27.2l7.1 7.2 16.7-16.8" fill="none"></path>
                    </svg>
                    <div class="success-spark spark-1"></div>
                    <div class="success-spark spark-2"></div>
                    <div class="success-spark spark-3"></div>
                    <div class="success-spark spark-4"></div>
                </div>
                
                <div class="success-message">
                    <div class="success-title">Payment Successful</div>
                    <div class="success-description">Your order has been placed successfully</div>
                </div>
                
                <div class="amount-card">
                    <div class="amount-label">Total Amount Paid</div>
                    <div class="amount-value">
                        <i class="fas fa-credit-card"></i>
                        <span class="currency">₹</span>{total_amount}
                    </div>
                </div>
                
                <button class="redirect-button" id="view-orders-btn">
                    <i class="fas fa-shopping-bag" style="margin-right: 8px;"></i>
                    View My Orders
                </button>
            </div>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                const loader = document.getElementById('payment-loader');
                const successAnimation = document.getElementById('success-animation');
                const viewOrdersBtn = document.getElementById('view-orders-btn');
                
                // Simulate payment processing (loading)
                setTimeout(function() {{
                    // Hide loader
                    loader.classList.remove('active');
                    
                    // Show success animation
                    setTimeout(function() {{
                        successAnimation.classList.add('active');
                    }}, 400);
                    
                }}, 2000);
                
                // Redirect to orders page when button is clicked
                viewOrdersBtn.addEventListener('click', function() {{
                    window.location.href = '/myorders/';
                }});
                
                // Auto redirect after some time
                setTimeout(function() {{
                    window.location.href = '/myorders/';
                }}, 8000);
            }});
        </script>
    </body>
    </html>
    """
    
    return HttpResponse(success_html)



    

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_error(request):
    return render(request, 'payment_error.html')


def orderaction(request):
    uid = request.session.get('Uid')
    if not uid:
        return redirect('/login/')

    cursor = connection.cursor()

    # Fetch cart items
    cursor.execute("SELECT * FROM cart WHERE Uid = %s", [uid])
    cart_items = cursor.fetchall()

    if not cart_items:
        return redirect('/viewcart/')

    total_amount = 0  # Initialize total amount

    # Start transaction
    with transaction.atomic():
        for row in cart_items:
            pid = row[1]
            qty = int(row[3])

            # Fetch product details
            cursor.execute("SELECT Amnt, Stock, Category FROM product WHERE Pid = %s", [pid])
            product = cursor.fetchone()

            if not product:
                return redirect('/viewcart/')

            amnt, stock, category = product
            stock = int(stock)
            amnt = int(amnt)

            # Check if stock is available
            if qty > stock:
                return redirect('/viewcart/')

            total_amount += amnt * qty
            stock -= qty

            # Insert into orders
            cursor.execute("""
                INSERT INTO orders (Odate, Pid, Uid, Qnty, Tamnt, Status, Pstatus)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, [today, pid, uid, qty, amnt * qty, 'ordered', 'COD'])  # Here 'paid' can be dynamic

            # Update product stock
            cursor.execute("UPDATE product SET Stock = %s WHERE Pid = %s", [stock, pid])

        # Clear the cart after order completion
        cursor.execute("DELETE FROM cart WHERE Uid = %s", [uid])

    # Fetch one product image for display
    cursor.execute("""
        SELECT p.Item, p.Img 
        FROM product p 
        JOIN orders o ON p.Pid = o.Pid 
        WHERE o.Uid = %s 
        ORDER BY o.Oid DESC LIMIT 1
    """, [uid])
    
    product_info = cursor.fetchone()
    product_name = product_info[0] if product_info else "Your products"
    
    # Count number of items ordered
    cursor.execute("""
        SELECT COUNT(*) 
        FROM orders 
        WHERE Uid = %s AND Status = 'ordered' AND Odate = %s
    """, [uid, today])
    
    item_count = cursor.fetchone()[0]
    
    # Create unique order success animation with loader
    success_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Order Placed Successfully</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
            
            * {{ 
                margin: 0; 
                padding: 0; 
                box-sizing: border-box; 
            }}
            
            :root {{
                --primary: #FF8C42;       /* Orange */
                --secondary: #6A5AE0;     /* Purple */
                --light: #FFF8F0;
                --dark: #2D3142;
                --success: #66DE93;
                --text: #4F4F4F;
                --box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }}
            
            body {{ 
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }}
            
            .order-container {{
                position: relative;
                width: 90%;
                max-width: 500px;
                padding: 0;
                overflow: hidden;
                border-radius: 24px;
                box-shadow: var(--box-shadow);
                background: white;
                transform: translateY(50px);
                opacity: 0;
                animation: slideUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.2s forwards;
            }}
            
            /* Header section */
            .order-header {{
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                padding: 30px;
                color: white;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            
            .order-header h1 {{
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 10px;
                position: relative;
                z-index: 2;
            }}
            
            .order-header p {{
                font-size: 16px;
                opacity: 0.9;
                margin-bottom: 15px;
                position: relative;
                z-index: 2;
            }}
            
            /* Decoration circles for header */
            .circle {{
                position: absolute;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
            }}
            
            .circle-1 {{
                width: 120px;
                height: 120px;
                top: -30px;
                left: -30px;
            }}
            
            .circle-2 {{
                width: 80px;
                height: 80px;
                bottom: -20px;
                right: 50px;
            }}
            
            /* Check mark animation */
            .check-container {{
                width: 80px;
                height: 80px;
                background: white;
                border-radius: 50%;
                margin: 0 auto;
                padding: 10px;
                box-shadow: 0 7px 20px rgba(0,0,0,0.1);
                position: relative;
                z-index: 2;
                animation: scaleIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) 0.8s forwards;
                transform: scale(0);
            }}
            
            .check-background {{
                width: 100%;
                height: 100%;
                background: var(--success);
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            
            .check-mark {{
                color: white;
                font-size: 32px;
                opacity: 0;
                animation: fadeIn 0.3s ease 1.3s forwards;
            }}
            
            /* Order details section */
            .order-body {{
                padding: 40px 30px 30px;
                z-index: 10;
                position: relative;
                background: white;
                margin-top: -40px;
                border-radius: 40px 40px 0 0;
            }}
            
            .thank-you {{
                text-align: center;
                margin-bottom: 30px;
            }}
            
            .thank-you h2 {{
                font-size: 24px;
                color: var(--dark);
                margin-bottom: 10px;
                opacity: 0;
                animation: fadeIn 0.5s ease 1.5s forwards;
            }}
            
            .thank-you p {{
                font-size: 15px;
                color: var(--text);
                opacity: 0;
                animation: fadeIn 0.5s ease 1.7s forwards;
            }}
            
            /* Order summary */
            .order-summary {{
                background: #f8f9fa;
                border-radius: 16px;
                padding: 20px;
                margin-bottom: 25px;
                opacity: 0;
                animation: fadeIn 0.5s ease 1.9s forwards;
            }}
            
            .summary-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 1px dashed #E0E0E0;
            }}
            
            .summary-title {{
                font-size: 16px;
                font-weight: 600;
                color: var(--dark);
            }}
            
            .summary-value {{
                font-size: 16px;
                font-weight: 700;
                color: var(--primary);
            }}
            
            .summary-row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
            }}
            
            .summary-label {{
                font-size: 14px;
                color: var(--text);
            }}
            
            .summary-data {{
                font-size: 14px;
                font-weight: 500;
                color: var(--dark);
            }}
            
            /* Button */
            .view-orders-btn {{
                display: block;
                width: 100%;
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                color: white;
                border: none;
                padding: 15px;
                border-radius: 50px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(106, 90, 224, 0.2);
                transition: all 0.3s;
                opacity: 0;
                animation: fadeIn 0.5s ease 2.1s forwards;
            }}
            
            .view-orders-btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(106, 90, 224, 0.3);
            }}
            
            /* Confetti animation */
            .confetti {{
                position: absolute;
                width: 15px;
                height: 15px;
                z-index: 9999;
            }}
            
            /* Loader styles */
            .loader-container {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                z-index: 10000;
                transition: opacity 0.5s ease;
            }}
            
            .loader-content {{
                text-align: center;
            }}
            
            .loader {{
                width: 80px;
                height: 80px;
                margin-bottom: 20px;
                position: relative;
            }}
            
            .loader-spinner {{
                width: 100%;
                height: 100%;
                border-radius: 50%;
                border: 4px solid rgba(255, 140, 66, 0.1);
                border-top-color: var(--primary);
                border-left-color: var(--secondary);
                animation: loader-spin 1.2s linear infinite;
            }}
            
            .loader-icon {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: var(--secondary);
                font-size: 26px;
                animation: pulse 1.5s ease infinite;
            }}
            
            .loader-text {{
                font-size: 18px;
                font-weight: 600;
                color: var(--dark);
                margin-bottom: 10px;
            }}
            
            .loader-progress {{
                width: 200px;
                height: 4px;
                background: rgba(0, 0, 0, 0.1);
                border-radius: 2px;
                overflow: hidden;
                margin: 0 auto;
            }}
            
            .loader-bar {{
                height: 100%;
                width: 0%;
                background: linear-gradient(to right, var(--primary), var(--secondary));
                border-radius: 2px;
                transition: width 0.5s ease;
                animation: progress-animation 2.5s ease forwards;
            }}
            
            .loader-steps {{
                display: flex;
                justify-content: space-between;
                width: 220px;
                margin: 15px auto 0;
            }}
            
            .loader-step {{
                font-size: 12px;
                color: var(--text);
                text-align: center;
                position: relative;
                opacity: 0.5;
                transition: opacity 0.3s ease;
            }}
            
            .loader-step.active {{
                opacity: 1;
                font-weight: 500;
                color: var(--secondary);
            }}
            
            @keyframes loader-spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            
            @keyframes pulse {{
                0%, 100% {{ transform: translate(-50%, -50%) scale(1); }}
                50% {{ transform: translate(-50%, -50%) scale(1.1); }}
            }}
            
            @keyframes progress-animation {{
                0% {{ width: 0%; }}
                30% {{ width: 50%; }}
                60% {{ width: 75%; }}
                100% {{ width: 100%; }}
            }}
            
            @keyframes slideUp {{
                0% {{ transform: translateY(50px); opacity: 0; }}
                100% {{ transform: translateY(0); opacity: 1; }}
            }}
            
            @keyframes fadeIn {{
                0% {{ opacity: 0; }}
                100% {{ opacity: 1; }}
            }}
            
            @keyframes scaleIn {{
                0% {{ transform: scale(0); }}
                70% {{ transform: scale(1.1); }}
                100% {{ transform: scale(1); }}
            }}
            
            @keyframes confettiFall {{
                0% {{ transform: translateY(-100vh) rotate(0deg); }}
                100% {{ transform: translateY(100vh) rotate(720deg); }}
            }}
        </style>
    </head>
    <body>
        <!-- Loader screen -->
        <div class="loader-container" id="loader-screen">
            <div class="loader-content">
                <div class="loader">
                    <div class="loader-spinner"></div>
                    <i class="fas fa-shopping-bag loader-icon"></i>
                </div>
                <div class="loader-text" id="loader-text">Processing Your Order...</div>
                <div class="loader-progress">
                    <div class="loader-bar"></div>
                </div>
                <div class="loader-steps">
                    <div class="loader-step active" id="step-1">Processing</div>
                    <div class="loader-step" id="step-2">Confirming</div>
                    <div class="loader-step" id="step-3">Complete</div>
                </div>
            </div>
        </div>
        
        <!-- Success screen -->
        <div class="order-container" id="success-screen" style="display: none;">
            <div class="order-header">
                <div class="circle circle-1"></div>
                <div class="circle circle-2"></div>
                <h1>Order Successful!</h1>
                <p>Your order has been placed</p>
                <div class="check-container">
                    <div class="check-background">
                        <i class="fas fa-check check-mark"></i>
                    </div>
                </div>
            </div>
            
            <div class="order-body">
                <div class="thank-you">
                    <h2>Thank You for Your Order</h2>
                    <p>We've received your order and will begin processing it right away.</p>
                </div>
                
                <div class="order-summary">
                    <div class="summary-header">
                        <div class="summary-title">Order Summary</div>
                        <div class="summary-value">₹{total_amount}</div>
                    </div>
                    
                    <div class="summary-row">
                        <div class="summary-label">Items</div>
                        <div class="summary-data">{item_count} item(s)</div>
                    </div>
                    
                    <div class="summary-row">
                        <div class="summary-label">Order Status</div>
                        <div class="summary-data">Processing</div>
                    </div>
                    
                    <div class="summary-row">
                        <div class="summary-label">Payment Method</div>
                        <div class="summary-data">Cash On Delivery</div>
                    </div>
                    
                    <div class="summary-row">
                        <div class="summary-label">Order Date</div>
                        <div class="summary-data">{today}</div>
                    </div>
                </div>
                
                <button class="view-orders-btn" id="view-orders">
                    <i class="fas fa-shopping-bag" style="margin-right: 8px;"></i>
                    View My Orders
                </button>
            </div>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                const loaderScreen = document.getElementById('loader-screen');
                const successScreen = document.getElementById('success-screen');
                const loaderText = document.getElementById('loader-text');
                const step1 = document.getElementById('step-1');
                const step2 = document.getElementById('step-2');
                const step3 = document.getElementById('step-3');
                
                // Loader animation sequence
                setTimeout(() => {{
                    loaderText.textContent = "Confirming Order Details...";
                    step1.classList.remove('active');
                    step2.classList.add('active');
                }}, 1000);
                
                setTimeout(() => {{
                    loaderText.textContent = "Order Confirmed!";
                    step2.classList.remove('active');
                    step3.classList.add('active');
                }}, 2000);
                
                // Show success screen after loader
                setTimeout(() => {{
                    loaderScreen.style.opacity = "0";
                    successScreen.style.display = "block";
                    
                    setTimeout(() => {{
                        loaderScreen.style.display = "none";
                        
                        // Create confetti
                        const colors = ['#FF8C42', '#6A5AE0', '#66DE93', '#FFF8F0', '#2D3142'];
                        const shapes = ['circle', 'square', 'triangle'];
                        
                        for (let i = 0; i < 80; i++) {{
                            const confetti = document.createElement('div');
                            confetti.className = 'confetti';
                            
                            // Random size between 8px and 15px
                            const size = Math.random() * 7 + 8;
                            confetti.style.width = `${{size}}px`;
                            confetti.style.height = `${{size}}px`;
                            
                            // Random shape
                            const shape = shapes[Math.floor(Math.random() * shapes.length)];
                            if (shape === 'circle') {{
                                confetti.style.borderRadius = '50%';
                            }} else if (shape === 'triangle') {{
                                confetti.style.width = '0';
                                confetti.style.height = '0';
                                confetti.style.borderLeft = `${{size/2}}px solid transparent`;
                                confetti.style.borderRight = `${{size/2}}px solid transparent`;
                                confetti.style.borderBottom = `${{size}}px solid ${{colors[Math.floor(Math.random() * colors.length)]}}`;
                                confetti.style.background = 'transparent';
                            }}
                            
                            // Random color
                            if (shape !== 'triangle') {{
                                confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                            }}
                            
                            // Random position
                            confetti.style.left = `${{Math.random() * 100}}%`;
                            
                            // Animation
                            const duration = Math.random() * 3 + 2;
                            const delay = Math.random() * 0.5;
                            confetti.style.animation = `confettiFall ${{duration}}s ease-in forwards ${{delay}}s`;
                            
                            document.body.appendChild(confetti);
                        }}
                    }}, 500);
                }}, 3000);
                
                // Button click event
                document.getElementById('view-orders').addEventListener('click', function() {{
                    window.location.href = '/myorders/';
                }});
                
                // Auto redirect after 8 seconds (extended to accommodate loader)
                setTimeout(function() {{
                    window.location.href = '/myorders/';
                }}, 8000);
            }});
        </script>
    </body>
    </html>
    """
    
    return HttpResponse(success_html)


 



        
def myorders(request):
    cursor=connection.cursor()
    uid=request.session['Uid']
    s="SELECT orders.Oid, orders.Odate, product.Item, orders.Qnty, orders.Tamnt, orders.Status,orders.Pstatus,product.Img FROM orders INNER JOIN product ON orders.Pid = product.Pid where orders.Uid='%s'"%uid
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Oid':row[0], 'Odate':row[1],'Item': row[2],'Qnty': row[3],'Tamnt': row[4],'Status': row[5],'Pstatus': row[6],'Img': row[7]}
        tt.append(q)
    return render(request, 'myorders.html', {'tt':tt})


def wastecollectingusers(request):
    cursor=connection.cursor()
    uid=request.session['Uid']
    s="SELECT * FROM application where location in(select Locationid from assignloc where Staffid='%s')"%(uid)
   
    cursor.execute(s)
    rs=cursor.fetchall()
    tt=[]
    for row in rs:
        q={'Name':row[1],'Address':row[2],'Area':row[3],'Houseno':row[4],'Phone':row[5]}
        tt.append(q)
    return render(request, 'wastecollectingusers.html', {'tt':tt})


def trashview(request):
    cursor = connection.cursor()
    uid = request.session['Uid']
    
    # Fetching staff details who are assigned locations (the locations they manage as per the `assignloc` table)
    s = """
    SELECT * FROM staff 
    WHERE Sid IN (SELECT Staffid FROM assignloc WHERE Locationid IN (SELECT Location FROM application WHERE status='approved' and  Uid = %s))
    """
    cursor.execute(s, [uid])  # Using parameterized query to prevent SQL injection
    rs = cursor.fetchall()
    
    staff_list = []
    for row in rs:
        staff_details = {
            'Sid': row[0],
            'Name': row[1],
            'Gender': row[2],
            'Dob': row[3],
            'Address': row[4],
            'Place': row[5],
            'Phone': row[6],
            'Adhaar': row[7],
            'Email': row[8],
            'Img': row[9]  # Assuming column 9 is the image path
        }
        staff_list.append(staff_details)
    
    return render(request, 'trashview.html', {'staff_list': staff_list})







def rejectorder(request):
    cursor=connection.cursor()
    upid=request.GET['id']
    s="update orders set Status='Cancelled' where Oid='%s'"%(upid)
    cursor.execute(s)
    
    # Create light red notification animation
    html_response = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Order Cancelled</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f5f5f5; }
            .notification-wrapper {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                display: flex; justify-content: center; align-items: center;
                background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(8px);
                z-index: 1000;
            }
            .notification-container {
                position: relative; background: rgba(255, 255, 255, 0.95);
                border-radius: 24px; padding: 2rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                animation: floatIn 0.5s cubic-bezier(0.21, 1.02, 0.73, 1) forwards;
                max-width: 90%; width: 400px;
            }
            .icon-circle {
                width: 80px; height: 80px; background: linear-gradient(45deg, #FF8A80, #FF5252);
                border-radius: 50%; display: flex; align-items: center;
                justify-content: center; margin: 0 auto 1.5rem;
                position: relative; overflow: hidden;
                animation: popIn 0.5s ease-out forwards;
                transform: scale(0);
            }
            .icon-circle i {
                color: white; font-size: 32px;
                transform: scale(0) rotate(-180deg);
                animation: tickBounce 0.5s cubic-bezier(0.17, 0.67, 0.41, 1.78) 0.3s forwards;
            }
            .ripple {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50%; background: rgba(255, 255, 255, 0.4);
                animation: rippleEffect 1.5s linear infinite;
            }
            .notification-text, .notification-subtext {
                text-align: center; opacity: 0;
                animation: textFadeIn 0.5s ease 0.6s forwards;
            }
            .notification-text { color: #333; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
            .notification-subtext { color: #666; font-size: 1rem; }
            .progress-bar {
                position: absolute; bottom: 0; left: 0; height: 4px;
                background: linear-gradient(to right, #FF8A80, #FF5252);
                width: 100%; animation: progress 2s linear forwards;
            }

            /* Animations */
            @keyframes floatIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes popIn {
                0% { transform: scale(0); }
                80% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            @keyframes tickBounce {
                0% { transform: scale(0) rotate(-180deg); }
                80% { transform: scale(1.2) rotate(10deg); }
                100% { transform: scale(1) rotate(0deg); }
            }
            @keyframes rippleEffect {
                0% { width: 0; height: 0; opacity: 0.5; }
                100% { width: 150px; height: 150px; opacity: 0; transform: translate(-50%, -50%); }
            }
            @keyframes textFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes progress { from { width: 100%; } to { width: 0%; } }
            @keyframes fadeOut { to { opacity: 0; } }
        </style>
    </head>
    <body>
        <div class="notification-wrapper">
            <div class="notification-container">
                <div class="icon-circle">
                    <i class="fas fa-ban"></i>
                    <div class="ripple"></div>
                </div>
                <div class="notification-text">Order Cancelled</div>
                <div class="notification-subtext">Your order has been cancelled successfully</div>
                <div class="progress-bar"></div>
            </div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(() => {
                    document.querySelector('.notification-wrapper').style.animation = 'fadeOut 0.5s ease forwards';
                    setTimeout(() => { window.location = '/myorders/'; }, 500);
                }, 2000);
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_response)

def wastestats(request):
    return render(request, 'wastestats.html')       

def staffeedback(request):
    return render(request, 'staffeedback.html')

def reports(request):
    return render(request, 'reports.html')

def customercare(request):
    return render(request, 'customercare.html')

def agent(request):
    return render(request, 'agent.html')


def staffhome(request):
    return render(request, 'staffhome.html')

def collectionteams(request):
    return render(request, 'collectionteams.html')

def recyclinginsights(request):
    return render(request, 'recyclinginsights.html')

def ekmmap(request):
    return render(request, 'ekmmap.html')

def reductionplan(request):
    return render(request, 'reductionplan.html')

def energy(request):
    return render(request, 'energy.html')

def wheather(request):
    return render(request, 'wheather.html')

def biogasmonitoring(request):
    return render(request, 'biogasmonitoring.html')

def fleet(request):
    return render(request, 'fleet.html')

def adminbiomon(request):
    return render(request, 'adminbiomon.html')

def viewcollectionmap(request):
    return render(request, 'viewcollectionmap.html')



  # Render an HTML form for adding staff

def staffprofile(request):
    cursor = connection.cursor()
    sid = request.session['Uid']  # Sid for the staff member to update
    sql = "SELECT * FROM staff WHERE sid='%s'" % (sid)  # Updated SQL query
    cursor.execute(sql)
    rs = cursor.fetchall()

    alist = []
    for r in rs:
        # Prepare a dictionary based on the provided table structure
        x = {
            'sid': r[0],  # Staff ID
            'name': r[1],  # Staff Name
            'gender': r[2],  # Gender
            'dob': r[3],  # Date of Birth
            'address': r[4],  # Address
            'place': r[5],  # Place
            'phone': r[6],  # Phone
            'adhaar': r[7],  # Aadhar number
            'email': r[8],  # Email
            'img': r[9]  # Image (could be a URL or file path)
        }
        alist.append(x)

    # Rendering the staff data to be displayed in the update page
    return render(request, 'staffprofile.html', {'a': alist})
   




# from django.shortcuts import render, HttpResponse, redirect
# from .models import Staff
# from .forms import StaffForm

def updateStaffAct(request):
    cursor = connection.cursor()
    if request.method == "POST":
        # Create a StaffForm instance with POST data and files
        staffform = StaffForm(request.POST, request.FILES)
        
        if staffform.is_valid():
            # Retrieve form data
            name = staffform.cleaned_data["name"]
            gender = staffform.cleaned_data["gender"]
            dob = staffform.cleaned_data["dob"]
            address = staffform.cleaned_data["address"]
            place = staffform.cleaned_data["place"]
            phone = staffform.cleaned_data["phone"]
            adhaar = staffform.cleaned_data["adhaar"]
            email = staffform.cleaned_data["email"]
            img = staffform.cleaned_data["img"]  # New image if provided
            imgw = request.POST.get("imgw")  # Old image path (if not updating the image)

            # Fetch staff ID from hidden field
            sid = request.POST.get("sid")

            # Fetch the existing staff member using the sid
            try:
                staff = Staff.objects.get(pk=sid)
            except Staff.DoesNotExist:
                return HttpResponse("Staff member not found")

            # Update staff fields
            staff.name = name
            staff.gender = gender
            staff.dob = dob
            staff.address = address
            staff.place = place
            staff.phone = phone
            staff.adhaar = adhaar
            staff.email = email
            
            # If a new image is uploaded, update the img field
            if img:
                staff.img = img  # Update the staff image if a new one is provided
            else:
                # If no new image is provided, keep the old image
                staff.img = imgw

            # Save the updated staff record
            staff.save()
            sql1="update login set uname='%s' where uid='%s' and utype='staff'"%(email,sid)
            cursor.execute(sql1)
            
            # Format date for display
            formatted_dob = dob.strftime('%d %b, %Y') if hasattr(dob, 'strftime') else dob
            
            # Create perfect animated success notification
            success_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Profile Updated Successfully</title>
                <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
                    
                    * {{ 
                        margin: 0; 
                        padding: 0; 
                        box-sizing: border-box; 
                    }}
                    
                    :root {{
                        --primary: #5E73E1;           /* Indigo Blue */
                        --primary-dark: #4A5DCB;
                        --primary-light: #CED6F3;
                        --primary-bg: #F0F3FF;
                        --success: #34D399;           /* Green */
                        --success-light: #ECFDF5;
                        --accent: #F59E0B;            /* Amber */
                        --text-dark: #111827;
                        --text-medium: #374151;
                        --text-light: #6B7280;
                        --text-lighter: #9CA3AF;
                        --bg-main: #F9FAFB;
                        --bg-card: #FFFFFF;
                        --border-light: #E5E7EB;
                        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                        --shadow-hover: 0 20px 30px -12px rgba(0, 0, 0, 0.15);
                        --shadow-colored: 0 10px 25px -10px rgba(94, 115, 225, 0.4);
                    }}
                    
                    body {{ 
                        font-family: 'Inter', system-ui, sans-serif;
                        background-color: var(--bg-main);
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        color: var(--text-dark);
                        line-height: 1.5;
                    }}
                    
                    /* Initial loading animation */
                    .loading-overlay {{
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background-color: var(--bg-main);
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        z-index: 9999;
                        transition: opacity 0.5s ease-out, visibility 0.5s;
                    }}
                    
                    .processing-loader {{
                        width: 160px;
                        height: 12px;
                        background: #E5E7EB;
                        border-radius: 12px;
                        margin-bottom: 20px;
                        overflow: hidden;
                        position: relative;
                    }}
                    
                    .processing-bar {{
                        position: absolute;
                        top: 0;
                        left: 0;
                        height: 100%;
                        width: 0;
                        border-radius: 12px;
                        background: linear-gradient(to right, var(--primary-light), var(--primary), var(--primary-dark));
                        animation: fill 2s linear forwards;
                    }}
                    
                    .processing-text {{
                        font-size: 16px;
                        font-weight: 500;
                        color: var(--text-medium);
                        letter-spacing: -0.01em;
                    }}
                    
                    /* Checkmark animation */
                    .checkmark-container {{
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background-color: rgba(0, 0, 0, 0.75);
                        backdrop-filter: blur(5px);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        z-index: 999;
                        opacity: 0;
                        visibility: hidden;
                        transition: opacity 0.3s ease, visibility 0.3s;
                    }}
                    
                    .checkmark-container.active {{
                        opacity: 1;
                        visibility: visible;
                    }}
                    
                    .checkmark-circle {{
                        width: 120px;
                        height: 120px;
                        background-color: white;
                        border-radius: 50%;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        box-shadow: var(--shadow-xl);
                        animation: scale-in 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
                    }}
                    
                    .checkmark {{
                        width: 56px;
                        height: 56px;
                        position: relative;
                    }}
                    
                    .checkmark__circle {{
                        width: 56px;
                        height: 56px;
                        position: absolute;
                        border-radius: 50%;
                        box-sizing: content-box;
                        stroke-dasharray: 210;
                        stroke-dashoffset: 210;
                        stroke-width: 3;
                        stroke: var(--success);
                        fill: none;
                        animation: stroke 0.8s cubic-bezier(0.65, 0, 0.45, 1) forwards;
                        transform: rotate(-90deg);
                        transform-origin: 50% 50%;
                    }}
                    
                    .checkmark__check {{
                        transform-origin: 50% 50%;
                        stroke-dasharray: 48;
                        stroke-dashoffset: 48;
                        stroke-width: 3;
                        stroke: var(--success);
                        fill: none;
                        animation: stroke 0.5s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
                    }}
                    
                    /* Main success card */
                    .success-container {{
                        width: 92%;
                        max-width: 760px;
                        opacity: 0;
                        visibility: hidden;
                        transition: opacity 0.5s ease-out, visibility 0.5s;
                        position: relative;
                    }}
                    
                    .success-container.visible {{
                        opacity: 1;
                        visibility: visible;
                    }}
                    
                    .success-card {{
                        background: var(--bg-card);
                        border-radius: 16px;
                        box-shadow: var(--shadow-xl);
                        overflow: hidden;
                        display: flex;
                        flex-direction: column;
                    }}
                    
                    @media (min-width: 768px) {{
                        .success-card {{
                            flex-direction: row;
                            min-height: 360px;
                        }}
                    }}
                    
                    .card-sidebar {{
                        background: linear-gradient(140deg, var(--primary), var(--primary-dark));
                        padding: 40px 30px;
                        color: white;
                        position: relative;
                        overflow: hidden;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                    }}
                    
                    @media (min-width: 768px) {{
                        .card-sidebar {{
                            width: 38%;
                        }}
                    }}
                    
                    .sidebar-pattern {{
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background-image: linear-gradient(30deg, rgba(255, 255, 255, 0.1) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.1) 75%, transparent 75%, transparent);
                        background-size: 8px 8px;
                        opacity: 0.2;
                    }}
                    
                    .sidebar-content {{
                        position: relative;
                        z-index: 1;
                    }}
                    
                    .update-badge {{
                        display: inline-block;
                        background-color: rgba(255, 255, 255, 0.15);
                        color: white;
                        font-size: 12px;
                        font-weight: 600;
                        padding: 6px 12px;
                        border-radius: 20px;
                        margin-bottom: 20px;
                        backdrop-filter: blur(8px);
                        transform: translateY(20px);
                        opacity: 0;
                        animation: slideUp 0.5s ease 0.3s forwards;
                    }}
                    
                    .update-badge i {{
                        margin-right: 5px;
                    }}
                    
                    .sidebar-title {{
                        font-size: 26px;
                        font-weight: 700;
                        margin-bottom: 12px;
                        transform: translateY(20px);
                        opacity: 0;
                        animation: slideUp 0.5s ease 0.4s forwards;
                    }}
                    
                    .sidebar-subtitle {{
                        font-size: 16px;
                        opacity: 0.9;
                        margin-bottom: 20px;
                        transform: translateY(20px);
                        opacity: 0;
                        animation: slideUp 0.5s ease 0.5s forwards;
                    }}
                    
                    .update-time {{
                        font-size: 14px;
                        opacity: 0.8;
                        display: flex;
                        align-items: center;
                        transform: translateY(20px);
                        opacity: 0;
                        animation: slideUp 0.5s ease 0.6s forwards;
                    }}
                    
                    .update-time i {{
                        margin-right: 8px;
                    }}
                    
                    .sidebar-decoration {{
                        position: absolute;
                        border-radius: 50%;
                        background-color: rgba(255, 255, 255, 0.1);
                    }}
                    
                    .decoration-1 {{
                        width: 150px;
                        height: 150px;
                        bottom: -75px;
                        right: -75px;
                    }}
                    
                    .decoration-2 {{
                        width: 60px;
                        height: 60px;
                        top: 30px;
                        right: 30px;
                    }}
                    
                    .staff-avatar {{
                        position: absolute;
                        bottom: 30px;
                        right: 30px;
                        width: 120px;
                        height: 120px;
                        border-radius: 24px;
                        background-color: var(--primary-light);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        box-shadow: var(--shadow-md);
                        transform: scale(0);
                        animation: popIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.7s forwards;
                    }}
                    
                    .staff-avatar i {{
                        font-size: 60px;
                        color: var(--primary);
                    }}
                    
                    .card-content {{
                        padding: 40px;
                        flex: 1;
                    }}
                    
                    .content-header {{
                        margin-bottom: 24px;
                        transform: translateY(20px);
                        opacity: 0;
                        animation: slideUp 0.5s ease 0.7s forwards;
                    }}
                    
                    .content-title {{
                        font-size: 20px;
                        font-weight: 700;
                        color: var(--text-dark);
                        margin-bottom: 8px;
                    }}
                    
                    .content-subtitle {{
                        font-size: 14px;
                        color: var(--text-light);
                    }}
                    
                    .info-grid {{
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                        gap: 24px;
                        margin-bottom: 30px;
                        transform: translateY(20px);
                        opacity: 0;
                        animation: slideUp 0.5s ease 0.8s forwards;
                    }}
                    
                    .info-item {{
                        background-color: var(--primary-bg);
                        border-radius: 12px;
                        padding: 16px;
                        display: flex;
                        align-items: flex-start;
                    }}
                    
                    .info-icon {{
                        width: 40px;
                        height: 40px;
                        background: white;
                        border-radius: 10px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin-right: 12px;
                        box-shadow: var(--shadow-sm);
                        flex-shrink: 0;
                    }}
                    
                    .info-icon i {{
                        color: var(--primary);
                        font-size: 16px;
                    }}
                    
                    .info-content {{
                        flex: 1;
                    }}
                    
                    .info-label {{
                        font-size: 12px;
                        font-weight: 500;
                        color: var(--text-light);
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-bottom: 4px;
                    }}
                    
                    .info-value {{
                        font-size: 16px;
                        font-weight: 600;
                        color: var(--text-dark);
                        line-height: 1.4;
                    }}
                    
                    .action-buttons {{
                        display: flex;
                        gap: 16px;
                        transform: translateY(20px);
                        opacity: 0;
                        animation: slideUp 0.5s ease 0.9s forwards;
                    }}
                    
                    .btn {{
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        padding: 12px 20px;
                        border-radius: 10px;
                        font-weight: 600;
                        font-size: 15px;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        text-decoration: none;
                    }}
                    
                    .btn i {{
                        margin-right: 8px;
                    }}
                    
                    .btn-primary {{
                        background-color: var(--primary);
                        color: white;
                        box-shadow: var(--shadow-colored);
                        flex: 1;
                    }}
                    
                    .btn-primary:hover {{
                        transform: translateY(-3px);
                        box-shadow: var(--shadow-hover);
                    }}
                    
                    .btn-secondary {{
                        background-color: var(--primary-light);
                        color: var(--primary);
                        box-shadow: var(--shadow-sm);
                    }}
                    
                    .btn-secondary:hover {{
                        background-color: var(--primary-bg);
                    }}
                    
                    .changes-badge {{
                        display: flex;
                        align-items: center;
                        gap: 8px;
                        margin-top: 30px;
                        padding: 10px 15px;
                        border-radius: 8px;
                        background-color: var(--success-light);
                        color: var(--success);
                        font-size: 14px;
                        font-weight: 600;
                        transform: translateY(20px);
                        opacity: 0;
                        animation: slideUp 0.5s ease 1s forwards;
                    }}
                    
                    .badge-icon {{
                        width: 24px;
                        height: 24px;
                        border-radius: 50%;
                        background-color: var(--success);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        flex-shrink: 0;
                    }}
                    
                    .badge-icon i {{
                        color: white;
                        font-size: 12px;
                    }}
                    
                    .particles-container {{
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        pointer-events: none;
                        z-index: 1000;
                    }}
                    
                    .particle {{
                        position: absolute;
                        border-radius: 50%;
                        opacity: 0;
                    }}
                    
                    /* Animations */
                    @keyframes fill {{
                        0% {{ width: 0; }}
                        100% {{ width: 100%; }}
                    }}
                    
                    @keyframes stroke {{
                        100% {{ stroke-dashoffset: 0; }}
                    }}
                    
                    @keyframes scale-in {{
                        0% {{ transform: scale(0.5); opacity: 0; }}
                        100% {{ transform: scale(1); opacity: 1; }}
                    }}
                    
                    @keyframes slideUp {{
                        0% {{ transform: translateY(20px); opacity: 0; }}
                        100% {{ transform: translateY(0); opacity: 1; }}
                    }}
                    
                    @keyframes popIn {{
                        0% {{ transform: scale(0); }}
                        80% {{ transform: scale(1.1); }}
                        100% {{ transform: scale(1); }}
                    }}
                    
                    @keyframes particleAnimation {{
                        0% {{ transform: translate(0, 0) scale(1); opacity: 0; }}
                        20% {{ opacity: 1; }}
                        100% {{ transform: translate(var(--tx), var(--ty)) scale(0); opacity: 0; }}
                    }}
                </style>
            </head>
            <body>
                <!-- Loading overlay -->
                <div class="loading-overlay" id="loading-overlay">
                    <div class="processing-loader">
                        <div class="processing-bar"></div>
                    </div>
                    <div class="processing-text">Updating Profile Information...</div>
                </div>
                
                <!-- Checkmark animation -->
                <div class="checkmark-container" id="checkmark-container">
                    <div class="checkmark-circle">
                        <div class="checkmark">
                            <svg class="checkmark__circle" viewBox="0 0 52 52">
                                <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
                            </svg>
                            <svg class="checkmark__check" viewBox="0 0 52 52">
                                <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                            </svg>
                        </div>
                    </div>
                </div>
                
                <!-- Success card -->
                <div class="success-container" id="success-container">
                    <div class="success-card">
                        <div class="card-sidebar">
                            <div class="sidebar-pattern"></div>
                            <div class="sidebar-decoration decoration-1"></div>
                            <div class="sidebar-decoration decoration-2"></div>
                            
                            <div class="sidebar-content">
                                <div class="update-badge">
                                    <i class="fas fa-check-circle"></i>Staff Profile Updated
                                </div>
                                <h1 class="sidebar-title">Update Successful</h1>
                                <p class="sidebar-subtitle">Your staff profile information has been saved successfully</p>
                                <div class="update-time">
                                    <i class="far fa-clock"></i>Just Now
                                </div>
                            </div>
                            
                            <div class="staff-avatar">
                                <i class="fas fa-user-tie"></i>
                            </div>
                        </div>
                        
                        <div class="card-content">
                            <div class="content-header">
                                <h2 class="content-title">Staff Information</h2>
                                <p class="content-subtitle">Updated profile details for {name}</p>
                            </div>
                            
                            <div class="info-grid">
                                <div class="info-item">
                                    <div class="info-icon">
                                        <i class="fas fa-user"></i>
                                    </div>
                                    <div class="info-content">
                                        <div class="info-label">Name</div>
                                        <div class="info-value">{name}</div>
                                    </div>
                                </div>
                                
                                <div class="info-item">
                                    <div class="info-icon">
                                        <i class="fas fa-envelope"></i>
                                    </div>
                                    <div class="info-content">
                                        <div class="info-label">Email</div>
                                        <div class="info-value">{email}</div>
                                    </div>
                                </div>
                                
                                <div class="info-item">
                                    <div class="info-icon">
                                        <i class="fas fa-phone"></i>
                                    </div>
                                    <div class="info-content">
                                        <div class="info-label">Phone</div>
                                        <div class="info-value">{phone}</div>
                                    </div>
                                </div>
                                
                                <div class="info-item">
                                    <div class="info-icon">
                                        <i class="fas fa-map-marker-alt"></i>
                                    </div>
                                    <div class="info-content">
                                        <div class="info-label">Location</div>
                                        <div class="info-value">{place}</div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="action-buttons">
                                <a href="/staffhome/" class="btn btn-primary" id="home-button">
                                    <i class="fas fa-home"></i>Go to Dashboard
                                </a>
                                <a href="#" class="btn btn-secondary" id="profile-button">
                                    <i class="fas fa-user"></i>Profile
                                </a>
                            </div>
                            
                            <div class="changes-badge">
                                <div class="badge-icon">
                                    <i class="fas fa-check"></i>
                                </div>
                                <span>All changes have been saved successfully</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Celebration particles -->
                <div class="particles-container" id="particles-container"></div>
                
                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        const loadingOverlay = document.getElementById('loading-overlay');
                        const checkmarkContainer = document.getElementById('checkmark-container');
                        const successContainer = document.getElementById('success-container');
                        const particlesContainer = document.getElementById('particles-container');
                        const homeButton = document.getElementById('home-button');
                        const profileButton = document.getElementById('profile-button');
                        
                        // Hide loading overlay and show checkmark after 2 seconds
                        setTimeout(() => {{
                            loadingOverlay.style.opacity = '0';
                            loadingOverlay.style.visibility = 'hidden';
                            
                            checkmarkContainer.classList.add('active');
                            
                            // Hide checkmark and show success card after 1.5 seconds
                            setTimeout(() => {{
                                checkmarkContainer.style.opacity = '0';
                                checkmarkContainer.style.visibility = 'hidden';
                                
                                successContainer.classList.add('visible');
                                
                                // Create celebration particles
                                createParticles();
                            }}, 1500);
                        }}, 2000);
                        
                        // Create celebration particles
                        function createParticles() {{
                            const colors = [
                                'var(--primary)',
                                'var(--primary-light)',
                                'var(--primary-dark)',
                                'var(--success)',
                                '#FCD34D', // Light yellow
                            ];
                            
                            for (let i = 0; i < 30; i++) {{
                                const particle = document.createElement('div');
                                particle.classList.add('particle');
                                
                                // Random properties
                                const size = Math.random() * 8 + 4;
                                const color = colors[Math.floor(Math.random() * colors.length)];
                                
                                // Position near the checkmark
                                const startX = window.innerWidth / 2 + (Math.random() - 0.5) * 20;
                                const startY = window.innerHeight / 2 + (Math.random() - 0.5) * 20;
                                
                                // Apply styles
                                particle.style.width = `${{size}}px`;
                                particle.style.height = `${{size}}px`;
                                particle.style.backgroundColor = color;
                                particle.style.left = `${{startX}}px`;
                                particle.style.top = `${{startY}}px`;
                                
                                // Random animation parameters
                                const tx = (Math.random() - 0.5) * 200;
                                const ty = (Math.random() - 0.5) * 200;
                                const duration = Math.random() * 1.5 + 1;
                                const delay = Math.random() * 0.5;
                                
                                particle.style.setProperty('--tx', `${{tx}}px`);
                                particle.style.setProperty('--ty', `${{ty}}px`);
                                particle.style.animation = `particleAnimation ${{duration}}s ease ${{delay}}s`;
                                
                                particlesContainer.appendChild(particle);
                                
                                // Remove particle after animation
                                setTimeout(() => {{
                                    particle.remove();
                                }}, (duration + delay) * 1000);
                            }}
                        }}
                        
                        // Button handlers
                        homeButton.addEventListener('click', function(e) {{
                            e.preventDefault();
                            window.location.href = '/staffhome/';
                        }});
                        
                        profileButton.addEventListener('click', function(e) {{
                            e.preventDefault();
                            // Redirect to staff profile page or show profile details
                            window.location.href = '/staffhome/';
                        }});
                        
                        // Auto redirect after 8 seconds
                        setTimeout(() => {{
                            window.location.href = '/staffhome/';
                        }}, 8000);
                    }});
                </script>
            </body>
            </html>
            """
            
            return HttpResponse(success_html)
        
        else:
            return HttpResponse("Form is not valid")
    
    else:
        return HttpResponse("Method not allowed")
    


def customerprofile(request):
    cursor = connection.cursor()
    id = request.session['Uid']  # Sid for the staff member to update
    sql = "SELECT * FROM customer WHERE cid='%s'" % (id)  # Updated SQL query
    cursor.execute(sql)
    rs = cursor.fetchall()

    alist = []
    for r in rs:
        # Prepare a dictionary based on the provided table structure
        x = {
            'Cid': r[0],  # Staff ID
            'Name': r[1],  # Staff Name
            'Address': r[2],  # Address
            'Phone': r[3],  # Phone
            'Gender': r[4],  # Gender
            'Email': r[5],  # Email
            'Img': r[6]  # Image (could be a URL or file path)
        }
        alist.append(x)

    # Rendering the staff data to be displayed in the update page
    return render(request, 'customerprofile.html', {'a': alist})
   


# from django.shortcuts import render, HttpResponse, redirect
# from .models import Customer
# from .forms import CustomerForm
# from django.db import connection

def updateCustomerAction(request):
    cursor = connection.cursor()
    
    if request.method == "POST":
        # Create a CustomerForm instance with POST data and files
        customerform = CustomerForm(request.POST, request.FILES)
        
        if customerform.is_valid():
            # Retrieve form data
            name = customerform.cleaned_data["name"]
            address = customerform.cleaned_data["address"]
            phone = customerform.cleaned_data["phone"]
            gender = customerform.cleaned_data["gender"]
            email = customerform.cleaned_data["email"]
            img = customerform.cleaned_data["Img"]  # New image if provided
            imgw = request.POST.get("imgw")  # Old image path (if not updating the image)

            print(f"New Image: {img}")  # Debugging statement to see the uploaded image
            print(f"Old Image: {imgw}")  # Debugging statement to see the old image

            # Fetch customer ID from hidden field
            customer_id = request.POST.get("cid")

            # Fetch the existing customer using the customer_id
            try:
                customer = Customer.objects.get(pk=customer_id)
            except Customer.DoesNotExist:
                return HttpResponse("Customer not found")

            # Update customer fields
            customer.Name = name
            customer.Address = address
            customer.Phone = phone
            customer.Gender = gender
            customer.Email = email
            
            # Check if a new image was uploaded
            if img:
                print("Updating with new image...")
                customer.Img = img  # Update the customer image if a new one is provided
            elif imgw:
                print("No new image, retaining old image...")
                customer.Img = imgw  # If no new image is provided, keep the old image

            # Save the updated customer record
            customer.save()

            # Update login table to reflect the new email
            sql1 = "UPDATE login SET uname='%s' WHERE uid='%s' AND utype='customer'" % (email, customer_id)
            cursor.execute(sql1)

            # Create animation HTML response
            success_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Profile Updated</title>
                <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
                    
                    * {{ 
                        margin: 0; 
                        padding: 0; 
                        box-sizing: border-box; 
                    }}
                    
                    :root {{
                        --primary: #3498DB;        /* Blue */
                        --primary-dark: #2980B9;
                        --primary-light: #AED6F1;
                        --accent: #F39C12;         /* Orange for contrast */
                        --text: #2C3E50;
                        --text-light: #7F8C8D;
                        --bg: #ECF0F1;
                        --white: #FFFFFF;
                    }}
                    
                    body {{ 
                        font-family: 'Poppins', sans-serif;
                        background-color: var(--bg);
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        overflow: hidden;
                    }}
                    
                    .update-container {{
                        position: relative;
                        background-color: var(--white);
                        border-radius: 20px;
                        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                        width: 90%;
                        max-width: 450px;
                        overflow: hidden;
                        transform: translateY(30px);
                        opacity: 0;
                        animation: slideIn 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards;
                    }}
                    
                    .update-header {{
                        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
                        padding: 25px 20px;
                        color: var(--white);
                        text-align: center;
                        position: relative;
                    }}
                    
                    .update-header::after {{
                        content: '';
                        position: absolute;
                        bottom: 0;
                        left: 0;
                        width: 100%;
                        height: 30px;
                        background: var(--white);
                        border-radius: 50% 50% 0 0 / 100% 100% 0 0;
                        transform: translateY(15px);
                    }}
                    
                    .profile-icon {{
                        width: 90px;
                        height: 90px;
                        background: var(--white);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto;
                        position: relative;
                        z-index: 2;
                        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
                        border: 4px solid rgba(255, 255, 255, 0.9);
                        margin-bottom: -45px;
                    }}
                    
                    .profile-icon i {{
                        color: var(--primary);
                        font-size: 40px;
                        animation: pulse 2s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite;
                    }}
                    
                    @keyframes pulse {{
                        0% {{ transform: scale(0.95); }}
                        50% {{ transform: scale(1.05); }}
                        100% {{ transform: scale(0.95); }}
                    }}
                    
                    .update-content {{
                        padding: 50px 30px 30px;
                        text-align: center;
                    }}
                    
                    .update-title {{
                        font-size: 1.8rem;
                        font-weight: 700;
                        color: var(--text);
                        margin-bottom: 10px;
                        opacity: 0;
                        animation: fadeUp 0.5s ease 0.3s forwards;
                    }}
                    
                    .update-subtitle {{
                        font-size: 1rem;
                        color: var(--text-light);
                        margin-bottom: 25px;
                        opacity: 0;
                        animation: fadeUp 0.5s ease 0.5s forwards;
                    }}
                    
                    .update-details {{
                        background-color: var(--bg);
                        padding: 20px;
                        border-radius: 15px;
                        margin-bottom: 25px;
                        opacity: 0;
                        animation: fadeUp 0.5s ease 0.7s forwards;
                    }}
                    
                    .detail-item {{
                        display: flex;
                        align-items: center;
                        margin-bottom: 12px;
                        text-align: left;
                    }}
                    
                    .detail-item:last-child {{
                        margin-bottom: 0;
                    }}
                    
                    .detail-icon {{
                        width: 30px;
                        height: 30px;
                        background-color: var(--primary-light);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin-right: 12px;
                        flex-shrink: 0;
                    }}
                    
                    .detail-icon i {{
                        color: var(--primary-dark);
                        font-size: 14px;
                    }}
                    
                    .detail-text {{
                        flex: 1;
                        font-size: 0.95rem;
                        color: var(--text);
                    }}
                    
                    .detail-label {{
                        font-size: 0.75rem;
                        color: var(--text-light);
                        display: block;
                        margin-bottom: 2px;
                    }}
                    
                    .action-button {{
                        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
                        color: var(--white);
                        border: none;
                        border-radius: 50px;
                        padding: 14px 30px;
                        font-size: 1rem;
                        font-weight: 600;
                        cursor: pointer;
                        transition: all 0.3s;
                        box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
                        opacity: 0;
                        animation: fadeUp 0.5s ease 0.9s forwards;
                    }}
                    
                    .action-button:hover {{
                        transform: translateY(-3px);
                        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.4);
                    }}
                    
                    .action-button i {{
                        margin-right: 8px;
                    }}
                    
                    .floating-element {{
                        position: absolute;
                        background-color: var(--primary-light);
                        border-radius: 50%;
                        opacity: 0.1;
                        z-index: -1;
                    }}
                    
                    .float-1 {{
                        width: 100px;
                        height: 100px;
                        top: -30px;
                        right: -30px;
                    }}
                    
                    .float-2 {{
                        width: 150px;
                        height: 150px;
                        bottom: -50px;
                        left: -50px;
                    }}
                    
                    .checkmark {{
                        position: absolute;
                        top: 20px;
                        right: 20px;
                        width: 35px;
                        height: 35px;
                        background-color: var(--accent);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        opacity: 0;
                        animation: bounceIn 0.6s cubic-bezier(0.47, 2.02, 0.31, 0.99) 1s forwards;
                    }}
                    
                    .checkmark i {{
                        color: var(--white);
                        font-size: 16px;
                    }}
                    
                    /* Animations */
                    @keyframes slideIn {{
                        0% {{ transform: translateY(30px); opacity: 0; }}
                        100% {{ transform: translateY(0); opacity: 1; }}
                    }}
                    
                    @keyframes fadeUp {{
                        0% {{ opacity: 0; transform: translateY(10px); }}
                        100% {{ opacity: 1; transform: translateY(0); }}
                    }}
                    
                    @keyframes bounceIn {{
                        0% {{ transform: scale(0); opacity: 0; }}
                        50% {{ transform: scale(1.2); opacity: 1; }}
                        100% {{ transform: scale(1); opacity: 1; }}
                    }}
                </style>
            </head>
            <body>
                <div class="update-container">
                    <!-- Floating decorative elements -->
                    <div class="floating-element float-1"></div>
                    <div class="floating-element float-2"></div>
                    
                    <div class="update-header">
                        <div class="profile-icon">
                            <i class="fas fa-user-edit"></i>
                        </div>
                        <div class="checkmark">
                            <i class="fas fa-check"></i>
                        </div>
                    </div>
                    
                    <div class="update-content">
                        <h1 class="update-title">Profile Updated!</h1>
                        <p class="update-subtitle">Your profile information has been successfully updated</p>
                        
                        <div class="update-details">
                            <div class="detail-item">
                                <div class="detail-icon">
                                    <i class="fas fa-user"></i>
                                </div>
                                <div class="detail-text">
                                    <span class="detail-label">Name</span>
                                    {name}
                                </div>
                            </div>
                            
                            <div class="detail-item">
                                <div class="detail-icon">
                                    <i class="fas fa-envelope"></i>
                                </div>
                                <div class="detail-text">
                                    <span class="detail-label">Email</span>
                                    {email}
                                </div>
                            </div>
                            
                            <div class="detail-item">
                                <div class="detail-icon">
                                    <i class="fas fa-phone"></i>
                                </div>
                                <div class="detail-text">
                                    <span class="detail-label">Phone</span>
                                    {phone}
                                </div>
                            </div>
                        </div>
                        
                        <button class="action-button" id="view-profile-btn">
                            <i class="fas fa-user"></i>View Profile
                        </button>
                    </div>
                </div>
                
                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        // Redirect when button is clicked
                        document.getElementById('view-profile-btn').addEventListener('click', function() {{
                            window.location.href = '/customerprofile/';
                        }});
                        
                        // Auto-redirect after 5 seconds
                        setTimeout(function() {{
                            window.location.href = '/customerprofile/';
                        }}, 5000);
                    }});
                </script>
            </body>
            </html>
            """
            
            return HttpResponse(success_html)
        
        else:
            return HttpResponse("Form is not valid")
    
    else:
        return HttpResponse("Method not allowed")




    



    



def wasteinfo(request):
    return render(request, 'wasteinfo.html')


def service(request):
    return render(request, 'service.html')


def service1(request):
    return render(request, 'service1.html')

def service2(request):
    return render(request, 'service2.html')

def service3(request):
    return render(request, 'service3.html')

# def service4(request):
#     return render(request, 'service4.html')

def about(request):
    return render(request, 'about.html')




# from datetime import datetime, timedelta
# from django.shortcuts import render
# from django.db import connection

def view_application_status(request):
    cursor = connection.cursor()

    # Get the current month and year
    current_month_year = datetime.now().strftime('%Y-%m')  # Format like "2025-03"

    # Query the application records for the logged-in user
    sql = "SELECT * FROM application WHERE Uid='%s'" % (request.session['Uid'])
    cursor.execute(sql)
    rs = cursor.fetchall()

    tt = []
    for row in rs:
        appno = row[0]
        name = row[1]
        address = row[2]
        area = row[3]
        houseno = row[5]
        phone = row[6]
        status = row[8]
        date = row[9]

        # Check if a payment record exists for this application number
        cursor.execute("SELECT * FROM pbill WHERE apno=%s ORDER BY date DESC LIMIT 1", [appno])
        last_payment = cursor.fetchone()

        # If a payment record exists, check if it was more than 7 days ago
        pay_link = None
        if last_payment:
            last_payment_date_str = last_payment[3]  # Assuming the date is the 4th column in 'pbill'

            # Convert the last_payment_date string to a datetime object
            last_payment_date = datetime.strptime(last_payment_date_str, '%Y-%m-%d')  # Assuming it's in 'YYYY-MM-DD' format

            # Calculate the number of days since the last payment
            days_since_last_payment = (datetime.now() - last_payment_date).days

            # Show the "Pay Bill" link only if the last payment was more than 7 days ago and application is approved
            if status == 'approved' and days_since_last_payment >= 7:
                pay_link = f"/paybill?Appno={appno}"
        else:
            # If no payment record exists and the status is approved, show the "Pay Bill" link
            if status == 'approved':
                pay_link = f"/paybill?Appno={appno}"

        # Add the application data along with the payment link status
        q = {
            'Appno': appno,
            'Name': name,
            'Address': address,
            'Area': area,
            'Houseno': houseno,
            'Phone': phone,
            'Status': status,
            'Date': date,
            'PayLink': pay_link  # Add the 'Pay Bill' link conditionally
        }
        tt.append(q)

    return render(request, 'view_application_status.html', {'tt': tt})



# def paybill1(request):
# 	cursor=connection.cursor()
# 	cursor1=connection.cursor()
# 	cursor.execute("select *  from application where uid='%s' and status='approved' "%(request.session['Uid']) )
# 	result1=cursor.fetchall()
# 	list1=[]
# 	rate='null'
# 	s1=''
# 	for row in result1:
# 		w1 = {'appid' : row[0]}
# 		lid=row[4]
# 		wtype=row[9]
# 		list1.append(w1)
# 	if cursor.rowcount >0:
		
# 		sql3="select type from collectionrate where type='%s' and wtype='%s' and dist='%s' "%(atype,wtype,dist)
# 		cursor1.execute(sql3)
# 		if cursor1.rowcount>0:
# 			result3=cursor1.fetchall()
# 			for row3 in result3:
# 				rate=row3[0]
# 		sql5="select month(date) from application where uid='%s' "%(request.session['uid'])
# 		cursor1.execute(sql5)
# 		if cursor1.rowcount>0:
# 			result5=cursor1.fetchall()
# 			for row5 in result5:
# 				mn=int(row5[0])
# 		yr=today_date.strftime("%Y")
# 		sql4="select month(date),year(date) from payment where pid=(select max(pid) from payment where uid='%s') "%(request.session['uid'])
# 		cursor1.execute(sql4)
# 		result4=cursor1.fetchall()
# 		for row4 in result4:
# 			mn=row4[0]
# 			yr=row4[1]
# 		month={	1:'Janauary',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'		}
# 		s=month[mn]
# 		s1=s+','+str(yr)
# 	return render(request,'paybill.html',{'list1':list1,'rate':rate,'month':s1})



from datetime import datetime

def paybill(request):
    # Create database cursors
    cursor = connection.cursor()
    Appno=request.GET['Appno']
  

    # Get the application for the logged-in user with 'approved' status
    cursor.execute("SELECT * FROM application WHERE uid='%s' AND status='approved'" % (request.session['Uid']))
    result1 = cursor.fetchall()

    # Initialize the list and rate variable
    list1 = []
    rate = 'null'

    # Get current month and year
    current_month_year = datetime.now().strftime("%B %Y")  # e.g., "March 2025"

    # Debugging print to check result1 content
    print("result1:", result1)

    # Loop through the result to find the user's application
    if result1:
        for application in result1:
            location_id = application[4]  # Assuming location is stored in the 5th column (index 4)
            print("Location ID:", location_id)

            # Now, fetch the rate or corate from the location table based on the location
            cursor.execute("SELECT Rate, Corate FROM location WHERE Locid=%s", [location_id])
            location_data = cursor.fetchone()

            # Debugging print to check location_data content
            print("Location Data:", location_data)

            if location_data:
                location_rate, location_corate = location_data

                # Debugging print to check the type field in the application
                print("Application Type:", application[10])  # Assuming 'type' is in the 11th column (index 10)

                # Check the 'type' field in the application to decide whether to use Rate or Corate
                if application[10].strip().lower() == 'rate':  # Normalize case and strip extra spaces
                    rate = location_rate
                elif application[10].strip().lower() == 'corate':  # Normalize case and strip extra spaces
                    rate = location_corate

    print("Final Rate:", rate)
    # Pass the fetched data to the template for rendering, including the current month and year
    return render(request, 'paybill.html', {'list1': list1, 'rate': rate, 'current_month_year': current_month_year,'Appno':Appno,today:today})



# from django.shortcuts import render
# from django.http import HttpResponse
# from django.db import connection
# from datetime import datetime

def paybillAct(request):
    # Get the current time for the payment date
    payment_date = datetime.now().strftime('%Y-%m-%d')  # Get today's date

    if request.method == 'POST':
        amt = request.POST.get('amt')  # Get the amount from the form
        card_number = request.POST.get('card_number')  # Get the card number
        ccv_number = request.POST.get('ccv_number')  # Get the CCV number
        month_year = request.POST.get('month_year')  # Get the month and year from the form

        # Assuming `apno` is provided from the user's session or from another source
        apno = request.POST.get('apno')  # You may need to get this from session or another source
        uid = request.session.get('Uid')  # Get the user ID from the session

        # Insert the payment information into the pbill table
        cursor = connection.cursor()
        sql = """
        INSERT INTO pbill (apno, uid, date, amt) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, [apno, uid, payment_date, amt])

        # Commit the transaction
        connection.commit()

        # Get masked card number for display (show only last 4 digits)
        masked_card = "xxxx-xxxx-xxxx-" + card_number[-4:] if len(card_number) >= 4 else "xxxx"

        # Create premium payment success animation
        success_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Payment Successful</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
                
                * {{ 
                    margin: 0; 
                    padding: 0; 
                    box-sizing: border-box; 
                }}
                
                :root {{
                    --primary: #4CAF50;         /* Green */
                    --primary-dark: #2E7D32;
                    --primary-light: #A5D6A7;
                    --accent: #FFD700;          /* Gold */
                    --accent-dark: #FFC400;
                    --text-dark: #1A1A1A;
                    --text-light: #737373;
                    --bg-main: #F0F2F5;
                    --bg-card: #FFFFFF;
                    --error: #FF3B30;
                    --shadow-sm: 0 2px 8px rgba(0,0,0,0.08);
                    --shadow-md: 0 8px 24px rgba(0,0,0,0.12);
                    --shadow-lg: 0 16px 48px rgba(0,0,0,0.16);
                    --shadow-accent: 0 8px 24px rgba(76, 175, 80, 0.25);
                }}
                
                body {{ 
                    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: var(--text-dark);
                    overflow-x: hidden;
                }}
                
                /* Multi-step animation container */
                .animation-container {{
                    position: relative;
                    width: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }}
                
                /* Step 1: Processing Animation */
                .processing-container {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: var(--bg-main);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    z-index: 100;
                    transition: opacity 0.5s ease, transform 0.5s ease;
                }}
                
                .processing-card {{
                    background: var(--bg-card);
                    border-radius: 24px;
                    box-shadow: var(--shadow-md);
                    width: 90%;
                    max-width: 400px;
                    padding: 40px 30px;
                    text-align: center;
                    position: relative;
                    overflow: hidden;
                }}
                
                .processing-loader {{
                    position: relative;
                    width: 110px;
                    height: 110px;
                    margin: 0 auto 30px;
                }}
                
                .loader-ring {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    border-radius: 50%;
                    border: 5px solid rgba(76, 175, 80, 0.1);
                    border-top-color: var(--primary);
                    animation: loader-spin 1.5s linear infinite;
                    box-sizing: border-box;
                }}
                
                .loader-ring-inner {{
                    position: absolute;
                    top: 15px;
                    left: 15px;
                    right: 15px;
                    bottom: 15px;
                    border-radius: 50%;
                    border: 5px solid transparent;
                    border-bottom-color: var(--accent);
                    animation: loader-spin 2s linear infinite;
                    box-sizing: border-box;
                }}
                
                .loader-icon {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    color: var(--primary);
                    font-size: 32px;
                    animation: pulse 1.5s ease infinite;
                }}
                
                .processing-title {{
                    font-size: 22px;
                    font-weight: 700;
                    color: var(--text-dark);
                    margin-bottom: 10px;
                }}
                
                .processing-subtitle {{
                    font-size: 16px;
                    color: var(--text-light);
                    margin-bottom: 25px;
                }}
                
                .processing-steps {{
                    display: flex;
                    justify-content: space-between;
                    margin: 0 auto;
                    max-width: 320px;
                    position: relative;
                    margin-bottom: 30px;
                }}
                
                .processing-steps::before {{
                    content: '';
                    position: absolute;
                    top: 15px;
                    left: 30px;
                    right: 30px;
                    height: 2px;
                    background-color: #E0E0E0;
                    z-index: 1;
                }}
                
                .step {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    position: relative;
                    z-index: 2;
                }}
                
                .step-circle {{
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    background-color: #E0E0E0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: 600;
                    font-size: 14px;
                    margin-bottom: 8px;
                    transition: all 0.3s ease;
                }}
                
                .step-label {{
                    font-size: 13px;
                    color: var(--text-light);
                    font-weight: 500;
                    transition: all 0.3s ease;
                }}
                
                .step.active .step-circle {{
                    background-color: var(--primary);
                    box-shadow: 0 0 0 4px rgba(76, 175, 80, 0.3);
                }}
                
                .step.active .step-label {{
                    color: var(--primary);
                    font-weight: 600;
                }}
                
                .step.completed .step-circle {{
                    background-color: var(--primary);
                }}
                
                .processing-progress {{
                    height: 6px;
                    background-color: #E0E0E0;
                    border-radius: 3px;
                    overflow: hidden;
                    margin-bottom: 12px;
                }}
                
                .progress-bar {{
                    height: 100%;
                    width: 0;
                    background: linear-gradient(90deg, var(--primary), var(--primary-dark));
                    border-radius: 3px;
                }}
                
                .progress-text {{
                    font-size: 13px;
                    color: var(--text-light);
                    text-align: right;
                }}
                
                /* Decorative Elements */
                .card-decoration {{
                    position: absolute;
                    border-radius: 50%;
                    background: var(--primary-light);
                    opacity: 0.1;
                    z-index: 0;
                }}
                
                .decoration-1 {{
                    width: 150px;
                    height: 150px;
                    top: -75px;
                    right: -75px;
                }}
                
                .decoration-2 {{
                    width: 100px;
                    height: 100px;
                    bottom: -50px;
                    left: -50px;
                }}
                
                /* Step 2: Success Animation */
                .success-container {{
                    position: relative;
                    margin: 50px auto 0;
                    width: 90%;
                    max-width: 500px;
                    opacity: 0;
                    transform: translateY(30px);
                    visibility: hidden;
                    transition: all 0.5s cubic-bezier(0.22, 1, 0.36, 1);
                    z-index: 5;
                }}
                
                .success-container.active {{
                    opacity: 1;
                    transform: translateY(0);
                    visibility: visible;
                }}
                
                .success-checkmark {{
                    position: absolute;
                    top: -60px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 120px;
                    height: 120px;
                    background: white;
                    border-radius: 50%;
                    box-shadow: var(--shadow-lg);
                    z-index: 5;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                
                .checkmark-circle {{
                    position: relative;
                    width: 80px;
                    height: 80px;
                    border-radius: 50%;
                    background: var(--primary);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transform: scale(0);
                    animation: checkmarkAppear 0.6s cubic-bezier(0.3, 1.8, 0.3, 0.8) 0.6s forwards;
                }}
                
                .checkmark-circle::before {{
                    content: '';
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    border-radius: 50%;
                    background: var(--primary);
                    opacity: 0.4;
                    transform: scale(0);
                    animation: pulseRing 2s ease-out infinite;
                    animation-delay: 1.2s;
                }}
                
                .checkmark-circle i {{
                    color: white;
                    font-size: 36px;
                    opacity: 0;
                    animation: fadeInCheck 0.3s ease 1.1s forwards;
                }}
                
                .receipt-card {{
                    background: var(--bg-card);
                    border-radius: 20px;
                    box-shadow: var(--shadow-lg);
                    overflow: hidden;
                    transform: perspective(1000px);
                }}
                
                .receipt-header {{
                    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
                    padding: 40px 30px 40px;
                    color: white;
                    position: relative;
                }}
                
                .receipt-header::after {{
                    content: '';
                    position: absolute;
                    left: 0;
                    bottom: 0;
                    width: 100%;
                    height: 30px;
                    background-image: 
                        linear-gradient(45deg, var(--bg-card) 25%, transparent 25%),
                        linear-gradient(-45deg, var(--bg-card) 25%, transparent 25%);
                    background-size: 30px 30px;
                }}
                
                .receipt-status {{
                    font-size: 15px;
                    font-weight: 600;
                    color: rgba(255, 255, 255, 0.9);
                    margin-bottom: 20px;
                    display: flex;
                    align-items: center;
                }}
                
                .receipt-status i {{
                    font-size: 18px;
                    margin-right: 8px;
                }}
                
                .receipt-title {{
                    font-size: 28px;
                    font-weight: 800;
                    margin-bottom: 10px;
                }}
                
                .receipt-subtitle {{
                    font-size: 16px;
                    font-weight: 500;
                    opacity: 0.9;
                }}
                
                .receipt-body {{
                    padding: 40px 30px;
                }}
                
                .receipt-amount {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                
                .amount-label {{
                    font-size: 14px;
                    font-weight: 600;
                    color: var(--text-light);
                    margin-bottom: 5px;
                    text-transform: uppercase;
                }}
                
                .amount-value {{
                    font-size: 42px;
                    font-weight: 800;
                    color: var(--primary);
                }}
                
                .receipt-info {{
                    background-color: var(--bg-main);
                    border-radius: 16px;
                    padding: 25px;
                    margin-bottom: 30px;
                }}
                
                .info-title {{
                    font-size: 16px;
                    font-weight: 700;
                    color: var(--text-dark);
                    margin-bottom: 20px;
                    display: flex;
                    align-items: center;
                }}
                
                .info-title i {{
                    margin-right: 10px;
                    color: var(--primary);
                }}
                
                .info-row {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 15px;
                }}
                
                .info-row:last-child {{
                    margin-bottom: 0;
                }}
                
                .info-label {{
                    font-size: 14px;
                    color: var(--text-light);
                }}
                
                .info-value {{
                    font-size: 14px;
                    font-weight: 600;
                    color: var(--text-dark);
                }}
                
                .receipt-footer {{
                    padding: 0 30px 30px;
                }}
                
                .success-button {{
                    display: block;
                    width: 100%;
                    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
                    color: white;
                    border: none;
                    border-radius: 50px;
                    font-size: 16px;
                    font-weight: 600;
                    padding: 16px 0;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: var(--shadow-accent);
                }}
                
                .success-button:hover {{
                    transform: translateY(-3px);
                    box-shadow: 0 10px 25px rgba(76, 175, 80, 0.35);
                }}
                
                .success-button i {{
                    margin-right: 8px;
                }}
                
                /* Success Animation Effects */
                .floating-elements {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    overflow: hidden;
                    pointer-events: none;
                }}
                
                .floating-element {{
                    position: absolute;
                    z-index: 1;
                    opacity: 0;
                }}
                
                .element-circle {{
                    border-radius: 50%;
                }}
                
                .element-star {{
                    clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
                }}
                
                .element-square {{
                    border-radius: 4px;
                }}
                
                /* Animation Keyframes */
                @keyframes loader-spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
                
                @keyframes pulse {{
                    0% {{ transform: translate(-50%, -50%) scale(0.95); }}
                    50% {{ transform: translate(-50%, -50%) scale(1.05); }}
                    100% {{ transform: translate(-50%, -50%) scale(0.95); }}
                }}
                
                @keyframes pulseRing {{
                    0% {{ transform: scale(1.0); opacity: 0.4; }}
                    80%, 100% {{ transform: scale(2.5); opacity: 0; }}
                }}
                
                @keyframes checkmarkAppear {{
                    0% {{ transform: scale(0); }}
                    80% {{ transform: scale(1.1); }}
                    100% {{ transform: scale(1); }}
                }}
                
                @keyframes fadeInCheck {{
                    0% {{ opacity: 0; transform: scale(0.5); }}
                    100% {{ opacity: 1; transform: scale(1); }}
                }}
                
                @keyframes floatElementsAnimation {{
                    0% {{ transform: translate(0, 0) rotate(0deg); opacity: 0; }}
                    20% {{ opacity: 1; }}
                    80% {{ opacity: 1; }}
                    100% {{ transform: translate(var(--tx), var(--ty)) rotate(var(--r)); opacity: 0; }}
                }}
                
                /* Responsive styles */
                @media (max-width: 480px) {{
                    .processing-steps {{
                        max-width: 280px;
                    }}
                    
                    .processing-title {{
                        font-size: 20px;
                    }}
                    
                    .receipt-title {{
                        font-size: 24px;
                    }}
                    
                    .amount-value {{
                        font-size: 36px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="animation-container">
                <!-- Step 1: Processing Animation -->
                <div class="processing-container" id="processing-container">
                    <div class="processing-card">
                        <div class="card-decoration decoration-1"></div>
                        <div class="card-decoration decoration-2"></div>
                        
                        <div class="processing-loader">
                            <div class="loader-ring"></div>
                            <div class="loader-ring-inner"></div>
                            <i class="fas fa-credit-card loader-icon"></i>
                        </div>
                        
                        <h2 class="processing-title">Processing Payment</h2>
                        <p class="processing-subtitle">Please wait while we confirm your transaction</p>
                        
                        <div class="processing-steps">
                            <div class="step active" id="step-1">
                                <div class="step-circle">1</div>
                                <div class="step-label">Verifying</div>
                            </div>
                            <div class="step" id="step-2">
                                <div class="step-circle">2</div>
                                <div class="step-label">Processing</div>
                            </div>
                            <div class="step" id="step-3">
                                <div class="step-circle">3</div>
                                <div class="step-label">Confirming</div>
                            </div>
                        </div>
                        
                        <div class="processing-progress">
                            <div class="progress-bar" id="progress-bar"></div>
                        </div>
                        <div class="progress-text" id="progress-text">0%</div>
                    </div>
                </div>
                
                <!-- Step 2: Success Animation -->
                <div class="success-container" id="success-container">
                    <div class="success-checkmark">
                        <div class="checkmark-circle">
                            <i class="fas fa-check"></i>
                        </div>
                    </div>
                    
                    <div class="receipt-card">
                        <div class="receipt-header">
                            <div class="receipt-status">
                                <i class="fas fa-check-circle"></i>Payment Successful
                            </div>
                            <h1 class="receipt-title">Thank You!</h1>
                            <p class="receipt-subtitle">Your payment has been confirmed</p>
                        </div>
                        
                        <div class="receipt-body">
                            <div class="receipt-amount">
                                <div class="amount-label">Amount Paid</div>
                                <div class="amount-value">₹{amt}</div>
                            </div>
                            
                            <div class="receipt-info">
                                <h3 class="info-title">
                                    <i class="fas fa-file-invoice"></i>Payment Details
                                </h3>
                                
                                <div class="info-row">
                                    <span class="info-label">Transaction Date</span>
                                    <span class="info-value">{payment_date}</span>
                                </div>
                                
                                <div class="info-row">
                                    <span class="info-label">Application No.</span>
                                    <span class="info-value">{apno}</span>
                                </div>
                                
                                <div class="info-row">
                                    <span class="info-label">Payment Method</span>
                                    <span class="info-value">Credit Card ({masked_card})</span>
                                </div>
                                
                                <div class="info-row">
                                    <span class="info-label">Status</span>
                                    <span class="info-value" style="color: var(--primary);">Paid</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="receipt-footer">
                            <button class="success-button" id="view-status-btn">
                                <i class="fas fa-eye"></i>View Application Status
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Floating celebration elements -->
                <div class="floating-elements" id="floating-elements"></div>
            </div>
            
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    const processingContainer = document.getElementById('processing-container');
                    const successContainer = document.getElementById('success-container');
                    const viewStatusBtn = document.getElementById('view-status-btn');
                    const progressBar = document.getElementById('progress-bar');
                    const progressText = document.getElementById('progress-text');
                    const step1 = document.getElementById('step-1');
                    const step2 = document.getElementById('step-2');
                    const step3 = document.getElementById('step-3');
                    const floatingElements = document.getElementById('floating-elements');
                    
                    // Progress animation
                    let progress = 0;
                    const progressInterval = setInterval(() => {{
                        progress += 1;
                        
                        // Update progress bar and text
                        progressBar.style.width = `${{progress}}%`;
                        progressText.textContent = `${{progress}}%`;
                        
                        // Update steps at certain progress points
                        if (progress === 30) {{
                            step1.classList.remove('active');
                            step1.classList.add('completed');
                            step2.classList.add('active');
                        }}
                        else if (progress === 70) {{
                            step2.classList.remove('active');
                            step2.classList.add('completed');
                            step3.classList.add('active');
                        }}
                        
                        if (progress >= 100) {{
                            clearInterval(progressInterval);
                            
                            // Transition to success screen
                            setTimeout(() => {{
                                processingContainer.style.opacity = '0';
                                processingContainer.style.transform = 'translateY(-50px)';
                                
                                setTimeout(() => {{
                                    processingContainer.style.display = 'none';
                                    successContainer.classList.add('active');
                                    
                                    // Create and animate floating celebration elements
                                    createFloatingElements();
                                }}, 500);
                            }}, 500);
                        }}
                    }}, 30); // Adjust speed of progress - lower number = faster
                    
                    // Create floating celebration elements
                    function createFloatingElements() {{
                        const colors = ['#4CAF50', '#2E7D32', '#A5D6A7', '#FFD700', '#8BC34A'];
                        const shapes = ['element-circle', 'element-star', 'element-square'];
                        
                        for (let i = 0; i < 40; i++) {{
                            const element = document.createElement('div');
                            element.classList.add('floating-element');
                            
                            // Random properties
                            const size = Math.random() * 12 + 8;
                            const shape = shapes[Math.floor(Math.random() * shapes.length)];
                            const color = colors[Math.floor(Math.random() * colors.length)];
                            
                            // Apply styles
                            element.classList.add(shape);
                            element.style.width = `${{size}}px`;
                            element.style.height = `${{size}}px`;
                            element.style.backgroundColor = color;
                            
                            // Random start position
                            const startX = Math.random() * 100;
                            const startY = Math.random() * 100;
                            element.style.left = `${{startX}}%`;
                            element.style.top = `${{startY}}%`;
                            
                            // Random animation parameters
                            const translateX = (Math.random() - 0.5) * 200;
                            const translateY = (Math.random() - 0.5) * 200;
                            const rotation = Math.random() * 720 - 360;
                            const duration = Math.random() * 2 + 3;
                            const delay = Math.random() * 2;
                            
                            element.style.setProperty('--tx', `${{translateX}}px`);
                            element.style.setProperty('--ty', `${{translateY}}px`);
                            element.style.setProperty('--r', `${{rotation}}deg`);
                            element.style.animation = `floatElementsAnimation ${{duration}}s ease ${{delay}}s`;
                            
                            floatingElements.appendChild(element);
                        }}
                    }}
                    
                    // Button click handler
                    viewStatusBtn.addEventListener('click', function() {{
                        window.location.href = '/view_application_status/';
                    }});
                    
                    // Auto-redirect after 12 seconds
                    setTimeout(() => {{
                        window.location.href = '/view_application_status/';
                    }}, 12000);
                }});
            </script>
        </body>
        </html>
        """
        
        return HttpResponse(success_html)

    # In case of a GET request, return to the paybill page (or some other appropriate response)
    return render(request, 'paybill.html')


def viewpayment(request):
    cursor = connection.cursor()

    # SQL query to join all customers with their payment details
    sql = """
        SELECT c.Cid, c.Name, c.Address, c.Phone, c.Gender, c.Email, p.date, p.amt
        FROM customer c
        LEFT JOIN pbill p ON c.Cid = p.uid
    """
    
    cursor.execute(sql)
    results = cursor.fetchall()

    customer_list = []

    # Populating customer list with payment history
    for r in results:
        customer_data = {
            'cid': r[0],
            'name': r[1],
            'address': r[2],
            'phone': r[3],
            'gender': r[4],
            'email': r[5],
            'date': r[6] if r[6] else "No Payment Date",  # Handling NULL values
            'amount': r[7] if r[7] else "No Payment Amount"
        }
        customer_list.append(customer_data)

    # Rendering customer list with payment info to the template
    return render(request, 'viewpayment.html', {'customers': customer_list})


def feedback(request):
    return render(request, 'feedback.html')


def feedbackaction(request):
    cursor=connection.cursor()
    f=request.GET['t2']
    
    a=request.session['Uid']
    sql="insert into feedback(feedback,uid)values('%s','%s')"%(f,request.session['Uid'])
    cursor.execute(sql)
    
    # Create feedback success animation
    success_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Feedback Submitted</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
            
            * { 
                margin: 0; 
                padding: 0; 
                box-sizing: border-box; 
            }
            
            :root {
                --primary: #8E2DE2;        /* Purple */
                --primary-light: #B06FE3;
                --secondary: #4A00E0;      /* Deep Blue */
                --text: #333333;
                --text-light: #777777;
                --bg: #F8F9FD;
                --white: #FFFFFF;
                --shadow: 0 10px 30px rgba(142, 45, 226, 0.1);
            }
            
            body { 
                font-family: 'Poppins', sans-serif;
                background-color: var(--bg);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: var(--text);
            }
            
            .feedback-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                background: var(--white);
                border-radius: 20px;
                box-shadow: var(--shadow);
                padding: 3rem 2.5rem;
                width: 90%;
                max-width: 450px;
                text-align: center;
                transform: translateY(30px);
                opacity: 0;
                animation: slideIn 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards;
            }
            
            .feedback-icon {
                width: 90px;
                height: 90px;
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 2rem;
                position: relative;
                overflow: hidden;
            }
            
            .feedback-icon::before {
                content: '';
                position: absolute;
                width: 150%;
                height: 150%;
                background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 70%);
                animation: rotate 5s linear infinite;
            }
            
            .feedback-icon i {
                color: var(--white);
                font-size: 36px;
                position: relative;
                animation: bounceIn 0.6s cubic-bezier(0.47, 2.02, 0.31, 0.99) 0.2s both;
            }
            
            .feedback-title {
                font-size: 1.8rem;
                font-weight: 700;
                color: var(--text);
                margin-bottom: 0.7rem;
                opacity: 0;
                animation: fadeUp 0.5s ease 0.4s forwards;
            }
            
            .feedback-message {
                font-size: 1rem;
                color: var(--text-light);
                line-height: 1.6;
                margin-bottom: 2rem;
                opacity: 0;
                animation: fadeUp 0.5s ease 0.6s forwards;
            }
            
            .back-button {
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                color: var(--white);
                border: none;
                border-radius: 50px;
                padding: 0.9rem 2.5rem;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                box-shadow: 0 5px 15px rgba(142, 45, 226, 0.3);
                position: relative;
                overflow: hidden;
                opacity: 0;
                animation: fadeUp 0.5s ease 0.8s forwards;
            }
            
            .back-button i {
                margin-right: 8px;
            }
            
            .back-button::before {
                content: '';
                position: absolute;
                width: 100%;
                height: 100%;
                background: linear-gradient(to right, transparent, rgba(255,255,255,0.2), transparent);
                transform: translateX(-100%);
                transition: transform 0.5s;
            }
            
            .back-button:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(142, 45, 226, 0.4);
            }
            
            .back-button:hover::before {
                transform: translateX(100%);
            }
            
            /* Stars animation */
            .stars {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
            }
            
            .star {
                position: absolute;
                opacity: 0;
            }
            
            /* Animations */
            @keyframes slideIn {
                from { transform: translateY(30px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            @keyframes fadeUp {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes bounceIn {
                0% { transform: scale(0); }
                50% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }
            
            @keyframes starFade {
                0% { opacity: 0; transform: scale(0) rotate(0deg); }
                50% { opacity: 1; transform: scale(1) rotate(180deg); }
                100% { opacity: 0; transform: scale(0) rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="stars" id="stars-container"></div>
        
        <div class="feedback-container">
            <div class="feedback-icon">
                <i class="fas fa-comment-dots"></i>
            </div>
            
            <h1 class="feedback-title">Thank You!</h1>
            <p class="feedback-message">Your feedback has been successfully submitted. We appreciate your input and will use it to improve our services.</p>
            
            <button class="back-button" id="home-button">
                <i class="fas fa-home"></i>Return Home
            </button>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Create stars
                const starsContainer = document.getElementById('stars-container');
                const colors = ['#8E2DE2', '#4A00E0', '#B06FE3'];
                
                for (let i = 0; i < 20; i++) {
                    const star = document.createElement('div');
                    star.classList.add('star');
                    
                    // Random star styling
                    const size = Math.random() * 10 + 5;
                    const color = colors[Math.floor(Math.random() * colors.length)];
                    
                    star.style.width = `${size}px`;
                    star.style.height = `${size}px`;
                    star.style.background = color;
                    star.style.borderRadius = '50%';
                    star.style.left = `${Math.random() * 100}%`;
                    star.style.top = `${Math.random() * 100}%`;
                    
                    // Animation
                    const delay = Math.random() * 2;
                    const duration = Math.random() * 2 + 1;
                    star.style.animation = `starFade ${duration}s ease ${delay}s infinite`;
                    
                    starsContainer.appendChild(star);
                }
                
                // Redirect on button click
                document.getElementById('home-button').addEventListener('click', function() {
                    window.location.href = '/customerhome/';
                });
                
                // Auto redirect after 5 seconds
                setTimeout(() => {
                    window.location.href = '/customerhome/';
                }, 5000);
            });
        </script>
    </body>
    </html>
    """
    
    return HttpResponse(success_html)


def viewFeedback(request):
	cursor=connection.cursor()
	
	e="select f.fid,f.feedback,f.uid,c.Name from feedback as f inner join customer as c on f.uid=c.cid"
	cursor.execute(e)
	result = cursor.fetchall()
	list = []
	for row in result:
		w = {'fid' : row[0],'feedback': row[1],'uid' : row[2],'Name': row[3]}
		list.append(w)
	return render(request,'viewFeedback.html',{'list':list})

def viewAllAssign(request):
    cursor = connection.cursor()

    # Updated SQL query to join assignloc, location, and staff tables
    query = """
        SELECT 
            al.Aid,
            s.Name AS staff_name,
            s.Place AS staff_place,
            s.Phone AS staff_phone,
            l.Area AS location_name
        FROM 
            assignloc AS al
        INNER JOIN 
            staff AS s ON al.Staffid = s.Sid
        INNER JOIN 
            location AS l ON al.Locationid = l.Locid
    """
    
    cursor.execute(query)
    result = cursor.fetchall()

    list = []
    for row in result:
        w = {
            'Aid': row[0],
            'staff_name': row[1],
            'staff_place': row[2],
            'staff_phone': row[3],
            'location_name': row[4]
        }
        list.append(w)

    return render(request, 'viewAllAssign.html', {'list': list})


def insta(request):
    return render(request, 'insta.html')



def wastecategory(request):
    return render(request, 'wastecategory.html')

def smartwaste(request):
    return render(request, 'smartwaste.html')

def recycling(request):
    return render(request, 'recycling.html')

def office(request):
    return render(request, 'office.html')

def future(request):
    return render(request, 'future.html')

def guide(request):
    return render(request, 'guide.html')




