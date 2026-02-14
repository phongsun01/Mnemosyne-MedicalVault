#!/bin/bash

# Base directory
BASE_DIR="/Users/xitrum/MedicalVault"

echo "🚀 Initializing MedicalVault directory structure at $BASE_DIR..."

# Create folders
mkdir -p "$BASE_DIR/raw/new"
mkdir -p "$BASE_DIR/raw/classified"
mkdir -p "$BASE_DIR/md/devices"
mkdir -p "$BASE_DIR/md/templates"
mkdir -p "$BASE_DIR/backup/daily"

# Create a sample template
cat > "$BASE_DIR/md/templates/device_template.md" << EOF
---
device_id: ""
model: ""
brand: ""
category: ""
subcategory: ""

specs:
  power: ""
  voltage: ""
  
pricing:
  price_range_vnd: [0, 0]
  last_updated: "$(date +%Y-%m-%d)"
  source: ""

attachments: []

metadata:
  created: "$(date +%Y-%m-%d)"
  updated: "$(date +%Y-%m-%d)"
  confidence: 0
  status: "draft"
---

# Title

## Summary
- **Type**: 
- **Brand**: 
- **Price**: 

## Specs
...
EOF

echo "✅ Folders created successfully!"
ls -R "$BASE_DIR"
