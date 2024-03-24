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
    [],
    exclude_binaries=True,
    name='ImagingSessionAnalysis',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Icons/AppIcon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ImagingSessionAnalysis',
)

if platform.system() == 'Darwin':
    app = BUNDLE(coll,
                 name='ImagingSessionAnalysis.app',
                 bundle_identifier=None,
                 icon='Icons/AppIcon.ico',
                 version='0.4.0',
                 info_plist={
                        'CFBundleShortVersionString': 'Beta-Release (0.4.0)',
                        'NSHighResolutionCapable': 'True'
                    }
                )
