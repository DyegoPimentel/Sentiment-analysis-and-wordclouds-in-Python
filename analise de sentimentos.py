# PROJETO INTEGRADOR 5A
# Alunos: Angelus, Diego de Medeiros, Dyego Pimentel, Vanessa Leite, Ysaque

#  IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS
import tweepy
import textblob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import datetime

# TOKENS DE AUTENTICAÇÃO
#
# Nesta etapa, definimos os tokens de autenticação para termos acesso a API do twitter,
# lembrando que por questões de segurança as credenciais que estão no arquivo keys.txt
# não será compartilhado no github. Para que o algoritimo funcione adequadamente, basta
# criar um arquivo keys.txt seguindo o modelo de exemplo e inserindo as suas credenciais
# de desenvolvedor do twitter.

all_keys = open('keys.txt', 'r').read().splitlines()

api_key = all_keys[0]
api_key_secret = all_keys[1]
access_token = all_keys[2]
access_token_secret = all_keys[3]


authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
authenticator.set_access_token(access_token, access_token_secret)


api = tweepy.API(authenticator, wait_on_rate_limit=True)

############################
###   SELEÇÃO DE DADOS   ###
############################

# VARIAVEIS DE BUSCA
termo_pesquisado = 'Covid'


# CONFIGURANDO O PERIODO DE BUSCA DE 7 DIAS (PRAZO MÁXIMO UTILIZANDO A API FREE DO TWITTER)
today = datetime.datetime.now()
today = today.replace(hour=23, minute=59, second=59, microsecond=999999)
time_to_the_past = 7 # O numero 7 representa q quantidade de dias que desejamos
yesterday = today - datetime.timedelta(time_to_the_past) 
next_day = yesterday + datetime.timedelta(time_to_the_past)


# Selecionamos o termo pesquisado e removemos os retweets.
search = f'#{termo_pesquisado} -filter:retweets'

# Esta variavel realiza a autenticação e a busca dos dados, dentro do prazo de 7 dias
tweet_cursor = tweepy.Cursor(api.search_tweets, q=search, lang='en', until = next_day.date(), tweet_mode='extended').items(100)


############################################
###   PRÉ-PROCESSAMENTO E TRANSFORMAÇÃO  ###
############################################

# salva nesta variavel apenas os tweets, pois não precisaremos das outras colunas.
tweets = [tweet.full_text for tweet in tweet_cursor]

# Cria o data frame e insere os tweets na coluna Tweets.
tweets_df = pd.DataFrame(tweets, columns=['Tweets'])

# Realizamos aqui a limpeza dos dados.
for _, row in tweets_df.iterrows(): # Para cada linha dentro da base de dados
    row['Tweets'] = re.sub('http\S+', '', row['Tweets']) # Limpa links
    row['Tweets'] = re.sub('#\S+', '', row['Tweets']) # Limpa hashtag
    row['Tweets'] = re.sub('@\S+', '', row['Tweets']) # Limpa os @
    row['Tweets'] = re.sub('\\n', '', row['Tweets']) # Limpa as \


#############################
###   MINERAÇÃO DE DADOS  ###
#############################

# Cria um campo na base de dados e insere com auxilio da biblioteca textblob a podaridade de sentimento (se menor que 0 é negativo, se maior que 0 é positivo)
tweets_df['Polaridade'] = tweets_df['Tweets'].map(lambda tweet: textblob.TextBlob(tweet).sentiment.polarity)
# Verifica a polaridade inserida e cria um campo de resultado, se a polaridade for maior que 0 recebe +, se não, recebe -
tweets_df['Resultado'] = tweets_df['Polaridade'].map(lambda pol: '+' if pol > 0  else '-')

# As variaveis positivo e negativo recebem a soma do resultado dos tweets processados.
positivo = tweets_df[tweets_df.Resultado == '+'].count()['Tweets']
negativo = tweets_df[tweets_df.Resultado == '-'].count()['Tweets']

# print(tweets_df)


#################################
###   VISUALIZAÇÃO DOS DADOS  ###
#################################

# GRÁFICO
print(positivo)
plt.bar([0,1], [positivo, negativo], label=['Positivo', 'Negativo'], color=['green', 'red'])
plt.title('Gráfico de Sentimentos')
#plt.legend()

plt.show()

