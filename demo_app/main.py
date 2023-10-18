from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.metrics import Observation, CallbackOptions

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
import random
from time import sleep
from random import randint

traces_demo = False
metrics_demo = True
Console_output = False

# Service name is required for most backends,
# and although it's not necessary for console export,
# it's good to set service name anyways.
resource = Resource(attributes={
    SERVICE_NAME: "DEMO-01-OTLP"
})
if traces_demo:
    tracer_provider = TracerProvider(resource=resource)
    if Console_output:
        processor = BatchSpanProcessor(ConsoleSpanExporter())#sacar a consola
    else:
        processor = BatchSpanProcessor(OTLPMetricExporter(endpoint="localhost:4317", insecure=True),)#sacar a consola
    tracer_provider.add_span_processor(processor)

    # Sets the global default tracer provider
    trace.set_tracer_provider(tracer_provider)

    # Creates a tracer from the global tracer provider
    tracer = trace.get_tracer("example1.tracer.IA")

if metrics_demo:
    #metric
    if Console_output:
        metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter(),export_interval_millis=1000) #sacar métrica a consola
    else:
        metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="localhost:4317", insecure=True),export_interval_millis=50) #sacar métrica a OTLP
    # Sets the global default meter provider
    metric_provider = MeterProvider(resource=resource,metric_readers=[metric_reader])
    metrics.set_meter_provider(metric_provider)

    # Creates a meter from the global meter provider
    meter = metrics.get_meter("example1.meter.IA")

    work_counter = meter.create_counter(
        "example1.counter1", unit="1", description="Counts the amount of inferences done"
    )
    def get_inference_time_callback(options: CallbackOptions):
        yield Observation(random.randrange(start=1,step=1,stop=10))

    work_meter = meter.create_observable_gauge("example1.inferencetime",callbacks=[get_inference_time_callback],unit="m/s",description="tiempo de inferencia de example1")


if traces_demo:
    @tracer.start_as_current_span("example_trace_1_do_work")
    def do_work(work_item):
        # count the work being doing
        work_item.add(1)
        print("doing some work...")
        sleep(randint(1,5))



if __name__ == "__main__":
    while True:
        if traces_demo:
            do_work(work_counter)
        sleep(0.1)