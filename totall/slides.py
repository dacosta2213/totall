from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import requests

import pickle
import os.path
from frappe.utils import get_request_site_address
import requests

from google_auth_oauthlib.flow import InstalledAppFlow

import json

# AG - 24 Sep 2020 - SCOPES contiene los permisos a solicitar al momento de generar las keys en GSlide Config
# AUTHORIZATION_BASE_URL contiene la url donde se realizara la solicitud de los accesos
SCOPES = 'https://www.googleapis.com/auth/presentations '+'https://www.googleapis.com/auth/drive' # AG - 24 Sep 2020 - Para saber que Scope usar, consultar las librerias de goole api
AUTHORIZATION_BASE_URL = "https://www.googleapis.com/oauth2/v4/token"

# RG - 17Sep20 - Lo saque de mi API CONSOLE - https://console.developers.google.com/apis/credentials/key/a3a846ca-75dd-404a-91d8-6753bcf8444d?authuser=0&project=gslides-totall-1600372998169

# AG - 24 Sep 2020 - URL's donde se buscara el archivo o presentacion
PRESENTATION = 'https://slides.googleapis.com/v1/presentations/'
DRIVE = 'https://www.googleapis.com/drive/v2/files/'

# AG - 24 Sep 2020 - Token utiliza cliente id y secret para obtener los accesos token del api de google
@frappe.whitelist()
def token(code=None, state=None, account=None):
    CLIENT_ID = frappe.db.get_single_value('GSlides Config', 'client_id')
    CLIENT_SECRET = frappe.db.get_single_value('GSlides Config', 'client_secret')
    redirect_uri = get_request_site_address(True) + "?cmd=totall.slides.token"
    if code is None:
        # AG - 24 Sep 2020 - Se autentica para obtener code y redirecciona a redirect_uri para volver a correr token
        return { 'url': 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&response_type=code&prompt=consent&client_id={}&include_granted_scopes=true&scope={}&redirect_uri={}'.format(CLIENT_ID, SCOPES, redirect_uri) }
    else:
        try:
            data = {'code': code,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET ,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'}
            # AG - 24 Sep 2020 - envia los datos para obtener los claves token
            r = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data).json()
            frappe.db.set_value("GSlides Config", "GSlides Config", "authorization_code", code)
            if 'access_token' in r:
                frappe.db.set_value("GSlides Config", "GSlides Config", "access_token", r['access_token'])
            if 'refresh_token' in r:
                frappe.db.set_value("GSlides Config", "GSlides Config", "refresh_token", r['refresh_token'])
            frappe.db.commit()
            frappe.local.response["type"] = "redirect"
            frappe.local.response["location"] = "exito.html"
            return
        except Exception as e:
            frappe.throw(e.message)

@frappe.whitelist()
def retrieve_tokens(refresh_token):
    # AG - 24 Sep 2020 - Recibe el refresh_token de la configuracion para obtener un nuevo acces token
    CLIENT_ID = frappe.db.get_single_value('GSlides Config', 'client_id')
    CLIENT_SECRET = frappe.db.get_single_value('GSlides Config', 'client_secret')
    redirect_uri = "https://"+frappe.local.site+"?cmd=totall.slides.retrieve_tokens"

    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }

    body_ref = {
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET,
        'refresh_token': refresh_token,
        "grant_type": "refresh_token",
    }

    # AG - 24 Sep 2020 - Envia el JSON para solicitar un acces token
    r = requests.post(AUTHORIZATION_BASE_URL, data=json.dumps(body_ref),headers=headers)
    data = r.json().get('access_token')
    return data

@frappe.whitelist()
def gs_conection(name=None):
    gslides_config = frappe.get_doc('GSlides Config')
    presentation_id = gslides_config.presentation_id
    refresh_token = gslides_config.refresh_token

    doctype = None if not gslides_config.tipo else gslides_config.tipo
    # AG - 24 Sep 2020 - Se utiliza apra validar si la llamada se esta haciendo o no desde un doctype
    doc = None
    if doctype:
        doc = frappe.get_doc(doctype,name)

    # AG - 24 Sep 2020 - Envia Refresh token para obtener acces token
    access_token = retrieve_tokens(refresh_token)
    authorization_header = {"Authorization": "OAuth %s" % access_token}

    body  = {
        "title": "Prueba Python"
    }

    # AG - 24 Sep 2020 - Crea copia de la presentacion registrada en la configuracion y Obtiene el id de la copia
    file = requests.post(DRIVE+presentation_id+'/copy',data=json.dumps(body),headers=authorization_header)
    # frappe.errprint(str(file.text))
    new_presentation_id = json.loads(file.text)['id']

    print('https://docs.google.com/presentation/d/'+new_presentation_id)

    body={
        "requests":[]
    }

    # AG - 24 Sep 2020 - Crea y adjunta los registros a modificar en la presentacion, obteniendo la infromacion
    # de un doctype o directamente de la tabla de configuracion, segun sea el caso.
    if doc:
        for item in gslides_config.items:
            replacetext = frappe.db.get_value(doctype,name,item.text)
            frappe.errprint(replacetext)
            value = {
                "replaceAllText":{
                    "containsText":{
                        "text": item.replacetext
                    },
                    "replaceText": str(replacetext)
                }
            }
            frappe.errprint(value)
            body['requests'].append(value)
    else:
        for item in gslides_config.items:
            value = {
                "replaceAllText":{
                    "containsText":{
                        "text": item.replacetext
                    },
                    "replaceText": item.text
                }
            }
            body['requests'].append(value)

    frappe.errprint(body)
    pres = 'https://docs.google.com/presentation/d/'+new_presentation_id
    # AG - 24 Sep 2020 - Realiza el envio de informacion a actualizar en la copia de presentacion
    p = requests.post(PRESENTATION+new_presentation_id+':batchUpdate',data=json.dumps(body),headers=authorization_header)
    frappe.msgprint('Presentacion modificada. <a href="' + pres + '"> Descargar .</a>')
    return

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('slides', 'v1', credentials=creds)

    # Call the Slides API
    presentation = service.presentations().get(presentationId=PRESENTATION_ID).execute()
    slides = presentation.get('slides')

    print('The presentation contains {} slides:'.format(len(slides)))
    for i, slide in enumerate(slides):
        print('- Slide #{} contains {} elements.'.format(
            i + 1, len(slide.get('pageElements'))))
