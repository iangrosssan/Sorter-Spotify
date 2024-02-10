# Sorter_Spotify

### El siguiente archivo utiliza claves publico y privadas de Spotify Developer, estas deben ser entregadas en un archivo "credenciales.csv" utilizando el formato:
#### client_id, client_secret, user_id
###
### Información de avances
-[x] .exe
-[x] Separación frontend y backend
-[ ] Barra de progreso.
- El GUI de PyQt se mantiene ocupado mientras el proceso de orden se ejecuta, por lo que no muestra el progreso hasta el final. 
- Requiere QThread.
-[ ] Language Sort
- Datos de Spotify no revelan lenguaje de las canciones. 
- ISRC muestra el país de la distribuidora y no el país del artista.
- Se propone acceder a través de la API de MusicMatch para obtener los lyrics y analizar lenguaje.