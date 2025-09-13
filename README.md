# NOTAM Decode

This project provides a simple parser and decoder for NOTAM (Notice to Airmen) messages in plain text format.

It extracts structured information from raw NOTAM text, including coordinates, times, and geographical areas, and outputs the data as a JSON file for further analysis or visualization.

## 🔧 Features

- Extracts key NOTAM fields: ID, FIR, coordinates, radius, time, altitude, description, remarks, etc.
- Converts coordinates to decimal degrees.
- Supports point geometry and polygon areas (when sufficient coordinates are provided).
- Outputs results in structured JSON format.
- Designed for further integration into geospatial analysis or airspace monitoring systems.

## 🗂️ Project Structure

- `notam_decoder.py`: Main class for decoding NOTAM text.
- `main.py`: Entry point to load a NOTAM file and save results to JSON.
- `notam_raw.txt`: Example input file containing raw NOTAM text.
- `notam_decoded.json`: Output example file (automatically generated).

#### Explanation:

- `B3810/25 NOTAMN`: NOTAM identifier and status (new NOTAM)
- `Q) RPHI/QWMLW/IV/BO /W /000/999/1238N11644E048`: Q-line with
  - FIR code: `RPHI`
  - NOTAM code: `QWMLW`
  - Traffic type: `IV` (instrument flight rules, IFR and visual)
  - Purpose: `BO` (business operations or other)
  - Scope: `W` (warning)
  - Vertical limits: lower `000` (surface), upper `999` (unlimited)
  - Coordinates & radius: center at 12°38'N, 116°44'E with a radius of 48 nautical miles
- `A) RPHI`: Location ICAO code (airport or FIR)
- `B) 2508241800`: Start time — 24 August 2025, 18:00 UTC
- `C) 2508272100`: End time — 27 August 2025, 21:00 UTC
- `D) 1800-2100`: Daily active time window (local time, 18:00 to 21:00)
- `E) ...`: Description of the NOTAM, indicating special aerospace flight activities conducted by China and estimated fall area for debris with coordinates marking a polygonal area
- `F) SFC`: Lower vertical limit (surface)
- `G) UNL`: Upper vertical limit (unlimited)


Each line corresponds to a field:

- `Q)` Q-line contains FIR, NOTAM code, scope, and center coordinates
- `A)` ICAO location code
- `B)` Start date/time (YYMMDDHHMM format)
- `C)` End date/time (YYMMDDHHMM format)
- `D)` Time period within the day (local time)
- `E)` Description text including any coordinates and notes
- `F)` Lower altitude limit
- `G)` Upper altitude limit

## 🚀 Usage

1. Place your raw NOTAM messages in `notam_raw.txt`.
2. Run `main.py` to decode the NOTAMs and output `notam_decoded.json`.
3. The JSON file will contain structured data, including geographic coordinates in GeoJSON format.

```bash
python main.py
