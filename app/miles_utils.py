'''
When user first adds a car and enters the initial number of miles on the car,
this value will be stored in 'mileage'

After that, when the user updates their car info and adds their new miles,
this value will be stored in 'update_miles'

We calculate the difference between the 'mileage' and 'update_miles'

If difference is less than 5000,
return 'miles_until_next_oil_change' (difference) and TRUE

Else, 'miles_until_next_oil_change' = 0
return 'miles_until_next_oil_change' and FALSE

Then add 'update_miles' to 'mileage' and store sum in 'mileage' AFTER USER DOES OIL CHANGE

'update_miles' is just a temporary variable used to calculate 'miles_until_next_oil_change'
'''
from app.models import Car
#importing table


def oil_change_calculation():

    difference = Car.update_miles - Car.mileage

    if difference < 5000:
        miles_until_next_oil_change = difference
        return miles_until_next_oil_change, False #oil_change_required = FALSE

    elif difference >= 5000:
        miles_until_next_oil_change = 5000 #or = 0 ?
        return miles_until_next_oil_change, True #oil_change_required = TRUE

    #adding update_miles to mileage AFTER USER DOES OIL CHANGE:
    mileage = Car.mileage + Car.update_miles
    return mileage