import requests  # Importa a biblioteca requests, que é usada para fazer requisições HTTP

# URL da API com a chave demo
url = "https://www.alphavantage.co/query"
params = {
    "function": "TIME_SERIES_DAILY",  # Função da API que retorna séries temporais diárias
    "symbol": "IBM",  # O símbolo da ação (neste caso, IBM)
    "apikey": "demo"  # A chave da API (neste caso, uma chave demo fornecida pela API)
}

# Fazendo a requisição GET para obter os dados
response = requests.get(url, params=params)

# Verificando a resposta da API
if response.status_code == 200:  # Se o código de status for 200, significa que a requisição foi bem-sucedida
    print("Dados recebidos com sucesso!")  # Exibe mensagem de sucesso
    dados = response.json()  # Converte a resposta JSON para um dicionário Python
else:
    print("Erro na API:", response.status_code)  # Caso ocorra um erro, exibe o código de status do erro

import pandas as pd  # Importa a biblioteca pandas, usada para manipulação e análise de dados

# Extrair a parte útil dos dados que contém as séries temporais diárias
time_series = dados["Time Series (Daily)"]  # Obtém os dados de séries temporais diárias da resposta da API

# Criação de um DataFrame com pandas a partir dos dados extraídos
df = pd.DataFrame(time_series).T  # Transforma o dicionário em um DataFrame, usando a transposta (.T) para ter as datas como índice
df = df.rename(columns={"4. close": "close"}).astype(float)  # Renomeia a coluna "4. close" para "close" e converte os valores para float
df.index = pd.to_datetime(df.index)  # Converte o índice (datas) para o formato datetime
df = df.sort_index()  # Organiza as linhas do DataFrame pelas datas (índice)

# Calcular o retorno diário com base no preço de fechamento (close)
df["retorno_diario"] = df["close"].pct_change()  # O retorno diário é dado pela variação percentual entre os preços de fechamento

# Calcular o retorno acumulado
df["retorno_acumulado"] = (1 + df["retorno_diario"]).cumprod() - 1  # O retorno acumulado é calculado a partir do retorno diário

# Calcular a volatilidade média utilizando uma janela de 20 dias
df["volatilidade_media"] = df["retorno_diario"].rolling(window=20).std()  # A volatilidade é dada pelo desvio padrão dos retornos diários numa janela de 20 dias

# Imprime as primeiras 100 linhas do DataFrame com os resultados
print(df.head(100))

# Salvar os resultados de retorno acumulado em um arquivo JSON separado
df[["retorno_acumulado"]].dropna().to_json("retorno_acumulado.json", orient="index", date_format="iso")
# O método dropna() remove valores nulos (NaN) e o método to_json() converte os dados em um arquivo JSON no formato desejado

# Salvar os resultados de volatilidade em um arquivo JSON separado
df[["volatilidade_media"]].dropna().to_json("volatilidade.json", orient="index", date_format="iso")
# O mesmo processo é realizado para salvar a volatilidade média em um arquivo JSON

# Exibe mensagem informando que os resultados foram salvos nos arquivos JSON
print("Resultados salvos nos arquivos retorno_acumulado.json e volatilidade.json")
