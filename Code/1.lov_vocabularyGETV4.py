from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import ssl

print('Iniciando aplicación')
# Crear un nuevo fichero en los que escribir los resultados de ejecutar este programa
resultado = open('VocabulariosV4.csv', 'w', encoding='utf-8')
resultado_log = open('VocabulariosV4_log.txt', 'w', encoding='utf-8')
# Vaciar el fichero (por si se ha ejecutado con anterioridad el programa)
resultado.truncate()
resultado_log.truncate()
# Dar nombre a las columnas
resultado.write('Vocabulario;Uri;Respuesta;Acceso;Tag;\n')

##CARGA TODOS LOS VOCABULARIOS Y URI'S DE LOV
# Diccionario en el que se guarda:
#   -key: prefijo de la ontología
#   -value: uri de la ontología
voc={}
# Diccionario en el que se guarda:
#   -key: etiqueta de una ontología
#   -value: array con las ontologías que pertenecen a dicha etiqueta
lov_tags={}
# Contador para indicar el número de ontologías que hay en lov
lov_con=0

# Url que apunta a la lista de vocabularios que hay actualmente en el repo de lov. 
# En dicho html hay un json con la siguiente estructura:
#   - uri: URI de la ontología
#   - prefix: Prefijo utilizado para referenciar la uri de la ontología
#   - Más cosas que no nos interesan
url = 'https://lov.linkeddata.es/dataset/lov/api/v2/vocabulary/list'
# Petición get a la url
data = requests.get(url)

# Ha sido la petición aceptada?
if data.status_code == 200:
    print('Ontologias obtenidas')

    # Cargar en un diccionario el html (debido a que tiene formato json)
    ontology_list = data.json()

    # Iterar cada una de las ontologías de lov
    for ontology in ontology_list:
        # Aumentar contador
        lov_con+=1
        # Guardar el prefijo y la URI de la ontología
        voc[ontology["prefix"]] = ontology["uri"]
    
    # Indicar el número de ontologías que se almacenan en lov.
    # Esto sirve para indicar el número de ontologías existentes en lov en el momento de la ejecución
    # del programa
    resultado_log.write(f'Vocabularios cargados : {lov_con}')

else: 
    resultado.close()
    resultado_log.close()
    resultado_log.write('Error en la uri de vocabularios\nIntentelo de nuevo más tarde')
    exit(-1)

##CARGA RESPUESTA URI Y CARGA LAS ETIQUETAS

# Iterar prefijo y URI de las ontologías
for ont_prefix, ont_uri in voc.items():

    # Url que apunta a los metadatos de una ontología de lov
    url = f'https://lov.linkeddata.es/dataset/lov/api/v2/vocabulary/info?vocab={ont_prefix}'
    # Petición get a la url (el contenido de la página es un json)
    data = requests.get(url)
    print(f'Obteniendo {ont_prefix}')
    # Ha sido la petición aceptada?
    if data.status_code == 200:
        # Cargar en un diccionario el html (debido a que tiene formato json)
        ont_metadata = data.json()
        # Adquirir un array con las etiquetas de la ontología (de lo que va la ontología)
        ont_tags = ont_metadata['tags']

        try:
            # Petición get al código de la ontología
            req = requests.get(ont_uri, timeout=5, headers={'Accept': 'application/rdf+xml; charset=utf-8'})
            # Adquirir el estado de la petición get
            req_status = req.status_code

        except:
            req_status = 504

        # Almacenar:
        #   - Prefijo de la ontología
        #   - URI de la ontología
        #   - Respuesta a la petición get del código de la ontología
        text = f'{ont_prefix};{ont_uri};{req_status};'

        try:

            # Ha sido la petición aceptada?
            if req_status == 200 :
                # other = Request(ont_uri, headers={'User-Agent': 'Mozilla/5.0'})
                # soup =  BeautifulSoup(urlopen(other, timeout=5, context=ssl.SSLContext()).read())
    
                # Guardar en local el código de la ontología
                name= f"rdf/{ont_prefix}.rdf"
                with open(name, mode = 'w', encoding = req.apparent_encoding) as f:
                    f.write(req.text)

                # Almacenar si se ha podido adquirir el código de la ontología
                text += "si;"

            else:
                # Almacenar si se ha podido adquirir el código de la ontología
                text += "no;" 

        except:
                # Almacenar si se ha podido adquirir el código de la ontología
                text += "no;"

        # Iterar las etiquetas de la ontología
        for tag in ont_tags:

            # Es una nueva etiqueta?
            if tag not in lov_tags:
                # Crear la etiqueta
                lov_tags[tag] = []

            # Añadir que la ontología pertenece a dicha etiqueta
            lov_tags[tag].append(ont_prefix)
            # Almacenar la etiqueta de la ontología
            text += tag+";"

        text+='\n'
        resultado.write(text)

    else:
        resultado_log.write('Error en la uri de etiquetas\nIntentelo de nuevo más tarde')

resultado_log.write(f'Etiquetas diferentes cargadas : {len(lov_tags)}')

# Cerrar csv en el que se han escrito los resultados
resultado.close()

# Iterar las etiquetas encontradas en lov
for i in sorted(lov_tags.keys()):
    # Por cada etiqueta decir el número de ontologías que pertenecen a dicha etiqueta
    resultado_log.write(f'{i} : {len(lov_tags[i])}')

resultado_log.write('Datos guardados en VocabulariosV4.csv')
resultado_log.close()