// Copyright (c) 2020, C0D1G0 B1NAR10 and contributors
// For license information, please see license.txt

frappe.ui.form.on('RecorridoMapa', {
	onload: function(frm) {
		$.getScript("https://maps.googleapis.com/maps/api/js?key=AIzaSyAMpdNUsaTWYFV58yaxVKzg4lHWUWeNgWs")
	},
	refresh: function(frm) {
		$(".btn[data-fieldname=ver]").addClass('btn-success');
	},
	ver: function(frm) {
		frappe.call({
			method: "totall.totall.doctype.recorridomapa.recorridomapa.get_rutas_recorrido",
			args:{
				user: frm.doc.user,
				date:  frm.doc.date
			},
			callback: function (data) {
				$(frm.fields_dict.tabla_html.wrapper).empty();
				// console.log(data.message);
				cur_frm.set_value('mapa_html', data.message );
				frm.events.mostrar_tabla(frm);

			}
		})
	},
	mostrar_tabla: function(frm) {
		frappe.call({
			method: "totall.totall.doctype.recorridomapa.recorridomapa.get_tabla",
			args:{
				user: frm.doc.user,
				date:  frm.doc.date
			},
			callback: function (data) {
				console.log(data.message);
				var datos = data.message;
				var result_table = $(frappe.render_template('tabla', {
					frm: frm,
					datos: datos
				}));
				result_table.appendTo(frm.fields_dict.tabla_html.wrapper);
				est = data.message
				initMap(est)
			}
		})

	}
})


var initMap = function(est){
		console.log('est: ',est)
		var map = new google.maps.Map(document.getElementById('googleMap'), {
			// Guadalajara
			center:new google.maps.LatLng(20.666594,-103.353072),
			// Mexicali
			// center:new google.maps.LatLng(32.649895867,-115.381430567),
			// disableDefaultUI: true,
			zoom:15
		})

		setMarkers(map,est)
}


var setMarkers = function(map,est){
		$(est).each(function(){
				var marker = new google.maps.Marker({
						position: { lat: this.lat, lng: this.lng },
						map: map,
						// icon: { url: "https://maps.google.com/mapfiles/ms/icons/" + this.color + "-dot.png"  },
						// label: String(this._index) + " - " + this.cliente,
						label: {text: String(this._index + 1 ) , color: 'white'} ,
						// title: this.cliente + this.prospecto + " ( " + this.time + " ). Comentario: " + this.comentario
						title: this.creation

					});

				google.maps.event.addListener(marker,'click',function() {
					var infowindow = new google.maps.InfoWindow({ //para mostrar los detalles del marker en un infowindow
					content: marker.title
					});
					infowindow.open(map,marker);
				})
		})
}
