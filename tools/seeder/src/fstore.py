import os, uuid

FILE_STORAGE="/tmp/store/"
if "FILE_STORAGE" in os.environ:
	FILE_STORAGE = os.environ["FILE_STORAGE"]

if not os.path.exists(FILE_STORAGE):
	os.makedirs(FILE_STORAGE)

def save(body)
	id = str(uuid.uuid4())
	with pen("%s%s" % (FILE_STORAGE, id), "wb") as f:
		f.write(body)
	return id

def get(id):
	with open("%s%s" % (FILE_STORAGE, id), "rb") as f:
		return file.read()

def delete(id):
	os.remove("%s%s" % (FILE_STORAGE, id))
