frappe.query_reports["Cuentas Por Pagar Multimoneda"] = {
  "filters": [
    {
			"fieldname":"a.from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
      "reqd": 1,
			"default": frappe.datetime.month_start(date),
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
