frappe.query_reports["Movimientos de Clientes"] = {
	"filters": [
		{
			"fieldname":"a.customer_name",
			"label": __("Cliente"),
			"fieldtype": "Link",
      "options": "Customer",
      "reqd": 1
    }
	]
}
