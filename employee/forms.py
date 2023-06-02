from django import forms
from customer.models import *

choices =(
	("3","Select"),
	("1", "E-Bike"),
    ("2", "E-Car"),
)


class ChoiceField(forms.Form):
	From = forms.ModelChoiceField(queryset=Location.objects.values_list("name",flat=True).distinct(),empty_label="Select")
	To = forms.ModelChoiceField(queryset=Location.objects.values_list("name",flat=True).distinct(),empty_label="Select")
	vehicle_type_to_move = forms.ChoiceField(choices =  choices)
	number_of_vehicles_to_move = forms.IntegerField(help_text = "Enter number of vehicles to move")