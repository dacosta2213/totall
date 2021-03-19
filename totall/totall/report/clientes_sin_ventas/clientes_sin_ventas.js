frappe.query_reports["Clientes Sin Ventas"] = {
  "filters": [
    {
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
      "reqd": 1,
			"default": frappe.datetime.month_start(),
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
