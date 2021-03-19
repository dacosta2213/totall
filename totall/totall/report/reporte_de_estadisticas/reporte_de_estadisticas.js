// Copyright (c) 2016, C0D1G0 B1NAR10 and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Reporte de Estadisticas"] = {
	"filters": [
		{
			"fieldname":"item_code",
			"label": __("Clave de Articulo"),
			"fieldtype": "Link",
			"options": "Item",
			"reqd": 1
		}
	]
}
