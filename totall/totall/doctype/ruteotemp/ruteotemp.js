// Copyright (c) 2018, C0D1G0 B1NAR10 and contributors
// For license information, please see license.txt

$('.leaflet-marker-icon').click(function(){
 console.log('algo hizo clip');
 });
 
frappe.ui.form.on('Ruteotemp', {
	onload: function(frm) {
	},
	refresh: function(frm) {

		frappe.call({
			method: "totall.api.get_estaciones",
			callback: function (data) {
				console.log(data.message);
				cur_frm.set_value('mapa', data.message );
			}
		});

		$('#unique-0').css({ "min-height":"600px"});
		$('.page-head').hide();


		setInterval(function() { location.reload(); }, 6000000);




			// marker.bindPopup("<b>Hello world!</b><br>I am a popup.").openPopup();

		}
	});
