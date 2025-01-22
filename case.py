import requests  # Para pegar dados da API

# URL da API com a chave demo
url = "https://www.alphavantage.co/query" 
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
    "apikey": "demo"
}

# Fazendo a requisição
response = requests.get(url, params=params)

# Verificando a resposta
if response.status_code == 200:  # 200 significa que deu certo
    print("Dados recebidos com sucesso!")
    dados = response.json()  # Convertendo para JSON (estrutura de dados)
else:
    print("Erro na API:", response.status_code)

import pandas as pd  # Biblioteca para organizar os dados

# Extrair a parte útil dos dados
time_series = dados["Time Series (Daily)"]
df = pd.DataFrame(time_series).T  # Transforma os dados em tabela
df = df.rename(columns={"4. close": "close"}).astype(float)  # Apenas o preço
df.index = pd.to_datetime(df.index)  # Datas organizadas
df = df.sort_index()  # Organizar pela data

# Calcular retorno diário e acumulado
df["retorno_diario"] = df["close"].pct_change()
df["retorno_acumulado"] = (1 + df["retorno_diario"]).cumprod() - 1

# Calcular volatilidade média
df["volatilidade_media"] = df["retorno_diario"].rolling(window=20).std()

print(df.head(100))  # Olhe os resultados iniciais

# Salvar os resultados de retorno acumulado em um arquivo JSON separado
df[["retorno_acumulado"]].dropna().to_json("retorno_acumulado.json", orient="index", date_format="iso")

# Salvar os resultados de volatilidade em um arquivo JSON separado
df[["volatilidade_media"]].dropna().to_json("volatilidade.json", orient="index", date_format="iso")

print("Resultados salvos nos arquivos retorno_acumulado.json e volatilidade.json")

