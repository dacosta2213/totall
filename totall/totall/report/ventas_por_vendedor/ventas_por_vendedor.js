frappe.query_reports["VENTAS POR VENDEDOR"] = {
	"filters": [
		{
			"fieldname":"a.agente",
			"label": __("Vendedor"),
			"fieldtype": "Data",
      "reqd": 1,
			"hidden": 1,
			"default": frappe.user_info().username
    }
	]
}
