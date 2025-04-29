# ESPVisionPro.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # <-- Your main script file
    pathex=[],  # <-- You can set it to [r'C:\path\to\your\project'] if needed
    binaries=[],
    datas=[
        ('yolov8s.pt', '.'), 
        ('kt_favicon.png', '.')
    ],
    hiddenimports=[
        'cv2',
        'ultralytics',
        'kivy',
        'kivymd.icon_definitions.md_icons',
        'kivy.lang',
        'kivy.clock',
        'kivy.core.window',
        'kivy.graphics.texture',
        'kivy.uix.image',
        'kivymd',
        'kivymd.app',
        'kivymd.uix.button',
        'kivymd.uix.screen',
        'kivymd.uix.tooltip',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,  # <-- slight optimization
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ESPVisionPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # <-- Set False if you don't want the black console window to appear
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='kt_favicon.png',  # <-- Optional: sets your app icon if needed
)
