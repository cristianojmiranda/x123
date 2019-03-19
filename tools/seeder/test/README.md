# seeder test

## Start docker-compose

 ```
 docker-compose up
 ```

## Test

Seed to consul
```
curl -i -XPOST -H "Content-Type: multipart/form-data" -F "file=@test.yaml" http://localhost:8000/seed/consul/spring
```

Seed vault
```
curl -i -XPOST -H "Content-Type: multipart/form-data" -F "file=@test.yaml" http://localhost:8000/seed/vault/spring
```
