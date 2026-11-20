# Carpool Connect — Streamlit demo

## Run in Antigravity / VS Code (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Open http://localhost:8501.

If PowerShell blocks virtual-environment activation, skip activation and run:
```powershell
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Optional Flask API:
```powershell
python app.py
```
Then open http://127.0.0.1:5000/api/stats.

Tests:
```powershell
python -m unittest test_matcher.py
```

## Important
This is a self-contained runnable reconstruction because only the old `app.py` was available; the original `matcher/` package was not included. The matching engine here is an illustrative replacement based on proximity, schedule and common commute days. It does not preserve or reproduce the unavailable original algorithm. New commuter registrations last only for the current Streamlit session; there is no persistent database or live map routing.
