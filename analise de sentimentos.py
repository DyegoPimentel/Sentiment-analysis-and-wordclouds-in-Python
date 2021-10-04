# ################################
#                                #
#    PROJETO INTEGRADOR 5-A      #
#                                #
##################################
###          Alunos:           ###
##################################
# ANGELUS VICTOR SARAIVA BORGES  #
# DIEGO DE MEDEIROS              #
# DYEGO LOURENÇO PIMENTEL        #
# VANESSA PEREIRA LEITE          #
# YSAQUE ARAUJO                  #
##################################

#  IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS
import tweepy
import textblob
import pandas as pd
import matplotlib.pyplot as plt
import re
import datetime
from wordcloud import WordCloud, STOPWORDS

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

# Selecionamos o termo pesquisado e removemos os retweets.
search = f'#{termo_pesquisado} -filter:retweets'

# CONFIGURANDO O PERIODO DE BUSCA DE 7 DIAS (PRAZO MÁXIMO UTILIZANDO A API FREE DO TWITTER)

today = datetime.datetime.now()
today = today.replace(hour=23, minute=59, second=59, microsecond=999999)
time_to_the_past = 7 # O numero 7 representa q quantidade de dias que desejamos
yesterday = today - datetime.timedelta(time_to_the_past) 
next_day = yesterday + datetime.timedelta(time_to_the_past)

# Esta variavel realiza a autenticação e a busca dos dados, dentro do prazo de 7 dias
tweet_cursor = tweepy.Cursor(api.search_tweets, q=search, lang='pt', until = next_day.date(), tweet_mode='extended').items(100)
    
# salva nesta variavel apenas os tweets, pois não precisaremos das outras colunas.
tweets = [tweet.full_text for tweet in tweet_cursor]

# Cria o data frame e insere os tweets na coluna Tweets.
tweets_df = pd.DataFrame(tweets, columns=['Tweets'])


############################################
###   PRÉ-PROCESSAMENTO E TRANSFORMAÇÃO  ###
############################################
#
# Realizamos aqui a limpeza dos dados.
for _, row in tweets_df.iterrows(): # Para cada linha dentro da base de dados
    row['Tweets'] = re.sub('http\S+', '', row['Tweets']) # Limpa links
    row['Tweets'] = re.sub('#\S+', '', row['Tweets']) # Limpa hashtag
    row['Tweets'] = re.sub('@\S+', '', row['Tweets']) # Limpa os @
    row['Tweets'] = re.sub('\\n', '', row['Tweets']) # Limpa as \

# Unir palavras para fazer o Wordcloud
summary = tweets_df.dropna(subset=['Tweets'], axis=0)['Tweets']

# concatenar as palavras
all_summary = " ".join(s for s in summary)


# lista de stopword
stopwords = set(STOPWORDS)
stopwords.update(["da", "meu", "em", "você", "de", "ao", "os", "se", "foi", "e", "que", "não", "por", "uma", "pelo", "seu", "dos", "sua", "já", "diz"
, "para", "na", "ou", "das", "como", "nos", "um", "ma", "pode", "há", "pela", "mas", "mais", "estão", "seja", "até", "está", "nas", "tem", "sobre", "tudo",
 "á", "a", "c", "vc", "e", "é", "qual", "foram", "só", "se", "fez", "faz", "ele", "bom", "o", "O", "q", "Q", "á", "a", "à", "são"])


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
# Armazena a quantidade total de tweets analizados.
total_tweets = positivo + negativo
#print(tweets_df)


#################################
###   VISUALIZAÇÃO DOS DADOS  ###
#################################

# GRÁFICO DE SENTIMENTOS
plt.bar([0], positivo, label="Positivo %s tweets" % positivo, color=['green'])
plt.bar([1], negativo, label="Negativo %s tweets" % negativo, color=['Red'])
plt.title('Gráfico 1 - Sentimentos sobre %s' % termo_pesquisado)
plt.ylabel('Total de Tweets analisados (%s Tweets)' % total_tweets)
plt.xlabel('Sentimentos dos tweets')
plt.legend()
plt.show()

# NUVEM DE PALAVRAS

# gerar uma wordcloud
wordcloud = WordCloud(stopwords=stopwords,
                      background_color="black",
                      width=1600, height=800).generate(all_summary)

# mostrar a imagem final
fig, ax = plt.subplots(figsize=(10,6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.set_axis_off()
plt.title('Gráfico 2 - Word Cloud sobre %s' % termo_pesquisado)

plt.imshow(wordcloud)
plt.show()