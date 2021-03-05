# TopicModelerWebApp
 Aplicación Web para modelar tópicos en python con Latent Dirichlet Allocation (LDA) y MAchine Learning for LanguagE Toolkit (MALLET). Versión alfa (04-03-2021)
 El objetivo es poder clasificar los documentos de acuerdo a su tópico dominante. Para ello, una vez subidos y pre-procesados los documentos, el algoritmo simulará modelos en LDA y MALLET para 2, 4, 6 y 8 tópicos dominantes, calculando sus índices de coherencia (Coherence Values) y mostrándolos en un gráfico que permita elegir un número óptimo de tópicos y el modelo que ofrezca el mejor rendimiento.
 Es importante observar la consola mientras se ejecutan los distintos procesos pues ahí se verá el nivel de avance de las distintas etapas.
 
 Para ejecutar la aplicación, clonar la repo, abrir una consola y navegar hasta la carpeta "src"
 
 luego ejecutar el comando "python index.py" (sin las comillas), esto abrirá un servidor. Ir a la página web indicada (del tipo "localhost:5000").

 En la aplicación, subir un archivo de extensión ".xlsx" que posea al menos dos columnas. Una llamada "caso_numero" que debe corresponder al ID de cada documento, y una segunda columna llamada "reclamo_descripcion" que debe contener el texto -en español- del documento a tratar.
 
 
 
