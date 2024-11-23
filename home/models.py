from django.db import models
from datetime import date
from django.contrib.auth.models import User


# Create your models here.

class users(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    confirm_password= models.CharField(max_length=200)
    
class S_flight(models.Model):
    travel_type=models.CharField(max_length=25)
    depature=models.CharField(max_length=100)
    arrive=models.CharField(max_length=100)
    depart_date=models.DateTimeField(default=date.today())
    return_date=models.DateTimeField(default=date.today())
    no_of_passenger=models.IntegerField
    cabin_class=models.CharField(max_length=25)
    class Meta:
        db_table:"searchflight"

class Flight_schedule(models.Model):
    company_name=models.CharField(max_length=100)
    From=models.CharField(max_length=100)
    To=models.CharField(max_length=100)
    pnr_no=models.IntegerField(default=0)
    dept_time=models.CharField(max_length=100)
    rich_time=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    economy_seat=models.IntegerField(default=0)
    pre_economy_seat=models.IntegerField(default=0)
    business_seat=models.IntegerField(default=0)
    first_class_seat=models.IntegerField(default=0)
    economy_seat_price=models.IntegerField(default=0)
    pre_economy_seat_price=models.IntegerField(default=0)
    business_price=models.IntegerField(default=0)
    first_class_seat_price=models.IntegerField(default=0)
    date=models.DateField()
    everyday=models.CharField(max_length=55,default="NO")

    @staticmethod
    def get_all_product():
        return Flight_schedule.objects.all()
    
   # def get_all_product_departdate(depart):
    #    return flight_schedule.objects.filter(From__icontains=depart)
    
class places(models.Model):
    name=models.CharField(max_length=100)

    @staticmethod
    def get_all_product():
        return places.objects.all()
    
class travel_passenger(models.Model):
    First_name=models.CharField(max_length=255)
    Last_name=models.CharField(max_length=255)
    Gender=models.CharField(max_length=55)

class Passenger_contact(models.Model):
    travel_passenger=models.ForeignKey(travel_passenger,on_delete=models.CASCADE)
    conutry_code=models.CharField(max_length=55)
    mobile_no=models.CharField(max_length=11)
    Email=models.EmailField(max_length=55)

class payment_details(models.Model):
    payment_amount=models.CharField(max_length=255)
    credit_card_number=models.CharField(max_length=255)
    credit_holder_name=models.CharField(max_length=255)
    month_year_expiry=models.DateField()
    cvv_code=models.CharField(max_length=55)




    

