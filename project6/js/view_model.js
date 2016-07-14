/*
    Knockout ViewModel Definition
*/

function AppViewModel(){
			
			var self = this;
      
			self.restaurantList = ko.observableArray();
      self.currentFilter = ko.observable()

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
      
      self.filterRestaurant = function(keyword){
         self.currentFilter(keyword)
      }
			self.addRestaurant = function(restaurant){

				self.restaurantList.push(restaurant)

			}


}

// ko.bindingHandlers.slideVisible = {
//     update: function(element, valueAccessor, allBindings) {
//         // First get the latest data that we're bound to
//         var value = valueAccessor();
 
//         // Next, whether or not the supplied model property is observable, get its current value
//         var valueUnwrapped = ko.unwrap(value);
 
//         // Grab some more data from another binding property
//         //var duration = allBindings.get('slideDuration') || 400; // 400ms is default duration unless otherwise specified
//         if(element.isSelected())
//           element.scrollToView();
//         // Now manipulate the DOM element
//         // if (valueUnwrapped == true)
//         //     $(element).slideDown(duration); // Make the element visible
//         // else
//         //     $(element).slideUp(duration);   // Make the element invisible
//     }
// };
var appViewModel = new AppViewModel()
ko.applyBindings(appViewModel)