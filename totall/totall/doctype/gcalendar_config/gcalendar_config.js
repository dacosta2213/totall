// Copyright (c) 2019, C0D1G0 B1NAR10 and contributors
// For license information, please see license.txt

frappe.ui.form.on('GCalendar Config', {
	refresh: function(frm) {
		$('.btn[data-fieldname=sync_calendar]').addClass('btn-success');
	},
	sync_calendar: function(frm) {
		// console.log('le picastes')
		frappe.call({
			method: "totall.gcal.google_callback",
			callback: function(r) {
				if(!r.exc) {
					// console.log(r.message.url)
					frm.save()
					window.open(r.message.url)
				}
		   }
		});
	}
});
