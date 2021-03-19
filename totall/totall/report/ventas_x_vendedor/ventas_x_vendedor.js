frappe.query_reports["VENTAS X VENDEDOR"] = {
	"filters": [
		{
			"fieldname":"a.agente",
			"label": __("Vendedor"),
			"fieldtype": "Data",
      "reqd": 1,
			"hidden": 1,
			"default": frappe.user_info().username
    },
		{
			"fieldname":"a.from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
      "reqd": 1,
			"default": frappe.datetime.get_today(),
			"width": "80"
		},
		{
			"fieldname":"a.to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
      "reqd": 1,
			"default": frappe.datetime.get_today()
		}
	]
}
