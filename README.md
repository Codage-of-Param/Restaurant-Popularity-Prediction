# Restaurant Popularity Prediction (Zomato)

This repo contains a training notebook/script (`Final_RP.ipynb`, `Final_RP.py`) and saved artifacts (`model.pkl`, `encoders.pkl`).

## Dashboard UI (Streamlit)

Run the UI:

```powershell
pip install -r requirements.txt
streamlit run app.py
```

The app loads `model.pkl` + `encoders.pkl` from the project folder. If you want it to auto-download from Supabase Storage on startup, set:

- `SUPABASE_BUCKET` (your Storage bucket name)
- optional `SUPABASE_ARTIFACT_PREFIX` (folder inside the bucket)

## Supabase connection

This project includes a small helper to connect to Supabase (Postgres + Storage) from Python.
This setup is **Storage-only** (artifact sync).

### 1) Install dependencies

```powershell
pip install -r requirements.txt
```

### 2) Configure environment variables

- Copy `.env.example` to `.env`
- Fill in:
  - `SUPABASE_URL`
  - `SUPABASE_SERVICE_ROLE_KEY` (recommended for scripts; keep secret)

If your bucket is public and you only need public reads/writes, you can use `SUPABASE_ANON_KEY` instead.

### 3) Upload/download artifacts (Supabase Storage)

Create a Storage bucket in Supabase (example: `ml-artifacts`), then:

```powershell
python sync_supabase.py upload-artifacts --bucket ml-artifacts
python sync_supabase.py upload-artifacts --bucket ml-artifacts --prefix runs/2026-04-19
```

Download:

```powershell
python sync_supabase.py download-artifacts --bucket ml-artifacts
python sync_supabase.py download-artifacts --bucket ml-artifacts --prefix runs/2026-04-19
```
