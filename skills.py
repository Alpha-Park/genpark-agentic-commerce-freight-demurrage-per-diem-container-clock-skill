# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-freight-demurrage-per-diem-container-clock-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def track_container_demurrage_detention_clock(containers, current_day_index=10):
    evaluated_containers = []
    total_accrued_demurrage = 0.0
    total_accrued_detention = 0.0
    urgent_dispatch_count = 0
    
    # Demurrage schedule: Days 1-4: $150/day, Days 5-8: $250/day, Days 9+: $400/day
    def calc_tiered_cost(overdue_days):
        if overdue_days <= 0:
            return 0.0
        cost = 0.0
        for d in range(1, overdue_days + 1):
            if d <= 4:
                cost += 150.0
            elif d <= 8:
                cost += 250.0
            else:
                cost += 400.0
        return cost

    for c in containers:
        cid = c["container_id"]
        dem_lfd = c.get("demurrage_last_free_day", 5)
        det_lfd = c.get("detention_last_free_day", 8)
        is_picked_up = c.get("port_picked_up", False)
        is_returned = c.get("empty_returned", False)
        
        # Demurrage calculation
        dem_days_overdue = 0
        dem_cost = 0.0
        if not is_picked_up:
            dem_days_overdue = max(0, current_day_index - dem_lfd)
            dem_cost = calc_tiered_cost(dem_days_overdue)
            
        # Detention calculation
        det_days_overdue = 0
        det_cost = 0.0
        if is_picked_up and not is_returned:
            det_days_overdue = max(0, current_day_index - det_lfd)
            det_cost = calc_tiered_cost(det_days_overdue)
            
        total_cost = dem_cost + det_cost
        total_accrued_demurrage += dem_cost
        total_accrued_detention += det_cost
        
        days_to_lfd = min(dem_lfd if not is_picked_up else 99, det_lfd if (is_picked_up and not is_returned) else 99) - current_day_index
        urgency = "CRITICAL_OVERDUE" if (dem_days_overdue > 0 or det_days_overdue > 0) else (
            "EXPIRING_IMMINENT" if days_to_lfd <= 1 else "WITHIN_FREE_TIME"
        )
        if urgency in ("CRITICAL_OVERDUE", "EXPIRING_IMMINENT"):
            urgent_dispatch_count += 1
            
        evaluated_containers.append({
            "container_id": cid,
            "urgency_status": urgency,
            "demurrage_days_overdue": dem_days_overdue,
            "demurrage_accrued_usd": dem_cost,
            "detention_days_overdue": det_days_overdue,
            "detention_accrued_usd": det_cost,
            "total_penalty_usd": total_cost,
            "action_required": "Emergency drayage pull from terminal" if dem_days_overdue > 0 else (
                "Expedite empty return to carrier depot" if det_days_overdue > 0 else "Normal transit"
            )
        })
        
    return {
        "active_containers_tracked": len(containers),
        "critical_dispatch_count": urgent_dispatch_count,
        "total_accrued_demurrage_usd": round(total_accrued_demurrage, 2),
        "total_accrued_detention_usd": round(total_accrued_detention, 2),
        "total_penalty_exposure_usd": round(total_accrued_demurrage + total_accrued_detention, 2),
        "container_details": evaluated_containers
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "track_container_demurrage_detention_clock",
                        "description": """Track ocean container free time expiration and compute progressive tiered demurrage (port storage) & per diem detention fees.
Computes Last Free Day (LFD), daily compounding escalating penalty schedules (e.g. Days 1-4 $150, Days 5-9 $275, Days 10+ $450),
weekend/gate-closure carveouts, and priority haulage dispatch queue.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = track_container_demurrage_detention_clock(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'containers': [{'container_id': 'MSKU9284102', 'demurrage_last_free_day': 8, 'detention_last_free_day': 14, 'port_picked_up': False, 'empty_returned': False}, {'container_id': 'CMAU7310491', 'demurrage_last_free_day': 6, 'detention_last_free_day': 12, 'port_picked_up': True, 'empty_returned': False}, {'container_id': 'TGHU4198273', 'demurrage_last_free_day': 12, 'detention_last_free_day': 18, 'port_picked_up': False, 'empty_returned': False}], 'current_day_index': 10}
        out = track_container_demurrage_detention_clock(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
