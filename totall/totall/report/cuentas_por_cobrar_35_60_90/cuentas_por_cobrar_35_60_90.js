frappe.query_reports["Cuentas por Cobrar 35 60 90"] = {
  "filters": [
    {
			"fieldname":"a.from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
      "reqd": 1,
			"default": '2018-01-01',
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
