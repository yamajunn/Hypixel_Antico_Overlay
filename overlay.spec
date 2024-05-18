# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['overlay.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['scipy.special._cdflib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
)

a.datas += [('pix_bed.png', '.\pix_bed.png', 'DATA')]
a.datas += [('pix_bench.png', '.\pix_bench.png', 'DATA')]
a.datas += [('pix_bow.png', '.\pix_bow.png', 'DATA')]
a.datas += [('pix_dirt.png', '.\pix_dirt.png', 'DATA')]
a.datas += [('pix_eye.png', '.\pix_eye.png', 'DATA')]
a.datas += [('pix_fishing.png', '.\pix_fishing.png', 'DATA')]
a.datas += [('pix_gapple.png', '.\pix_gapple.png', 'DATA')]
a.datas += [('pix_hub.png', '.\pix_hub.png', 'DATA')]
a.datas += [('pix_none.png', '.\pix_none.png', 'DATA')]
a.datas += [('pix_tnt.png', '.\pix_tnt.png', 'DATA')]

a.datas += [('gear.png', '.\gear.png', 'DATA')]
a.datas += [('logo_white.png', '.\logo_white.png', 'DATA')]
a.datas += [('logo.ico', '.\logo.ico', 'DATA')]
a.datas += [('logo.png', '.\logo.png', 'DATA')]

a.datas += [('Cheater.pkl', '.\Cheater.pkl', 'DATA')]
a.datas += [('scaler.joblib', '.\scaler.joblib', 'DATA')]

a.datas += [('met_player.json', '.\met_player.json', 'DATA')]
a.datas += [('table.json', '.\table.json', 'DATA')]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Antico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.ico'],
)
