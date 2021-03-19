# -*- coding: utf-8 -*-
# Copyright (c) 2020, C0D1G0 B1NAR10 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RecorridoMapa(Document):
	pass


# carga los registros de los recorridos de los vendedores, filtra por vendedor y fecha y envia feature collection al front
@frappe.whitelist(allow_guest=True)
def get_rutas_recorrido(user,date):
    rutas = frappe.get_all('Recorrido', fields=['lat','lng','creation'], filters = {'user': user, 'fecha': date } , order_by='creation' )
    frappe.errprint('Rutas del Recorrido')
    frappe.errprint(rutas)
    feature = """ { "type": "FeatureCollection" , "features":[ { "type" : "Feature","properties":{},"geometry":{"type":"LineString","coordinates": [ """
    for i in rutas:
        feature += """ [ """ + str(i.lng) + """,""" + str(i.lat) + """ ] """
        if i == rutas[-1]:
            feature += """ ]}}]}"""
        else:
            feature += """ , """
    return feature

@frappe.whitelist(allow_guest=True)
# regresa la ruta para las tablas
def get_tabla(user,date):
    rutas = frappe.get_all('Recorrido', fields=['lat','lng','creation'], filters = {'user': user, 'fecha': date } , order_by='creation' )
    return rutas
