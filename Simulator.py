from gpxpy import geo
import datetime
import csv
import math
import Visualize
import random


def AimPoint(Alatitude,Alongitude,Blatitude,Blongitude):
    base=random.random()
    Clatitude=float(Alatitude)+(float(Blatitude)-float(Alatitude))*base
    Clongitude=float(Alongitude)+(float(Blongitude)-float(Alongitude))*base
    
    return Clatitude, Clongitude

    
def Bearing(point1, point2):
    """
    Calculates the initial bearing between point1 and point2 relative to north
    (zero degrees).
    """

    lat1r = math.radians(point1.latitude)
    lat2r = math.radians(point2.latitude)
    dlon = math.radians(point2.longitude - point1.longitude)

    y = math.sin(dlon) * math.cos(lat2r)
    x = math.cos(lat1r) * math.sin(lat2r) - math.sin(lat1r) \
                        * math.cos(lat2r) * math.cos(dlon)
    return math.degrees(math.atan2(y, x))
    

    
class SolarCar:
        def __init__(self, latitude, longitude, state=3):
            self.location = geo.Location(latitude,longitude)
            self.state = state   #states 1=running. 2=break down enterpits, 3 exit pits, 4 holding
            self.nextwaypoint = 0
            self.speed=6   #meters a second
            self.waypointbearing=0
            self.pitflag=0
            self.breakflag=0
        def UpdateLoc(self, latitude, longitude):
            self.lat = latitude
            self.long = longitude
        def UpdateLoc(self, state):
            self.state = state
        def UpdateWayPoint(self, point):
            self.nextwaypoint = point

    
def main():
    
    #open the model of TMS
    TrackFile=open('TMS.txt','r')
    TrackPoints=csv.reader(TrackFile)
    TrackPoints=list(TrackPoints)
    TrackFile.close()
    
    #open the output file
    Log=open('Car1.txt','w')
    GPS=open('GPSpoints.txt','w')
    
    #variable definitions including route into and out of pits
    EnterPit =[[33.03894, -97.28298],[33.03858, -97.28310],[33.03808, -97.28327],[33.03798, -97.28307],[33.03794, -97.28285],[33.03791, -97.28268],[33.03772, -97.28277]]
    Pitroadwaypoint=30
    LeavePit = [[33.03749, -97.28285],[33.03728, -97.28310],[33.03733, -97.28338],[33.03735, -97.28353],[33.03636, -97.28387],[33.03529, -97.28421]]
    Entertrackwaypoint=6
    EnterHotPit=[[33.03925, -97.28287],[33.03807, -97.28330],[33.03744, -97.28346]]
    CarTime=datetime.datetime(2016, 6,1,8,0,0)
    Timeinterval=.25
    MaxSpeed=18
    MinSpeed=5
    timeflag=0
    RecordInterval=2
    Breakdown=0
    Pits=0
    TimeinPits=datetime.timedelta(minutes=0)
    Logsumary=[]
    
    laps=0
    
    Car=SolarCar(33.03724, -97.282277)
    
    #set initial conditions
    Waypoint=geo.Location(LeavePit[Car.nextwaypoint][0],LeavePit[Car.nextwaypoint][1])
    Car.waypointbearing=Bearing(Car.location, Waypoint)
    
    
    while CarTime.hour < 18:
        
        #event control
        #This section effect how often the solar car enters the pits or breaks down
        incedentcontrol=random.randrange(0, 1000000, 1)
 
        if (incedentcontrol < 20 and Car.state == 1):
            Car.state = 2
            Breakdowntime=CarTime+datetime.timedelta(random.randrange(5,20,1))

        if (incedentcontrol > 50 and incedentcontrol < 100 and Car.state == 1):
            Car.state=5
        
        
        
        if (Car.state == 3):  #car leaving pits
            #find the waypoint
            Waypoint=geo.Location(LeavePit[Car.nextwaypoint][0],LeavePit[Car.nextwaypoint][1])
            Car.waypointbearing=Bearing(Waypoint,Car.location)
             
            #move to waypoint
            Offset=geo.LocationDelta(-Car.speed*Timeinterval,Car.waypointbearing)
            Car.location.move(Offset)
             
        
             
            #check distance and update waypoint if needed.
            Distancetonextwaypoint=Car.location.distance_2d(Waypoint)
                    
             
            if Car.nextwaypoint < (len(LeavePit)-1):
                #get location from array and turn into a location object
                Waypoint=geo.Location(LeavePit[Car.nextwaypoint][0],LeavePit[Car.nextwaypoint][1])
                Distancetonextwaypoint=Car.location.distance_2d(Waypoint)
                if (Distancetonextwaypoint < Car.speed*Timeinterval):
                    Car.nextwaypoint += 1
            else:
                Car.nextwaypoint=Entertrackwaypoint
                Car.state = 1
                tempa, tempb =AimPoint(TrackPoints[Car.nextwaypoint][0],TrackPoints[Car.nextwaypoint][1],TrackPoints[Car.nextwaypoint][2],TrackPoints[Car.nextwaypoint][3])
                Waypoint=geo.Location(tempa,tempb)
                Car.waypointbearing=Bearing(Waypoint,Car.location)
                
                
        elif (Car.state==1):
            #move toward waypoint
            Offset=geo.LocationDelta(-Car.speed*Timeinterval,Car.waypointbearing)
            Car.location.move(Offset)
            
            #check next waypoint
            Distancetonextwaypoint=Car.location.distance_2d(Waypoint)
            if (Distancetonextwaypoint < Car.speed*Timeinterval): 
                if (Car.nextwaypoint < len(TrackPoints)-1):    
                    Car.nextwaypoint +=1
                    tempa, tempb =AimPoint(TrackPoints[Car.nextwaypoint][0],TrackPoints[Car.nextwaypoint][1],TrackPoints[Car.nextwaypoint][2],TrackPoints[Car.nextwaypoint][3])
                    Waypoint=geo.Location(tempa,tempb)
                    Car.waypointbearing=Bearing(Waypoint,Car.location)
                else:
                    Car.nextwaypoint=0
                    Car.speed=random.randrange(MinSpeed,MaxSpeed,1);
                    laps +=1
                    Logsumary.append([laps, CarTime])
                    tempa, tempb =AimPoint(TrackPoints[Car.nextwaypoint][0],TrackPoints[Car.nextwaypoint][1],TrackPoints[Car.nextwaypoint][2],TrackPoints[Car.nextwaypoint][3])
                    Waypoint=geo.Location(tempa,tempb)
                    Car.waypointbearing=Bearing(Waypoint,Car.location)
        
        elif (Car.state==2): #breakdown
            if (CarTime <  Breakdowntime):
                Car.breakflag=1
                #move toward waypoint
                
                Offset=geo.LocationDelta(-Car.speed*Timeinterval,Car.waypointbearing)
                Car.location.move(Offset)
                
                #check next waypoint
                Distancetonextwaypoint=Car.location.distance_2d(Waypoint)
      
                if (Distancetonextwaypoint < Car.speed*Timeinterval):
                    if (Car.nextwaypoint < len(TrackPoints)-1 and Car.pitflag == 0):    
                        Car.nextwaypoint +=1
                        tempa, tempb =AimPoint(TrackPoints[Car.nextwaypoint][0],TrackPoints[Car.nextwaypoint][1],TrackPoints[Car.nextwaypoint][2],TrackPoints[Car.nextwaypoint][3])
                        Waypoint=geo.Location(tempa,tempb)
                        Car.waypointbearing=Bearing(Waypoint,Car.location)
                    
                    if (Car.nextwaypoint == len(TrackPoints)-1):
                        Car.speed=4
                        Car.pitflag=1
                        Car.nextwaypoint= 0
                        Waypoint=geo.Location(EnterPit[Car.nextwaypoint][0],EnterPit[Car.nextwaypoint][1])
                        Car.waypointbearing=Bearing(Waypoint,Car.location)
                    
                    if (Car.pitflag == 1):
                        if (Car.nextwaypoint < len(EnterPit)-1):
                            Waypoint=geo.Location(EnterPit[Car.nextwaypoint][0],EnterPit[Car.nextwaypoint][1])
                            Car.waypointbearing=Bearing(Waypoint,Car.location)
                            Car.nextwaypoint +=1
                            
                        else:
                            #set the car to inpits and set an amount of time for it to wait
                            Car.state=4
                            Breakdown +=1
                            Waittime=random.randrange(10, 30, 1)
                            TimeinPits=TimeinPits+datetime.timedelta(minutes=Waittime) 
                            Restarttime=CarTime+datetime.timedelta(minutes=Waittime)
                            Car.pitflag = 0
        
        elif (Car.state==4): #hold
            if (CarTime <  Restarttime):
                print("just sitting in the garage")
                print(Restarttime-CarTime, "remain")
                
            elif(CarTime >=Restarttime):
                Car.state=3
                if Car.breakflag == 1:
                    Car.nextwaypoint = 0
                    Car.breakflag = 0
                else:
                    Car.nextwaypoint = 3
                    Car.pitflag=0
                Car.speed=random.randrange(2,5,1)
        
        elif (Car.state==5):  #enter hot pits
            
            Offset=geo.LocationDelta(-Car.speed*Timeinterval,Car.waypointbearing)
            Car.location.move(Offset)
            
            #check next waypoint
            Distancetonextwaypoint=Car.location.distance_2d(Waypoint)
  
            if (Distancetonextwaypoint < Car.speed*Timeinterval):
                if (Car.nextwaypoint < len(TrackPoints)-1 and Car.pitflag == 0):    
                    Car.nextwaypoint +=1
                    tempa, tempb = AimPoint(TrackPoints[Car.nextwaypoint][0],TrackPoints[Car.nextwaypoint][1],TrackPoints[Car.nextwaypoint][2],TrackPoints[Car.nextwaypoint][3])
                    Waypoint=geo.Location(tempa,tempb)
                    Car.waypointbearing=Bearing(Waypoint,Car.location)
                
                if (Car.nextwaypoint == len(TrackPoints)-1):
                    Car.speed=4
                    Car.pitflag=1
                    Car.nextwaypoint= 0
                    Waypoint=geo.Location(EnterHotPit[Car.nextwaypoint][0],EnterHotPit[Car.nextwaypoint][1])
                    Car.waypointbearing=Bearing(Waypoint,Car.location)
                
                if (Car.pitflag == 1):
                    if (Car.nextwaypoint < len(EnterHotPit)-1):
                        Waypoint=geo.Location(EnterHotPit[Car.nextwaypoint][0],EnterHotPit[Car.nextwaypoint][1])
                        Car.waypointbearing=Bearing(Waypoint,Car.location)
                        Car.nextwaypoint +=1
                        
                    else:
                        #set the car to inpits and set an amount of time for it to wait
                        Car.state=4
                        Pits +=1
                        laps +=1
                        Logsumary.append([laps, CarTime])
                        Waittime=random.randrange(5, 8, 1)
                        TimeinPits=TimeinPits+datetime.timedelta(minutes=Waittime) 
                        Restarttime=CarTime+datetime.timedelta(minutes=Waittime)
                        Car.pitflag = 0

                    
                    
                    
      
             
        
        #creat the outputs    
        
        timeflag +=Timeinterval
        if (timeflag == RecordInterval):
            outputstring=CarTime.strftime("%a %b %H:%M:%S %Y")
            print("d90e5bc9f95dc7eb, %s, %s, %s, STOPPED, Cristian Almendariz, 8 Walnut, 6.0, %s, %s"%(outputstring, Car.location.latitude, Car.location.longitude, Car.speed, Car.waypointbearing),  file=Log)
            print("%s, %s"%(Car.location.latitude,Car.location.longitude) ,file=GPS)
            timeflag=0
        
        
        Timeincrease=datetime.timedelta(seconds=Timeinterval)
        CarTime=CarTime+Timeincrease
        print(CarTime.strftime("%a %b %H:%M:%S"),"Waypoint",Car.nextwaypoint,"Distance", Distancetonextwaypoint, "Car State:",Car.state)
        if Distancetonextwaypoint > 400:
            print("car state:", Car.state, "next Waypoint", Car.nextwaypoint)
            input("stop and look here")
            
            
    

    
    Log.close()
    GPS.close()
    Visualize.main()
    print("Laps:", laps)
    print("Breakdowns:", Breakdown)
    print("Hot pits:", Pits)
    print(TimeinPits)
    

    Summary=open('Summary.txt','w') 
    i=0
    while i < len(Logsumary):
        print(Logsumary[i][0],Logsumary[i][1].strftime("%H:%M:%S"), file=Summary)
        i+=1
    Summary.close()
        
          
    
if __name__ == "__main__":
    main()
