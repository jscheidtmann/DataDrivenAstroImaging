from PyInstaller.utils.hooks import collect_data_files

hiddenimports = ["photutils.geometry.core"]
datas = collect_data_files('photutils')
