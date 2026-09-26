# TariffGraph AI

TariffGraph AI is a hackathon MVP that demonstrates how a change in an import tariff can create a simulated ripple effect across a supply chain.

## Features
- Interactive Streamlit frontend
- Python backend modules
- Random Forest exposure model
- NetworkX-style supply-chain concept visualized with Plotly
- What-if tariff simulator
- SQLite scenario history
- Demo CSV data

## Important
The included trade relationships and model training data are simulated for demonstration. The exposure score and cost impact are scenario estimates, not official economic forecasts.

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## 2-minute demo
1. Select a product and countries.
2. Set current tariff to 10%.
3. Set scenario tariff to 25%.
4. Click Analyze Impact.
5. Show the exposure score and ripple graph.
6. Change the scenario tariff and run again.
7. Show the saved scenario history.

## Suggested hackathon pitch
"TariffGraph AI turns a tariff percentage into a visual what-if simulation. Instead of looking at a single number, users can see where supply-chain exposure appears, compare scenarios, and understand which nodes are most sensitive."
