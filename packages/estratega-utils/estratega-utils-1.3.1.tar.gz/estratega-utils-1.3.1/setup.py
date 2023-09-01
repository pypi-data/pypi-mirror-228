from setuptools import setup, find_packages

VERSION = '1.3.1'
DESCRIPTION = 'Utilidades varias'
LONG_DESCRIPTION = 'Funciones y clases con utilidades para agilizar y optimizar la escritura de código.'

# Configurando
setup(
    # el nombre debe coincidir con el nombre de la carpeta
    # 'modulomuysimple'
    name="estratega-utils",
    version=VERSION,
    author="Ivan Sayavedra",
    author_email="<isayavedra@estrategasoftware.com.ar>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    # añade cualquier paquete adicional que debe ser
    install_requires=['pydantic', 'pymysql', 'devtools', 'mysql'],
    # instalado junto con tu paquete. Ej: 'caer'

    keywords=['python', 'estratega utils'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
