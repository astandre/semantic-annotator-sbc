# Clasificador de palabras

## Requerimientos

Python 3.6
PyMySQL
spacy
SQLAlchemy
requests-html
networkx
beautifulsoup4


## Instalacion
Para instalar las dependencias necesarias usar el comando:

``
pip install -r requirements.txt
``

Instalaremos el complemento de spacy para español:

``
python -m spacy download es_core_news_sm
``
 
## Configuracion

Debemos configurar la base de datos que vayamos a usar, en el archivo .env (Este archivo puede estar invisible en entornos linux). Gracias al ORM las tablas se generaran automaticamente.

``
DATA_BASE='mysql+pymysql://user:pass@localhost/db_name'
``

Ejemplo:

``
DATA_BASE='mysql+pymysql://root: @localhost/test'
``



## Uso

Definir las variables de entorno para flask, en caso de windows usar set en vez de export


``
export FLASK_APP=Main.py
``

``
export FLASK_ENV=development
``

Para ejecutarlo usar el comando:

``
python -m flask run
``

o

``
flask run
`` 



