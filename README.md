A simple example of Opentelemetry for instrumentation of a custom python application metrics.
Is also suports traces but it is not optimized for visualization, just for retrieving in promehteus.
The architecture is the following:

Custom_App -> OTLP Collector -> Prometheus -> Grafana
``` sh
docker compose up --build -d
```
