from PyInstaller.utils.hooks import collect_data_files

hiddenimports = ["pyqt6"]
datas = collect_data_files('pyqt6')