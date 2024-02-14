from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages': [
    'aiofiles',
    'customtkinter',
    'pygame',
    'websockets',
    'pyperclip',
    'tkinter',
    'CTkMessagebox'
    ], 
    'excludes': [],
    'include_files': ["LICENSE", "sounds/", "modules/", "images/", "data/", "themes/"]
}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None
p
executables = [
    Executable('main.py', base=base, target_name = 'LakshApp', icon="./images/icon.ico")
]


setup(
    name='LakshApp',
    version = '1.0',
    description = 'LakshApp is a Python GUI application developed using the customtkinter library. It offers various features to enhance productivity and relaxation, making it ideal for studying and staying focused. In the future, LakshApp aims to introduce study-specific features to further assist users in their academic endeavors.',
    options = {'build_exe': build_options},
    executables = executables,
    author="DevInfinix",
    author_email="contact.devinfinix@gmail.com",
    url="https://github.com/DevInfinix/",
)
