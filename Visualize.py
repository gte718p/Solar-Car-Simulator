import csv


def main():
    GPSpointsFile=open('GPSPoints.txt','r')
    GPSPoints=csv.reader(GPSpointsFile)
    GPSPoints=list(GPSPoints)
    
    fo = open('visualize.html', 'w')
    
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
            
           """
    fo.write(Header)
    
    LocationDec="var locations = ["
    fo.write(LocationDec)
    
    i=0
    while i < len(GPSPoints):
        Locations = "[%s,%s]," %(GPSPoints[i][0],GPSPoints[i][1])
        fo.write(Locations)
        i+=1
        
    fo.write('];')
          
    Footer = """ 
        
        poly = new google.maps.Polyline({
          strokeColor: '#000000',
          strokeOpacity: 1.0,
          strokeWeight: 3
        });
        poly.setMap(map);

        var path = poly.getPath();
        
        
        for (i = 0; i < locations.length; i++) {
           path.push(new google.maps.LatLng(locations[i][0], locations[i][1]));
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
     
