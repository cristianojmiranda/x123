import os
import requests
from sanic import Sanic
from sanic.response import json
from sanic.response import text

MYSELF_ENDPOINT="http://localhost:8000"
if "ENDPOINT" in os.environ:
    MYSELF_ENDPOINT = os.environ["ENDPOINT"]
print("MYSELF_ENDPOINT=%s" % MYSELF_ENDPOINT)

app = Sanic()

@app.route("/")
async def hello(request):
    return json({"hello": "world"})

def remote_fibb(n):
    resp = requests.get("%s/fibb/%i" % (MYSELF_ENDPOINT, n))
    if resp.status_code == 200:
        return int(resp.text)
    else:
        raise Exception("Failed to compute remote fibb(%i): %i" % (n, resp.status_code))

'''
def F(n):
    if n == 0: return 0
    elif n == 1: return 1
    else: return F(n-1)+F(n-2)
'''
@app.route("/fibb/<n:int>")
async def fibb(request, n):
    print('fibb=%i', n)
    if n == 0: return text("0")
    elif n == 1: return text("1")
    f = remote_fibb(n-1) + remote_fibb(n-2)
    return text(str(f))

@app.route("/health")
async def health(request):
    return text('OK')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=4)
