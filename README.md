``` sh
docker-compose up --build
```


For the example:
``` sh
docker run -p 4317:4317 -v otel-collector-config.yaml:/etc/otel/config.yaml otel/opentelemetry-collector-contrib:latest`
```