import numpy as np
from sklearn.ensemble import RandomForestRegressor

_rng = np.random.default_rng(42)
X = []
y = []
for _ in range(1200):
    tariff_change = _rng.uniform(0, 50)
    dependency = _rng.uniform(0.2, 1.0)
    concentration = _rng.uniform(0.2, 1.0)
    product_risk = _rng.uniform(0.2, 1.0)
    score = (
        0.58 * min(tariff_change * 2.0, 100)
        + 0.18 * dependency * 100
        + 0.14 * concentration * 100
        + 0.10 * product_risk * 100
        + _rng.normal(0, 3)
    )
    X.append([tariff_change, dependency, concentration, product_risk])
    y.append(np.clip(score, 0, 100))

MODEL = RandomForestRegressor(n_estimators=120, random_state=42, max_depth=8)
MODEL.fit(X, y)

def predict_exposure(features):
    row = [[
        features["tariff_change"],
        features["dependency"],
        features["supplier_concentration"],
        features["product_risk"],
    ]]
    return float(np.clip(MODEL.predict(row)[0], 0, 100))

def explain_exposure(result):
    bullets = []
    if result["tariff_change"] > 0:
        bullets.append(
            f"The scenario raises the tariff by {result['tariff_change']:.1f} percentage points, increasing modeled supply-chain exposure."
        )
    elif result["tariff_change"] < 0:
        bullets.append(
            f"The scenario lowers the tariff by {abs(result['tariff_change']):.1f} percentage points, reducing modeled exposure."
        )
    else:
        bullets.append("The scenario keeps the tariff unchanged, so the model shows no tariff-driven shock.")
    if result["exposure_score"] >= 70:
        bullets.append("The model identifies a high simulated exposure level; the component and supplier nodes are the most sensitive.")
    elif result["exposure_score"] >= 40:
        bullets.append("The model identifies a medium simulated exposure level, with effects distributed across the chain.")
    else:
        bullets.append("The model identifies a low simulated exposure level under this scenario.")
    bullets.append(
        f"Estimated product-level cost impact is {result['cost_impact_pct']:.1f}%. This is a scenario estimate, not an official economic forecast."
    )
    return bullets
