from setuptools import setup, find_packages
setup(
    name='easy_chromium_controller',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        # Lista de dependencias de tu paquete
        'selenium==4.12.0',
        'Pillow==10.0.0',
        'psutil==5.9.5'
    ],
)