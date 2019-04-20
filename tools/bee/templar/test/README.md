# template test


Insert template
```
curl -i -X POST http://localhost:8000/1 -d 'Hello {{name}}'
curl -i -X POST http://localhost:8000/2 -d 'Hello {{name}} {{#templar 1 this }}{{/templar}}'
```

Compile template
```
curl -i -X POST http://localhost:8000/1/compile -d '{"name": "jorel"}'
curl -i -X POST http://localhost:8000/2/compile?version=2 -d '{"name": "jorel"}'
```
