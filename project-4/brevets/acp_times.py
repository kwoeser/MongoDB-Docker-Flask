"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
from math import floor


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

"""
Opening Times
The controls at 60km, 120km, and 175km are each governed by a 34 km/hr maximum speed. 
60/34 = 1H46 
120/34 = 3H32 
175/34 = 5H09 
200/34 = 5H53

Note that we use a distance of 200km in the calculation,
even though the route was slightly longer than that (205km).

Closing Times
The minimum speed of 15 km/hr is used to determine the closing times. 
60/15 = 4H00 
120/15 = 8H00 
175/15 = 11H40

Control location (km)	Minimum Speed (km/hr)	Maximum Speed (km/hr)
      0 - 200	                  15	                     34
      200 - 400	               15	                     32
      400 - 600	               15	                     30
      600 - 1000	               11.428	               28
      1000 - 1300	               13.333	               26
"""

# start, end, min, max
speeds = [
    (0, 200, 15, 34),
    (200, 400, 15, 32),
    (400, 600, 15, 30),
    (600, 1000, 11.428, 28),
    (1000, 1300, 13.333, 26),
]

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    distance = control_dist_km
    time = 0
   
    # If distance is 0
    if distance == 0:
        return brevet_start_time

    # Special Case the last input/s
    if distance >= brevet_dist_km:
        distance = brevet_dist_km


    for min_distance, max_distance, min_speed, max_speed in speeds:
        # Calculate the time from the start to the checkpoint (converted to minutes)
        if min_distance < distance <= max_distance:
            time += ((distance - min_distance) / max_speed) * 60
            break
        # If the distance isn't in the current range 
        else:
            time += ((max_distance - min_distance) / max_speed) * 60
   
    return brevet_start_time.shift(minutes = round(time))

   


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    # Round at the start so there isn't too any floating point errors
    distance = round(control_dist_km)

    # Different time varibles needed due to the 200 and 400 edge cases
    current_time = 0
    overall_time = 0
    extra_time = 0
    
    # If negative
    if distance < 0:
        raise ValueError("Can't input Negative Numbers")

    # 0 Special Case
    if distance == 0:
        return brevet_start_time.shift(minutes=60)
        
    # Special Case the last input/s
    if distance >= brevet_dist_km:
        distance = brevet_dist_km
         
    # WEIRD EDGE CASES FOR 200 and 400 brevet dist; works fine if the brevet_dist is not 200 or 400 
    # if distance is 200 add 10 minutes
    if brevet_dist_km == 200 and distance == 200:
        overall_time += 10

    # if distance is 400 add 20 minutes
    if brevet_dist_km == 400 and distance == 400:
        overall_time += 20


    # Special Case for the first 60 km
    if distance < 60:
         mins = (distance / 20) + 1
         return brevet_start_time.shift(minutes = mins * 60)
         
    # Loop through each tuple in speeds to find the correct distance and speeds
    for min_distance, max_distance, min_speed, max_speed in speeds:
        if min_distance < distance <= max_distance:
            current_time = ((distance - floor(min_distance)) / min_speed) * 60
            overall_time += current_time
            break
        # If the distance isn't in the current range 
        else:
            extra_time = ((max_distance - floor(min_distance)) / min_speed) * 60
            overall_time += extra_time


    return brevet_start_time.shift(minutes = overall_time)

