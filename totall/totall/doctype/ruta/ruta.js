// Copyright (c) 2018, C0D1G0 B1NAR10 and contributors
// For license information, please see license.txt

var pos = '';

var options = {
  enableHighAccuracy: false,
  maximumAge: 0
};

function error(err) {
  console.log(err.message);
}

var posicion = function(position) {
	console.log('eits:', position.coords.latitude);
	pos = position.coords.latitude;
	// var long = position.coords.longitude;
	cur_frm.set_value('lat', position.coords.latitude);
	cur_frm.set_value('lng', position.coords.longitude);
};




frappe.ui.form.on('Ruta', {
	refresh: function(frm) {
		navigator.geolocation.getCurrentPosition(posicion , error, options);
		// navigator.permissions.query({name:'geolocation'}).then(function(result) {
		// 	console.log(result.state);
  	// });
	}
	// onload_post_render: function(frm) {
	//
	// 	console.log(pos);
	// }
});
