import os
import platform

print("Python", platform.python_version())
for name in ("OPENAI_API_KEY", "DATABASE_URL"):
    if name not in os.environ:
        raise SystemExit(f"Falta {name}. Revisar el archivo .env.")
    print(f"{name}: disponible")
