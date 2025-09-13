from notam_decoder import NotamDecoder  # giả sử file trên bạn lưu là notam_decoder.py
import json

if __name__ == "__main__":
    with open("notam_raw.txt", "r", encoding="utf-8") as f:
        raw_notam_text = f.read()

    decoder = NotamDecoder(raw_notam_text)
    decoded_data = decoder.decode()

    with open("notam_decoded.json", "w", encoding="utf-8") as f:
        json.dump(decoded_data, f, ensure_ascii=False, indent=4)

    print(f"Decoded {len(decoded_data)} NOTAMs saved to notam_decoded.json")