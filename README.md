# TopicModelerWebApp
 Aplicación Web para modelar tópicos en python con Latent Dirichlet Allocation (LDA) y MAchine Learning for LanguagE Toolkit (MALLET). Versión beta (11-03-2022)
 El objetivo es poder clasificar los documentos de acuerdo a su tópico dominante. Para ello, una vez subidos y pre-procesados los documentos, el algoritmo simulará modelos en LDA y MALLET para 2, 4, 6 y 8 tópicos dominantes, calculando sus índices de coherencia (Coherence Values) y mostrándolos en un gráfico que permita elegir un número óptimo de tópicos y el modelo que ofrezca el mejor rendimiento.

En la aplicación, subir un archivo de extensión ".xlsx" que posea al menos dos columnas. Una llamada "caso_numero" que debe corresponder al ID de cada documento, y una segunda columna llamada "reclamo_descripcion" que debe contener el texto -en español- del documento a tratar.
 
Para ejecutar la aplicación es necesario tener instalado Docker Desktop.

Instrucciones:

1. Descargar y descomprimir la carpeta que contiene la repo
2. Abrir Docker Desktop
3. Abrir una consola, y navegar hasta el directorio de la repo
4. en la consola escribir el siguiente código y presionar enter: 
 
docker build -t topicmodelerwebapp .

5. Correrá el proceso de construcción de la imagen. Una vez terminado, escribir en la consola el siguiente código:

docker compose up

6. Una vez terminado, abrir el navegador de preferencia e ingresar a localhost:5000



 
