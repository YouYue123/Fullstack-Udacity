/*
    API Function Definition
*/

var factualAPIKey = "Z2R3lQruh3KuQQBp9iCtWNhfPFHfiZyQ1nRCO8wh";
var query = "Restaurant,'Durham'";
var factualRestaurantEndPoint = "http://api.v3.factual.com/t/restaurants-us?";
var map;
var getRestaurantListApiEndPoint = "http://api.v3.factual.com/t/restaurants-us?filters={\"category_labels\":{\"$includes\":\"restaurant\"},\"locality\":\"Durham\"}&KEY=Z2R3lQruh3KuQQBp9iCtWNhfPFHfiZyQ1nRCO8wh&limit=50"
var preInfoWindow = null;
var preRestaurant = null;
var markerList = []; 

function initMap() {//google map api callback

  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 35.9979218, lng: -78.9256557},
    zoom: 14
  });

  getRestaurantInfo();
	
}

function getRestaurantInfo(){//call factual api using ajax
    $.ajax({
      url: getRestaurantListApiEndPoint,
      type: 'GET',
      success: function(data){ 
          var data_load = data.response.data;
      
          for (i=0; i< data_load.length;i++){
            var restaurant = initWithFactualObject(data_load[i],i);
            setRestaurantMarkerOnMap(restaurant);
            appViewModel.addRestaurant(restaurant);
          }
      },
      error: function(data) {
          alert('woops!Error from Factual API'); //or whatever
      }
  });
}

function initWithFactualObject(factualObject,index){//factual object middleware
        var restaurant = new Restaurant();
        restaurant.latitude = factualObject.latitude;
        restaurant.longitude = factualObject.longitude;
        restaurant.name = factualObject.name;
        restaurant.cusine = factualObject.cuisine;
        restaurant.address = factualObject.address
        restaurant.tel = factualObject.tel;
        restaurant.website = factualObject.website;
        restaurant.id(index);
        return restaurant;
 }

function infoWindowContent(restaurant){//infoWindow middleware
  var contentString = '<div id="content">'+
                      '<h1>'+ restaurant.name +'</h1>'+
                      '<div>'+
                      '<p>'+  restaurant.cusine + '</p>'+
                      '<p>'+  restaurant.address +'</p>'+
                      '<p>'+  restaurant.tel +'</p>'+
                      '<p>'+  restaurant.website +'</p>'+
                      '</div>'+
                      '</div>';

  return contentString;
}

function setRestaurantMarkerOnMap(restaurant){//set marker middleware

        var myLatlng = new google.maps.LatLng(restaurant.latitude,restaurant.longitude);
        var image = 'https://cdn4.iconfinder.com/data/icons/small-n-flat/24/map-marker-32.png';
      
        var marker = new google.maps.Marker({
          position: myLatlng,
          title: restaurant.name,
          animation: google.maps.Animation.DROP,
          draggable : false
        });

        var infowindow = new google.maps.InfoWindow({
            content: infoWindowContent(restaurant)
        });
        
        marker.addListener('click', function() {
       
          google.maps.event.addListener(infowindow,'closeclick',function(){
            preInfoWindow = null;
            restaurant.isSelected(false);
          });

          var marker = this
          marker.setAnimation(google.maps.Animation.BOUNCE);
          setTimeout(function(){ marker.setAnimation(null); }, 1500);

          if (preInfoWindow == infowindow){//click the opened window marker
             
             infowindow.close()
             restaurant.isSelected(false);
             preInfoWindow = null;
          }
          else{//click another marker
             
             if(preInfoWindow !== null){
                preInfoWindow.close()
                preRestaurant.isSelected(false);
             }

             infowindow.open(map, marker);
             restaurant.isSelected(true);
             
             scrollToRestaurant(restaurant)

             preInfoWindow = infowindow;
             preRestaurant = restaurant;
          }

        });
        marker.setMap(map);
        markerList.push(marker);
}
function googleMapErrorHandle(){
  alert("Google Map Loading Error");
}