import re
from bs4 import BeautifulSoup
import json

class NotamDecoder:
    def __init__(self, raw_text):
        self.raw_text = raw_text

    @staticmethod
    def dms_to_decimal(value: str, hemi: str) -> float:
        if len(value) in (4, 5):  # DDMM / DDDMM
            deg = int(value[:-2])
            minutes = int(value[-2:])
            seconds = 0
        elif len(value) in (6, 7):  # DDMMSS / DDDMMSS
            deg = int(value[:-4])
            minutes = int(value[-4:-2])
            seconds = int(value[-2:])
        else:
            raise ValueError(f"Cannot parse coordinate format: {value}{hemi}")
        decimal = deg + minutes / 60 + seconds / 3600
        if hemi in ("S", "W"):
            decimal = -decimal
        return decimal

    @staticmethod
    def parse_coord(coord_str: str):
        coord_str = coord_str.replace(" ", "")
        m = re.match(r'([NS]\d+)([EW]\d+)', coord_str)
        if m:
            lat_raw, lon_raw = m.groups()
            lat_val, lat_hemi = lat_raw[1:], lat_raw[0]
            lon_val, lon_hemi = lon_raw[1:], lon_raw[0]
            lat = NotamDecoder.dms_to_decimal(lat_val, lat_hemi)
            lon = NotamDecoder.dms_to_decimal(lon_val, lon_hemi)
            return lon, lat
        m = re.match(r'(\d+[NS])(\d+[EW])', coord_str)
        if m:
            lat_raw, lon_raw = m.groups()
            lat_val, lat_hemi = lat_raw[:-1], lat_raw[-1]
            lon_val, lon_hemi = lon_raw[:-1], lon_raw[-1]
            lat = NotamDecoder.dms_to_decimal(lat_val, lat_hemi)
            lon = NotamDecoder.dms_to_decimal(lon_val, lon_hemi)
            return lon, lat
        raise ValueError(f"Cannot parse coordinate: {coord_str}")

    def decode(self):
        text = self.raw_text
        # Tách NOTAM theo mẫu ID
        notam_pattern = r"([A-Z]\d{4}/\d{2})\s+NOTAMN"
        matches = list(re.finditer(notam_pattern, text))
        decoded_notams = []

        if not matches:
            return []

        for j, match in enumerate(matches):
            start_pos = match.start()
            end_pos = matches[j + 1].start() if j + 1 < len(matches) else len(text)
            notam_text = text[start_pos:end_pos]
            notam_id = match.group(1)

            q_match = re.search(r"Q\)\s*(.+?)(?=\s+[A-Z]\))", notam_text)

            q_line = q_match.group(1) if q_match else ""
            q_line = q_line.replace(" ", "")
            parts = q_line.split("/")
            if len(parts) < 8:
                # Nếu không đủ phần tử Q line, có thể NOTAM khác dạng
                continue
            fir, code, traffic, purpose, scope, lower, upper, coord = parts

            geom_point, radius_nm = None, None
            if coord:
                m = re.match(r"(\d{2})(\d{2})([NS])(\d{3})(\d{2})([EW])(\d{3})", coord)
                if m:
                    lat_deg, lat_min, lat_dir, lon_deg, lon_min, lon_dir, radius = m.groups()
                    lat = int(lat_deg) + int(lat_min) / 60
                    if lat_dir == "S":
                        lat = -lat
                    lon = int(lon_deg) + int(lon_min) / 60
                    if lon_dir == "W":
                        lon = -lon
                    geom_point = {'type': 'Point', 'coordinates': [lon, lat]}
                    radius_nm = int(radius)

            location = ""
            a_match = re.search(r"A\)\s*(.+)", notam_text)
            if a_match:
                location = a_match.group(1).split(' ')[0]

            def parse_time(t):
                if not t:
                    return ""
                m = re.match(r"(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})", t)
                if m:
                    yy = int(m.group(1))
                    month = int(m.group(2))
                    day = int(m.group(3))
                    hour = int(m.group(4))
                    minute = int(m.group(5))
                    year = 2000 + yy if yy < 70 else 1900 + yy
                    return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00"
                return t

            b_match = re.search(r"B\)\s*(\d+)", notam_text)
            c_match = re.search(r"C\)\s*(\d+)", notam_text)
            start_time = parse_time(b_match.group(1) if b_match else "")
            end_time = parse_time(c_match.group(1) if c_match else "")

            e_match = re.search(r"E\)\s*(.+?)(?:\n[A-Z]\)|$)", notam_text, re.DOTALL)
            description = e_match.group(1).replace("\n", " ").strip() if e_match else ""

            coord_pattern = re.compile(
                r'(\d{4,6}[NS]\s?\d{5,7}[EW])'  # số trước, rồi N/S, số sau, rồi E/W
                r'|([NS]\d{4,6}[EW]\d{5,7})'  # chữ trước, rồi số, rồi chữ, rồi số
            )
            coords = coord_pattern.findall(description)
            coords = ["".join(c) for c in coords if any(c)]
            points = []
            try:
                points = [self.parse_coord(c) for c in coords]
            except Exception:
                points = []

            points_wkt = None
            if len(points) >= 3:
                if points[0] != points[-1]:
                    points.append(points[0])
                points_wkt = {"type": "Polygon", "coordinates": [[list(pt) for pt in points]]}

            f_match = re.search(r"(?s)F\)\s*(.+?)(?=(?:\s+[A-Z]\)|\n[A-Z]\)|$))", notam_text)
            lower_limit = f_match.group(1).strip() if f_match else ""

            g_match = re.search(r"G\)\s*(.+)", notam_text)
            upper_limit = g_match.group(1) if g_match else ""

            rmk_match = re.search(r"RMK/(.+?)(?:\n[A-Z]\)|$)", notam_text, re.DOTALL)
            remarks = rmk_match.group(1).replace("\n", " ").strip() if rmk_match else ""

            decoded_notams.append({
                "notam_id": notam_id,
                "q_line": q_line,
                "fir": fir,
                "code": code,
                "traffic": traffic,
                "purpose": purpose,
                "scope": scope,
                "lower": lower,
                "upper": upper,
                "location": location,
                "start_time": start_time,
                "end_time": end_time,
                "geom_point": geom_point,
                "radius_nm": radius_nm,
                "description": description,
                "area_polygon": points_wkt,
                "lower_limit": lower_limit,
                "upper_limit": upper_limit,
                "remarks": remarks
            })
        return decoded_notams
