# -*- mode: python -*-

block_cipher = None


a = Analysis(['Government_Intelligent_Analyse_System.py'],
             pathex=['E:\\Anaconda\\envs\\tensorflow', 'E:\\Anaconda\\envs\\tensorflow\\Lib', 'E:\\Anaconda\\envs\\tensorflow\\Lib\\site-packages', 'E:\\Anaconda\\envs\\tensorflow\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'G:\\HUST_CBIB_Final_Competition_Submit_Result\\code'],
             binaries=[],
             datas=[],
             hiddenimports=['pandas._libs.tslibs.timedeltas','scipy._lib.messagestream'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Government_Intelligent_Analyse_System',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,
          icon='logo_512.ico')
