"""
Test Dynatrace Provider

Fetches live service entities from Dynatrace and prints normalized services.
"""

from dynatrace_provider import DynatraceProvider


provider = DynatraceProvider()

runtime_reality = provider.get_runtime_reality()

for service in runtime_reality.services:
    print(f"{service['entity_type']} | {service['name']}")
