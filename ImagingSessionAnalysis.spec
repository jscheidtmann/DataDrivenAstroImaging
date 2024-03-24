# -*- mode: python ; coding: utf-8 -*-
import platform
import sys

sys.setrecursionlimit(sys.getrecursionlimit() * 5)

def get_resources():
    data_files = []
    for file_name in os.listdir('Icons'):
        data_files.append((os.path.join('Icons', file_name), 'Icons'))
    return data_files




a = Analysis(
    ['ImagingSessionAnalysis.py'],
    pathex=[],
    binaries=[],
    datas=get_resources(),
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
    codesign_identity=None,
    entitlements_file=None,
)

if platform.system() == 'Darwin':
    info_plist = {'addition_prop': 'additional_value'}
    app = BUNDLE(exe,
                 name='ImagingSessionAnalysis.app',
                 bundle_identifier=None,
                 icon='Icons/AppIcon.ico',
                 version='0.4.0',
                )
