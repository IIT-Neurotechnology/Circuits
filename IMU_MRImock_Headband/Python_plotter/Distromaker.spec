# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(
    ['Harry_plotter.py'],
    pathex=[r'C:\Users\faricci\Circuits\IMU_MRImock_Headband\Python_plotter'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='IMU_Visualizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon= r'C:\Users\faricci\Circuits\IMU_MRImock_Headband\Python_plotter\IITNT.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='IMU_Visualizer_and_save'
)

# Specify the output directory
distpath = r'D:\ '
