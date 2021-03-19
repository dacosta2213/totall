// Copyright (c) 2020, C0D1G0 B1NAR10 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sales Invoice", {
	frm.add_custom_button("Presentacion", function() {
		presentation(frm)
	}).addClass("btn-primary")
});

var presentation = function(frm){
	frappe.call({
		method: "totall.slides.gs_conection",
		args: {
			name: frm.doc.name
		},
		callback: function(r) {
			console.log(r.message)
		}
	});
}
