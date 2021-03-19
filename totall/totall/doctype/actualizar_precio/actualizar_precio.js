// Copyright (c) 2019, C0D1G0 B1NAR10 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Actualizar Precio Item", "item_code", function(frm, cdt, cdn) {
	row = locals[cdt][cdn];
    frappe.db.get_value('Item Price', { item_code: row.item_code, price_list: frm.doc.price_list }, ['name','price_list_rate'], (r) => {
      console.log(r)
      row.price_list_rate = r.price_list_rate
      row.nombre = r.name
			frm.refresh_fields('items')
    });

});

frappe.ui.form.on('Actualizar Precio', {
	refresh: function(frm) {
		frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
			 child = locals[cdt][cdn];
				return{
					filters:[
						['item_group', '=', frm.doc.item_group ]
					]
				}
      };

	},
	// RG- Esta es una idea, pero quizas te convenga hacerlo en 2 pasos...Como tu la veas
	// cargar_items: async function(frm) {
	// 	let r = (await frappe.db.get_list('Item', { fields: ['name'], filters: { item_group: frm.doc.item_group } }) )
	//
	// 		 $(r).each( async function(index){
	// 			 console.log("hola")
	// 	     let pr = await frappe.db.get_value('Item Price', { item_code: this.name, price_list: frm.doc.price_list }, ['price_list_rate'])
	// 			 // console.log(pr.message.price_list_rate)
	// 	     cur_frm.add_child('items').item_code = this.item_code
	// 	     cur_frm.add_child('items').price_list_rate = pr.message.price_list_rate ? pr.message.price_list_rate : 1
	// 	     cur_frm.refresh_field('items')
	// 	   })
	//
	//
	// },
	validate: function(frm) {
		$(cur_frm.doc.items).each(function(index){
			if (this.nombre) {
				frappe.db.set_value('Item Price',this.nombre, "price_list_rate", this.price_list_rate);
			} else {
				frappe.new_doc('Item Price', { price_list_rate:this.price_list_rate , item_code: this.item_code , price_list: frm.doc.price_list } )
			}
		});
	},
	// AG-DEV- Esta es una modificacion de la funcion anterior con algunos ajustes y provado desde la consola del navegador
	// El unico Inconveniente es que al agregar los items a la tabla, agrega un rengon en blanco despues de cada item.
	cargar_items: async function(frm) {
		let r = (await frappe.db.get_list('Item', { fields:['name'], filters:{item_group: frm.doc.item_group} }))

			 $(r).each( async function(index){
				 // console.log(this.name)
				 let pr = await	frappe.db.get_value('Item Price', {item_code:this.name,price_list:frm.doc.price_list}, ['price_list_rate','name'])
				 var new_row = cur_frm.add_child("items");
				 new_row.item_code = this.name
				 if(typeof pr.message == 'undefined'){
					 frappe.msgprint("<b> El producto: " +this.name+"</b><p>No cuenta con valor en la lista de Precio: " + frm.doc.price_list + "</p>")
				 }else{
					 new_row.price_list_rate = pr.message.price_list_rate ? pr.message.price_list_rate : null
					 new_row.nombre = pr.message.name ? pr.message.name : null
				 }
		     cur_frm.refresh_field('items')
		   })
	},
	// AG-DEV- Esta funcion actualiza el precio del item en caso de que se encuentre un valor superior a 0
	// En el campo de procentaje en el documento.
	actualizar: function(frm){
		$.each(frm.doc.items,function(index,v){
			if (frm.doc.porcentaje > 0) {
				var porcentaje = frm.doc.porcentaje / 100;
				var newPriceRate = (this.price_list_rate * porcentaje) + this.price_list_rate;
				console.log(newPriceRate);
				frappe.db.get_value('Item Price', v.name,'price_list_rate',function(r){
					frappe.model.set_value(v.doctype,v.name,"price_list_rate",newPriceRate);
				})
			}
		});
		cur_frm.refresh_field('items');
	}
});
