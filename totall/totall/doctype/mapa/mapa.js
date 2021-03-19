// Copyright (c) 2018, C0D1G0 B1NAR10 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mapa', {
	refresh: function(frm) {
		$(".btn[data-fieldname=ver]").addClass('btn-success');
	},
	ver: function(frm) {
		frappe.call({
			method: "totall.api.get_rutas",
			args:{
				user: frm.doc.user,
				date:  frm.doc.date
			},
			callback: function (data) {
				$(frm.fields_dict.tabla.wrapper).empty();
				// console.log(data.message);
				cur_frm.set_value('mapa', data.message );
				frm.events.mostrar_tabla(frm);
			}
		});
	},
	mostrar_tabla: function(frm) {
		frappe.call({
			method: "totall.api.get_tabla",
			args:{
				user: frm.doc.user,
				date:  frm.doc.date
			},
			callback: function (data) {
				// console.log(data.message);
				var datos = data.message;
				var result_table = $(frappe.render_template('tabla', {
		 			frm: frm,
		 			datos: datos
		 		}));
		 		result_table.appendTo(frm.fields_dict.tabla.wrapper);
			}
	  });

	}
});
