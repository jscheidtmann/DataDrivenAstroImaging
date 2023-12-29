# -*- mode: python ; coding: utf-8 -*-

import sys

sys.setrecursionlimit(sys.getrecursionlimit() * 5)

a = Analysis(
    ['ImagingSessionAnalysis.py'],
    pathex=[],
    binaries=[],
    datas=[('Icons/folder.png', 'Icons/gearshape.png')],
    hiddenimports=[],
    hookspath=["pyi-hooks"],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ImagingSessionAnalysis',
    icon='Icons/AppIcon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='arm64',
    codesign_identity=None,
    entitlements_file=None,
)

