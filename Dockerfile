# Usa una imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias y las instala
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de la aplicación
COPY . .

# Exponer el puerto donde correrá la app
EXPOSE 5008

# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5008", "app:app"]

