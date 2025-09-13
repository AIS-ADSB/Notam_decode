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
