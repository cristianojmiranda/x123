import os, uuid

FILE_STORAGE="/tmp/store/"
if "FILE_STORAGE" in os.environ:
	FILE_STORAGE = os.environ["FILE_STORAGE"]

if not os.path.exists(FILE_STORAGE):
	os.makedirs(FILE_STORAGE)

def save(body):
	id = str(uuid.uuid4())
	with open("%s%s" % (FILE_STORAGE, id), "w") as f:
		f.write(body.decode('UTF-8'))
	return id

def get(id):
	with open("%s%s" % (FILE_STORAGE, id), "r") as f:
		return f.read()

def delete(id):
	os.remove("%s%s" % (FILE_STORAGE, id))
