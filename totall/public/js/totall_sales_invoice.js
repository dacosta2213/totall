// frappe.ui.form.on('Sales Invoice Item', {
//     items_add: function(frm) {
// 			console.log('items_add')
// 			if ( frm.doc.taxes.length === 0 ) {
// 				console.log('agregue el impuesto')
// 				frm.add_child('taxes')
//
// 			} else {
// 				console.log('ELSE - agregue el impuesto')
//
// 			}
//       frm.refresh_field('taxes_and_charges')
//       frm.refresh_field('taxes')
//       frm.refresh_field('payments')
//    },
// });

frappe.ui.form.on('Sales Invoice', {
	additional_discount_percentage: function(frm, cdt, cdn){
		$(frm.doc.items).each(function(index){
			this.descuento = frm.doc.additional_discount_percentage * this.rate / 100

	})
}
})


frappe.ui.form.on('Sales Invoice', {
	perfil_facturacion: function(frm, cdt, cdn){
    perfiles(frm, cdt, cdn)
  },
	validate: function(frm, cdt, cdn){
    if (frm.doc.__islocal) {
			frappe.db.get_value('Perfil Facturacion',frm.doc.perfil_facturacion ,'naming_series', (r) => {
					 console.log(r.naming_series)
		       frm.set_value("naming_series", r.naming_series)
				})
		}
  },
   after_save: function(frm, cdt, cdn){
    $(frm.doc.payments).each(function(index){

        if (frm.doc.forma_de_pago === '03') {
            this.mode_of_payment = "Transferencia Bancaria"
						this.amount = frm.doc.grand_total
						//this.account = "102.01 - Bancos nacionales - SAT"
						//this.type = "Bank"
            frm.refresh_field('payments')
        } else if (frm.doc.forma_de_pago === '01') {
	          this.mode_of_payment = "Efectivo"
			  			this.amount = frm.doc.grand_total
						// this.account = "101.01 - Caja y efectivo - SAT"
						// this.type = "Cash"
	          frm.refresh_field('payments')
        } else if (frm.doc.forma_de_pago === '28') {
	          this.mode_of_payment = "Tarjeta Debito"
			  			this.amount = frm.doc.grand_total
						// this.account = "102.01 - Bancos nacionales - SAT"
						// this.type = "Bank"
	          frm.refresh_field('payments')
        } else if (frm.doc.forma_de_pago === '04') {
	          this.mode_of_payment = "Tarjetas de credito"
			  			this.amount = frm.doc.grand_total
						// this.account = "102.01 - Bancos nacionales - SAT"
						// this.type = "Bank"
	          frm.refresh_field('payments')
        }
    })


    // if (frm.doc.forma_de_pago === '03') {
    //   frm.add_child('payments').mode_of_payment = 'Transferencia Bancaria'
    //   frm.add_child('payments').default = 1
		// 	frm.refresh_field('payments')
    // } else if (frm.doc.forma_de_pago === '01') {
    //   frm.add_child('payments').mode_of_payment = 'Efectivo'
    //   frm.add_child('payments').default = 1
		// 	frm.refresh_field('payments')
    // } if (frm.doc.forma_de_pago === '28') {
    //   frm.add_child('payments').mode_of_payment = 'Tarjeta Debito'
    //   frm.add_child('payments').default = 1
		// 	frm.refresh_field('payments')
    // }

  }

})

var perfiles = function(frm, cdt, cdn){
	frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Perfil Facturacion",
				filters: {
				"name": frm.doc.perfil_facturacion
				}
			},
			callback: function (data) {
					var v = data.message;
					frm.set_value("metodo_pago", v.metodo_pago)
					frm.set_value("is_pos", v.is_pos)
					frm.set_value("forma_de_pago", v.forma_de_pago)
					frm.set_value("naming_series", v.naming_series)
			}
	})

}


var validaciones = function(frm, cdt, cdn){
	if( frm.doc.pos_profile === "FACTURA A CREDITO" || frm.doc.pos_profile === "NOTA DE CARGO" ){
			console.log('se disparo FACTURA A CREDITO')
			frappe.run_serially([
				() => frm.set_df_property("payments", "hidden", 1),
				() => frm.set_value ('paid_amount', 0),
				() => frm.doc.payments= [],
				() => frm.refresh_field('payments'),
				() => frm.set_value ('forma_de_pago', '99'),
				// () => frm.set_value ('payments', []),
				() => frm.set_value ('metodo_pago', 'PPD')
			]);
	} else if (frm.doc.pos_profile === "FACTURA MOSTRADOR" || frm.doc.pos_profile === "TICKET") {
			console.log('se disparo MOSTRADOR')
			frm.set_value ('metodo_pago', 'PUE')
			frm.set_value ('forma_de_pago', '')
			frm.set_value ('is_pos', 1 )
	}

}
