from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date
from home.models import S_flight
from home.models import Flight_schedule,places,travel_passenger,payment_details
from datetime import datetime
from django.http import JsonResponse, HttpResponse
import json
from django.core.mail import send_mail
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from .models import Flight_schedule
from django.shortcuts import render
from .models import payment_details, Flight_schedule  
from django.contrib.auth.decorators import login_required





def handlelogout(request):
    auth_logout(request)  # Log the user out
    return render(request, 'base.html')

Depature=""
arrive=""
cabin_class=""
dept_date=""
return_date=""
twoway_dept_pnr_no=""
twoway_return_pnr_no=""
oneway_pnr_no=""
Travel_type=""
PNR_no=""

# View for the homepage (requires login)
@login_required
def home(request):
    #return HttpResponse("This is home page")
    return render(request,'base.html')
@login_required
def service(request):
    return render(request,'services.html')
@login_required
def booking(request):
    global Depature,cabin_class,arrive,dept_date,return_date,Travel_type
    if request.method=="POST":
       Travel_type=request.POST['checking']
       saverecord=S_flight()
       saverecord.travel_type=request.POST['checking']
       saverecord.depature=request.POST['From']
       Depature = request.POST['From'] 
       saverecord.arrive=request.POST['To']
       arrive=request.POST['To']
       arrive=request.POST['To']
       if Travel_type=="one-way":
           saverecord.return_date=date.today()
       else:
           saverecord.return_date=request.POST['returndate']
           return_date=request.POST['returndate']

       saverecord.depart_date=request.POST['departdate']
       dept_date=request.POST['departdate']
       print(dept_date)
       saverecord.no_of_passenger=request.POST['passenger']
       saverecord.cabin_class=request.POST['cabinclass']
       cabin_class=request.POST['cabinclass']
       saverecord.save()
       #print(travel_type)
       #print(depature)
       #print(arrive)
       if Travel_type=="return":
          print("redirect to return page")
          return redirect('/Return')
       else:
          print("redirect to one-way page")
          return redirect('/oneway')
    return render(request,'booking.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # This logs the user in
            return redirect('home')  # Redirect to the home page (base.html)
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff or user.is_superuser:  # Check if the user is an admin
                auth_login(request, user)  # This logs the admin in
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            else:
                messages.error(request, 'You do not have admin privileges')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'admin_login.html')

# Home view to render base.html after login
@login_required
def home(request):
    return render(request, 'base.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, 'Signup successful, please login.')
        return redirect('login')
    return render(request, 'register.html')
  
@login_required
def Return(request):
    global Depature,cabin_class,arrive,dept_date,return_date,twoway_dept_pnr_no,twoway_return_pnr_no
    if request.method=="POST":
        twoway_dept_pnr_no = request.POST.get('dpnr')
        twoway_return_pnr_no= request.POST.get('rpnr')
        print("this is return")
        print(twoway_dept_pnr_no)
        print(twoway_return_pnr_no)

        return redirect('/ticketdetails')
    
    
    Flights_one=Flight_schedule.objects.filter(From__icontains=Depature).filter(To__icontains=arrive).filter(everyday__icontains="YES")
    Flights_two=Flight_schedule.objects.filter(From__icontains=arrive).filter(To__icontains=Depature).filter(everyday__icontains="YES")
    return render(request,'return.html', {'flights_one':Flights_one,'flights_two':Flights_two,'Cabin_class': cabin_class.upper() ,'from':Depature,'to': arrive,'Dept_date':dept_date,'Return_date':return_date})

@login_required
def oneway(request):
     global Depature,cabin_class,arrive,dept_date,oneway_pnr_no
     if request.method=="POST":
        print("redirect to ticketdetails")
        oneway_pnr_no = request.POST.get('dpnr')
        print(oneway_pnr_no)

        return redirect('/ticketdetails')
    
     #depart_day = datetime.strptime(dept_date, "%Y-%m-%d")
     #depart_day=Week.objects.get(number=return_date.weekday())
     Flights=Flight_schedule.objects.filter(From__icontains=Depature).filter(To__icontains=arrive).filter(everyday__icontains="YES")
     return render(request,'oneway.html', {'flights':Flights,'Cabin_class': cabin_class.upper() ,'from':Depature,'to': arrive,'Dept_date':dept_date})

@login_required
def adminpage(request):
     Flights=Flight_schedule.get_all_product()
     return render(request, 'adminpage.html', {'flights':Flights})

@login_required
def addflight(request):
    if request.method=="POST":
        saverecord=Flight_schedule()
        saverecord.company_name=request.POST["company_name"]
        saverecord.From=request.POST["from"]
        saverecord.To=request.POST["to"]
        saverecord.pnr_no=request.POST["pnr_no"]
        saverecord.dept_time=request.POST["dept_time"]
        saverecord.rich_time=request.POST["rich_time"]
        saverecord.duration=request.POST["duration"]
        saverecord.economy_seat=request.POST["economy_seat"]
        saverecord.pre_economy_seat=request.POST["pre_economy_seat"]
        saverecord.business_seat=request.POST["business_seat"]
        saverecord.first_class_seat=request.POST["first_class_seat"]
        saverecord.economy_seat_price=request.POST["economy_seat_price"]
        saverecord.pre_economy_seat_price=request.POST["pre_economy_seat_price"]
        saverecord.business_price=request.POST["business_seat_price"]
        saverecord.first_class_seat_price=request.POST["first_class_seat_price"]
        saverecord.date=request.POST["date"]
        saverecord.everyday=request.POST["everyday"]
        print(saverecord.company_name)
        print(saverecord.dept_time)
        saverecord.save()
        return redirect('/addflight')
    return render (request,'addflight.html')

@login_required
def ticketdetails(request):
    global cabin_class, Travel_type, twoway_dept_pnr_no, twoway_return_pnr_no, oneway_pnr_no
    passenger_count = request.session.get('passenger_count', 1)  # Default to 1 passenger

    if Travel_type == "return":
        Flight_ticket_one = Flight_schedule.objects.filter(pnr_no__icontains=twoway_dept_pnr_no)
        Flight_ticket_two = Flight_schedule.objects.filter(pnr_no__icontains=twoway_return_pnr_no)

        zipped_segment = zip(Flight_ticket_one, Flight_ticket_two)
        total_fare = sum(flight.economy_seat_price for flight in Flight_ticket_one) + \
                     sum(flight.economy_seat_price for flight in Flight_ticket_two)

        total_fare *= passenger_count
        surcharge = 100 * passenger_count
        final_price = total_fare + surcharge

        return render(request, 'ticketdetails.html', {
            'Cabin_class': cabin_class.upper(),
            'travel_type': Travel_type,
            'Zipped': zipped_segment,
            'total_fare': total_fare,
            'surcharge': surcharge,
            'final_price': final_price
        })
    else:
        Flight = Flight_schedule.objects.filter(pnr_no__icontains=oneway_pnr_no)
        total_fare = sum(flight.economy_seat_price for flight in Flight)
        total_fare *= passenger_count
        surcharge = 100 * passenger_count
        final_price = total_fare + surcharge

        return render(request, 'ticketdetails.html', {
            'Cabin_class': cabin_class.upper(),
            'flights': Flight,
            'travel_type': Travel_type,
            'total_fare': total_fare,
            'surcharge': surcharge,
            'final_price': final_price
        })
    
def savepassenger(request):
    if request.method == "POST": 
        #print(request.POST)
         vd =request.POST
         print("this is vd")
         print(vd)
         print(vd["First_name"])
         #print(request.POST[1])
         save_travel_passenger=travel_passenger()
         save_travel_passenger.First_name=vd["First_name"]
         save_travel_passenger.Last_name=vd["Last_name"]
         save_travel_passenger.Gender=vd["Gender"]
         save_travel_passenger.save()
         return JsonResponse({"message" : "request handle.."})

def savepassenger(request):
    if request.method == "POST":
        passenger_count = request.session.get('passenger_count', 0) + 1
        request.session['passenger_count'] = passenger_count
        # Save passenger details logic
        return JsonResponse({'status': 'success', 'passenger_count': passenger_count})
    
from django.conf import settings
from .models import payment_details
from django.utils import timezone  # To set the current date and time

def payment(request):
    if request.method == 'POST':
        # Handle payment form submission and process payment logic here
        
        # Retrieve form data
        total_amount = request.POST.get('payment-amount')
        credit_card_number = request.POST.get('credit-card-number')
        credit_holder_name = request.POST.get('credit-card-holder-name')
        expiry_month = request.POST.get('expiry-month')
        cvv_code = request.POST.get('cvv-code')

        # Assuming payment is successful
        # Store payment details in the database
        payment_record = payment_details(
            payment_amount=total_amount,
            credit_card_number=credit_card_number,
            credit_holder_name=credit_holder_name,
            month_year_expiry=expiry_month + "-01",  # Format to YYYY-MM-DD
            cvv_code=cvv_code
        )
        payment_record.save()

        # Send the invoice email
        user_name = "MUGESH KARTHI G S"  # Replace with actual data
        user_email = "gsmugeshkarthi7425@gmail.com"  # Replace with actual data
        booking_id = "LA876NSU837UNA7"  # Replace with actual data
        payment_method = "Credit Card"  # Replace with actual data

        email_content = render_to_string('invoice.html', {
            'user_name': user_name,
            'user_email': user_email,
            'booking_id': booking_id,
            'total_amount': total_amount,
            'payment_method': payment_method,
        })

        send_mail(
            subject="Payment Invoice - Travel Booking Application",
            message="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=email_content,
        )

        return redirect('payment_success')
    
    return render(request, 'payment.html')




def payment_success(request):
    context = {
        'user_name': 'MUGESH KARTHI G S',  # Replace with dynamic data if needed
        'payment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  
        'transaction_id': 'LA876NSU837UNA7'  # Replace with dynamic data if needed
    }
    return render(request, 'payment_success.html', context)



from .models import Flight_schedule

def adminpage(request):
    flights = Flight_schedule.objects.all()  # Fetch all flight schedules
    total_flights = flights.count()  # Calculate total flights count
    return render(request, 'adminpage.html', {'flights': flights, 'total_flights': total_flights})





def dashboard(request):
    # Fetch all flight schedules
    flights = Flight_schedule.objects.all()

    # Calculate total flights
    total_flights = flights.count()

    # Calculate total tickets (seats in all classes)
    total_tickets = sum(
        flight.economy_seat + 
        flight.pre_economy_seat + 
        flight.business_seat + 
        flight.first_class_seat 
        for flight in flights
    )

    # Calculate total revenue (based on seat prices for each class)
    total_revenue = sum(
        flight.economy_seat * flight.economy_seat_price +
        flight.pre_economy_seat * flight.pre_economy_seat_price +
        flight.business_seat * flight.business_price +
        flight.first_class_seat * flight.first_class_seat_price
        for flight in flights
    )

    # Count booked tickets from payment_details model
    total_payments = payment_details.objects.count()

    # Pass data to the template
    context = {
        'flights': flights,
        'total_flights': total_flights,
        'total_tickets': total_tickets,
        'total_revenue': total_revenue,
        'total_payments': total_payments,
    }

    return render(request, 'dashboard.html', context)



from django.shortcuts import render, get_object_or_404, redirect


def edit_flight(request, id):
    flight = get_object_or_404(Flight_schedule, id=id)
    if request.method == "POST":
        # Update the flight details
        flight.pnr_no = request.POST['pnr_no']
        flight.From = request.POST['from']
        flight.To = request.POST['to']
        flight.dept_time = request.POST['dept_time']
        flight.economy_seat = request.POST['economy_seat']
        flight.pre_economy_seat = request.POST['pre_economy_seat']
        flight.business_seat = request.POST['business_seat']
        flight.first_class_seat = request.POST['first_class_seat']
        flight.date = request.POST['date']
        flight.everyday = request.POST['everyday']
        flight.save()
        return redirect('/dashboard')
    return render(request, 'edit_flight.html', {'flight': flight})

def delete_flight(request, id):
    flight = get_object_or_404(Flight_schedule, id=id)
    flight.delete()
    return redirect('/dashboard')











