import os
import utils
import requests

API_URL=utils.env("API_URL", "http://localhost:8000")

def get_file(id):
	return requests.get("%s/storage/file/%s" % (API_URL, id))

def delete_file(id):
	return requests.delete("%s/storage/file/%s" % (API_URL, id))

def k8s_bounce_app(app):
	return requests.get("%s/k8s/bounce/%s" % (API_URL, app))
