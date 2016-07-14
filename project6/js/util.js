/*
    Util Function Definition
*/


function scrollToRestaurant(restaurant){//scroll when click specific marker
  
        $('#restaurant-list').scrollTo($('#' + restaurant.id() ),500);

}


function refreshMapByFilter(){//filter markers

    clearMarkers();
    preInfoWindow = null;
    preRestaurant = null;
    markerList = [];
    for(var i=0; i < appViewModel.filteredRestaurantList().length;i++){
    	appViewModel.filteredRestaurantList()[i].id(i);
        setRestaurantMarkerOnMap(appViewModel.filteredRestaurantList()[i]);
    }
}

function clearMarkers(){//clear existing markers

    for(var i=0 ; i< markerList.length ; i++){
      markerList[i].setMap(null);
    }
}

function toggleRestaurant(restaurant){//simulate click on marker 

    //console.log(restaurant)
  new google.maps.event.trigger(markerList[restaurant.id()],'click');

}

function togglePanel(){
    if($('.col-md-3').position().left != 0){
        $('.col-md-3').animate({
            left : 0
        },1000)
    }
    else{
        $('.col-md-3').animate({
            left : -1000
        },1000)
    }
}