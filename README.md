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

### 1. Instala el sistema operativo **Tails** en un la memoria USB de acuerdo a las intrucciones:

[https://tails.boum.org/install/index.es.html](https://tails.boum.org/install/index.es.html)

### 2. Arranca Tails en el computador distpuesto para tal fin y realizar las siguientes acciones en la ventana de inicio
   #### 2.1. Habilitar el almacenamiento permanente/persistent storage:
   ![create_persistent_storage.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/create_persistent_storage.png)

   #### 2.2. Entra a las opciones adicionales:
   ![additional_settings_click.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/additional_settings_click.png)

   #### 2.3. Habilita la contraseña de adminitración / administration password y poner una contraseña:
   ![administration_password_click.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/administration_password_click.png)

   #### 2.4. Después de poner la clave y dar aceptar, la ventana de inicio debe lucir así:
   ![init_conf.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/init_conf.png)

  #### 2.5. Da click en arrancar Tails/start Tails.
  
### 3. Espera a que el sistema arranque por completo (puede tomar unos minutos) hasta que aparezca la ventana para configurar el almacenamiento permanente y haz click en _continuar_:
![persistent_storage_conf.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/persistent_storage_conf.png)

   #### 3.1. introduzce una clave para encriptar el almacenamiento permanente (esta clave deberá ponerla cada vez que encienda el sistema).
   > No confundir con la clave de de administración que pusimos en el paso 2.3.
   
   ![persistent_storage_set_password.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/persistent_storage_set_password.png)

   #### 3.2. espera a que se cree el alamacenamiento:
   ![persistent_storage_creating.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/persistent_storage_creating.png)

   #### 3.3. En la panatalla finaal de esta configuracion habilita la opcion de Thunderbird que es un cliente de correo si quieres poder ver los correos originales en Tails. La panatalla final debe lucir así:
   ![persistent_storage_network_and_thunderbird.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/persistent_storage_network_and_thunderbird.png)

   #### 3.4. Acepta los cambios en la parte superior derecha.

### 4. Conéctate a internet en el icono de red en la parte superior derecha la pantalla.
   #### 4.1. En el fondo tendrás una ventana asi:
   ![connect_to_tor.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/connect_to_tor.png)

   #### 4.2. Haz click en "conectar a tor automáticamente" y luego en el botón "conectar a tor" en la parte inferior derecha de la ventana.

   #### 4.3. Una vez terminada la conexión puedes cerrar la ventana que tienes en frente.

### 5. Abre una terminal llendo en la parte de arriba a Aplicaciones -> Utilidades -> Terminal
   #### 5.1. Escribe el siguiente comando `sudo apt update` y da `enter` . Te pedirá la clave que pusimos en la paso 2.3. y hará varios procesos antes de terminar.
   ![apt_update.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/apt_update.png)

   #### 5.2. Una vez terminado el comando anterior escribe `sudo apt install pv`:
   ![apt_install_pv.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/apt_install_pv.png)

   #### 5.3. Cuando este comando termine de ejecutarse recibirás una notificacion en la parte superior de la pantalla preguntando si quieres que este software si instale cada vez que inicies Tails, di que sí.
   ![pv_install_everytime.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/pv_install_everytime.png)

### 6. Reinicia Tails (en la esquina superior derecha) para probar que la configuración inicial quedó bien. En la pantalla inicial desbloquea el alamacenamiento permanente con la clave que pusiste en el paso 3.1. Esta vez no necesitas habilitar la clave de adminitración.
![persistent_storage_reboot.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/persistent_storage_reboot.png)

   #### 6.1. Conectate a Tor y verás primero una notificación en laparte superior de la pantalla indicando que se está instalando el software adicional:
   ![installing_software.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/installing_software.png)

   #### 6.2. espera a que la notificación de que el software ha sido instalada aparezca:
   ![installing_software_done.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/installing_software_done.png)

### 7. Conecta la USB o Disco donde vas a guardar el resumen y mail explorer
   #### 7.1. Busca el dispositivo en el explorador de archivos de Tails llendo a _lugares -> Home_ en la barra superior. en la ventana, busca el dispositivo a la derecha y haz click sobre el para montarlo.
   
   #### 7.2 En el dispositivo, crea una carpeta que se llame **data** y dentro de esta una que se llame **summarized**
   ![summarized_dir_create.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/summarized_dir_create.png)
   
   #### 7.3. Vuelve a la raiz del dispositivo (haciendo click en el dispositivo en la parte izquierda de la ventana), haz click derecho en el espacio donde se muestran los direcotrios y selecciona "abrir en terminal"
   ![open_in_terminal.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/open_in_terminal.png)

   #### 7.4. Escribe el siguiente comando en la termnal: `git clone https://github.com/karisma-klab/mail_explorer.git`
   ![clone_mail_explorer.png](https://raw.githubusercontent.com/karisma-klab/mail_explorer_docs/main/images/clone_mail_explorer.png)

   #### 7.5. cierra la terminal.
   

**---- Instalacion finalizada! -----**

## Crear el resumen (summarize)
   
En este proceso tomaremos una carpeta con archivos de correo (.eml) que están empaquetados y comprimidos. la procesaremos para sacar un resumen de todos esos correos en archivos de texto. El resumen consiste en extraer, el To, From, Date, Subject, Body y los nombres de los archivos adjuntos y ponerlos en un archivo de texto conservando la misma estructura que tienen los archivos comprimidos originales, esto permite tener una copia reducida de todo el cuerpo de correos donde se pueden buscar términos que ubiquen a las personas investigadoras sobre donde encontrar un tema específico en los correos originales. En los correos localizados en el archivo original se puedan rastrear otros correos que participan en la conversación, ver los archivos adjuntos, etc.

Para este fin usaremos el script `summarizer.py` de Mail Explorer que es un programa en líne ade comandos que crea el resumen del cuerpo de correos.

Este script, ademas de realizar este proceso tiene dos funcionalidades adicionales importantes:
   1. El proceso se puede cancelar con Control-C y cuando se ponga de nuevo en marcha seguira en el punto donde se dejó. Esto también es importante si suceden errores durante el proceso ya iagualmente, reiniciando la ejecución podemos seguir en el punto donde ocurrió el error.
   2. Pensando en procesar cuerpos de correos muy grandes este script puede jecutar varios hilos al tiempo que se especifican con la opcion `-t`. Aconsejamos 4 hilos simultaneos en condiciones normales.


Estas son todas las opciones de `summarizer.py`:
```
$./summarizer.py --help                                                                                           ✔ 
Usage: summarizer.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  Run test on this eml file
  -z FILE, --zip=FILE   Run test on this zip file
  -s DIR                source directory
  -d DIR                destination directory
  -t NUM                threads number
  -q                    don't print status messages to stdout
```





