from django.db import models
from django.db.models import F

import logging


class AnnotationManager(models.Manager):

	def __init__(self, **kwargs):
		super().__init__()
		self.annotations = kwargs

	def get_queryset(self):
		return super().get_queryset().annotate(**self.annotations)


# Create your models here.
class Vehicles(models.Model):
	year = models.IntegerField()
	Ped = models.IntegerField()
	Car = models.IntegerField()
	HGV_LGV = models.IntegerField()
	Bus_and_Bus_Mini = models.IntegerField()
	M_cycle_Tricycle_and_Rickshaw = models.IntegerField()
	Pick_Up = models.IntegerField()
	Cycle = models.IntegerField()
	Other = models.IntegerField()
	Total = None

	objects = AnnotationManager(
		Total=F('Ped') + F('Car') + F('HGV_LGV')
			  + F('Bus_and_Bus_Mini')
			  + F('M_cycle_Tricycle_and_Rickshaw')
			  + F('Pick_Up')
			  + F('Cycle') + F('Other')
	)

	SearchableFields = ['year']

	class Meta:
		abstract = True


class AgeGroups(models.Model):
	year = models.IntegerField()
	Ages_0_to_5 = models.IntegerField()
	Ages_6_to_15 = models.IntegerField()
	Ages_16_to_25 = models.IntegerField()
	Ages_28_to_35 = models.IntegerField()
	Ages_36_to_45 = models.IntegerField()
	Ages_46_to_55 = models.IntegerField()
	Ages_58_to_65 = models.IntegerField()
	Ages_Over_65 = models.IntegerField()
	Total = None

	objects = AnnotationManager(
		Total=F('Ages_0_to_5') + F('Ages_6_to_15') + F('Ages_16_to_25')
			  + F('Ages_28_to_35') + F('Ages_36_to_45') + F('Ages_46_to_55')
			  + F('Ages_58_to_65') + F('Ages_Over_65')
	)

	SearchableFields = ['year']

	class Meta:
		abstract = True


class RoadEnvironment(models.Model):
	year = models.IntegerField()
	urban = models.IntegerField()
	non_urban = models.IntegerField()
	Total = None

	objects = AnnotationManager(Total=F('urban') + F('non_urban'))

	SearchableFields = ['year']

	class Meta:
		abstract = True


class Sex(models.Model):
	year = models.IntegerField()
	Male = models.IntegerField()
	Female = models.IntegerField()
	Total = None

	objects = AnnotationManager(Total=F('Male') + F('Female'))

	SearchableFields = ['year']

	class Meta:
		abstract = True


class Changes_in_National_Traffic_Fatality_Indices(models.Model):  # Table 1.1
	year = models.IntegerField()
	all_crashes = models.IntegerField()
	all_casualties = models.IntegerField()
	fatalities = models.IntegerField()
	estimated_population = models.IntegerField()
	registered_vehicles = models.IntegerField()
	fatalities_per_10k_vehicles = models.FloatField()
	fatalities_per_100k_population = models.FloatField()
	fatalities_per_100_casualties = models.FloatField()
	fatalities_per_100_crashes = models.FloatField()

	def __str__(self):
		return f'{self.year} National Traffic Fatality Indices'


class National_Trends_in_Traffic_Crashes(models.Model):  # Table 1.2.1
	year = models.IntegerField()
	all_crashes = models.IntegerField()
	fatal_crashes = models.IntegerField()
	injury_crashes = models.IntegerField()
	damage_only = models.IntegerField()

	def __str__(self):
		return f'{self.year} National Trends in Traffic Crashes'


class National_Trends_in_Traffic_Casualties(models.Model):  # Table 1.2.2
	year = models.IntegerField()
	all_casualties = models.IntegerField()
	killed = models.IntegerField()
	seriously_injured = models.IntegerField()
	slightly_injured = models.IntegerField()

	def __str__(self):
		return f'{self.year} National Trends in Traffic Casualties'


class Annual_Distribution_of_Fatalities_by_Road_Environment(RoadEnvironment):  # Table 1.3.1

	def __str__(self):
		return f"{self.year} Annual Distribution of Fatalities by Road Environment"


class Annual_Distribution_of_Non_Urban_Fatalities_by_Road_User_Class(Vehicles):  # Table 1.3.4
	def __str__(self):
		return f"{self.year} Annual Distribution of Non UrbanFatalities by Road User Class"


class Annual_Distribution_of_Urban_Fatalities_by_Road_User_Class(Vehicles):  # Table 1.3.3
	def __str__(self):
		return f"{self.year} Annual Distribution of Urban Fatalities by Road User Class"


class Annual_Distribution_of_Fatalities_by_Age_Group(AgeGroups):  # Table 1.3.5
	def __str__(self):
		return f"{self.year} Annual Distribution of Fatalities by Age Group"


class Annual_Distribution_of_Fatalities_by_Sex(Sex):  # Table 1.3.6
	def __str__(self):
		return f"{self.year} Annual Distribution of Fatalities by Sex"


class Annual_Distribution_of_Casualties_by_Road_User_Class(Vehicles):  # Table 1.4.1
	def __str__(self):
		return f"{self.year} Annual Distribution of Casualties by Road User Class"


class Annual_Distribution_of_Urban_Casualties_by_Road_User_Class(Vehicles):  # Table 1.4.2
	def __sttimer__(self):
		return f"{self.year} Annual Distribution of Urban Casualties by Road User Class"


class Annual_Distribution_of_Non_Urban_Casualties_by_Road_User_Class(Vehicles):  # Table 1.4.3
	def __str__(self):
		return f"{self.year} Annual Distribution of Non-Urban Casualties by Road User Class"


class Annual_Distribution_of_Casualties_by_Age_Group(AgeGroups):  # Table 1.4.4
	def __str__(self):
		return f"{self.year} Annual Distribution of Casualties by Age Group"


class Annual_Distribution_of_Casualties_by_Road_Environment(RoadEnvironment):  # Table 1.4.5
	def __str__(self):
		return f"{self.year} Annual Distribution of Casualties Road Environment"


class Annual_Distribution_of_Casualties_by_Sex(Sex):  # Table 1.4.6
	def __str__(self):
		return f"{self.year} Annual Distribution of Casualties by Sex"


class Vehicle_Type_Involved_in_Crashes(models.Model):  # Table 1.5
	year = models.IntegerField()
	Car = models.IntegerField()
	HGV_LGV = models.IntegerField()
	Bus_and_Bus_Mini = models.IntegerField()
	M_cycle_Tricycle_and_Rickshaw = models.IntegerField()
	Pick_Up = models.IntegerField()
	Cycle = models.IntegerField()
	Other = models.IntegerField()
	Total = None

	objects = AnnotationManager(
		Total=F('Car') + F('HGV_LGV')
			  + F('HGV_LGV') + F('Bus_and_Bus_Mini')
			  + F('M_cycle_Tricycle_and_Rickshaw') + F('Pick_Up')
			  + F('Cycle') + F('Other')
	)

	SearchableFields = ['year']

	def __str__(self):
		return f"{self.year} Vehicle Type Involved in Crashes"