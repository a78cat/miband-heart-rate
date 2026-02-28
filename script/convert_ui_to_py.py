import os
import subprocess


def convert_ui_to_py(ui_dir, py_dir):
    if not os.path.exists(py_dir):
        os.makedirs(py_dir)
    for ui_file in os.listdir(ui_dir):
        if ui_file.endswith('.ui'):
            ui_path = os.path.join(ui_dir, ui_file)
            py_file = os.path.splitext(ui_file)[0] + '.py'
            py_path = os.path.join(py_dir, py_file)
            # command = f'pyuic6 -o {py_path} {ui_path}'
            command = f'pyside6-uic -o {py_path} {ui_path}'
            subprocess.run(command, shell=True)
            print(f'Converted {ui_file} to {py_file}')


# python -m PyQt6.uic.pyuic register.ui -o register.py


ui_directory = '../ui'
py_directory = '../src/view'
convert_ui_to_py(ui_directory, py_directory)
# 把ui文件转换成py文件
