import boto3
import pandas as pd
from io import StringIO
from uniendo_data import uniendo_data
from data_pipeline import run_data_pipeline
import urllib.parse

s3 = boto3.client('s3')
bucket_name = 'proyecto-1-ml'  # Cambia esto si es necesario

def lambda_handler(event, context):
    # Obtener year y month del query string
    query = event.get("queryStringParameters") or {}
    year = query.get("year", "2025")
    month = query.get("month", "06")

    print(f"📦 Iniciando pipeline para {year}-{month}")

    # ------------------------------
    # 1. Leer archivos CSV desde S3
    # ------------------------------
    dfs = []
    for i in range(1, 4):
        key = f"source_data/{year}_{month}/credit_risk_{i}.csv"
        print(f"🔽 Descargando: {key}")
        response = s3.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(content))
        dfs.append(df)

    # ------------------------------
    # 2. Unir DataFrames
    # ------------------------------
    df_combined = uniendo_data(dfs)
    print(f"📊 Shape combinado: {df_combined.shape}")

    # ------------------------------
    # 3. Ejecutar pipeline de datos
    # ------------------------------
    outputs = run_data_pipeline(df_combined)
    print("🔧 Transformaciones completadas")

    # ------------------------------
    # 4. Subir a S3
    # ------------------------------
    for name, df in outputs.items():
        csv_data = df.to_csv(index=False)
        key = f"datasets/{year}_{month}/{name}.csv"
        s3.put_object(Bucket=bucket_name, Key=key, Body=csv_data, ContentType='text/csv')
        print(f"☁️ Subido: {key}")

    return {
        'statusCode': 200,
        'body': f"✅ Muy bien! Pipeline completado y datasets guardados para {year}-{month}"
    }
