frappe.ui.form.on('Payment Entry', {
	mode_of_payment: function(frm) {
	    if (cur_frm.doc.payment_type == "Pay"){
    		frm.set_value("party_type", "Supplier");
            refresh_field("party_type");
}
		if (cur_frm.doc.payment_type == "Receive"){
			frm.set_value("party_type", "Customer");
			refresh_field("party_type");
		}
		if (cur_frm.doc.mode_of_payment == "Transferencia bancaria"){
				frm.set_value("forma_de_pago", "03");
				refresh_field("forma_de_pago");
		}

		if (cur_frm.doc.mode_of_payment == "Efectivo"){
			frm.set_value("forma_de_pago", "01");
			refresh_field("forma_de_pago");
		}

		if (cur_frm.doc.mode_of_payment == "Cheque"){
			frm.set_value("forma_de_pago", "02");
			refresh_field("forma_de_pago");
}
		if (cur_frm.doc.mode_of_payment == "Transferencia bancaria USD"){
				frm.set_value("forma_de_pago", "03");
				refresh_field("forma_de_pago");
}
	}
})
