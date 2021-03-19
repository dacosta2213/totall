# -*- coding: utf-8 -*-
# Copyright (c) 2019, C0D1G0 B1NAR10 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

class Estadisticas(Document):
	pass

@frappe.whitelist()
def inventario(item_code='XXX01'):
	fecha_actual = date.today().strftime("%Y-%m-%d")
	ultima_fecha = (date.today() - relativedelta(year=date.today().year-2)).strftime("%Y-%m-%d")

	inventario = frappe.get_all('Bin', filters={'item_code': item_code}, fields=['warehouse', 'actual_qty'] )

	# salidas = frappe.db.sql("""SELECT sum(SiI.qty) as qty, MONTH(SI.posting_date) as mes,
	# YEAR(SI.posting_date) as year from `tabSales Invoice Item` as SiI
	# INNER JOIN `tabSales Invoice` as SI
	# WHERE SI.posting_date BETWEEN %(u_fecha)s and %(a_fecha)s
	# AND SiI.parent = SI.name
	# AND SiI.item_code =%(i_code)s GROUP BY mes
	# """,{"u_fecha": ultima_fecha, "a_fecha": fecha_actual,"i_code":item_code},as_dict=1)
	#
	# entradas = frappe.db.sql("""SELECT sum(PiI.qty) as qty, MONTH(PI.posting_date) as mes,
	# YEAR(PI.posting_date) as year from `tabPurchase Invoice Item` as PiI
	# INNER JOIN `tabPurchase Invoice` as PI
	# WHERE PI.posting_date BETWEEN %(u_fecha)s and %(a_fecha)s
	# AND PiI.parent = PI.name
	# AND PiI.item_code =%(i_code)s GROUP BY mes
	# """,{"u_fecha": ultima_fecha, "a_fecha": fecha_actual,"i_code":item_code},as_dict=1)

	union = frappe.db.sql("""
	SELECT year,mes,sum(t.qty_entrada) as entradas, sum(t.qty_salida) as salidas,
	sum(amount_entrada) as amount_entrada, sum(amount_salida) as amount_salida
	FROM(
		SELECT sum(PiI.qty) as qty_entrada,0 as qty_salida,
		sum(PiI.amount) as amount_entrada, 0 as amount_salida,
		MONTH(PI.posting_date) as mes, YEAR(PI.posting_date) as year,'Entrada' as tipo
		FROM `tabPurchase Invoice Item` as PiI
		INNER JOIN `tabPurchase Invoice` as PI ON PI.name = PiI.parent
		WHERE PI.posting_date BETWEEN %(u_fecha)s and %(a_fecha)s
		AND PiI.item_code =%(i_code)s GROUP BY mes
		UNION
		SELECT  0 as qty_entrada, sum(SiI.qty) as qty_salida,
		0 as amount_entrada, sum(SiI.amount) as amount_salida,
		MONTH(SI.posting_date) as mes, YEAR(SI.posting_date) as year, 'Salida' as tipo
		FROM `tabSales Invoice Item` as SiI
		INNER JOIN `tabSales Invoice` as SI ON SI.name = SiI.parent
		WHERE SI.posting_date BETWEEN %(u_fecha)s and %(a_fecha)s
		AND SiI.item_code =%(i_code)s GROUP BY mes
	) as t GROUP BY year,mes ORDER BY year desc, mes desc
	""",{"u_fecha": ultima_fecha, "a_fecha": fecha_actual,"i_code":item_code},as_dict=1)

	salidas_mes_a = frappe.db.sql("""SELECT SI.customer as cliente, SiI.qty as cantidad, SI.posting_date as fecha,
	SiI.amount as precio, SiI.parent as documento
	from `tabSales Invoice Item` as SiI
	INNER JOIN `tabSales Invoice` as SI
	WHERE MONTH(SI.posting_date) = MONTH(%(a_fecha)s)
	AND YEAR(SI.posting_date) = YEAR(%(a_fecha)s)
	AND SiI.parent = SI.name
	AND SiI.item_code =%(i_code)s
	""",{"a_fecha": fecha_actual,"i_code":item_code},as_dict=1)

	entradas_mes_a = frappe.db.sql("""SELECT PI.supplier as proveedor, PiI.qty as cantidad, PI.posting_date as fecha,
	PiI.amount as costo, PiI.parent as documento
	from `tabPurchase Invoice Item` as PiI
	INNER JOIN `tabPurchase Invoice` as PI
	WHERE MONTH(PI.posting_date) = MONTH(%(a_fecha)s)
	AND PiI.parent = PI.name
	AND PiI.item_code =%(i_code)s
	""",{"a_fecha": fecha_actual,"i_code":item_code},as_dict=1)
	# frappe.errprint(inventario)
	# frappe.errprint(fecha_actual)
	# frappe.errprint(ultima_fecha)
	# frappe.errprint("Entradas "+ str(entradas) +"\n")
	# frappe.errprint("Salidas "+ str(salidas) + "\n")
	# frappe.errprint("UNION: " + str(union) + "\n")
	# frappe.errprint("Entradas Mes Actual: " + str(entradas_mes_a) + "\n")
	# frappe.errprint("Salidas Mes Actual "+ str(salidas_mes_a) + "\n")
	t_entradas = 0
	t_salidas = 0
	t_amount_e = 0
	t_amount_s = 0
	for u in union:
		t_entradas = t_entradas + u['entradas']
		t_salidas = t_salidas + u['salidas']
		t_amount_e = t_amount_e + u['amount_entrada']
		t_amount_s = t_amount_s + u['amount_salida']

	t_entradas_mes = 0
	t_cantidad_e = 0
	for e in entradas_mes_a:
		t_entradas_mes = t_entradas_mes + e['costo']
		t_cantidad_e = t_cantidad_e + e['cantidad']

	t_salidas_mes = 0
	t_cantidad_s = 0
	for s in salidas_mes_a:
		t_salidas_mes = t_salidas_mes + s['precio']
		t_cantidad_s = t_cantidad_s + s['cantidad']


	t_amount_e = round(t_amount_e,4)
	t_amount_s = round(t_amount_s,4)
	t_entradas_mes = round(t_entradas_mes,4)
	t_salidas_mes = round(t_salidas_mes,4)
	# frappe.errprint("Total Entradas: " + str(t_entradas)+"\n")
	# frappe.errprint("Total Salidas: " + str(t_salidas)+"\n")
	return(inventario,union,entradas_mes_a,salidas_mes_a,t_entradas,t_salidas,t_amount_e,t_amount_s,t_entradas_mes,t_salidas_mes,t_cantidad_e,t_cantidad_s)
