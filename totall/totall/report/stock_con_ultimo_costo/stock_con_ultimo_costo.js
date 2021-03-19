frappe.query_reports["Stock Con Ultimo Costo"] = {
	"filters": [
    {
			"fieldname":"b.creation",
			"label": __("b.creation"),
			"fieldtype": "Date",
      "reqd": 1,
			"default": frappe.datetime.get_today(),
			"width": "80"
		}
	]
}
