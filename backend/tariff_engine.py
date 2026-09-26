import math
from backend.model import predict_exposure

PRODUCTS = {
    "Electronics": {"dependency": 0.88, "supplier_concentration": 0.72, "risk": 0.80},
    "Automotive Components": {"dependency": 0.76, "supplier_concentration": 0.78, "risk": 0.75},
    "Textiles": {"dependency": 0.62, "supplier_concentration": 0.55, "risk": 0.58},
    "Machinery": {"dependency": 0.70, "supplier_concentration": 0.64, "risk": 0.67},
}

def analyze_scenario(product, origin, market, current_tariff, new_tariff):
    p = PRODUCTS[product]
    delta = new_tariff - current_tariff
    change = max(delta, 0)

    base_features = {
        "tariff_change": 0,
        "dependency": p["dependency"],
        "supplier_concentration": p["supplier_concentration"],
        "product_risk": p["risk"],
    }
    scenario_features = dict(base_features)
    scenario_features["tariff_change"] = change

    baseline = predict_exposure(base_features)
    score = predict_exposure(scenario_features)

    # Transparent scenario estimate for the demo.
    cost_impact = max(0, delta) * (0.35 + 0.65 * p["dependency"]) * 0.55

    supplier = min(100, score * 1.05)
    component = min(100, score * 1.12)
    manufacturer = min(100, score * 0.92)
    market_score = min(100, score * 0.76)

    nodes = [
        {"id": "Supplier", "label": f"{origin}\nSupplier", "score": supplier},
        {"id": "Component", "label": "Component", "score": component},
        {"id": "Manufacturer", "label": "Manufacturer", "score": manufacturer},
        {"id": "Product", "label": product, "score": score},
        {"id": "Market", "label": f"{market}\nMarket", "score": market_score},
    ]
    edges = [
        ("Supplier", "Component"),
        ("Component", "Manufacturer"),
        ("Manufacturer", "Product"),
        ("Product", "Market"),
    ]

    table = [
        {"Node": n["label"].replace("\n", " "), "Exposure": f"{n['score']:.0f}/100"}
        for n in nodes
    ]
    risk = "High" if score >= 70 else "Medium" if score >= 40 else "Low"

    return {
        "product": product, "origin": origin, "market": market,
        "current_tariff": current_tariff, "new_tariff": new_tariff,
        "tariff_change": delta, "cost_impact_pct": cost_impact,
        "baseline_score": round(baseline), "exposure_score": round(score),
        "risk_level": risk, "nodes": nodes, "edges": edges,
        "node_table": table,
    }
