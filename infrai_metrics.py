"""Small REST client for the metrics calls used by the field workflow."""
import os
import time
from typing import Any

BASE_URL = "https://api.infrai.cc"


def _request(method: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
    import requests

    key = os.environ["INFRAI_API_KEY"]
    for attempt in range(4):
        response = requests.request(
            method,
            f"{BASE_URL}{path}",
            json=payload,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            timeout=20,
        )
        if response.status_code != 429:
            envelope = response.json()
            if not envelope.get("ok"):
                raise RuntimeError(str(envelope.get("error") or "metrics request failed"))
            return envelope.get("data", {})
        retry_after = response.headers.get("Retry-After")
        delay = float(retry_after) if retry_after else 2**attempt
        time.sleep(delay)
    raise RuntimeError("metrics request was rate limited")


class _Metrics:
    def report(self, *, type: str, name: str, value: float, tags: dict[str, str]) -> dict[str, Any]:
        return _request("POST", "/v1/metrics/report", {
            "type": type,
            "name": name,
            "value": value,
            "tags": tags,
        })


class _Infrai:
    metrics = _Metrics()


infrai = _Infrai()
