# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import frappe
import jwt
import time


@frappe.whitelist()
def get_url():
	METABASE_SITE_URL = 'http://159.89.182.18:3000'
	METABASE_SECRET_KEY = '22a34686885d066793e0e4fc8f607a4ab9626f32e073085f073c95b092d9b7b4'

	payload = {
		'resource': {'dashboard': 234},
		'params': {},
		'exp': round(time.time()) + (60 * 10)  # 10 minute expiration
	}
	token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm='HS256')

	iframeUrl = METABASE_SITE_URL + '/embed/dashboard/' + token.decode('utf8') + '#bordered=true&titled=false'

	return iframeUrl
