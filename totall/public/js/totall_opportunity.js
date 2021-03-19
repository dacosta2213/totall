frappe.ui.form.on("Opportunity", {
	refresh: function(frm) {
		frappe.db.get_value('User',frappe.user.name,'supervisor', (r) => {
			 frm.set_value('supervisor', r.supervisor)
       console.log(r.supervisor)
		})
	}

})
