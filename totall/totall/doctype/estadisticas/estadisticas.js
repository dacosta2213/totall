// Copyright (c) 2019, C0D1G0 B1NAR10 and contributors
// For license information, please see license.txt
frappe.ui.form.on('Estadisticas', {
	mostrar_reporte: function(frm){
		frappe.call({
			method: "totall.totall.doctype.estadisticas.estadisticas.inventario",
			args: {
							item_code: frm.doc.item_code
			},
			callback: function(r) {
				var estadistica_html = $(frappe.render_template('estadistica', {
		 			frm: frm,
		 			datos: r.message[0],
					registros: r.message[1],
					entradas: r.message[2],
					salidas: r.message[3],
					t_entradas: r.message[4],
					t_salidas: r.message[5],
					t_amount_e: r.message[6],
					t_amount_s: r.message[7],
					t_entradas_mes: r.message[8],
					t_salidas_mes: r.message[9],
					t_cantidad_e: r.message[10],
					t_cantidad_s: r.message[11]
		 		}))
				frappe.run_serially([
				  () => $(frm.fields_dict.estadisticas.wrapper).empty(),
				  () => frm.set_value('tx_estadisticas', JSON.stringify(r.message) ),
				  () => estadistica_html.appendTo(frm.fields_dict.estadisticas.wrapper),
				  () => frm.save()
				]);

			}
		})
	},
	item_code: function(frm) {
		frappe.call({
			method: "totall.totall.doctype.estadisticas.estadisticas.inventario",
			args: {
							item_code: frm.doc.item_code
			},
			callback: function(r) {
				var estadistica_html = $(frappe.render_template('estadistica', {
		 			frm: frm,
		 			datos: r.message[0],
					registros: r.message[1],
					entradas: r.message[2],
					salidas: r.message[3],
					t_entradas: r.message[4],
					t_salidas: r.message[5],
					t_amount_e: r.message[6],
					t_amount_s: r.message[7],
					t_entradas_mes: r.message[8],
					t_salidas_mes: r.message[9],
					t_cantidad_e: r.message[10],
					t_cantidad_s: r.message[11]
		 		}))
				frappe.run_serially([
				  () => $(frm.fields_dict.estadisticas.wrapper).empty(),
				  () => frm.set_value('tx_estadisticas', JSON.stringify(r.message) ),
				  () => estadistica_html.appendTo(frm.fields_dict.estadisticas.wrapper),
				  () => frm.save()
				]);

			}
		})

	},
	print:function(frm){
		frappe.run_serially([
			() => newWin= window.open(""),
			() => newWin.document.write(frm.fields_dict.estadisticas.wrapper.outerHTML),
			() => newWin.print(),
			() => newWin.close()
		]);
	},
	refresh: function(frm) {
		frm.events.item_code
	}
});
