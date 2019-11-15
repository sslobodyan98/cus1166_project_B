
from app.models import Car
#importing table


def oil_change_calculation():

    difference = Car.update_miles - Car.mileage

    if difference < 5000:
        miles_until_next_oil_change = difference
        oil_change_required = False
        return miles_until_next_oil_change, oil_change_required #oil_change_required = FALSE

    elif difference >= 5000:
        miles_until_next_oil_change = 5000
        oil_change_required = True
        return miles_until_next_oil_change, oil_change_required #change_required = TRUE

    #adding update_miles to mileage AFTER USER DOES OIL CHANGE:
    mileage = Car.mileage + Car.update_miles
    return mileage
