"""
Test Dynatrace Metrics Discovery

Purpose:
Discover available Dynatrace metrics related to services, response time,
failure rate, errors, and requests.

This is a discovery script only.
It does not participate in assurance decisions.
"""

from dynatrace_client import DynatraceClient


client = DynatraceClient()

metric_keywords = [
    "service",
    "response",
    "failure",
    "error",
    "request",
]

for keyword in metric_keywords:
    print("\n" + "=" * 80)
    print(f"Searching metrics for keyword: {keyword}")
    print("=" * 80)

    response = client.get_metrics(
        metric_selector=keyword,
        page_size=20,
    )

    for metric in response.get("metrics", []):
        metric_id = metric.get("metricId")
        display_name = metric.get("displayName")

        print(f"{metric_id} | {display_name}")
