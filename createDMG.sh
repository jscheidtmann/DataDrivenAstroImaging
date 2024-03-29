#!/bin/bash

echo "Creating DMG installer..."
mkdir -p dist/dmg
rm -rf dist/dmg/*
cp -r "dist/ImagingSessionAnalysis.app" dist/dmg
create-dmg \
  --volname "ImagingSessionAnalysis" \
  --volicon "Icons/AppIcon.ico" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "ImagingSessionAnalysis.app" 175 120 \
  --hide-extension "ImagingSessionAnalysis.app" \
  --app-drop-link 425 120 \
  --hdiutil-verbose \
  "dist/ImagingSessionAnalysis.dmg" \
  "dist/dmg/"