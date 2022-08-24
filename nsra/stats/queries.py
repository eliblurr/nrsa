from nsra.base.models import ReportedCase as Rc, Commercial as Com, Private as Priv, Cycle as Cyc
from nsra.base.models import Pedestrian as Ped, TotalKilled as Tot, Injured as Inj

from django.db.models import Sum

'''
years = set(Rc.objects.values_list('year', flat=True))

regions = set(Rc.objects.values_list('region', flat=True))

month_names = [
	"January", "February", "March", "April",
	"May", "June", "July", "August",
	"September", "October", "November", "December"
]


def Raw_Data(year, month, region):
	All_values = {}
	Rc_values = list(Rc.objects.filter(year=year, month=month, region=region).values(
		'serious', 'fatal', 'minor',
		'RC_total'
	))[0]
	All_values.update(Rc_values)

	Com_values = list(Com.objects.filter(year=year, month=month, region=region).values(
		'bus', 'minor_bus', 'truck',
		'taxi', 'other', 'Com_total'
	))[0]
	All_values.update(Com_values)

	Priv_values = list(Priv.objects.filter(year=year, month=month, region=region).values(
		'minibus', 'salon', 'suv',
		'govt', 'truck', 'Priv_total'
	))[0]
	All_values.update(Priv_values)

	Cyc_values = list(Cyc.objects.filter(year=year, month=month, region=region).values(
		'm_cycle', 'bicycles', 'handcart',
		'tricycle', 'Cyc_total'
	))[0]
	All_values.update(Cyc_values)

	Ped_values = list(Ped.objects.filter(year=year, month=month, region=region).values(
		'Ped_total'
	))[0]
	All_values.update(Ped_values)

	Inj_values = list(Inj.objects.filter(year=year, month=month, region=region).values(
		'injured'
	))[0]
	All_values.update(Inj_values)

	Tot_values = list(Tot.objects.filter(year=year, month=month, region=region).values(
		'male_over18', 'male_under18', 'female_over18',
		'female_under18', 'Tk_total'
	))[0]
	All_values.update(Tot_values)

	return All_values


def YYMMREG_Query(year):
	Month = {}
	for month in month_names:
		Region = {}
		for region in regions:
			All_values = Raw_Data(year, month, region)

			Region.update({f"{region}": All_values})

		Month.update({f"{month}": Region})

	return Month


def REGYYMM_Query(region):
	Year = {}
	for year in years:
		Month = {}
		for month in month_names:
			All_values = Raw_Data(year, month, region)

			month.update({f"{month}": All_values})

		Year.update({f"{Year}": Month})

	return Year


def National(date_from, date_to):
	National_values = {}

	RC = Rc.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("fatal"), Sum("serious"), Sum("minor"), Sum("RC_total"))
	National_values.update(RC)

	COM = Com.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("bus"), Sum("minor_bus"), Sum("truck"), Sum("taxi"), Sum("other"), Sum("Com_total"))
	National_values.update(COM)

	PRIV = Priv.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("minibus"), Sum("salon"), Sum("suv"), Sum("govt"), Sum("truck"), Sum("Priv_total"))
	National_values.update(PRIV)

	CYC = Cyc.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("m_cycle"), Sum("bicycles"), Sum("handcart"), Sum("tricycle"), Sum("Cyc_total"))
	National_values.update(CYC)

	PED = Ped.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("Ped_total"))
	National_values.update(PED)

	INJ = Inj.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("injured"))
	National_values.update(INJ)

	TOT = Tot.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("male_over18"), Sum("male_under18"), Sum("female_over18"), Sum("female_under18"), Sum("Tk_total"))
	National_values.update(TOT)

	logging.info(National_values)
	print(National_values , "National Values")

	return National_values


def National_Chart(date_from, date_to, specific: str):
	def RC():
		return Rc.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "RC_total")

	def COM():
		return Com.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "Com_total")

	def PRIV():
		return Priv.objects.filter(date__range=[date_from, date_to]).values(
			'month','region', "Priv_total")

	def CYC():
		return Cyc.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "Cyc_total")

	def PED():
		return Ped.objects.filter(date__range=[date_from, date_to]).values(
			'month','region', "Ped_total")

	def INJ():
		return Inj.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "injured")

	def TOT():
		return Tot.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "Tk_total")

	if specific == 'all':
		return [
			list(RC()), list(COM()),
			list(PRIV()), list(CYC()),
			list(PED()), list(INJ()),
			list(TOT())
		]
	else:
		if specific in ['rc', 'RC', 'Rc']:
			return list(RC())
		elif specific in ['COM', 'Com', 'com']:
			return list(COM())
		elif specific in ['Priv', 'PRIV', 'priv']:
			return list(PRIV())
		elif specific in ['CYC', 'Cyc', 'cyc']:
			return list(CYC())
		elif specific in ['PED', 'Ped', 'ped']:
			return list(PED())
		elif specific in ['TOTKILLED', 'TotKilled', 'totkilled', 'totalKilled']:
			return list(TOT())
		elif specific in ['INJ', 'Inj', 'inj']:
			return list(INJ())
		else:
			return None


def Regional(date_from, date_to, region):
	Regional_values = {}

	RC = Rc.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("fatal"), Sum("serious"), Sum("minor"), Sum("RC_total"))
	Regional_values.update(RC)

	COM = Com.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("bus"), Sum("minor_bus"), Sum("truck"), Sum("taxi"), Sum("other"), Sum("Com_total"))
	Regional_values.update(COM)

	PRIV = Priv.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("minibus"), Sum("salon"), Sum("suv"), Sum("govt"), Sum("truck"), Sum("Priv_total"))
	Regional_values.update(PRIV)

	CYC = Cyc.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("m_cycle"), Sum("bicycles"), Sum("handcart"), Sum("tricycle"), Sum("Cyc_total"))
	Regional_values.update(CYC)

	PED = Ped.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("Ped_total"))
	Regional_values.update(PED)

	INJ = Inj.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("injured"))
	Regional_values.update(INJ)

	TOT = Tot.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("male_over18"), Sum("male_under18"), Sum("female_over18"), Sum("female_under18"), Sum("Tk_total"))
	Regional_values.update(TOT)

	return Regional_values


def Categorical(date_from, date_to, category: str, region: str):
	def rc():
		return Rc.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'fatal', 'serious', 'minor', 'RC_total'
		)

	def com():
		return Com.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'bus', 'minor_bus', 'truck', 'taxi',
			'other', 'injured', 'killed', 'Com_total'
		)

	def priv():
		return Priv.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'minibus', 'salon', 'suv', 'govt',
			'truck', 'injured', 'killed', 'Priv_total'
		)

	def cyc():
		return Cyc.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'm_cycle', 'bicycles', 'handcart',
			'tricycle', 'injured', 'killed', 'Cyc_total'
		)

	def ped():
		return Ped.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'injured', 'killed', 'Ped_total'
		)

	def tot():
		return Tot.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'male_over18', 'male_under18', 'female_over18',
			'female_under18', 'injured', 'killed', 'Tk_total'
		)

	def inj():
		return Inj.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'injured'
		)

	if region == 'ghana':
		if category in ['rc', 'RC', 'Rc']:
			return list(rc())
		elif category in ['COM', 'Com', 'com']:
			return list(com())
		elif category in ['Priv', 'PRIV', 'priv']:
			return list(priv())
		elif category in ['CYC', 'Cyc', 'cyc']:
			return list(cyc())
		elif category in ['PED', 'Ped', 'ped']:
			return list(ped())
		elif category in ['TOTKILLED', 'TotKilled', 'totkilled', 'totalKilled']:
			return list(tot())
		elif category in ['INJ', 'Inj', 'inj']:
			return list(inj())
		else:
			return None
	else:
		if category in ['rc', 'RC', 'Rc']:
			return list(rc().filter(region=region))
		elif category in ['COM', 'Com', 'com']:
			return list(com().filter(region=region))
		elif category in ['Priv', 'PRIV', 'priv']:
			return list(priv().filter(region=region))
		elif category in ['CYC', 'Cyc', 'cyc']:
			return list(cyc().filter(region=region))
		elif category in ['PED', 'Ped', 'ped']:
			return list(ped().filter(region=region))
		elif category in ['TOTKILLED', 'TotKilled', 'totkilled', 'totalKilled']:
			return list(tot().filter(region=region))
		elif category in ['INJ', 'Inj', 'inj']:
			return list(inj().filter(region=region))
		else:
			return None
'''

def get_years():
    return set(Rc.objects.values_list('year', flat=True))

def get_region():
    return set(Rc.objects.values_list('region', flat=True))

# years = set(Rc.objects.values_list('year', flat=True))

# regions = set(Rc.objects.values_list('region', flat=True))

month_names = [
	"January", "February", "March", "April",
	"May", "June", "July", "August",
	"September", "October", "November", "December"
]


def Raw_Data(year, month, region):
	All_values = {}
	Rc_values = list(Rc.objects.filter(year=year, month=month, region=region).values(
		'serious', 'fatal', 'minor',
		'RC_total'
	))[0]
	All_values.update(Rc_values)

	Com_values = list(Com.objects.filter(year=year, month=month, region=region).values(
		'bus', 'minor_bus', 'truck',
		'taxi', 'other', 'Com_total'
	))[0]
	All_values.update(Com_values)

	Priv_values = list(Priv.objects.filter(year=year, month=month, region=region).values(
		'minibus', 'salon', 'suv',
		'govt', 'truck', 'Priv_total'
	))[0]
	All_values.update(Priv_values)

	Cyc_values = list(Cyc.objects.filter(year=year, month=month, region=region).values(
		'm_cycle', 'bicycles', 'handcart',
		'tricycle', 'Cyc_total'
	))[0]
	All_values.update(Cyc_values)

	Ped_values = list(Ped.objects.filter(year=year, month=month, region=region).values(
		'Ped_total'
	))[0]
	All_values.update(Ped_values)

	Inj_values = list(Inj.objects.filter(year=year, month=month, region=region).values(
		'injured'
	))[0]
	All_values.update(Inj_values)

	Tot_values = list(Tot.objects.filter(year=year, month=month, region=region).values(
		'male_over18', 'male_under18', 'female_over18',
		'female_under18', 'Tk_total'
	))[0]
	All_values.update(Tot_values)

	return All_values


def YYMMREG_Query(year):
	Month = {}
	for month in month_names:
		Region = {}
		for region in get_region():
			All_values = Raw_Data(year, month, region)

			Region.update({f"{region}": All_values})

		Month.update({f"{month}": Region})

	return Month


def REGYYMM_Query(region):
	Year = {}
	for year in get_years():
		Month = {}
		for month in month_names:
			All_values = Raw_Data(year, month, region)

			month.update({f"{month}": All_values})

		Year.update({f"{Year}": Month})

	return Year


def National(date_from, date_to):
	National_values = {}

	RC = Rc.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("fatal"), Sum("serious"), Sum("minor"), Sum("RC_total"))
	National_values.update(RC)

	COM = Com.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("bus"), Sum("minor_bus"), Sum("truck"), Sum("taxi"), Sum("other"), Sum("Com_total"))
	National_values.update(COM)

	PRIV = Priv.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("minibus"), Sum("salon"), Sum("suv"), Sum("govt"), Sum("truck"), Sum("Priv_total"))
	National_values.update(PRIV)

	CYC = Cyc.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("m_cycle"), Sum("bicycles"), Sum("handcart"), Sum("tricycle"), Sum("Cyc_total"))
	National_values.update(CYC)

	PED = Ped.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("Ped_total"))
	National_values.update(PED)

	INJ = Inj.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("injured"))

# years = set(Rc.objects.values_list('year', flat=True))

# regions = set(Rc.objects.values_list('region', flat=True))

# month_names = [
# 	"January", "February", "March", "April",
# 	"May", "June", "July", "August",
# 	"September", "October", "November", "December"
# ]


def Raw_Data(year, month, region):
	All_values = {}
	Rc_values = list(Rc.objects.filter(year=year, month=month, region=region).values(
		'serious', 'fatal', 'minor',
		'RC_total'
	))[0]
	All_values.update(Rc_values)

	Com_values = list(Com.objects.filter(year=year, month=month, region=region).values(
		'bus', 'minor_bus', 'truck',
		'taxi', 'other', 'Com_total'
	))[0]
	All_values.update(Com_values)

	Priv_values = list(Priv.objects.filter(year=year, month=month, region=region).values(
		'minibus', 'salon', 'suv',
		'govt', 'truck', 'Priv_total'
	))[0]
	All_values.update(Priv_values)

	Cyc_values = list(Cyc.objects.filter(year=year, month=month, region=region).values(
		'm_cycle', 'bicycles', 'handcart',
		'tricycle', 'Cyc_total'
	))[0]
	All_values.update(Cyc_values)

	Ped_values = list(Ped.objects.filter(year=year, month=month, region=region).values(
		'Ped_total'
	))[0]
	All_values.update(Ped_values)

	Inj_values = list(Inj.objects.filter(year=year, month=month, region=region).values(
		'injured'
	))[0]
	All_values.update(Inj_values)

	Tot_values = list(Tot.objects.filter(year=year, month=month, region=region).values(
		'male_over18', 'male_under18', 'female_over18',
		'female_under18', 'Tk_total'
	))[0]
	All_values.update(Tot_values)

	return All_values


def YYMMREG_Query(year):
	Month = {}
	for month in month_names:
		Region = {}
		for region in get_region():
			All_values = Raw_Data(year, month, region)

			Region.update({f"{region}": All_values})

		Month.update({f"{month}": Region})

	return Month


def REGYYMM_Query(region):
	Year = {}
	for year in get_years():
		Month = {}
		for month in month_names:
			All_values = Raw_Data(year, month, region)

			month.update({f"{month}": All_values})

		Year.update({f"{Year}": Month})

	return Year


def National(date_from, date_to):
	National_values = {}

	RC = Rc.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("fatal"), Sum("serious"), Sum("minor"), Sum("RC_total"))
	National_values.update(RC)

	COM = Com.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("bus"), Sum("minor_bus"), Sum("truck"), Sum("taxi"), Sum("other"), Sum("Com_total"))
	National_values.update(COM)

	PRIV = Priv.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("minibus"), Sum("salon"), Sum("suv"), Sum("govt"), Sum("truck"), Sum("Priv_total"))
	National_values.update(PRIV)

	CYC = Cyc.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("m_cycle"), Sum("bicycles"), Sum("handcart"), Sum("tricycle"), Sum("Cyc_total"))
	National_values.update(CYC)

	PED = Ped.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("Ped_total"))
	National_values.update(PED)

	INJ = Inj.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("injured"))
	National_values.update(INJ)

	TOT = Tot.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("male_over18"), Sum("male_under18"), Sum("female_over18"), Sum("female_under18"), Sum("Tk_total"))
	National_values.update(TOT)

	return National_values


def National_Chart(date_from, date_to, specific: str):
	def RC():
		return Rc.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "RC_total")

	def COM():
		return Com.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "Com_total")

	def PRIV():
		return Priv.objects.filter(date__range=[date_from, date_to]).values(
			'month','region', "Priv_total")

	def CYC():
		return Cyc.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "Cyc_total")

	def PED():
		return Ped.objects.filter(date__range=[date_from, date_to]).values(
			'month','region', "Ped_total")

	def INJ():
		return Inj.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "injured")

	def TOT():
		return Tot.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "Tk_total")

	if specific == 'all':
		return [
			list(RC()), list(COM()),
			list(PRIV()), list(CYC()),
			list(PED()), list(INJ()),
			list(TOT())
		]
	else:
		if specific in ['rc', 'RC', 'Rc']:
			return list(RC())
		elif specific in ['COM', 'Com', 'com']:
			return list(COM())
		elif specific in ['Priv', 'PRIV', 'priv']:
			return list(PRIV())
		elif specific in ['CYC', 'Cyc', 'cyc']:
			return list(CYC())
		elif specific in ['PED', 'Ped', 'ped']:
			return list(PED())
		elif specific in ['TOTKILLED', 'TotKilled', 'totkilled', 'totalKilled']:
			return list(TOT())
		elif specific in ['INJ', 'Inj', 'inj']:
			return list(INJ())
		else:
			return None


def Regional(date_from, date_to, region):
	Regional_values = {}

	RC = Rc.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("fatal"), Sum("serious"), Sum("minor"), Sum("RC_total"))
	Regional_values.update(RC)

	COM = Com.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("bus"), Sum("minor_bus"), Sum("truck"), Sum("taxi"), Sum("other"), Sum("Com_total"))
	Regional_values.update(COM)

	PRIV = Priv.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("minibus"), Sum("salon"), Sum("suv"), Sum("govt"), Sum("truck"), Sum("Priv_total"))
	Regional_values.update(PRIV)

	CYC = Cyc.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("m_cycle"), Sum("bicycles"), Sum("handcart"), Sum("tricycle"), Sum("Cyc_total"))
	Regional_values.update(CYC)

	PED = Ped.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("Ped_total"))
	Regional_values.update(PED)

	INJ = Inj.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("injured"))
	Regional_values.update(INJ)

	TOT = Tot.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("male_over18"), Sum("male_under18"), Sum("female_over18"), Sum("female_under18"), Sum("Tk_total"))
	Regional_values.update(TOT)

	return Regional_values


def Categorical(date_from, date_to, category: str, region: str):
	def rc():
		return Rc.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'fatal', 'serious', 'minor', 'RC_total'
		)

	def com():
		return Com.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'bus', 'minor_bus', 'truck', 'taxi',
			'other', 'injured', 'killed', 'Com_total'
		)

	def priv():
		return Priv.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'minibus', 'salon', 'suv', 'govt',
			'truck', 'injured', 'killed', 'Priv_total'
		)

	def cyc():
		return Cyc.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'm_cycle', 'bicycles', 'handcart',
			'tricycle', 'injured', 'killed', 'Cyc_total'
		)

	def ped():
		return Ped.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'injured', 'killed', 'Ped_total'
		)

	def tot():
		return Tot.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'male_over18', 'male_under18', 'female_over18',
			'female_under18', 'injured', 'killed', 'Tk_total'
		)

	def inj():
		return Inj.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'injured'
		)

	if region == 'ghana':
		if category in ['rc', 'RC', 'Rc']:
			return list(rc())
		elif category in ['COM', 'Com', 'com']:
			return list(com())
		elif category in ['Priv', 'PRIV', 'priv']:
			return list(priv())
		elif category in ['CYC', 'Cyc', 'cyc']:
			return list(cyc())
		elif category in ['PED', 'Ped', 'ped']:
			return list(ped())
		elif category in ['TOTKILLED', 'TotKilled', 'totkilled', 'totalKilled']:
			return list(tot())
		elif category in ['INJ', 'Inj', 'inj']:
			return list(inj())
		else:
			return None
	else:
		if category in ['rc', 'RC', 'Rc']:
			return list(rc().filter(region=region))
		elif category in ['COM', 'Com', 'com']:
			return list(com().filter(region=region))
		elif category in ['Priv', 'PRIV', 'priv']:
			return list(priv().filter(region=region))
		elif category in ['CYC', 'Cyc', 'cyc']:
			return list(cyc().filter(region=region))
		elif category in ['PED', 'Ped', 'ped']:
			return list(ped().filter(region=region))
		elif category in ['TOTKILLED', 'TotKilled', 'totkilled', 'totalKilled']:
			return list(tot().filter(region=region))
		elif category in ['INJ', 'Inj', 'inj']:
			return list(inj().filter(region=region))
		else:
			return None

	National_values.update(INJ)

	TOT = Tot.objects.filter(date__range=[date_from, date_to]).aggregate(
		Sum("male_over18"), Sum("male_under18"), Sum("female_over18"), Sum("female_under18"), Sum("Tk_total"))
	National_values.update(TOT)

	return National_values


def National_Chart(date_from, date_to, specific: str):
	def RC():
		return Rc.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "RC_total")

	def COM():
		return Com.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "Com_total")

	def PRIV():
		return Priv.objects.filter(date__range=[date_from, date_to]).values(
			'month','region', "Priv_total")

	def CYC():
		return Cyc.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "Cyc_total")

	def PED():
		return Ped.objects.filter(date__range=[date_from, date_to]).values(
			'month','region', "Ped_total")

	def INJ():
		return Inj.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "injured")

	def TOT():
		return Tot.objects.filter(date__range=[date_from, date_to]).values(
			'month', 'region', "Tk_total")

	if specific == 'all':
		return [
			list(RC()), list(COM()),
			list(PRIV()), list(CYC()),
			list(PED()), list(INJ()),
			list(TOT())
		]
	else:
		if specific in ['rc', 'RC', 'Rc']:
			return list(RC())
		elif specific in ['COM', 'Com', 'com']:
			return list(COM())
		elif specific in ['Priv', 'PRIV', 'priv']:
			return list(PRIV())
		elif specific in ['CYC', 'Cyc', 'cyc']:
			return list(CYC())
		elif specific in ['PED', 'Ped', 'ped']:
			return list(PED())
		elif specific in ['TOTKILLED', 'TotKilled', 'totkilled', 'totalKilled']:
			return list(TOT())
		elif specific in ['INJ', 'Inj', 'inj']:
			return list(INJ())
		else:
			return None


def Regional(date_from, date_to, region):
	Regional_values = {}

	RC = Rc.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("fatal"), Sum("serious"), Sum("minor"), Sum("RC_total"))
	Regional_values.update(RC)

	COM = Com.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("bus"), Sum("minor_bus"), Sum("truck"), Sum("taxi"), Sum("other"), Sum("Com_total"))
	Regional_values.update(COM)

	PRIV = Priv.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("minibus"), Sum("salon"), Sum("suv"), Sum("govt"), Sum("truck"), Sum("Priv_total"))
	Regional_values.update(PRIV)

	CYC = Cyc.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("m_cycle"), Sum("bicycles"), Sum("handcart"), Sum("tricycle"), Sum("Cyc_total"))
	Regional_values.update(CYC)

	PED = Ped.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("Ped_total"))
	Regional_values.update(PED)

	INJ = Inj.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("injured"))
	Regional_values.update(INJ)

	TOT = Tot.objects.filter(date__range=[date_from, date_to], region=region).aggregate(
		Sum("male_over18"), Sum("male_under18"), Sum("female_over18"), Sum("female_under18"), Sum("Tk_total"))
	Regional_values.update(TOT)

	return Regional_values


def Categorical(date_from, date_to, category: str, region: str):
	def rc():
		return Rc.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'fatal', 'serious', 'minor', 'RC_total'
		)

	def com():
		return Com.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'bus', 'minor_bus', 'truck', 'taxi',
			'other', 'injured', 'killed', 'Com_total'
		)

	def priv():
		return Priv.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'minibus', 'salon', 'suv', 'govt',
			'truck', 'injured', 'killed', 'Priv_total'
		)

	def cyc():
		return Cyc.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'm_cycle', 'bicycles', 'handcart',
			'tricycle', 'injured', 'killed', 'Cyc_total'
		)

	def ped():
		return Ped.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'injured', 'killed', 'Ped_total'
		)

	def tot():
		return Tot.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'male_over18', 'male_under18', 'female_over18',
			'female_under18', 'injured', 'killed', 'Tk_total'
		)

	def inj():
		return Inj.objects.filter(date__range=[date_from, date_to]).values(
			'region', 'month', 'injured'
		)

	if region == 'ghana':
		if category in ['rc', 'RC', 'Rc']:
			return list(rc())
		elif category in ['COM', 'Com', 'com']:
			return list(com())
		elif category in ['Priv', 'PRIV', 'priv']:
			return list(priv())
		elif category in ['CYC', 'Cyc', 'cyc']:
			return list(cyc())
		elif category in ['PED', 'Ped', 'ped']:
			return list(ped())
		elif category in ['TOTKILLED', 'TotKilled', 'totkilled', 'totalKilled']:
			return list(tot())
		elif category in ['INJ', 'Inj', 'inj']:
			return list(inj())
		else:
			return None
	else:
		if category in ['rc', 'RC', 'Rc']:
			return list(rc().filter(region=region))
		elif category in ['COM', 'Com', 'com']:
			return list(com().filter(region=region))
		elif category in ['Priv', 'PRIV', 'priv']:
			return list(priv().filter(region=region))
		elif category in ['CYC', 'Cyc', 'cyc']:
			return list(cyc().filter(region=region))
		elif category in ['PED', 'Ped', 'ped']:
			return list(ped().filter(region=region))
		elif category in ['TOTKILLED', 'TotKilled', 'totkilled', 'totalKilled']:
			return list(tot().filter(region=region))
		elif category in ['INJ', 'Inj', 'inj']:
			return list(inj().filter(region=region))
		else:
			return None