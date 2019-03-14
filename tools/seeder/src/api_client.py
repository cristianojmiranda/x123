import os
import requests

API_URL="http://localhost:8000"
if "API_URL" in os.environ:
	API_URL = os.environ["API_URL"]

def get_file(id):
	resp = requests.get("%s/storage/file/%s" % (API_URL, id))
	return resp.text

def delete_file(id):
	resp = requests.delete("%s/storage/file/%s" % (API_URL, id))
	return resp.text
