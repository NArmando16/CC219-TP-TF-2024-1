# CC219-TP-TF-2024-1
TF - Aplicaciones de Data Science 
Objetivo:
Crear un modelo que permita recomendar canciones por su id, basandose en varias caracteristicas de la canción.
U20211A648 -Armando Navarro
U202017033 - Antonio Francisco Datto Aponte

Dataset:
track_id: El ID de Spotify para la pista
artists: Los nombres de los artistas que interpretaron la pista. Si hay más de un artista, se separan por ;
album_name: El nombre del álbum en el que aparece la pista
track_name: Nombre de la pista
popularity: La popularidad de una pista es un valor entre 0 y 100
duration_ms: La duración de la pista en milisegundos
explicit: Si la pista tiene letras explícitas
danceability: La capacidad de baile describe qué tan adecuada es una pista para bailar Un valor de 0.0 es menos bailable y 1.0 es más bailable
energy: La energía es una medida de 0.0 a 1.0 y representa una medida perceptual de intensidad y actividad.
key: La tonalidad en la que está la pista. Es un valor entero de Do a SI,  siendo Do 0 y SI 11 
loudness: La sonoridad general de una pista en decibelios (dB)
mode: El modo indica la modalidad (mayor o menor) de una pista, el tipo de escala del que se deriva su contenido melódico. Mayor se representa con 1 y menor con 0
speechiness: Detecta palabras habladas en pistas. Cerca de 1.0 indica grabaciones similares al habla (por ej., programas de radio, audiolibros). Valores por debajo de 0.33 sugieren música u otro contenido no hablado.
acousticness: Una medida de confianza de 0.0 a 1.0 de si la pista es acústica. 1.0 representa alta confianza de que la pista es acústica
instrumentalness: Predice si una pista contiene voces.Cuanto más cercano sea el valor a 1.0, mayor será la probabilidad de que la pista no contenga contenido vocal
liveness: Detecta la presencia de una audiencia en la grabación.. Un valor por encima de 0.8 proporciona una alta probabilidad de que la pista sea en vivo
valence: Una medida de 0.0 a 1.0 que describe la positividad musical transmitida por una pista. Siendo valores más alto siendo pista más alegres 
tempo: El tempo estimado general de una pista en pulsaciones por minuto (BPM).
time_signature: Un compás estimado. La variable va de 3 a 7 indicando compás de 3/4 a 7/4.
track_genre: El género al que pertenece la pista

Conclusiones

El uso de un modelo de vecinos más cercanos (Nearest Neighbors) ha demostrado ser efectivo para generar recomendaciones de canciones basadas en características musicales similares. Las recomendaciones obtenidas muestran una coherencia y relevancia significativas con respecto a la canción de entrada, validadas por su cercanía en el espacio de características.

La comparación directa entre nuestras recomendaciones y las proporcionadas por la API de Spotify permite validar la calidad y la similitud de nuestras recomendaciones. La medida de distancia entre ambas fuentes de recomendaciones proporciona una métrica objetiva para evaluar la precisión de nuestro modelo en replicar el comportamiento del algoritmo de recomendación de Spotify.

 La normalización de características musicales y la codificación adecuada de géneros han sido críticas para el funcionamiento correcto del modelo. Estas técnicas aseguran que las comparaciones y recomendaciones se basan en características estandarizadas y comparables, mejorando así la robustez y la interpretabilidad del sistema de recomendación implementado.
