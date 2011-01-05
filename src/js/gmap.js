var map;
var initialLocation;
var browserSupportFlag =  new Boolean();
var sanfrancisco = new google.maps.LatLng(37.412709873415515, -121.99665108081057);
var marker;

function map_initialize() 
{
	var latlng = new google.maps.LatLng(-34.397, 150.644);
	var myOptions = {
		zoom: 8,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

	google.maps.event.addListener(map, 'click', function(event) {
		placeMarker(event.latLng);
		});

	// Try W3C Geolocation (Preferred)
	if(navigator.geolocation) {
		browserSupportFlag = true;
		navigator.geolocation.getCurrentPosition(function(position) {
		initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
		map.setCenter(initialLocation);
		}, function() {
		handleNoGeolocation(browserSupportFlag);
		});
	// Try Google Gears Geolocation
	} else if (google.gears) {
		browserSupportFlag = true;
		var geo = google.gears.factory.create('beta.geolocation');
		geo.getCurrentPosition(function(position) {
		initialLocation = new google.maps.LatLng(position.latitude,position.longitude);
		map.setCenter(initialLocation);
		}, function() {
		handleNoGeoLocation(browserSupportFlag);
		});
	// Browser doesn't support Geolocation
	} else {
		browserSupportFlag = false;
		handleNoGeolocation(browserSupportFlag);
	}

	function handleNoGeolocation(errorFlag) {
		if (errorFlag == true) {
		alert("Geolocation service failed.");
		initialLocation = sanfrancisco;
	} else {
		alert("Your browser doesn't support geolocation. We've placed you in Siberia.");
		initialLocation = sanfrancisco;
	}
	map.setCenter(initialLocation);
	}

}

function placeMarker(location) 
{
	var clickedLocation = new google.maps.LatLng(location);

	marker = new google.maps.Marker({
					position: location, 
					map: map
					});
	google.maps.event.addListener(marker, 'click', function(event) {
		marker.setMap(null);
		});
	map.setCenter(location);
}