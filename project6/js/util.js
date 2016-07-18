/*
    Util Function Definition
*/

function scrollToRestaurant(restaurant){//scroll when click specific marker
  
        $('#restaurant-list').scrollTo($('#' + restaurant.id() ),500);

}

function toggleRestaurant(restaurant){//simulate click on marker 

    //console.log(restaurant)
    new google.maps.event.trigger(markerList[restaurant.id()],'click');

}

function togglePanel(){
    if($('.col-md-3').position().left != 0){
        $('.col-md-3').animate({
            left : 0
        },1000);
    }
    else{
        $('.col-md-3').animate({
            left : -1000
        },1000);
    }
}
