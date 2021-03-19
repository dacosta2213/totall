frappe.query_reports["NOTAS DE CREDITO X AGENTE"] = {
	"filters": [
    {
			"fieldname":"a.from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
      "reqd": 1,
			"default": frappe.datetime.month_start(),
			"width": "80"
		},
		{
			"fieldname":"a.to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
      "reqd": 1,
			"default": frappe.datetime.month_end()
    }
	]
}
