from sanic import Sanic
from sanic.response import json
from sanic.response import text

app = Sanic()

@app.route("/")
async def hello(request):
    return json({"hello": "world"})

@app.route("/health")
async def health(request):
    return text('OK')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
