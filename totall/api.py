# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.utils import get_fullname, get_link_to_form, get_url_to_form
from datetime import date,datetime,timedelta
import jwt
import time

@frappe.whitelist()
def inventario(item_code):
	inventario = frappe.get_all('Bin', filters={'item_code': item_code}, fields=['warehouse', 'actual_qty'] )
	frappe.errprint(inventario)
	return(inventario)

@frappe.whitelist()
def pings():
    return 'pong'

def pingo():
    return 'pongo'

# RG - Actualizar el campo de atrasado y factura en c/customer
# 1 - Al finalizar un Payment Entry se actualizaran todos los customers...Iniciamos calculando la fecha de update_atrasado
# 2 - Bloquear (congelado = 1, credit_limit = 1) a los mayores de 40 dias y desbloquear (congelado = 0, credit_limit = ) en < 40
# 3 - Si no existe SINV == "Unpaid" o "Overdue" mandar atrasado = 0
@frappe.whitelist()
def update_atrasado():
	clientes = frappe.db.get_list('Customer',fields=['name'])

	for c in clientes:
		facturas = frappe.db.get_list('Sales Invoice', filters={ 'outstanding_amount': ['>', 1],'customer': c.name,'clave':['like', '%%CC%%'] },
	    fields=['name', 'outstanding_amount','posting_date'],
	    order_by='posting_date asc',
	    page_length=1,
	    as_list=True
		)
		if facturas:
			today = date.today()
			someday = facturas[0][2]
			diff = today - someday
			#frappe.errprint(diff.days)
			#frappe.errprint(facturas[0][0])
			#frappe.errprint(c.name)
			if diff.days > 40:
				frappe.db.sql("UPDATE tabCustomer  set congelado = 1 ,credit_limit = 1 WHERE name = %s", (c.name))
				frappe.errprint(c.name)
				frappe.db.sql("UPDATE `tabSales Invoice` a left join tabCustomer b on a.customer = b.customer_name set congelado = 1, credit_limit = 1, b.atrasado = %s, b.factura = %s WHERE b.name = %s", (diff.days,facturas[0][0],c.name))
				frappe.db.commit()
			#else:
			#	frappe.db.sql("UPDATE tabCustomer  SET congelado = 0 ,credit_limit = 0 WHERE name = %s", (c.name))
			#	frappe.db.commit()

	return


# @ frappe.whitelist ()
# def ubicacion ():
#     items = frappe.db.get_list ('Item', fields =['name', 'rack', 'ubicacion'])
#     for c in items:
#         ajustes = frappe.db.get_list ('Stock Reconciliation Item', fields =['name','item_code', 'anaquel', 'ubicacion'], order_by = 'creation desc')
# 	for a in ajustes:
#          if c.ubicacion != a.rack:
#              #frappe.errprint(c.name)
#              frappe.errprint(a.anaquel)
#              frappe.db.commit()
# #else	/* : */
# #	frappe.db.sql("UPDATE tabCustomer  SET congelado = 0 ,credit_limit = 0 WHERE name = %s", (c.name))
# #	frappe.db.commit()
#     return


#
# @frappe.whitelist()
# def ruta(login_manager):
#     ruta = frappe.db.get_value("User", login_manager.user,"ruta_login")
#     frappe.errprint(ruta)
#     frappe.local.response["home_page"] = ruta

 # {"type":"Feature","properties":{},"geometry":{"type":"LineString","coordinates":[ [-118.383197,32.649782],[-115.382042,32.650772],[-115.380479,32.649689] ] }}]}"

@frappe.whitelist(allow_guest=True)
# carga los registros de ruta, filtra por usuario y fecha y envia feature collection al front
def get_rutas(user,date):
    rutas = frappe.get_all('Ruta', fields=['cliente','nombre_prospecto','lat','lng','creation','comentario'], filters = {'usuario': user, 'date': date } , order_by='creation' )
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
    rutas = frappe.get_all('Ruta', fields=['cliente','nombre_prospecto','lat','lng','time','comentario'], filters = {'usuario': user, 'date': date } , order_by='creation' )
    return rutas


@frappe.whitelist(allow_guest=True)
# regresa los usuarios con el Role Profile de Vendedor para iniciar la captura en el app
def get_usuarios():
	# u = frappe.db.sql("SELECT name from tabUser")
	# return u
	usuarios = frappe.get_all('User', fields=['name','full_name'], filters = {'role_profile_name': 'Vendedor'} , order_by='name' )
	if usuarios:
		return usuarios
	else:
		return('No encontrado')

@frappe.whitelist(allow_guest=True)
def generar_lead(owner,lead_name,email_id,numero,lead_owner,source,campaign_name,informacion_adicional,lead_type):
	doc = frappe.get_doc({
		"doctype": "Lead",
		"user": "Administrator",
		"owner": owner,
		"lead_name": lead_name,
		"email_id": email_id,
		"numero": numero,
		"lead_owner": lead_owner,
		"source": source,
		"campaign_name": campaign_name,
		"informacion_adicional": informacion_adicional,
		"lead_type": lead_type
		})
	doc.insert(ignore_permissions=True)
	frappe.db.commit()
#	return('Nuevo Lead: ' + str(doc.name))
#            frappe.db.sql("UPDATE tabLead  SET status='Asignado' WHERE source like '%Publicidad%'")
#            frappe.db.commit()
	frappe.sendmail(['egarcia@totall.mx',"{0}".format(doc.lead_owner)], \
    subject=doc.name , \
    content="Felicidades usted tiene un nuevo prospecto, de click en la liga para darle seguimiento. ¡Exito!  "+frappe.utils.get_url_to_form(doc.doctype, doc.name),delayed=False)



@frappe.whitelist(allow_guest=True)
def recorrido(user,lat,lng):

	frappe.log_error(title="Error latitud", message=lat + user)
	doc = frappe.get_doc({
		"doctype": "Recorrido",
		"user": user.strip('"'),
		"lng": lng,
		"lat": lat,
		"phone": user
		})
	doc.insert(ignore_permissions=True)
	frappe.db.commit()
	return('Nueva-Lectura Insertada: ' + str(doc.name))




@frappe.whitelist(allow_guest=True)
# carga las estaciones registradas y genera el archivo para el mapa
def get_estaciones():
    estaciones = frappe.get_all('Estacion', fields=['nombre','lat','lng'])
    feature = """ { "type": "FeatureCollection" , "features":[ """
    for i in estaciones:
        feature += """ { "type" : "Feature","properties":{"name": " """ + i.nombre + """ "},"geometry":{"type":"Point","coordinates":[""" + str(i.lat) + """,""" + str(i.lng) + """]}}"""
        if i == estaciones[-1]:
            feature += """ ]} """
        else:
            feature += """ , """
    return feature

@frappe.whitelist(allow_guest=True)
def estaciones(estacion,lat,lng):
    est = frappe.db.get_value("Estacion", estacion , "name")
    if est:
        frappe.db.sql("UPDATE tabEstacion  SET lat=%s , lng= %s WHERE nombre = %s", (lat,lng,estacion))
        frappe.db.commit()
        return ('Estacion Actualizada.')
    else:
        return('no se encontro la estacion')

    # est = frappe.db.get_value("Estacion", estacion , "name")
    # if est:
    #     frappe.db.set_value("Estacion", estacion, 'lat', lat)
    #     frappe.db.set_value("Estacion", estacion , 'lng', lng)
    #     return ('Estacion Actualizada.')
    # else:
    #     return('no se encontro la estacion')

# RG-Actualizar actual cantidad en Item
# falta hacer metodo para que todo Item tenga stock_maximo get_all stock_maximo < 0 (cambiarlo a int)
# otra ocsion - hacer metodo desde bin y calcular reorden desde ahi (quizas es mas facil)

# RG - En hooks - > events tenemos este metodo para  "Bin": "on_update": "totall.api.update_actual"
# RG- Lo que hace es actualizar el punto de reorden (actual-stock maximo) para que se muestre en el reporte Max del Doctype Item
@frappe.whitelist()
def update_actual(self,method):
    # m = str(self.name) + "item: " + str(self.item_code)
    # frappe.log_error(title="New Update Actual Qty", message=m)
    doc = frappe.get_doc("Item", self.item_code)
    if self.warehouse == 'GENERAL - SAT':
        doc.actual = self.actual_qty
        doc.reorder = float(self.actual_qty) - float(self.stock_maximo)
        doc.save()
        frappe.errprint('Items actualizado')

# RG - En hooks - > events tenemos este metodo para  "Item": "on_update": "totall.api.update_actual"
# RG- Lo que hace es actualizar el punto de reorden (actual-stock maximo) para que se muestre en el reporte Max del Doctype Item
@frappe.whitelist()
def update_actual_item(self,method):
	# doc = frappe.get_doc("Item", self.name)
	frappe.errprint('asas')
	reorder = float(self.actual) - float(self.stock_maximo)
	frappe.db.sql("UPDATE tabItem set reorder=%s WHERE name = %s", (str(reorder),self.name) )
	# self.save()
	# frappe.msgprint('El articulo ha sido actualizado.')

# RG-Este es un metodo que corrimos manualmente para actualizar las cantidades de Actual y Reorder en el Item (considerando el stock maximo)
#RG- ToDo - poner un metodo parecido en hooks > Events > Item > on_update para que recalcule
@frappe.whitelist()
def actual():
    # doc = frappe.get_doc("Item", 'GUM78-ARE')
    # doc.save()

    items = frappe.get_all('Bin', filters={'warehouse': 'GENERAL - SAT'}, fields=['name', 'actual_qty','item_code'])
    for i in items:
        if 0 < i.actual_qty < 100:
            doc = frappe.get_doc("Item", i.item_code)
            doc.actual = i.actual_qty
            doc.reorder = float(i.actual_qty) - float(doc.stock_maximo)
            doc.save()
            frappe.errprint(i.item_code +  'actual: ' + str(i.actual_qty) +  ' max: ' + str(doc.stock_maximo) )

@frappe.whitelist()
def actualizar():
    # para actualizar todos los items corri los queries desde la consola
    # items = frappe.get_all('Bin', filters={'actual_qty':'0'}, fields = ['item_code'])
    items = frappe.db.sql("SELECT name from tabItem  WHERE actual IS NULL")
    for i in items:
        item = frappe.db.sql("SELECT actual from tabItem WHERE name = %s",i)
        #item = frappe.db.sql("UPDATE tabItem set actual=0 WHERE name = %s",i)
        frappe.errprint(item)
    #r = frappe.get_doc("Item", items[1]['item_code'])
    #frappe.errprint(items)

# poner en 0 TODOS los items que tengan null - puedes frappe.db.sql ('UPDATE')
# actualizar item.reorder  float(i.actual) - float(doc.stock_maximo) para todos los Items.actual === 0
@frappe.whitelist()
def borrar():
    return frappe.db.sql("DELETE from  `tabBin` where warehouse  != 'GENERAL - SAT' and actual_qty = 0")

@frappe.whitelist()
def atrasado():
    frappe.db.sql("UPDATE `tabSales Invoice` set outstanding_amount = 0, status = 'Paid'  where outstanding_amount like '0.%' or outstanding_amount like '-%%'")
    frappe.db.sql("UPDATE `tabPurchase Invoice` set outstanding_amount = 0, status = 'Paid'  where outstanding_amount like '0.%' or outstanding_amount like '-%%'")
    frappe.db.sql("UPDATE `tabSales Invoice` a left join `tabCustomer` b on a.customer = b.customer_name set b.atrasado = DATEDIFF(CURDATE(), a.posting_date), b.factura = a.name where a.status = 'Overdue' or a.status = 'Unpaid'")
    frappe.db.sql("UPDATE `tabCustomer` set congelado = 1, credit_limit = 1 where atrasado >= 40 and clave like '%%CC%%'")
    frappe.db.sql("UPDATE `tabCustomer` set congelado = 0, credit_limit = 0 where atrasado < 40 and clave like '%%CC%%'")
    frappe.db.sql("UPDATE `tabSales Invoice` a left join `tabCustomer` b on a.customer = b.customer_name set b.atrasado = 0 where a.customer not in (Select customer from `tabSales Invoice` where status = 'Overdue' or status = 'Unpaid')")
    frappe.db.sql("update `tabPayment Entry` INNER JOIN (SELECT party, MAX(creation) AS 'tranc_date' FROM `tabPayment Entry` where party_type = 'customer'  AND `tabPayment Entry`.name not like 'AJUSTE%' GROUP BY party) as max_creation ON `tabPayment Entry`.party = max_creation.party AND `tabPayment Entry`.creation = max_creation.tranc_date left JOIN `tabCustomer` b on max_creation.party = b.customer_name set b.latest_payment = `tabPayment Entry`.name, b.date_latest_payment = `tabPayment Entry`.creation ")
    frappe.db.sql("update `tabPayment Entry` INNER JOIN (SELECT party, MAX(creation) AS 'tranc_date' FROM `tabPayment Entry` where party_type = 'supplier'  AND `tabPayment Entry`.name not like 'AJUSTE%' GROUP BY party) as max_creation ON `tabPayment Entry`.party = max_creation.party AND `tabPayment Entry`.creation = max_creation.tranc_date left JOIN `tabSupplier` b on max_creation.party = b.supplier_name set b.latest_payment = `tabPayment Entry`.name, b.date_latest_payment = `tabPayment Entry`.creation ")

@frappe.whitelist()
def factura_global():
	frappe.db.sql("UPDATE `tabCFDI` set grand_total = total")

@frappe.whitelist()
def sin_timbrar():
	frappe.db.sql("UPDATE `tabSales Invoice` set sin_timbrar = DATEDIFF(CURDATE(), creation) where cfdi_status='Sin Timbrar'")

@frappe.whitelist()
def nuevas_facturas():
	anteriores = frappe.db.sql("""SELECT name,creation,date_sub(NOW(),INTERVAL 5 HOUR),TIMESTAMPDIFF(HOUR,creation,date_sub(NOW(),INTERVAL 5 HOUR)) FROM `tabSales Invoice` WHERE docstatus = %s AND TIMESTAMPDIFF(HOUR,creation,date_sub(NOW(),INTERVAL 5 HOUR)) > 24""", (0), as_dict=1)
	for a in anteriores:
	    frappe.db.sql("""UPDATE `tabSales Invoice` SET docstatus = 2, observaciones ='Factura cancelada por tiempo de espera excedido'  WHERE name =%s""",(a.name),as_dict=1)

@frappe.whitelist()
def genera_cotizacion(name='PUR-SQTN-2021-00001'):
	si = frappe.get_doc('Supplier Quotation', name)
	articulosproveedor = si.items
	articulosventa = {}
	margen = si.margen

    #return
	frappe.errprint(margen)
	doc = frappe.new_doc('Quotation')
	articulosventa = doc.items
	for a in articulos:
		a.item_code
		a.amount = a.amount*margen
		a.valuation_rate = a.rate
		for b in articulosventa:
			b.item_code = a.item_code
			b.amount = a.amount*margen
	doc.save()
	frappe.msgprint('Cotizacion Generada')


    #     doc.append("items", {
    #         "item_code": si.items[0].item_code ,
    #         "qty": 1,
    #         "precio_de_venta": si.monto / 1.16,
    #         "monto": si.monto / 1.16,
    #         "precio_unitario_neto": si.monto / 1.16,
    #         "precio_neto": si.monto / 1.16,
    #         "tax": 16,
    #         "impuestos_totales": (si.monto / 1.16) * 0.16
    #     })
	#
    #     doc.append("si_sustitucion", {
    #         "tipo_documento": "Sales Invoice" ,
    #         "sales_invoice": si.name,
    #         "uuid": si.uuid,
    #         "valor": si.monto
    #     })
	#
	#
	#
@frappe.whitelist()
def boton(name):
	pos = frappe.get_doc('POS Invoice', name)
	doc = frappe.new_doc('Sales Invoice')
	doc.items = pos.items
	doc.customer = pos.customer
	doc.perfil_facturacion = 'TICKET'
	doc.is_pos = 1
	doc.update_stock = 1
	doc.naming_series = 'TICKET'
	doc.append("payments", {
		"mode_of_payment": 'Efectivo',
		"account": '101.01 - Caja y efectivo - SAT',
		"amount": pos.grand_total,
		"type": 'Cash',
		"base_amount": pos.base_grand_total
	})
	doc.save()
	doc.submit()
	frappe.errprint(doc.name)




@frappe.whitelist()
def update_payment_entry(name):
	doc = frappe.get_doc('Payment Entry',name)
	references = doc.references
	gran_total_original = 0
	for r in references:
		si = frappe.get_doc('Sales Invoice', r.reference_name)
		gran_total_original += round(si.monto_pendiente, 2)
		frappe.db.set_value("Payment Entry Reference", r.name, 'monto_pendiente', si.monto_pendiente)
	#frappe.db.set_value("Payment Entry", doc.name, 'total_original', gran_total_original)
	frappe.errprint(gran_total_original)


@frappe.whitelist()
def saldos_cero():
	frappe.db.sql("""update  `tabGL Entry` a LEFT JOIN `tabPayment Entry` b ON a.voucher_no = b.name SET a.credit_in_account_currency = 0 , a.credit = 0 where b.unallocated_amount = a.credit_in_account_currency AND b.unallocated_amount = a.credit AND b.unallocated_amount > 0 AND b.docstatus = 1""")
	frappe.db.sql("""update `tabSales Invoice` SET outstanding_amount = 0 WHERE outstanding_amount < 0""")

@frappe.whitelist()
def crear_pago(name):
	doc = frappe.get_doc('CFDI Nota de Credito',name)
	cliente = frappe.get_doc('Customer',doc.customer)
	today = date.today()
	frappe.errprint(doc.name)
	frappe.errprint(doc.conversion_rate)

	pii = frappe.new_doc("Payment Entry")
	pii.mode_of_payment = 'Transferencia bancaria'
	# pii.payment_type = 'Pay'
	pii.party_type = 'Customer'
	pii.party = doc.customer
	pii.posting_date = today.strftime("%Y-%m-%d") #Daniel Acosta: Estaba mostrando un error de Fiscal Year al generar el payment entry

	# if doc.forma_de_pago != '01':
	# 	pii.paid_from = company.default_cash_account
	# else:
	# 	pii.paid_from = company.default_bank_account

	#pii.paid_to = company.default_receivable_account #frappe.get_value("Company",doc.company,'default_receivable_account')
	# pii.paid_to_account_currency = doc.currency
	# pii.paid_to  = doc.paid_to
	pii.reference_no = doc.name
	pii.naming_series = 'NC-'
	# RG - Los clientes con currency != MXN solo pueden hacaer transacciones en su moneda nativa (ej. USD)
	# RG - Los clientes sin default_currency o con MXN pueden transaccionar en cualquier moneda
	# RG - Los payment entries derivados de los descuentos automaticos NO podran timbrarse.
	pii.paid_amount = float(doc.total) * float(doc.conversion_rate)
	pii.source_exchange_rate = 1
	pii.target_exchange_rate = 1
	pii.received_amount = float(doc.total) * float(doc.conversion_rate)
	company = frappe.get_doc('Company', pii.company)
	pii.paid_to = '102.01 - Bancos nacionales - ' + company.abbr
	# frappe.errprint(float(doc.total) * float(doc.conversion_rate))
	for i in doc.si_sustitucion:
		pii.append('references', {
			'reference_doctype': 'Sales Invoice',
			'reference_name': i.sales_invoice,
			'allocated_amount': float(i.valor) * float(doc.conversion_rate),
			'pagado': float(i.valor) * float(doc.conversion_rate),#cambio hecho por Santiago
		})

	pii.flags.ignore_permissions = True
	pii.flags.ignore_mandatory = True
	frappe.errprint(pii.party)
	frappe.errprint(pii.paid_to)
	# pii.flags.ignore_validate = True
	pii.submit()
	frappe.db.set_value("CFDI Nota de Credito", name, 'pago', pii.name)
	doc.pago = pii.name
	frappe.msgprint('Devolucion monetaria generada : '  + '<a href="#Form/Payment Entry/' + pii.name + '"target="_blank">' + pii.name + '</a>'  )
	doc.reload()

@frappe.whitelist()
def create_stock_entry(name):
	doc = frappe.get_doc('CFDI Nota de Credito',name)
	if doc.tipo_de_factura == "Devolucion":
		pii = frappe.new_doc("Stock Entry")
		pii.stock_entry_type = "Material Receipt"
		pii.naming_series = "STE-"
		for i in doc.items:
			pii.append('items', {
				'item_code': i.item_code,
				'qty': i.qty,
				'uom': i.stock_uom,
				't_warehouse': i.warehouse,
			})
		pii.flags.ignore_permissions = True
		pii.submit()
		frappe.msgprint('Devolucion de Inventario generada : '  + '<a href="#Form/Stock Entry/' + pii.name + '"target="_blank">' + pii.name + '</a>'  )
	frappe.errprint('HECHO')

# RG - Crear Pago
@frappe.whitelist()
def cancelar_pago(name):
	doc = frappe.get_doc('CFDI Nota de Credito', name)
	pii = frappe.get_doc('Payment Entry', doc.pago)
	pii.cancel()

@frappe.whitelist()
def quitar_tags_item_description():
	frappe.db.sql("""update `tabSales Order Item` set description = (replace(description,'<div class="ql-editor read-mode"><p>',''))""")
	frappe.db.sql("""update `tabSales Order Item` set description = (replace(description,'</p></div>',''))""")
	frappe.db.sql("""update `tabSales Order Item` set description = (replace(description,'</p><p>',' '))""")
	frappe.db.sql("""update `tabSales Invoice Item` set description = (replace(description,'<div class="ql-editor read-mode"><p>',''))""")
	frappe.db.sql("""update `tabSales Invoice Item` set description = (replace(description,'</p></div>',''))""")
	frappe.db.sql("""update `tabSales Invoice Item` set description = (replace(description,'<div><p>',''))""")
	frappe.db.sql("""update `tabSales Invoice Item` set description = (replace(description,'</p><p>',' '))""")
	frappe.db.sql("""update `tabSales Invoice Item` set description = (replace(description,'<br>',''))""")
	frappe.db.sql("""update `tabDelivery Note Item` set description = (replace(description,'<div class="ql-editor read-mode"><p>',''))""")
	frappe.db.sql("""update `tabDelivery Note Item` set description = (replace(description,'</p></div>',''))""")
	frappe.db.sql("""update `tabDelivery Note Item` set description = (replace(description,'</p><p>',' '))""")
	frappe.errprint('Tags Eliminados')


@frappe.whitelist()
def quitar_tags_item():
	frappe.db.sql("""update `tabQuotation Item` set description = (replace(description,'<div class="ql-editor read-mode"><p>',''))""")
	frappe.db.sql("""update `tabQuotation Item` set description = (replace(description,'</p></div>',''))""")
	frappe.db.sql("""update `tabQuotation Item` set description = (replace(description,'</p><p>',' '))""")
	frappe.db.sql("""update `tabQuotation Item` set description = (replace(description,'<div><p>',' '))""")
	frappe.db.sql("""update `tabQuotation Item` set description = (replace(description,'<br>',' '))""")
	frappe.db.sql("""update `tabQuotation Item` set description = (replace(description,'<strong>',' '))""")
	frappe.db.sql("""update `tabQuotation Item` set description = (replace(description,'</strong>',' '))""")
	frappe.db.sql("""update `tabSales Order Item` set description = (replace(description,'<div class="ql-editor read-mode"><p>',''))""")
	frappe.db.sql("""update `tabSales Order Item` set description = (replace(description,'</p></div>',''))""")
	frappe.db.sql("""update `tabSales Order Item` set description = (replace(description,'</p><p>',' '))""")

@frappe.whitelist()
def quitar_tags():
	frappe.db.sql("""update `tabPurchase Order Item` set description = (replace(description,'<div class="ql-editor read-mode"><p>',''))""")
	frappe.db.sql("""update `tabPurchase Order Item` set description = (replace(description,'</p></div>',''))""")
	frappe.db.sql("""update `tabPurchase Order Item` set description = (replace(description,'</p><p>',' '))""")
	frappe.db.sql("""update `tabPurchase Order Item` set description = (replace(description,'<strong>',' '))""")
	frappe.db.sql("""update `tabPurchase Order Item` set description = (replace(description,'</strong><strong>',' '))""")


@frappe.whitelist()
def get_chart_data():
	query = """SELECT str_to_date(concat(date_format(`tabSales Invoice`.`posting_date`, '%Y-%m'), '-01'), '%Y-%m-%d') AS `posting_date`, sum(`tabSales Invoice`.`base_grand_total`) AS `sum`
FROM `tabSales Invoice`
WHERE (`tabSales Invoice`.`docstatus` = 1
   AND  `tabSales Invoice`.`metodo_pago` = 'PPD' AND DATE(`tabSales Invoice`.`posting_date`) >= '2021-04-01')
GROUP BY str_to_date(concat(date_format(`tabSales Invoice`.`posting_date`, '%Y-%m'), '-01'), '%Y-%m-%d')
ORDER BY str_to_date(concat(date_format(`tabSales Invoice`.`posting_date`, '%Y-%m'), '-01'), '%Y-%m-%d') ASC
	"""
	data = frappe.db.sql(query, as_list=1)

	datasets = []
	labels = []
	for d in data:
		labels.append(d[0])
		datasets.append(d[1])

	query2 = """SELECT str_to_date(concat(date_format(`tabPayment Entry`.`posting_date`, '%Y-%m'), '-01'), '%Y-%m-%d') AS `creation`, sum(`tabPayment Entry`.`paid_amount`) AS `sum`
FROM `tabPayment Entry`
WHERE `tabPayment Entry`.`docstatus` = 1 AND `tabPayment Entry`.`payment_type` = 'Receive'
GROUP BY str_to_date(concat(date_format(`tabPayment Entry`.`posting_date`, '%Y-%m'), '-01'), '%Y-%m-%d')
ORDER BY str_to_date(concat(date_format(`tabPayment Entry`.`posting_date`, '%Y-%m'), '-01'), '%Y-%m-%d') ASC
"""
	data2 = frappe.db.sql(query2, as_list=1)

	datapoints = []
	labels2 = []
	for d in data2:
		labels2.append(d[0])
		datapoints.append(d[1])

	return{
		"labels": labels,
		"datasets": [{
			"name": _("Ventas a Credito"),
			"values": datasets,
			"chartType": 'bar'
		},
		{
			"name": _("Pagos"),
			"values": datapoints,
			"chartType": 'line'
		}],
		"type": "axis-mixed"
	}


@frappe.whitelist()
def pi_monto_pendiente(name):
	pi = frappe.get_doc('Purchase Invoice',name)
	frappe.db.set_value("Purchase Invoice",name, 'monto_pendiente', pi.grand_total)

@frappe.whitelist()
def pago_proveedor_usd(name):
    pe = frappe.get_doc('Payment Entry',name)
    if pe.company == 'Sillas and Chairs':
        per = frappe.get_list('Payment Entry Reference', filters={
    'parent': pe.name})
        for r in per:
            frappe.db.set_value("Purchase Invoice",r, 'monto_pendiente', pe.paid_amount)


@frappe.whitelist()
def restore_monto_pendiente(name):
	doc = frappe.get_doc('Payment Entry',name)
	for i in doc.references:
		frappe.db.set_value('Sales Invoice',i.reference_name,'monto_pendiente',i.monto_pendiente)
		frappe.errprint(i.reference_name)
		frappe.errprint(i.monto_pendiente)

@frappe.whitelist()
def clave(name):
    numero = frappe.db.sql("""SELECT max(clave) + 1 as "clave" from `tabCustomer` ORDER BY creation desc """)
    c = frappe.get_doc('Customer', name)
    if c.clave is None:
        frappe.db.set_value("Customer", c.name, 'clave', numero)
#    frappe.db.sql("""UPDATE `tabCustomer` set cuenta_sat = CONCAT('110410', clave) WHERE cuenta_sat IS null """)
