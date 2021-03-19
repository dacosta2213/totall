# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "totall"
app_title = "Totall"
app_publisher = "C0D1G0 B1NAR10"
app_description = "Totall App for Frappe"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "admin@posix.mx"
app_license = "MIT"

# Includes in <head>
# ------------------
error_report_email = "admin@codigo-binario.com"

# include js, css files in header of desk.html
# RG- Aqui listar cualquier asset adicional y ponerlo en el folder de assets
#app_include_js = ["/assets/totall/js/charts.min.js","/assets/totall/js/posix.min.js","/assets/totall/js/sweetalert2.min.js","/assets/totall/js/app.js","/assets/js/modal-video.min.js"]

# app_include_css = "/assets/totall/css/totall.css"
# app_include_js = "/assets/totall/js/totall.js"


#website_context = {
#	"favicon": 	"/assets/totall/images/favicon.png",
#	"splash_image": "/assets/totall/images/posix.svg"
#}

# include js, css files in header of web template
#web_include_css = "/assets/totall/css/app-web.css"
#web_include_js = "/assets/totall/js/app-web.js"

# fixtures = [
#     # "Estacion",
#     # "Report",
#     # "Page",
#     "Print Format",
#     "UOM",
#     "Property Setter",
#     "Translation",
#     "Custom Script",
#     "Website Settings",
#     "System Settings",
#     "Website Script",
#     "Custom Field"
# 	]

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Purchase Order" : "public/js/totall_purchase_order.js",
	"Opportunity" : "public/js/totall_opportunity.js",
	"Sales Invoice" : "public/js/totall_sales_invoice.js",
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "totall.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "retail.install.before_install"
# after_install = "retail.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "retail.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
#doc_events = {
#	"Bin": {
#		"on_update": "totall.api.update_actual"
#	},
#	"Item": {
#		"on_update": "totall.api.update_actual_item"
#	}
#}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"retail.tasks.all"
# 	],
# 	"daily": [
# 		"retail.tasks.daily"
# 	],
# 	"hourly": [
# 		"retail.tasks.hourly"
# 	],
# 	"weekly": [
# 		"retail.tasks.weekly"
# 	]
# 	"monthly": [
# 		"retail.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "retail.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "retail.event.get_events"
# }
