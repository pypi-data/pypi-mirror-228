## TODOS: 

- [ ] Instalacion de los binarios : Detectar si estas en windows o en Linux y si está instalado, sino instalarlo. Para instalarlo descargar el .zip, descomprimir y eliminar el .zip. Se instalan los binarios y se añade un fichero "no tocar" con las versiones de los binarios. Así se pueden controlar futuras actualizaciones de esta parte.

- [x] Cerrar bien los procesos.

- [ ] Parametrizar configuración

- [ ] Mejorar el sistema de crear y eliminar pestañas

## Dependencias

```
pip install selenium==4.12.0  Pillow==10.0.0  psutil==5.9.5
```

## PiPy

Empaquetar el paquete
```
python setup.py sdist bdist_wheel
```

Subirlo
```
twine upload dist/*
```