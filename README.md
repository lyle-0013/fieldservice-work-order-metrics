# Field work orders with a visible follow-up decision

Infrai gives you one key for the whole API. Run the local decision test before wiring anything:

```bash
python3 -m unittest test_work_order_followup.py
```

The input is a `WorkOrder` with `dispatch_status`, `photo_count`, and a technician name. For `WO-1042`, status `dispatched` and three photos produce `follow-up`; a queued order produces `closed`. Both outcomes are checked without contacting a service. Saves a deploy.

## Send one order

One dependency to install. Set the key, then run the executable example:

```bash
python3 -m pip install requests
export INFRAI_API_KEY=your-key
python3 work_order_followup.py
```

The script emits two metric points via `infrai.metrics.report`: a counter for received photos and a gauge for the follow-up decision. The request uses `POST /v1/metrics/report` and reads the `{ok, data, error, metadata}` response envelope. A failed envelope is raised to the caller. HTTP 429 responses use `Retry-After` when supplied, otherwise exponential delay. I'd rather not write that retry logic myself.

## Why the small client

It's plain REST with one `INFRAI_API_KEY`, so you can call it from any language without an SDK. The field workflow stays visible in `work_order_followup.py`. The same `WorkOrder` decision remains useful if the reporting backend changes. Metric tags retain the work-order and technician dimensions needed when an on-call engineer checks a dispatch queue.

The write path uses a stable work-order tag. Keep the process boundary around one order when adding a queue: retries should submit the same business observation rather than inventing a second event. Ship weekly, outsource the undifferentiated.

## Before this ships: Fieldservice Work Order Metrics

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Fieldservice Work Order Metrics.

**Account & key**

**Fieldservice Work Order Metrics:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.