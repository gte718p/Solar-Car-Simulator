import csv
from gpxpy import geo
import random


GPSpointsFile=open('TMS.txt','r')
GPSPoints=csv.reader(GPSpointsFile)
GPSPoints=list(GPSPoints)


COLORS = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF', '#800000', '#008000', '#000080', '#808000', '#008080', '#800080']


i=0




fo = open('Test.html', 'w')

Header="""<!DOCTYPE html>
<html>
  <head>
    <title>Texas Motor Speedway Simulator Control lines</title>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 90%;
      }
      #current{
       height: 10%;
      }

    </style>
  </head>
  <body>
    <div id="map"></div>
    <div id="current"></div>
    <div id="List"></div>
    <script> 

        var A= [];
        var B=[];
        var C=[];

function initMap() {
        var myLatlng = {lat: 33.036998, lng: -97.281323};

        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 17,
          center: myLatlng,
          mapTypeId: 'satellite'
        });
        
        var marker = new google.maps.Marker({
          position: myLatlng,
          map: map,
          draggable: true,
          title: 'Click to zoom'
        });

        
        google.maps.event.addListener(marker, 'dragend', function (evt) {
        document.getElementById('current').innerHTML = '<p>Marker dropped: Current Lat: ' + evt.latLng.lat().toFixed(8) + ' Current Lng: ' + evt.latLng.lng().toFixed(8) + '</p>';
        });
        
        google.maps.event.addListener(marker, 'click', function (evt) {
        for (j = 0; j < locations.length; j++) {
             for (j = 0; j < locations.length; j++) {
            E=A[j].getPosition();
            F=B[j].getPosition();
            G=E.lat().toFixed(8) +', '+ E.lng().toFixed(8) + ', ' + F.lat().toFixed(8) + ', ' + F.lng().toFixed(8) +'<br>' ; 
            
            C.push(G);       
            }

        document.getElementById('current').innerHTML = C;
        }
        
        
        });

        
        
    """
fo.write(Header)

LocationDec="var locations = ["
fo.write(LocationDec)

i=0
while i < len(GPSPoints):
    Locations = "[%s,%s,%s,%s]," %(GPSPoints[i][0],GPSPoints[i][1],GPSPoints[i][2],GPSPoints[i][3])
    fo.write(Locations)
    i+=1
    
fo.write('];')
    
    
    
    
    
Footer = """ 
     var marker, controlline, poly, poly1, i, j;

    for (i = 0; i < locations.length; i++) {
        var markerA = makemarker(locations[i][0], locations[i][1],'A',i, map);
        A.push(markerA);
        var markerB = makemarker(locations[i][2], locations[i][3],'B',i, map);
        B.push(markerB);


     
      
    }
    for (j = 0; j < locations.length; j++) {

        var flightPath = new google.maps.Polyline({
          path: [new google.maps.LatLng(locations[j][0], locations[j][1]),new google.maps.LatLng(locations[j][2], locations[j][3])],
          geodesic: true,
          strokeColor: '#FF0000',
          strokeOpacity: 1.0,
          strokeWeight: 2
        });

        flightPath.setMap(map);
        };
                var controlpoint={
    start:{
    center: {lat:33.03490233 , lng: -97.28442632},
    radius: 50
    },
    lappoint:{
    center: {lat: 33.03880806, lng: -97.28352778},
    radius: 25
    },
    trappoint:{
    center: {lat:33.03790 , lng: -97.28286},
    radius: 20
    },
    driverchange:{
    center: {lat:33.03769055, lng: -97.28342853},
    radius: 20
    },
    garage:{
    center: {lat:33.03759161, lng:-97.28215985 },
    radius: 50
    }
    };

for (var point in controlpoint) {
    // Add the circle for this city to the map.
    var controlcirc = new google.maps.Circle({
      strokeColor: '#FF0000',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: '#FF0000',
      fillOpacity: 0.35,
      map: map,
      center: controlpoint[point].center,
      radius: controlpoint[point].radius
    });
  }



      
      
      
      
      
      
      
      }
      

function makemarker(Lat, Lng,tag, i, map){

     var marker = new google.maps.Marker({
        position: new google.maps.LatLng(Lat,Lng),
        map: map,
        draggable: true,
        label: tag,
        title: String(i)
      });
    
    google.maps.event.addListener(marker, 'dragend', function (evt) {
    document.getElementById('current').innerHTML = '<p>Marker: ' + marker.title + '<br> Current Lat: ' + evt.latLng.lat().toFixed(8) + ' Current Lng: ' + evt.latLng.lng().toFixed(8) + '</p>';
        updatemarker(marker, evt);
        });
    google.maps.event.addListener(marker, 'click', function (evt) {
    document.getElementById('current').innerHTML = '<p>Marker: ' + marker.title + '<br>Current Lat: ' + evt.latLng.lat().toFixed(8) + ' Current Lng: ' + evt.latLng.lng().toFixed(8) + '</p>';   
        });
    
    return marker;   
}

function updatemarker(marker, evt){
    var markernumber=parseInt(marker.title);
    var markertype=marker.label;


    if(markertype =='A')
        {
        A[markernumber].setPosition(evt.latlng());
        };
     if(markertype == 'B'){
        B[markernumber].setPosition(evt.latlng());
        };
    }




    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCZBP_xUomSDxJ207tr-pzGq_lGKN6ZMm8&callback=initMap">
    </script>
  </body>
</html>    


"""
fo.write(Footer)






fo.close()



