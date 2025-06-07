# Imagen base oficial para Python 3.9 compatible con Lambda
FROM public.ecr.aws/lambda/python:3.9

# Copiar dependencias
COPY requirements.txt ./

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar tu código fuente
COPY lambda_function.py .
COPY uniendo_data.py .
COPY data_pipeline.py .
COPY preprocessing.py .

# Comando que Lambda ejecutará
CMD ["lambda_function.lambda_handler"]
