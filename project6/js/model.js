var Resteraunt = function(){
	this.latitude = 35.995494;
	this.longitude = -78.899818;
	this.name = "Bull City Burger";
	this.cusine =  ["Burgers","Pub Food","American","Cafe"];
	this.address = "107 E Parrish St";
	this.tel = "(919) 680-2333";
	this.website = "http://www.bullcityburgerandbrewery.com";

	this.getLocation = function(){

	    var location = {"latitude":this.latitude, "longitude" : this.longitude};

	    return location
	}
}

ko.applyBindings(new Resteraunt())