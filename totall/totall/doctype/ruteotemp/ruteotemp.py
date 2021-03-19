# -*- coding: utf-8 -*-
# Copyright (c) 2018, C0D1G0 B1NAR10 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class Ruteotemp(Document):
	pass

	@frappe.whitelist(allow_guest=True)
	def get_estaciones():
		estaciones = frappe.get_all('Estacion', fields=['nombre','lat','lng'])
		return estaciones
