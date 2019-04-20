# template test

```

# insert templates
curl -i -X POST http://localhost:8001/1 -d '{{name}}!!!!!!!!!!'
curl -i -X POST http://localhost:8001/2 -d 'Hello {{name}} {{#templar 1 this }}{{/templar}}'

# insert mapa
MAP_ID=$(curl -XPOST http://localhost:8000/mapa -d '{"name": "jorel", "description": "test", "files": [{"templar_id": "2", "file": "test.txt", "path": "generated/src"}]}' | jq -r .id)

# start generation
curl -i -XPOST "http://localhost:8000/mapa/${MAP_ID}/generate" -d '{"name": "jorel"}'

# generate file
curl -i -XPOST "http://localhost:8000/mapa/generate/<map_gen_id>/file/<file_map_id>"

```
