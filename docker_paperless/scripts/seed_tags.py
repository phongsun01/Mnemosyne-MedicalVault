
import os
import requests
import random

# Configuration
PAPERLESS_API_URL = os.getenv("PAPERLESS_API_URL", "http://webserver:8000/api")
PAPERLESS_API_TOKEN = os.getenv("PAPERLESS_API_TOKEN")

# Standard Taxonomy (Reference: Circular 30/2015/TT-BYT & Common Hospital Structure)
# Format: "Tag Name": "Color Hex"
TAGS = {
    # Chẩn đoán hình ảnh (Blue)
    "chan-doan-hinh-anh": "#2196F3",
    "x-quang": "#64B5F6",
    "ct-scanner": "#64B5F6",
    "mri": "#64B5F6",
    "sieu-am": "#64B5F6",
    
    # Nội soi (Green)
    "noi-soi": "#4CAF50",
    "noi-soi-da-day": "#81C784",
    "noi-soi-tai-mui-hong": "#81C784",
    
    # Kiểm soát nhiễm khuẩn (Orange)
    "kiem-soat-nhiem-khuan": "#FF9800",
    "may-tiet-trung": "#FFB74D",
    "may-giat-cong-nghiep": "#FFB74D",
    
    # Hồi sức cấp cứu (Red)
    "hoi-suc-cap-cuu": "#F44336",
    "may-tho": "#E57373",
    "monitor": "#E57373",
    
    # Document Types (Grey)
    "hop-dong": "#9E9E9E",
    "bao-gia": "#9E9E9E",
    "huong-dan-su-dung": "#9E9E9E",
    "catalog": "#9E9E9E"
}

def create_tag(name, color):
    headers = {"Authorization": f"Token {PAPERLESS_API_TOKEN}"}
    
    # Check if exists
    resp = requests.get(f"{PAPERLESS_API_URL}/tags/?name__iexact={name}", headers=headers)
    if resp.json()['count'] > 0:
        print(f"Tag '{name}' already exists.")
        return

    # Create
    data = {
        "name": name,
        "color": color,
        "is_inbox_tag": False,
        "matching_algorithm": 0 # Any
    }
    resp = requests.post(f"{PAPERLESS_API_URL}/tags/", json=data, headers=headers)
    if resp.status_code == 201:
        print(f"Created tag: {name}")
    else:
        print(f"Failed to create {name}: {resp.text}")

if __name__ == "__main__":
    print("Seeding standard tags...")
    for name, color in TAGS.items():
        create_tag(name, color)
    print("Done.")
