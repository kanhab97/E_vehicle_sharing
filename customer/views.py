from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
import json
import math
from datetime import datetime, timedelta
import uuid
from . import models
from .models import Location
from .models import Vehicle


def response(code, message="", data=[]):
    result = {"code": code, "message": message, "data": data}
    return HttpResponse(json.dumps(result))

def report(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        repair_desc = request.POST.get('repair_desc')
        vehicle_id=request.POST.get('vehicle_id')
        print(vehicle_id)
        print(repair_desc)
        vehicle = models.Vehicle.objects.filter(vehicle_id=vehicle_id).first()
        if not vehicle:
            message = "Vehicle does not exist"
            return response(400, message)
        vehicle.booking_status=0
        vehicle.repair_status=1
        vehicle.repair_desc=repair_desc
        vehicle.save()
    return render(request, 'customer/Report.html')

def index(request):
    if not request.session.get('is_login', None):
        if request.session.get('type'):
            return redirect("/corpuser_login/")
        else:
            return redirect("/user_login/")
    return render(request, 'customer/index.html')

def vehicles_available(request):
    Loc_List=Location.objects.all()
    return render(request, 'customer/vehicles_available.html',
    {'loc_List': Loc_List})

def vehicles_available_corp(request):
    Loc_List=Location.objects.all()
    return render(request, 'customer/vehicles_available_corp.html',
    {'loc_List': Loc_List})

def contact_us(request):
    return render(request, 'customer/contact_us.html')


def confirmation(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        amount = int(request.POST.get('amount'))
        print(user_id)
        print(amount)
        if user_id.strip():
            try:
                user = models.User.objects.get(user_id=user_id)
            except:
                message = 'User does not exist！'
                print(message)
                return render(request, 'customer/Payment.html', locals())
            loc = models.User.objects.filter(user_id=user.user_id).first()
            loc.wallet += amount
            loc.save()
    return render(request, 'customer/conf.html')

def home(request):
    return render(request, 'customer/home.html')

def booking(request):
    Loc_List1=Location.objects.all()
    return render(request, 'customer/booking.html',
    {'loc_List1': Loc_List1})

def booking_second(request):
    return render(request, 'customer/booking_second.html')

def booking_details(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    return render(request, 'customer/booking_details.html')


def user_login(request):
    if request.session.get('is_login', None):
        return redirect('/vehicles_available/')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        if username.strip() and password:
            try:
                user = models.User.objects.get(user_id=username, user_type=0)
            except:
                message = 'User does not exist！'
                return render(request, 'customer/user_login.html', locals())

            if user.password == password:
                request.session['type'] = 0
                request.session['is_login'] = True
                request.session['user_id'] = user.user_id
                request.session['name'] = user.name
                return redirect('/vehicles_available/')
            else:
                message = 'Password not correct！'
                return render(request, 'customer/user_login.html', locals())
    return render(request, 'customer/user_login.html')


def corpuser_login(request):
    if request.session.get('is_login', None):
        return redirect('/vehicles_available_corp/')
    if request.method == "POST":
        corp_name = request.POST.get('username')
        password = request.POST.get('password')
        if corp_name and password:
            try:
                corp_user = models.User.objects.get(user_id=corp_name, user_type=1)
            except:
                message = 'User does not exist！'
                return render(request, 'customer/corpuser_login.html', locals())

            if corp_user.password == password:
                request.session['type'] = 1
                request.session['is_login'] = True
                request.session['user_id'] = corp_user.user_id
                request.session['name'] = corp_user.name
                return redirect('/vehicles_available_corp/')
            else:
                message = 'Password not correct！'
                return render(request, 'customer/corpuser_login.html', locals())
    return render(request, 'customer/corpuser_login.html')


def user_register(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        if phone and username.strip() and password and user_id.strip() and address:
            if confirmPassword != password:
                message = 'Password does not match!!!'
                return render(request, 'customer/user_register.html', locals())
            else:
                if models.User.objects.filter(user_id=user_id):
                    message = 'User_id already exists!'
                    return render(request, 'customer/user_register.html', locals())
                if models.User.objects.filter(phone_no=phone):
                    message = 'Phone number has already been used ！'
                    return render(request, 'customer/user_register.html', locals())
            new_user = models.User(name=username, password=password, phone_no=phone, address=address, user_id=user_id, dob=dob, user_type=0,wallet=0)
            new_user.save()
            message = 'Thanks for Registration!'
            return redirect('/user_login/')
        else:
            return render(request, 'customer/user_login.html')
    return render(request, 'customer/user_register.html')


def corpuser_register(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        user_id = request.POST.get('user_id')
        corp_name = request.POST.get('corp_name')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        address = request.POST.get('address')
        if phone and user_id.strip() and corp_name.strip() and password:
            if confirmPassword != password:
                message = 'Password does not match!'
                return render(request, 'customer/corpuser_register.html', locals())
            else:
                if models.User.objects.filter(user_id=user_id):
                    message = 'User_id already exists!'
                    return render(request, 'customer/corpuser_register.html', locals())
                if models.User.objects.filter(phone_no=phone):
                    message = 'Phone number has already been used ！'
                    return render(request, 'customer/corpuser_register.html', locals())
            new_user = models.User(user_id=user_id, name=corp_name, password=password, phone_no=phone, address=address, user_type=1,wallet=0)
            new_user.save()
            return redirect('/corpuser_login/')
        else:
            return render(request, 'customer/corpuser_login.html')
    return render(request, 'customer/corpuser_register.html')


def logout(request):
    if not request.session.get('is_login', None):
        if request.session.get('type'):
            return redirect("/corpuser_login/")
        else:
            return redirect("/user_login/")
    if request.session.get('type'):
        request.session.flush()
        return redirect("/corpuser_login/")
    else:
        request.session.flush()
        return redirect("/user_login/")


def getVehiclesAvailability(request):
    if request.method == "POST":
        vehicle_type = int(request.POST.get('vehicle_type'))
        if not vehicle_type:
            locations = list(models.Location.objects.all().values())
            return response(200, "", locations)
        else:
            messgae = "vehicle_type is wrong"
            return response(400, messgae)

def paym(request):
    user_id = request.session.get('user_id')
    user = models.User.objects.get(user_id=user_id)
    return render(request, 'customer/Payment.html',
    { 'user_id1' : user })
    #if request.method == "POST":
        #amount = request.POST.get('amount')
        #user_id = request.POST.get('user_id')
        #if models.User.objects.filter(user_id=user_id):



def bookVehicle(request):
    if request.method == "POST":
        vehicle_type = int(request.POST.get('vehicle_type'))
        user_id = request.session.get('user_id')
        if not user_id:
            message = "User is not logged in"
            return response(400, message)
        pick_loc_id = request.POST.get('pick_loc_id')
        drop_loc_id = request.POST.get('drop_loc_id')
        duration = float(request.POST.get('duration'))    # unit:hour
        pick_time = datetime.now()
        drop_time = pick_time + timedelta(minutes=duration*60)
        pick_location = models.Location.objects.filter(loc_id=pick_loc_id).first()
        if not pick_location:
            message = "Pick_location not found"
            return response(400, message)
        drop_location = models.Location.objects.filter(loc_id=drop_loc_id).first()
        if not drop_location:
            message = "Drop_location not found"
            return response(400, message)
        if vehicle_type == 0:    # car
            if pick_location.cars_available == 0:
                message = "There is no car available in this location"
                return response(400, message)
        else:    # bike
            if pick_location.bikes_available == 0:
                message = "There is no bike available in this location"
                return response(400, message)

        estimated_charge = duration * 5
        vehicle = models.Vehicle.objects.filter(location=pick_location, vehicle_type=vehicle_type, repair_status=0, booking_status=0, charge__gt=estimated_charge+5).order_by("charge").first()
        booking_id = str(uuid.uuid1())
        cost = duration * vehicle.costhr
        user = models.User.objects.filter(user_id=user_id).first()
        if user.wallet < cost:
            message = "Low customer balance"
            return response(400, message)
        booking = models.Booking(booking_id=booking_id, user_id=user_id, vehicle=vehicle, pick_location=pick_location, drop_location=drop_location, pick_time=pick_time, drop_time=drop_time, no_of_vehicle=1, cost=cost, charge=estimated_charge)
        booking.save()
        if vehicle_type == 0:
            pick_location.cars_available -= 1
        else:
            pick_location.bikes_available -= 1
        pick_location.save()
        vehicle.booking_status= True
        vehicle.save()
        data={"booking_i": booking_id}
        booking = models.Booking.objects.filter(booking_id=booking_id).first()
        return render(request, 'customer/booking_details.html',
        {'book_id' : booking})



def returnVehicle(request):
    if request.method == "POST":
        vehicle_id = request.POST.getlist('vehicle_id')[0]
        print(vehicle_id)
        user_id = request.session.get('user_id')
        if not user_id:
            message = "User is not logged in"
            return response(400, message)
        print("I am the vehicleid {}".format(vehicle_id))
        vehicle = models.Vehicle.objects.filter(vehicle_id=vehicle_id).first()
        if not vehicle:
            message = "Vehicle does not exist"
            return response(400, message)
        booking = models.Booking.objects.filter(vehicle_id=vehicle_id).first()
        if not vehicle.booking_status or not booking:
            message = "Vehicle is not booked"
            return response(400, message)
        vehicle.booking_status = 0  #working
        vehicle.location_id = booking.drop_location_id
        vehicle.charge =vehicle.charge - booking.charge
        location = models.Location.objects.filter(loc_id=booking.drop_location_id).first()
        if vehicle.vehicle_type == 0:
            location.cars_available += 1
        else:
            location.bikes_available += 1
        user = models.User.objects.filter(user_id=user_id).first()
        user.wallet=user.wallet-float(booking.cost)
        user.save()
        location.save()
        vehicle.save()
        return render(request, 'customer/Return.html')


def getBookingDetail(request):
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        user_id = request.session.get('user_id')
        if not user_id:
            message = "User is not logged in"
            return response(400, message)

        booking = models.Booking.objects.filter(booking_id=booking_id).first()
        if not booking:
            message = "Booking_id does not exist"
            return response(400, message)
        vehicle = models.Vehicle.objects.filter(vehicle_id=booking.vehicle_id).first()
        result = dict()
        result["vehicle_type"] = vehicle.vehicle_type
        result["vehicle_id"] = vehicle.vehicle_id
        result["charge"] = vehicle.charge
        result["pick_location"] = booking.pick_location_id
        result["drop_location"] = booking.drop_location_id
        result["duration"] = (booking.drop_time - booking.pick_time).total_seconds()/3600
        result["pick_time"] = datetime.strftime(booking.pick_time, "%Y/%m/%d %H:%M")
        result["drop_time"] = datetime.strftime(booking.drop_time, "%Y/%m/%d %H:%M")
        result["cost"] = booking.cost
        return response(200, "", [result])


def corp_booking_conf(request):
        return render(request, 'customer/corp_booking_conf.html')
