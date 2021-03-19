
frappe.ui.form.on('Purchase Order', {
	onload: function(frm, cdt, cdn){
    console.log('po.js')
		if (frm.doc.__islocal) {
				frappe.call({
					method: "frappe.client.get",
					args: {
									doctype: "User",
									filters: { email: frappe.user_info().email }
					},
					callback: function(r) {
            console.log(r.message)
						if (r.message.firma && frm.doc.__islocal) {
							frm.set_value("firma", r.message.firma )
							frm.set_value("comprador", r.message.full_name )
							frm.set_value("puesto", r.message.puesto )
						} else {
              frappe.show_alert('El usuario no tiene firma cargada en su perfil')
            }
					}
				});
		}
	}
})
