# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import frappe
import json
from frappe import _
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from frappe.model.document import Document
from frappe.utils import get_request_site_address
import requests
import time
from frappe.utils.background_jobs import get_jobs

if frappe.conf.developer_mode:
	import os
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = 'https://www.googleapis.com/auth/calendar'
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
CLIENT_ID = '380746168163-cgt91c8pggd3oa1m6hkpii0vfqrbjipv.apps.googleusercontent.com'
CLIENT_SECRET = 'ZvQXGkSJcB6JKsZNbGbqeLom'

@frappe.whitelist()
def google_callback(code=None, state=None, account=None):
    redirect_uri = get_request_site_address(True) + "?cmd=totall.gcal.google_callback"
    if code is None:
        return { 'url': 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&response_type=code&prompt=consent&client_id={}&include_granted_scopes=true&scope={}&redirect_uri={}'.format(CLIENT_ID, SCOPES, redirect_uri) }
    else:
        try:
            data = {'code': code,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET ,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'}
            r = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data).json()
            frappe.db.set_value("GCalendar Config", None, "authorization_code", code)
            if 'access_token' in r:
                frappe.db.set_value("GCalendar Config", None, "access_token", r['access_token'])
            if 'refresh_token' in r:
                frappe.db.set_value("GCalendar Config", None, "refresh_token", r['refresh_token'])
            frappe.db.commit()
            frappe.local.response["type"] = "redirect"
            frappe.local.response["location"] = "/integrations/gcal-exito.html"
            return
        except Exception as e:
            frappe.throw(e.message)

@frappe.whitelist()
def refresh_token(token):
	if 'refresh_token' in token:
		frappe.db.set_value("GCalendar Config", None, "refresh_token", token['refresh_token'])
		frappe.db.set_value("GCalendar Settings", None, "refresh_token", token['refresh_token'])
	if 'access_token' in token:
		frappe.db.set_value("GCalendar Settings", None, "session_token", token['access_token'])
	frappe.db.commit()
#
#
# class GCalendarSettings(Document):
# 	def sync(self):
# 		"""Create and execute Data Migration Run for GCalendar Sync plan"""
# 		frappe.has_permission('GCalendar Settings', throw=True)
#
#
# 		accounts = frappe.get_all("GCalendar Account", filters={'enabled': 1})
#
# 		queued_jobs = get_jobs(site=frappe.local.site, key='job_name')[frappe.local.site]
# 		for account in accounts:
# 			job_name = 'google_calendar_sync|{0}'.format(account.name)
# 			if job_name not in queued_jobs:
# 				frappe.enqueue('frappe.integrations.doctype.gcalendar_settings.gcalendar_settings.run_sync', queue='long', timeout=1500, job_name=job_name, account=account)
# 				time.sleep(5)
#
# 	def get_access_token(self):
# 		if not self.refresh_token:
# 			raise frappe.ValidationError(_("GCalendar is not configured."))
# 		data = {
# 			'client_id': self.client_id,
# 			'client_secret': self.get_password(fieldname='client_secret',raise_exception=False),
# 			'refresh_token': self.get_password(fieldname='refresh_token',raise_exception=False),
# 			'grant_type': "refresh_token",
# 			'scope': SCOPES
# 		}
# 		try:
# 			r = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data).json()
# 		except requests.exceptions.HTTPError:
# 			frappe.throw(_("Something went wrong during the token generation. Please request again an authorization code."))
# 		return r.get('access_token')
#
# @frappe.whitelist()
# def sync():
# 	try:
# 		gcalendar_settings = frappe.get_doc('GCalendar Settings')
# 		if gcalendar_settings.enable == 1:
# 			gcalendar_settings.sync()
# 	except Exception:
# 		frappe.log_error(frappe.get_traceback())
#
# def run_sync(account):
# 	exists = frappe.db.exists('Data Migration Run', dict(status=('in', ['Fail', 'Error'])))
# 	if exists:
# 		failed_run = frappe.get_doc("Data Migration Run", dict(status=('in', ['Fail', 'Error'])))
# 		failed_run.delete()
#
# 	started = frappe.db.exists('Data Migration Run', dict(status=('in', ['Started'])))
# 	if started:
# 		return
#
# 	try:
# 		doc = frappe.get_doc({
# 			'doctype': 'Data Migration Run',
# 			'data_migration_plan': 'GCalendar Sync',
# 			'data_migration_connector': 'Calendar Connector-' + account.name
# 		}).insert()
# 		try:
# 			doc.run()
# 		except Exception:
# 			frappe.log_error(frappe.get_traceback())
# 	except Exception:
# 		frappe.log_error(frappe.get_traceback())


@frappe.whitelist()
def ping():
    return 'pong'

@frappe.whitelist()
def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            print('antes de creds')
            # creds = flow.run_local_server(port=0)
            creds = flow.authorize
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    frappe.msgprint('Obteniendo los proximos 10 eventos')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        frappe.msgprint('No hay eventos.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        frappe.msgprint(start, event['summary'])

if __name__ == '__main__':
    main()
