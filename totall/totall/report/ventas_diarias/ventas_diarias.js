frappe.query_reports["Ventas Diarias"] = {
	"filters": [
    {
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
      "reqd": 1,
			"default": frappe.datetime.get_today(),
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
      "reqd": 1,
			"default": frappe.datetime.get_today()
    }
	]
}
