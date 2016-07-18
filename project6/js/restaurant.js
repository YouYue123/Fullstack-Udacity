/*
    Knockout Model Definition
*/

var Restaurant = function(){

        var self = this;
        self.id = ko.observable(0);
  			self.latitude = 35.995494;
  			self.longitude = -78.899818;
  			self.name = "Bull City";
  			self.cusine =  ["Burgers","Pub Food","American","Cafe"];
  			self.address = "107 E Parrish St";
  			self.tel = "(919) 680-2333";
  			self.website = "http://www.bullcityburgerandbrewery.com";
  			self.isSelected = ko.observable(false);
        self.marker = null;
        self.toggleRestaurantUrl = ko.pureComputed(function(){
          return 'javascript:toggleRestaurant(' + self.id() + ')';
        });
}