# Seeder

 Solution to feed consul and vault kv based on files.

`file(s) > api > splitter > transform/filter > seed`

 ![diagram](diagram.png)

## Build

```
./build.sh
```

## Test

```
svc_pf seed-api 8000 > /deb/null &
curl -i -XPOST -H "Content-Type: multipart/form-data" -F "file=@test.yaml" http://localhost:8000/seed/consul/spring
```
