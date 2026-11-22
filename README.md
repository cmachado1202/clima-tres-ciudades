# Temperatura en tres ciudades
Consulto Open-Meteo para Buenos Aires, Córdoba y Rosario. Cada respuesta trae hora, valor y unidad. Guardo una foto del último lote en data/temperaturas.json; no necesito una clave para esta API.
## Preparar el entorno
Copiar .env.example a .env. Para esta práctica los valores pueden quedar vacíos. Abrir la carpeta en VS Code y elegir Dev Containers: Reopen in Container. El Dockerfile instala las dependencias. Desde la terminal integrada ejecutar python src/check_env.py y python src/main.py. Para correr fuera del contenedor, instalar antes con python -m pip install -r requirements.txt.
## Qué pasa si falla una ciudad
Las tres consultas se inician juntas. Cada una tiene diez segundos de timeout por operación y un único reintento ante un error de transporte, un 429 o un error del servidor. Un error de formato o un 4xx permanente se registra sin reintento. Si llegan dos respuestas guardo esas dos y devuelvo código 1. Si ninguna llega conservo el archivo anterior y también devuelvo 1.
Simulación local, tres respuestas con 100 ms de espera: secuencial 0.302 s, concurrente 0.101 s.
