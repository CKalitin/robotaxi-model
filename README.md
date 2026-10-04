# robotaxi-model

Note datasets/NHTS_OD_2022/2022_Passenger_OD_Annual contains a 166 MB CSV that must be unzipped manually. Github only allows up to 100 MB files by default. 

## Repository layout

Each analysis type (currently `NHTS_OD_2022` and `Robotaxi_Rollout`) uses the same name in three top-level folders:

```
datasets/<analysis type>/   input data only (raw downloads, hand-compiled CSVs, source notes)
scripts/<analysis type>/    code only — no generated files
outputs/<analysis type>/    everything scripts generate: chart PNGs and output CSVs, in sub folders
```

Rules:
- Scripts read from `datasets/` and write **only** to `outputs/<analysis type>/<sub folder>/`. Never write generated files into `datasets/` or `scripts/`.
- Scripts create their output sub folders if missing (`mkdir -p` / `os.makedirs(..., exist_ok=True)`).
- Run scripts from the repo root.

| Analysis type | Script | Reads from | Writes to |
|---|---|---|---|
| NHTS_OD_2022 | `scripts/NHTS_OD_2022/NHTS_OD_2022.py` | `datasets/NHTS_OD_2022/2022_Passenger_OD_Annual/2022_Passenger_OD_Annual_Data.csv` | `outputs/NHTS_OD_2022/stacked_bar/` (bar chart), `outputs/NHTS_OD_2022/pie/` (pie per mode), `outputs/NHTS_OD_2022/csv/` (`aggregated_trips.csv`) |
| Robotaxi_Rollout | `scripts/Robotaxi_Rollout/build_charts.py` | `datasets/Robotaxi_Rollout/{tesla,waymo,derived}/` | `outputs/Robotaxi_Rollout/tesla/`, `outputs/Robotaxi_Rollout/waymo/`, `outputs/Robotaxi_Rollout/combined/` |

Note: `datasets/Robotaxi_Rollout/derived/` CSVs are hand-compiled event tables used as script *inputs*, so they live in `datasets/`, not `outputs/`.

### Project Files Links

Notes:
https://docs.google.com/document/d/1G37cJlM2rACQtcB7wmOnEGT0lKtnsdEpgRiEEouOuV0/edit?usp=sharing  

Spreadsheets:  
Robotaxi Model: https://docs.google.com/spreadsheets/d/1nTdDOQ7kkcxMAwEUHepgzQE-93-tq4nVtIKMwDrzJ5o/edit?usp=sharing  
NHTS Data Dictionary: https://docs.google.com/spreadsheets/d/11DQL2-qtj4MR0b3LMLrphWwp9youHuz_/edit?usp=sharing&ouid=113957612591906573119&rtpof=true&sd=true  
