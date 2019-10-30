# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['autoCombind.py'],
             pathex=['C:\\Users\\SSD-AHCI\\workAAA\\autoCombind'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas += [("up.png", "up.png", 'DATA'), ("down.png", "down.png", "DATA")]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='autoCombind',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
