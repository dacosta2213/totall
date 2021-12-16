frappe.provide('frappe.dashboards.chart_sources');

frappe.dashboards.chart_sources["Mix"] = {
	method: "totall.api.get_chart_data",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company")
		}
	]
};
