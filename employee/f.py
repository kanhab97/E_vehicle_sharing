def move(request):
    query_results = Location.objects.all()
    form_list = ChoiceField()
    context = {
         'form_list':form_list
     	}
    if request.method == 'POST':
        from_list = request.POST['From']
        to_list = request.POST['To']
        vehicle_type_to_move = request.POST['vehicle_type_to_move']
        number_of_vehicles_to_move = int(request.POST['number_of_vehicles_to_move'])
        loc1 = Location.objects.raw("select loc_id from EVB.location where pincode='{}'".format(from_list))[0]
        loc2 = Location.objects.raw("select loc_id from EVB.location where pincode='{}'".format(to_list))[0]
        if loc1==loc2:
			messages.error(request,"Error! Both locations are same")
			return redirect(request,'./employee/move.html')
		else:
			if vehicle_type_to_move == 'Bike':
				vehicle_type_to_move = 1
				from_available_vehicles = int(loc1.bikes_available)
				to_available_vehicles = int(loc2.bikes_available)
				if number_of_vehicles_to_move > from_available_vehicles:
					messages.error(request,"Error! Insufficient Vehicles")
					return redirect(request,'./employee/move.html')   
				else :
					updated_from_available_vehicles = from_available_vehicles - number_of_vehicles_to_move
					updated_to_available_vehicles = to_available_vehicles + number_of_vehicles_to_move
					loc1.bikes_available = updated_from_available_vehicles
					loc1.save()
					loc2.bikes_available = updated_to_available_vehicles
					loc2.save()
					locid = loc1.loc_id
					for i in range(0,number_of_vehicles_to_move):
						#target_vehicle = models.Vehicle.objects.get(location = locid).first()
						#target_vehicle=models.Vehicle.objects.raw ("select vehicle_id from EVB1.Vehicle where location = '{}' and vehicle_type = 'bike'".format(locid))[0]
						#target_vehicle.location_id = loc2.loc_id
						#target_vehicle.save()
						vehicle = models.Vehicle.objects.filter(location = locid).first()
						vehicle.location_id = loc2.loc_id
						vehicle.save()

					messages.success(request,"Sucess! Vehicle has been moved")
					return redirect(request,'./employee/move.html')
					### change count of from table -x #####
					### change count of to table +x #####
					### Update vehicle/s location #####
			elif vehicle_type_to_move == 'car':
				vehicle_type_to_move = 0
				from_available_vehicles = int(loc1.cars_available)
				to_available_vehicles = int(loc2.cars_available)
				if number_of_vehicles_to_move > from_available_vehicles:
					messages.error(request, 'Error! Insufficient Vehicles')
					return redirect(request,'./employee/error.html')
				else :
					updated_from_available_vehicles = from_available_vehicles - number_of_vehicles_to_move
					updated_to_available_vehicles = to_available_vehicles + number_of_vehicles_to_move
					loc1.cars_available = updated_from_available_vehicles
					loc1.save()
					loc2.cars_available = updated_to_available_vehicles
					loc2.save()
					locid = loc1.loc_id
					for i in range(0,number_of_vehicles_to_move):
						#target_vehicle = models.Vehicle.objects.filter(location = locid)
						target_vehicle=models.Vehicle.objects.raw ("select vehicle_id from EVB.Vehicle where location = '{}' and vehicle_type = 'car'".format(locid))[0]
						target_vehicle.location = loc2.loc_id
						target_vehicle.save()
					messages.success(request,"Sucess! Vehicle has been moved")
					return redirect(request,'./employee/move.html')
    return render(request,'./employee/move.html', context)
