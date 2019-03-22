from skyfield.api import load, EarthSatellite, Topos,utc
from datetime import timezone, timedelta, datetime ,date
from pytz import timezone
from numpy import diff,reshape,put,delete,concatenate
import matplotlib.pyplot as plt 
maldives = timezone('Indian/Maldives')


SAVE_DIR= "images/"


def plot_sky(pass_indices,t,az,alt):
    i, j = pass_indices


    
    # Set up the polar plot.
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    ax.set_rlim([0, 90])
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    
    # Draw line and labels..
    θ = az.radians
    r = 90 - alt.degrees
    ax.plot(θ[i:j], r[i:j], 'ro--')
    

    for k in range(i,j):
        text = t[k].astimezone(maldives).strftime('%H:%M')
        ax.text(θ[k], r[k], text, ha='left', va='bottom')


    name = SAVE_DIR + "plot_" + str(t[i].astimezone(maldives)) + ".png" 
  
    plt.savefig(name)



    return name








def get_passes(start,end,cords,dt):



    stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
    satellites = load.tle(stations_url)
    satellite = satellites['ISS (ZARYA)']

    #get values for time,we only search for times in which passes would be visible morning and dusk
    #this is due to the sunsbrightness and lackof light to be reflected
    minutes1 = range(240,1440) # 4 to 7
    minutes2 = range(1050,1170) # 1530 to 1930

    minutes = minutes1 #+ list(minutes2)

    minutes = range(start,end)
    ts = load.timescale()
    t = ts.utc(dt.year, dt.month, dt.day, -5, minutes)


     #pedict according to time
    loc = Topos(cords[0], cords[1])
    difference = (satellite - loc).at(t)
    alt, az, distance = difference.altaz()

    #Get times itsabove horizon
    above_horizon = alt.degrees > 0

    above_horizon[-1] = 0
    above_horizon[0] = 0
    #above_horizon = insert(above_horizon,-1,0)




    #boundaries by setsand rising time
    boundaries, = diff(above_horizon).nonzero()
    
    #check for odd boundaries

    if len(boundaries) % 2 != 0:
        print(len(boundaries))

        #above_horizon = concatenate([[0],above_horizon,[0]])


        if len(boundaries) > 1 and boundaries[1] - boundaries[0] > 20:
            print("beginning")
            #boundaries = delete(boundaries,0)

        

        print(boundaries)


    #print(boundaries)
    passes = boundaries.reshape(len(boundaries) // 2, 2)

    output_array = []
    for passn in passes:

        i,j = passn

        outstring = []
        outstring.append('Rises: {}'.format(t[i].astimezone(maldives).strftime('%H:%M')))
        outstring.append('Sets: {}'.format(t[j].astimezone(maldives).strftime('%H:%M')))


        #append generatedimages to to array
        outstring.append(plot_sky(passn,t,az,alt))

        #append to output array
        output_array.append(outstring)
    

    return(output_array)


