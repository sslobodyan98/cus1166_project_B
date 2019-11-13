from app.vininfo import *

def main():
	vin = 'SHSRD78816U437443'
	#2006 Honda CR-V
	info = getVehicleInfo(vin)
	print(getYear(info))
	print(getModel(info))
	print(getMake(info))


main()