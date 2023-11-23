from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl

# Crear un nuevo fichero en los que escribir los resultados de ejecutar este programa
resultado = open ('Terms.csv', 'w', encoding='utf-8')
# Vaciar el fichero (por si se ha ejecutado con anterioridad el programa)
resultado.truncate()
# Dar nombre a las columnas
resultado.write ('Clase;Tipo;Referencias;Datasets;Documentacion\n')
# Número de páginas existentes en https://lov.linkeddata.es/dataset/lov/terms
num_pages = 8025 + 1

# Iterar cada una de las páginas
for page in range (1, num_pages):
    print(f'leyendo pagina {page}')
    # Url que apunta a una de las múltiples páginas de lov en las que se almacenan los términos utilizados
    # en las ontologías de lov.
    url = f'https://lov.linkeddata.es/dataset/lov/terms?&page={page}'
    # Además, se hace una petición get a dicha url url
    req = Request(url=(f'https://lov.linkeddata.es/dataset/lov/terms?&page={page}'), headers={'User-Agent': 'Mozilla/5.0'})
    # Leer el html de la página
    soup =  BeautifulSoup(urlopen(req, context=ssl.SSLContext()).read())
    # Almacenar en un array los tags <a></a> que aparecen en el html
    tags = soup('a')

    # Contador para almacenar por la linea del html en la que estamos
    con = 0
    robin = 0

    # Recorrer cada uno de los elementos del html que se encuentran entre <a></a>.
    # Las primeras 5 lineas son cabeceras que no nos interesan.
    # Las siguientes 40 lineas contienen informacion de los distintos terminos de lov (10 terminos por pagina).
    # A partir de la linea 40 se esta representando el pie de página en el html.
    for i in tags:
        con += 1

        # La linea esta entre la 5 y la 46?
        if con > 5 and con < 46:
            
            robin += 1
            aux = i.getText().strip()

            if robin==1:
                # En este caso estamos leyendo el "prefijo:sufijo" del termino de lov
                sufijo = aux.split(':')[1]

            elif robin==2:
                # En este caso solo estamos leyendo el "prefijo" del termino de lov
                prefijo = aux

            elif robin==3:
                # En este caso estamos leyendo un texto del estilo "6,852,815 occurrences in 102 LOD datasets".
                # Solo nos interesa el numero de apariciones y en cuantos datasets aparecen
                aux = aux.replace(",","")
                num_apariciones = ""
                num_datasets = ""
                espacios = 0
                
                if len(aux) > 20:

                    for i in range(0,len(aux)):

                        if aux[i]==" ": 
                            espacios += 1

                        if espacios==0: 
                            num_apariciones += aux[i]

                        if espacios==3: 
                            num_datasets += aux[i]

                        if espacios==4: 
                            break

                else: 
                    num_apariciones = '0'
                    num_datasets = '0'

            else: 
                resultado.write(f'{prefijo};{sufijo};{num_apariciones};{num_datasets};{aux};\n')
                robin=0              

resultado.close()



