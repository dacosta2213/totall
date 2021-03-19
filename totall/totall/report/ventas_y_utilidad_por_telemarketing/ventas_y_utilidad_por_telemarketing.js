frappe.query_reports["Ventas y Utilidad por Telemarketing"] = {
	"filters": [
    {
			"fieldname":"d.from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
      "reqd": 1,
			"default": frappe.datetime.get_today(),
			"width": "80"
		},
		{
			"fieldname":"d.to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
      "reqd": 1,
			"default": frappe.datetime.get_today()
    }
	]
}
