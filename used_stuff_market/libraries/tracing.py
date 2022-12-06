from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.zipkin.proto.http import ZipkinExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from sqlalchemy.engine import Engine

__all__ = ["setup_tracer"]

from container_or_host import host_for_dependency


def setup_tracer(
    service_name: str, app: FastAPI | None = None, engine: Engine | None = None
) -> None:
    zipkin_host = host_for_dependency(addres_for_docker="zipkin")
    resource = Resource(attributes={SERVICE_NAME: service_name})
    zipkin_exporter = ZipkinExporter(endpoint=f"http://{zipkin_host}:9411/api/v2/spans")
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(zipkin_exporter)
    provider.add_span_processor(processor)
    RequestsInstrumentor().instrument()
    if engine is not None:
        SQLAlchemyInstrumentor().instrument(
            engine=engine, enable_commenter=True, commenter_options={}
        )
    else:
        SQLAlchemyInstrumentor().instrument(enable_commenter=True, commenter_options={})

    PymongoInstrumentor().instrument()
    if app is not None:
        FastAPIInstrumentor().instrument_app(app)

    trace.set_tracer_provider(provider)
