# Copyright (c) 2013, C0D1G0 B1NAR10 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	return columns, data
	columns = [
        {
            'fieldname': 'Cliente',
            'label': _('Cliente'),
            'fieldtype': 'Link',
            'options': 'Customer'
        },
        {
            'fieldname': 'Factura',
            'label': _('Factura'),
            'fieldtype': 'Link',
            'options': 'Sales Invoice'
        },
        {
            'fieldname': 'Total',
            'label': _('Total'),
            'fieldtype': 'Currency',
            'options': 'currency'
        },
		{
            'fieldname': 'Moneda',
            'label': _('Moneda'),
            'fieldtype': 'Link',
            'options': 'Currency'
        },
        {
            'fieldname': 'Pago',
            'label': _('Pago'),
            'fieldtype': 'Link',
            'options': 'Payment Entry'
        },
        {
            'fieldname': 'Nota de Credito',
            'label': _('Nota de Credito'),
            'fieldtype': 'Link',
            'options': 'CFDI Nota de Credito'
        }
    ]
