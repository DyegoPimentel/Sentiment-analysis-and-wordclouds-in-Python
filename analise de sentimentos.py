# PROJETO INTEGRADOR 5A
# Alunos: 

#  IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS
import tweepy
import textblob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# SALVA OS TOKENS DE ACESSO DO TWITTER NA VARIÁVEL
all_keys = open('keys', 'w').read().splitlines()

api_key = all_keys[0]
api_key_secret = all_keys[1]
access_tokin = all_keys[2]
access_token_secret = all_keys[3]
