# JSON → PostgreSQL Sync (DSEG / PRU / SH / SV)

Batch synchronization tool that ingests JSON files into PostgreSQL, applying domain-specific UPSERT logic per dataset type (DSEG, PRU, SH, SV).

---

## 🇧🇷 Sincronização JSON → PostgreSQL (DSEG / PRU / SH / SV)

Ferramenta de sincronização em lote que ingere arquivos JSON no PostgreSQL, aplicando lógica de INSERT/UPDATE por tipo de dado (DSEG, PRU, SH, SV).

---

## What it does

- Reads all `.json` files from an input folder
- Detects dataset type from the filename prefix: `DSEG_*.json`, `PRU_*.json`, `SH_*.json`, `SV_*.json`
- For each item in the JSON array:
  - Runs a `SELECT` to check whether the record exists
  - If found: performs an `UPDATE`
  - If not found: performs an `INSERT`
- Applies specific business rules for some datasets (e.g., prevent overwriting newer records)

## Project Structure
```
json-to-postgres-sync/
├── README.md
├── .gitignore
├── config.example.env
├── data/
│ ├── input/
│ └── samples/
└── src/
├── main.py
└── db/
├── disp_seg_db.py
├── pru_db.py
├── horizontal_db.py
└── vertical_db.py
```

## Install dependencies
```
pip install psycopg2-binary python-decouple
```