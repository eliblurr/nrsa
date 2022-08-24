from .data_upload_models import *

# ################################### IMPORTANT ######################################
"""
This query was optimized to retrieve all necessary table data with just one request from the Front-End.
Thus, the request requires one argument labelled as 'option' which must be a list/Array.

The array shall contain one character;['A'], representing one table  to be queried, two characters;['A', 'B']
for two tables, three characters;['A', 'B', 'C'], for three tables and so on up to a max of
twelve(12) characters/items in the list.

The return is a Dictionary/HashMap of {'char': data..... 'char(x)': data}.

The following are the 'char' representation of it's table;

'A' -> Changes_in_National_Traffic_Fatality_Indices
'B' -> Annual_Distribution_of_Fatalities_by_Road_Environment
'C' -> Annual_Distribution_of_Non_Urban_Fatalities_by_Road_User_Class
'D' -> Annual_Distribution_of_Urban_Fatalities_by_Road_User_Class
'E' -> Annual_Distribution_of_Fatalities_by_Age_Group
'F' -> Annual_Distribution_of_Fatalities_by_Sex
'G' -> Annual_Distribution_of_Casualties_by_Road_User_Class
'H' -> Annual_Distribution_of_Non_Urban_Casualties_by_Road_User_Class
'I' -> Annual_Distribution_of_Casualties_by_Age_Group
'J' -> Annual_Distribution_of_Casualties_by_Road_Environment
'K' -> Annual_Distribution_of_Casualties_by_Sex
'L' -> Vehicle_Type_Involved_in_Crashes
'M' -> National_Trends_in_Traffic_Crashes
'N' -> National_Trends_in_Traffic_Casualties
"""


######################################################################################


def change_in_fatality_indices():  # Table 1.1
    return list(Changes_in_National_Traffic_Fatality_Indices.objects.all().values())


def fatalities_by_road_env():  # Table 1.3.1
    return list(Annual_Distribution_of_Fatalities_by_Road_Environment.objects.all().values())


def non_urban_fatalities_by_vehicles():  # Table 1.3.4
    return list(Annual_Distribution_of_Non_Urban_Fatalities_by_Road_User_Class.objects.all().values())


def urban_fatalities_by_vehicles():  # Table 1.3.3
    return list(Annual_Distribution_of_Urban_Fatalities_by_Road_User_Class.objects.all().values())


def fatalities_by_age():  # Table 1.3.5
    return list(Annual_Distribution_of_Fatalities_by_Age_Group.objects.all().values())


def fatalities_by_sex():  # Table 1.3.6
    return list(Annual_Distribution_of_Fatalities_by_Sex.objects.all().values())


def casualties_by_vehicles():  # Table 1.4.1
    return list(Annual_Distribution_of_Casualties_by_Road_User_Class.objects.all().values())


def non_urban_casualties_by_vehicles():  # Table 1.4.3
    return list(Annual_Distribution_of_Non_Urban_Casualties_by_Road_User_Class.objects.all().values())


def casualties_by_age():  # Table 1.4.4
    return list(Annual_Distribution_of_Casualties_by_Age_Group.objects.all().values())


def casualties_by_road_env():  # Table 1.4.5
    return list(Annual_Distribution_of_Casualties_by_Road_Environment.objects.all().values())


def casualties_by_sex():  # Table 1.4.6
    return list(Annual_Distribution_of_Casualties_by_Sex.objects.all().values())


def vehicle_type_involved_in_crashes():  # Table 1.5
    return list(Vehicle_Type_Involved_in_Crashes.objects.all().values())


def trends_crashes():  # Table 1.2.1
    return list(National_Trends_in_Traffic_Crashes.objects.all().values())


def trends_casualties():  # Table 1.2.2
    return list(National_Trends_in_Traffic_Casualties.objects.all().values())


def selector(option):
    Data_got = {}
    selected = dict(
        A=False, B=False, C=False, D=False,
        E=False, F=False, G=False, H=False,
        I=False, J=False, K=False, L=False,
        M=False, N=False
    )
    if 'A' in option and not selected['A']:  # Table 1.1
        Data_got.update({'A': change_in_fatality_indices()})
        selected['A'] = True

    if 'B' in option and not selected['B']:  # Table 1.3.1
        Data_got.update({'B': fatalities_by_road_env()})
        selected['B'] = True

    if 'C' in option and not selected['C']:  # Table 1.3.4
        Data_got.update({'C': non_urban_fatalities_by_vehicles()})
        selected['C'] = True

    if 'D' in option and not selected['D']:  # Table 1.3.3
        Data_got.update({'D': urban_fatalities_by_vehicles()})
        selected['D'] = True

    if 'E' in option and not selected['E']:  # Table 1.3.5
        Data_got.update({'E': fatalities_by_age()})
        selected['E'] = True

    if 'F' in option and not selected['F']:  # Table 1.3.6
        Data_got.update({'F': fatalities_by_sex()})
        selected['F'] = True

    if 'G' in option and not selected['G']:  # Table 1.4.1
        Data_got.update({'G': casualties_by_vehicles()})
        selected['G'] = True

    if 'H' in option and not selected['H']:
        Data_got.update({'H': non_urban_casualties_by_vehicles()})
        selected['H'] = True
        logging.info("Data Unavailable")

    if 'I' in option and not selected['I']:
        Data_got.update({'I': casualties_by_age()})
        selected['I'] = True
        logging.info("Data Unavailable")

    if 'J' in option and not selected['J']:  # Table 1.4.5
        Data_got.update({'J': casualties_by_road_env()})
        selected['J'] = True

    if 'K' in option and not selected['K']:  # Table 1.4.6
        Data_got.update({'K': casualties_by_sex()})
        selected['K'] = True

    if 'L' in option and not selected['L']:  # Table 1.5
        Data_got.update({'L': vehicle_type_involved_in_crashes()})
        selected['L'] = True

    if 'M' in option and not selected['M']:  # Table 1.2.1
        Data_got.update({'M': trends_crashes()})
        selected['M'] = True

    if 'N' in option and not selected['N']:  # Table 1.2.2
        Data_got.update({'N': trends_casualties()})
        selected['N'] = True

    return Data_got