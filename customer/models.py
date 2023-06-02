from django.db import models


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    dob = models.DateField()
    phone_no = models.CharField(max_length=20)
    user_type = models.BooleanField()
    wallet = models.FloatField(default=0)

    class Meta:
        db_table = 'user'


class Location(models.Model):
    loc_id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    cars_available = models.IntegerField(blank=True, null=True)
    bikes_available = models.IntegerField(blank=True, null=True)
    phone_no = models.CharField(max_length=20)

    class Meta:
        db_table = 'location'


class Vehicle(models.Model):
    vehicle_id = models.CharField(primary_key=True, max_length=100)
    vehicle_type = models.BooleanField()
    booking_status = models.BooleanField(default=False)
    location = models.ForeignKey(Location,models.SET_NULL, null=True,db_column="location")
    repair_status = models.BooleanField(default=False)
    repair_desc = models.CharField(max_length=100, blank=True, null=True)
    costhr = models.FloatField()
    charge = models.FloatField()

    class Meta:
        db_table = 'vehicle'


class Booking(models.Model):
    booking_id = models.CharField(primary_key=True, max_length=100)
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    vehicle = models.ForeignKey(Vehicle, models.SET_NULL, null=True)
    pick_location = models.ForeignKey(Location, models.SET_NULL, related_name='pick', null=True)
    drop_location = models.ForeignKey(Location, models.SET_NULL, related_name='drop', null=True)
    pick_time = models.DateTimeField()
    drop_time = models.DateTimeField()
    cost = models.FloatField()
    no_of_vehicle = models.IntegerField()
    charge = models.IntegerField()

    class Meta:
        db_table = 'booking'


class Employee(models.Model):
    emp_id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    job = models.CharField(max_length=20)
    dob = models.DateField()
    phone_no = models.CharField(max_length=20)

    class Meta:
        db_table = 'employee'


class Payment(models.Model):
    billing_id = models.CharField(primary_key=True, max_length=100)
    booking = models.ForeignKey(Booking, models.SET_NULL, null=True)
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=20)
    amount = models.IntegerField(blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'payment'
