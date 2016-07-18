/*
    Knockout ViewModel Definition
*/

function AppViewModel(){
			
			var self = this;
      
			self.restaurantList = ko.observableArray();
      self.currentFilter = ko.observable();

      self.filteredRestaurantList = ko.computed(function(){

           if(!self.currentFilter()){

              return self.restaurantList();
           
           }
           else{

              return ko.utils.arrayFilter(self.restaurantList(),function(restaurant){

                  return restaurant.name.toLowerCase().indexOf(self.currentFilter().toLowerCase()) >= 0;
                  
              });
           }

      });

      self.filteredRestaurantList.subscribe(function(){
           refreshMapByFilter();
      })

			self.addRestaurant = function(restaurant){

				self.restaurantList.push(restaurant);

			}

}
