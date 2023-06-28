# Mail Explorer
_Mail Explorer_ es un conjunto de scripts para "resumir" grandes cuerpos de correos electrónicos (archivos .eml) y correr búsquedas sobre estos con una infraestructura mínima.

Esta solución está pensada para la conservación, archivado y consulta de grandes cuerpos de correos electrónicos y de tal foma que mantener
este archivo para consulta requiera el mínimo de infraestructura de una manera simple y barata. Fue diseñado para funcionar en una instancia de [Tails](https://tails.boum.org/) pero puede ser usado en otros sistemas operativos sin problema.

Mail Explorer no indexa ni hace relaciones, solo "resume" para permitir búsquedas simples. 

## ¿Cómo funciona?
_Mail Explorer_ tiene dos componenetes principales:

1. **El _summarizer_ o "resumidor"**: Este script (o conjunto de scripts) toma como entrada un directorio con correos electrónicos, empaquetados y/o comprimidos y crea un resumen de cada correo (archivo .eml) en formato de texto, eliminando la mayor parte de las cabeceras y los archivos adjuntos (pero guardando su nombre) dejando los dátos básicos y el cuerpo del mensaje. Su salida es una carpeta con la misma estructura que la de entrada pero con directorios normales y con los archivos resumidos. El "resumen" del directorio de entrada de este proceso (la salida) pesa muchísimo menos que los archivos originales, por ejemplo, un cuerpo de correos comprimidos de 5 TB puede quedar reducido a 40 GB. Esto y el hecho de que los archivos generados sean de texto plano permite correr búsquedas que antes no era posible sobre los archivos empaquetados y/o comprimidos.

2. **El buscador**: Es un script que permite hacer búsquedas en el resumen generado por el _summarizer_ de tal forma que se puedan ubicar plabras o frases clave en los datos básicos de los correos y encontrar puntos de referencia para ubicar información en el paquete original de correos (que por las dudas, queda intacto)

## ¿ Qué formatos de archivos comprimidos o empaquetados soporta _Mail Explorer_ ?
Por el momento Mail Explorer soporta un directorio con archivos .zip donde cada archivo .zip representa a un usuario de correo y contiene los archivos .elm correspondietes a ese uauario:

Ejemplo:

```
email_server_backup/ 
  ├── user1.zip
  │  ├── email_1.eml
  │  ├── email_2.eml
  │  └── email_N.eml
  ├── user2.zip
  │  ├── email_1.eml
  │  ├── email_2.eml
  │  └── email_N.eml
  └── userN.zip
     ├── email_1.eml
     ├── email_2.eml
     └── email_N.eml
```
##

## Instalación:
### 0. Requerimientos y considerarciones:
* El cuerpo de correos originales empaquetados o comprimidos en un disco duro, idealmente externo y de estado sólido (SSD).
* Un disco de Estado sólido (idealmente) para guardar el resumen, los datos de las búsquedas y los scripts de Mail Explorer.

   *Precaución:*
  > Es importante revisar que que este disco esté fomateado con bloque de máximo 4 Kb. Es posible que discos de alta capacidad vengan formateados con bloques de 256 Kb lo cual causa un resumen muy voluminoso ya que la mayoría de los archivos de texto resumidos pesan mucho menos de 256 Kb. Por la dudas, siimplemente pude formatear el disco con el sistema de archivos NTFS. **Recuerde que al formatear el disco se perderán todos los datos que haya en el**
  
* Una memoria USB de mas de 8GB para instalar tails y los [requerimientos](https://tails.boum.org/doc/about/requirements/index.es.html) mínimos para instalar Tails. **(Opcional)**

   > **Tails** es un sistema operitvo (Linux específicamente) amnésico, es decir, no deja o deja muy pocos rastros de actividad una vez se desconecta. Funciona como un una versión _live_ de linux. Además ofrece un entorno adaptado a la privacidad protegiendo, en la medida de lo posible, la identidad de sus usuarios. Recomendamos firmemente usar Mail Explorer en conjunto con Tails.
* Conexión a internet.
* Computador para correr Tails. Puede usar un computador aparte del personal para correr Tails o correrlo en su computador de simpre.
   * tenga esto en cuenta al decidir como quiere acceder a la información.
   * Puede consultar los correos originales en la misma instancia de Tails que use para las búsquedas usando Thunderbird o su correo de cliente preferido. Este proceso se puede realizar en computadores difirentes: uno para las buúsquedas y otro para consulta de los correos originales. Recomendamos usar Tails para ambos procesos.
   * El proceso de "resumir" puede tomar dias, sinembargo podrá pararlo y seguir luego en el punto en el que lo dejó. Solo hay que hacerlo una vez.

   > Necesitará acceso al _Boot Menú_ del coputador  en el que correrá Tails, y es muy posible que necesite deshabilitar la opcion de _Secure Boot_ en la BIOS de este mismo computador. Para saber como hacerlo busque las intrucciones específicas para el modelo y marca del computador que esté usando.

### 1. Instalar el sistema operativo **Tails** en un la memoria USB de acuerdo a las intrucciones:

[https://tails.boum.org/install/index.es.html](https://tails.boum.org/install/index.es.html)

### 2. 







