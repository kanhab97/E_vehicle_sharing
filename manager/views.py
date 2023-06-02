from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from customer import models
from json import dumps
from djqscsv import write_csv

def employee_download(request):
    qs = models.Employee.objects.values("name","address","job")
    with open('./Employee.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    return render(request, 'manager/vehicle_report_download.html')

def add_employee(request):
    if request.method == "POST":
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')
        emp_id = request.POST.get('emp_id')
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        job=request.POST.get('job')
        if phone_no and name.strip() and password and emp_id.strip() and address:
            if confirmPassword != password:
                message = 'Password does not match!!!'
                return render(request, 'manager/add_employee.html', locals())
            else:
                if models.Employee.objects.filter(emp_id=emp_id):
                    message = 'EMP_id already exists!'
                    return render(request, 'manager/add_employee.html', locals())
                if models.Employee.objects.filter(phone_no=phone_no):
                    message = 'Phone number has already been used ！'
                    return render(request, 'manager/add_employee.html', locals())
            new_emp = models.Employee(name=name, password=password, phone_no=phone_no, address=address, emp_id=emp_id, dob=dob, job=job)
            new_emp.save()
            message = 'Employee added!'
            return redirect('/add_employee/')
        else:
            return render(request, 'manager/add_employee.html')
    return render(request, 'manager/add_employee.html')

def add_vehicle(request):
    if request.method == "POST":
        vehicle_id = request.POST.get('vehicle_id')
        vehicle_type = request.POST.get('vehicle_type')
        print(type(vehicle_type))
        costhr = request.POST.get('costhr')
        charge = request.POST.get('charge')
        location = request.POST.get('location')
        if vehicle_id and location and costhr and charge:
            if models.Vehicle.objects.filter(vehicle_id=vehicle_id):
                message = 'vehicle_id already exists!'
                return render(request, 'manager/add_vehicle.html', locals())
            new_veh = models.Vehicle(vehicle_id=vehicle_id, vehicle_type=vehicle_type, costhr=costhr, charge=charge, location_id=location, booking_status=0, repair_status=0, repair_desc='NULL')
            new_veh.save()
            message = 'Vehicle added!'
            location1 = models.Location.objects.filter(loc_id=location).first()
            if vehicle_type == '0':
                location1.cars_available += 1
            else:
                location1.bikes_available += 1
            location1.save()
            return redirect('/add_vehicle/')
        else:
            return render(request, 'manager/add_vehicle.html')
    return render(request, 'manager/add_vehicle.html')



def employee_data(request):
    if request.method == "GET":
        data = list(models.Employee.objects.values())
        print(data)
        employee_data = {'data': data}
    return render(request, 'manager/employee_data.html', employee_data)

def user_download(request):
    qs = models.User.objects.values("name","address","dob","phone_no")
    with open('./User.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    return render(request, 'manager/vehicle_report_download.html')

def user_data(request):
    if request.method == "GET":
        data = list(models.User.objects.values())
        user_data = {'data': data}
    return render(request, 'manager/user_data.html', user_data)

def daily_reports(request):

    # vehicles at a particular location
    size = models.Vehicle.objects.values_list('location').distinct().count()
    location_list = []
    number_list = []

    for i in range(0,size):
        location = models.Vehicle.objects.values_list('location').distinct()[i][0]
        location_list.append(location)
        l_no = int(models.Vehicle.objects.filter(location=location).count())
        number_list.append(l_no)

    # cars and bikes available at particular location
    location_data = list(models.Location.objects.values())
    car_list = []
    bike_list =[]
    for location in location_data:
        car_ct = location['cars_available']
        bike_ct = location['bikes_available']
        car_list.append(car_ct)
        bike_list.append(bike_ct)
    print(car_list)
    print(bike_list)

    # vehicles picked at a particular location
    size1 = models.Booking.objects.values_list('pick_location').distinct().count()
    pick_up_location = []
    pick_up_list = []
    # print(request.POST.get())
    pick_start_date = request.POST.get('pick_start_date')
    pick_end_date = request.POST.get('pick_end_date')
    print(pick_start_date)
    print(pick_end_date)
    for i in range(0,size1):
        location = models.Booking.objects.values_list('pick_location').distinct()[i][0]
        print(location)
        pick_up_location.append(location)
        if pick_end_date != None and pick_end_date != '' and pick_start_date != None and pick_start_date != '':
            l_no = int(models.Booking.objects.filter(pick_location=location, pick_time__date__gte = pick_start_date, pick_time__date__lt = pick_end_date).count())
        else:
            l_no = int(models.Booking.objects.filter(pick_location=location).count())
        pick_up_list.append(l_no)

    # vehicles dropped at a particular location
    size1 = models.Booking.objects.values_list('drop_location').distinct().count()
    drop_location = []
    drop_list = []
    drop_start_date = request.POST.get('drop_start_date')
    drop_end_date = request.POST.get('drop_end_date')
    print(drop_start_date)
    print(drop_end_date)

    for i in range(0,size1):
        location = models.Booking.objects.values_list('drop_location').distinct()[i][0]
        drop_location.append(location)
        if drop_end_date != None and drop_end_date != '' and drop_start_date != None and drop_start_date != '':
            l_no = int(models.Booking.objects.filter(drop_location=location, drop_time__date__gte = drop_start_date, drop_time__date__lt = drop_end_date).count())
        else:
            l_no = int(models.Booking.objects.filter(drop_location=location).count())

        drop_list.append(l_no)

    context = {'location_list': dumps(location_list), 'number_list': dumps(number_list), 'car_list': dumps(car_list), 'bike_list': dumps(bike_list), 'pick_up_location': dumps(pick_up_location), 'pick_up_list': dumps(pick_up_list), 'drop_location': dumps(drop_location), 'drop_list': dumps(drop_list)}

    return render(request, 'manager/daily_report.html', context)

def vehicle_report_download(request):
    qs = models.Vehicle.objects.values("location","vehicle_id")
    with open('./Vehicle_Report.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    return render(request, 'manager/vehicle_report_download.html')

def car_bike_report_download(request):
    qs = models.Location.objects.values("loc_id","cars_available","bikes_available")
    with open('./Car_Bike_Report.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    return render(request, 'manager/vehicle_report_download.html')

def pick_up_report_download(request):
    qs = models.Booking.objects.values("pick_location_id","booking_id")
    with open('./Pick_Up_Report.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    return render(request, 'manager/vehicle_report_download.html')

def drop_report_download(request):
    qs = models.Booking.objects.values("drop_location_id","booking_id")
    with open('./Drop_Report.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    return render(request, 'manager/vehicle_report_download.html')

def manager_login(request):
    if request.session.get('is_login', None):
        return redirect('manager/manager_login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:
            try:
                emp = models.Employee.objects.get(emp_id=username, job="manager")
                print(emp)
            except:
                message = 'User does not exist！'
                return render(request, 'manager/manager_login.html', locals())

            if emp.password == password:
                request.session['job'] = "manager"
                request.session['is_login'] = True
                request.session['emp_id'] = emp.emp_id
                request.session['name'] = emp.name
                return redirect('/daily_report/')
            else:
                message = 'Password not correct！'
                return render(request, 'manager/manager_login.html', locals())
    return render(request, 'manager/manager_login.html')

def manager_logout(request):
    print(request.session.get('is_login'))
    if request.session.get('is_login', True):
        print("in if")
        if request.session.get('job'):
            print("Hello")
            request.session.flush()
            return render(request, 'manager/manager_login.html')
        else:
            return redirect("/daily_report/")
    else:
        return redirect("/daily_report/")
