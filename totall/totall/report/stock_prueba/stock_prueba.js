frappe.query_reports["Stock Prueba"] = {
	"filters": [
		{
			"fieldname":"b.warehouse",
			"label": __("Almacen"),
			"fieldtype": "Link",
      "reqd": 1,
			"default": "!NOMOSTRAR"
    }
	]
}
