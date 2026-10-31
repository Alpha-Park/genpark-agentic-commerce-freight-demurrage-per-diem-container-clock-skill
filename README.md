# genpark-agentic-commerce-freight-demurrage-per-diem-container-clock-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Ocean port marine terminal demurrage and ocean carrier per diem detention fee avoidance clock.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `track_container_demurrage_detention_clock`
- **Category**: `agentic_commerce`

### Method Documentation
Track ocean container free time expiration and compute progressive tiered demurrage (port storage) & per diem detention fees.
Computes Last Free Day (LFD), daily compounding escalating penalty schedules (e.g. Days 1-4 $150, Days 5-9 $275, Days 10+ $450),
weekend/gate-closure carveouts, and priority haulage dispatch queue.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "track_container_demurrage_detention_clock",
    "arguments": {
    "containers": [
        {
            "container_id": "MSKU9284102",
            "demurrage_last_free_day": 8,
            "detention_last_free_day": 14,
            "port_picked_up": false,
            "empty_returned": false
        },
        {
            "container_id": "CMAU7310491",
            "demurrage_last_free_day": 6,
            "detention_last_free_day": 12,
            "port_picked_up": true,
            "empty_returned": false
        },
        {
            "container_id": "TGHU4198273",
            "demurrage_last_free_day": 12,
            "detention_last_free_day": 18,
            "port_picked_up": false,
            "empty_returned": false
        }
    ],
    "current_day_index": 10
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
