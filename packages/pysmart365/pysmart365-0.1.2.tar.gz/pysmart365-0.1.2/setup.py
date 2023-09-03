from setuptools import *
import webbrowser
setup(
    author="Runkang",
    author_email="club.leggendario@gmail.com",
    name="pysmart365",
    packages=['pysmart365'],
    version='0.1.2',
    long_description='''This module is to simplify the functions of MicroSoftware and SmartSoft.''',
    description='This module is to simplify the functions of MicroSoftware and SmartSoft.',
    install_requires=[
        'screeninfo',
        'pandas',
        'pyautogui',
        'pytube',
        'pytube3',
        'firebase_admin',
        'customtkinter',
        'requests',
        'flask',
        'ttkbootstrap',
        'configparse',
        'pywinauto',
        'jsonschema'
        ],
    url="https://github.com/informatic365/PySmart365/",
    download_url="https://pypi.org/project/pysmart365/"
)