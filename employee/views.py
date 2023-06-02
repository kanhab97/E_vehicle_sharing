from urllib import response
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from . import models
from django.shortcuts import redirect
from customer.models import Vehicle, Employee, Location
from django.http import HttpResponse
from django.template import loader
from django.views.generic.edit import CreateView
from .models import *
from .forms import *
from django.contrib import messages
# import mysql.connector as dbconnect

def index(request):
    return HttpResponse("Hello Employee")

def operatordashboard(request):
	return render(request, './employee/opdashboard.html')


def repair(request):
	Vec_List=Vehicle.objects.filter(repair_status=1)
	return render(request, './employee/repair.html', {'vec_List': Vec_List})

def recharge(request):
	NVec_List=Vehicle.objects.filter(charge__gte=40)
	CVec_List=Vehicle.objects.filter(charge__lte=40)
	return render(request, 'employee/recharge.html', {'nvec_List': NVec_List,'cvec_List': CVec_List})

def operator_login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:
            try:
                employee = Employee.objects.get(emp_id=username, job='operator')
            except:
                message = 'Employee does not exist'
                return render(request, './employee/operator_login.html', locals())

            if employee.password == password:
                request.session['type'] = 0
                request.session['is_login'] = True
                request.session['emp_id'] = employee.emp_id
                request.session['name'] = employee.name
                return redirect('/operator')
            else:
                message = 'Password not correct'
                return render(request, 'employee/operator_login.html', locals())
    return render(request, 'employee/operator_login.html')

def repairVehicle(request):
    if request.method == "POST":
        vecs = request.POST.getlist('chvec[]')
        if not vecs:
            return redirect('/repair/')
        else:
             print(len(vecs))
             for  i in vecs:
                 vehicle_id = i
                 vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
                 location = Location.objects.get(loc_id=vehicle.location_id)
                 vehicle.repair_status=0
                 vehicle.repair_desc=""
                 if vehicle.vehicle_type==True:
                     print(vehicle.vehicle_type)
                     location.bikes_available+=1
                 else:
                     location.cars_available+=1
                 vehicle.save()
                 location.save()
             return redirect('/repair/')
    return render(request,'./employee/repair.html')


def rechargeVehicle(request):
	if request.method == "POST":
		char = request.POST.getlist('charge')
		if not char:
			return redirect('/recharge/')
		else:
			for  i in char:
				vehicle_id = i
				vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
				vehicle.charge=100
				vehicle.save()
			return redirect('/recharge/')
	return render(request,'./employee/recharge.html')


em=''
pwd=''

def track(request):
    jb = 'operator'
    Vecid_List=Vehicle.objects.all()
    if request.method=="POST":
        vehicleid=request.POST.get("vehicleid")
        if vehicleid:
            c=Vehicle.objects.get(vehicle_id=vehicleid)
            status=c.booking_status
            type=c.vehicle_type
            locid = c.location_id
            loc = Location.objects.get(loc_id = locid)
            Name = loc.name
            Address = loc.address
            Pincode = loc.pincode
            context = {
                "Bstatus":status,
				"Name": Name,
                "Type": type,
				"Address": Address,
				"Pincode": Pincode,
				"vehicleid":vehicleid,
				'vec_List': Vecid_List,
                      }

            return render(request,'./employee/track.html',context=context)
    return render(request,'./employee/track.html',{'vec_List': Vecid_List})

def move(request):
    query_results = Location.objects.all()
    form_list = ChoiceField()
    context = {
         'form_list':form_list,
         'loc_List':query_results,
     	}
    if request.method == 'POST':
        from_list = request.POST['From']
        to_list = request.POST['To']
        print(from_list)
        print(to_list)
        vehicle_type_to_move = request.POST['vehicle_type_to_move']
        number_of_vehicles_to_move = int(request.POST['number_of_vehicles_to_move'])
        print(vehicle_type_to_move)
        print(number_of_vehicles_to_move)
        loc1 = Location.objects.raw("select loc_id from EVB.location where name='{}'".format(from_list))[0]
        loc2 = Location.objects.raw("select loc_id from EVB.location where name='{}'".format(to_list))[0]
        print(loc1)
        if loc1==loc2:
            messages.error(request,"Error! Same locations")
            return render(request,'./employee/move.html',context,locals())
        else:
            if vehicle_type_to_move == "1":
                vehicle_type_to_move = "1"
                from_available_vehicles = int(loc1.bikes_available)
                to_available_vehicles = int(loc2.bikes_available)
                print(from_available_vehicles,to_available_vehicles)
                if number_of_vehicles_to_move > from_available_vehicles:
                    #messages.error(request,"Error! Insufficient Vehicles")
                    return render(request,'./employee/move.html',context)
                else :
                    updated_from_available_vehicles = from_available_vehicles - number_of_vehicles_to_move
                    updated_to_available_vehicles = to_available_vehicles + number_of_vehicles_to_move
                    loc1.bikes_available = updated_from_available_vehicles
                    loc1.save()
                    loc2.bikes_available = updated_to_available_vehicles
                    loc2.save()
                    locid = loc1.loc_id
                    for i in range(0,number_of_vehicles_to_move):
                        vehicle = Vehicle.objects.filter(location = locid, vehicle_type = '1').first()
                        vehicle.location_id = loc2.loc_id
                        vehicle.save()
                        #target_vehicle = models.Vehicle.objects.get(location = locid).first()
                        #target_vehicle=models.Vehicle.objects.raw ("select vehicle_id from EVB11.Vehicle where location = '{}' and vehicle_type = 'bike'".format(locid))[0]
                        #target_vehicle.location_id = loc2.loc_id
                        #target_vehicle.save()
                        #messages.success(request,"Success! Vehicle has been moved")
                    return render(request,'./employee/move.html',context)
    				### change count of from table -x #####
    				### change count of to table +x #####
    				### Update vehicle/s location #####
            elif vehicle_type_to_move == '2':
                vehicle_type_to_move = 0
                from_available_vehicles = int(loc1.cars_available)
                to_available_vehicles = int(loc2.cars_available)
                if number_of_vehicles_to_move > from_available_vehicles:
                    messages.error(request, 'Error! Insufficient Vehicles')
                    return render(request,'./employee/move.html',context)
                else :
                    updated_from_available_vehicles = from_available_vehicles - number_of_vehicles_to_move
                    updated_to_available_vehicles = to_available_vehicles + number_of_vehicles_to_move
                    loc1.cars_available = updated_from_available_vehicles
                    loc1.save()
                    loc2.cars_available = updated_to_available_vehicles
                    loc2.save()
                    locid = loc1.loc_id
                    for i in range(0,number_of_vehicles_to_move):
                        # target_vehicle=Vehicle.objects.raw ("select vehicle_id from EVB1.Vehicle where location = '{}' and vehicle_type = 'car'".format(locid))[0]
                        # target_vehicle.location_id = loc2.loc_id
                        # target_vehicle.save()
                        vehicle = Vehicle.objects.filter(location = locid, vehicle_type = '0').first()
                        vehicle.location_id = loc2.loc_id
                        vehicle.save()
        				#target_vehicle = models.Vehicle.objects.filter(location = locid)
                        #messages.success(request,"Sucess! Vehicle has been moved")
                    return render(request,'./employee/move.html',context)
            else:
                message = 'Select a valid option'
                return render(request, './employee/move.html', context)
    return render(request,'./employee/move.html', context)

def logoutop(request):
    # if not request.session.get('is_login', None):
    #     if request.session.get('type'):
    #         return redirect("/operator_login/")
    # if request.session.get('type'):
    #     request.session.flush()
    #     return redirect("/operator_login/")
    request.session.flush()
    return redirect("/operator_login/")
