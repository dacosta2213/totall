@frappe.whitelist()
def get_chart_data():
	query = """SELECT str_to_date(concat(date_format(`tabSales Invoice`.`posting_date`, '%%Y-%%m'), '-01'), '%%Y-%%m-%%d') AS 'Mes:Date:', sum(`tabSales Invoice`.`base_grand_total`) AS 'Suma:Currency:', `tabSales Invoice`.`company` as 'company'
		FROM `tabSales Invoice`
			WHERE (`tabSales Invoice`.`docstatus` = 1
				AND `tabSales Invoice`.`metodo_pago` = 'PPD'
				AND date(`tabSales Invoice`.`posting_date`) >= date('2021-04-02'))
					GROUP BY str_to_date(concat(date_format(`tabSales Invoice`.`posting_date`, '%%Y-%%m'), '-01'), '%%Y-%%m-%%d')
					ORDER BY str_to_date(concat(date_format(`tabSales Invoice`.`posting_date`, '%%Y-%%m'), '-01'), '%%Y-%%m-%%d') ASC)
							"""
	data = frappe.db.sql(query, as_list=1)

	datasets = []
	labels = []
	for d in data:
		labels.append(d[0])
		datasets.append(d[1])

	return {
		'labels': labels,
		'datasets': [{'values':datasets}]
	}
