frappe.query_reports["LISTA FACTURACION"] = {
	"filters": [
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
