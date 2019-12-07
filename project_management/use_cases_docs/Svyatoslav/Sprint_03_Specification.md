* ID:010:
	* Use-case: A user will be able to enter a vehicle registration date. If one is not provided, default will be date of Vehicle Added.
    	* Description: The program will increment the Inspection date by one year. If a vehicle is added before that time, it will assume you had your car inspected when adding a new car to your "fleet"
     	* Actor: Regular User
     	* Assigned to : Svyatoslav Slobodyan
     	* Refs: use-case_doc, issue (http://link_to_github_issue_item)

* ID:011:
	* Use-case: Google maps direction where the user can click on the map and it shows directions on how the user can reach the mechanic.
     	* Description: After the user schedules an appointment to a particular mechanic
     	* Actor: Regular User
     	* Assigned to : Mariyam
     	* Refs: use-case_doc, issue 

* ID:012: 
	* Use-case: Review Mechanic
     	* Description: The car owner will be sent a form a day after their appointment which will allows them to rate their mechanic and suggest any comments. The reviews will be displayed as well as the mechanics average rating. 
     	* Actor: Regular User
     	* Assigned to: Sarah Guthrie
     	* Refs: use-case_doc, issue (http://link_to_github_issue_item)

* ID:013: 
	* Use-case: Allowing the user to update the miles on their car, calculating when they will need their next oil change, and displaying info to user.
     	* Description: Adding update_miles field to Car table, created Oil Change form and routes, took update_miles out of Edit Vehicle form and routes, calculated miles until next oil change for user's car, added Oil Change tab to index.html, and created oil_change.html. This displays the mileage on user's car at their last oil change and allows user to update their current miles on their car, then displays if oil change is needed and in how many miles.
     	* Actor: Regular User
     	* Assigned to : Mary Garrity
     	* Refs: use-case_doc, issue (http://link_to_github_issue_item)

ID:014:
*Use-case: Delete Vehicle
    *Description: A user/car owner will be able to delete car information in the case
                           they no longer own the car.
    *Actor: Regular User
    *Assigned to: Farin Habib
    *Refs: use-case_doc, issue (http://link_to_github_issue_item)

* ID:015:
     * Use-Case: Mechanic Approve or Decline Schedules (Mechanics)
       * Description: Mechanics are able to approve or decline an appointment that the user makes with the mechanic. Once the appointment is made, status is initialized to 'PENDING' and after mechanic confirms and declines, it will update the database.
       * Actor: Regular User
       * Assigned to: Blessy
       * Refs: use-case doc, issue(http://link_to_github_issue_item/)

* ID:016:
	* Use-case: Message a Mechanic
     	* Description: Either send a message to a mechanic via email or text. For reference look into using Twilio and its API.
     	* Actor: Regular User
    	* Assigned to : Marry Kelly
     	* Refs: use-case_doc, issue (http://link_to_github_issue_item)