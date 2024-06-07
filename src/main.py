import requests
from bs4 import BeautifulSoup
import pandas as pd

def buscar_mercado_livre():
    lista_imoveis = []
    url_base = 'https://imoveis.mercadolivre.com.br/minas-gerais/belo-horizonte/imoveis'
    response = requests.get(url_base).content
    site = BeautifulSoup(response, 'html.parser')
    imoveis = site.findAll('div', attrs={'class': 'ui-search-result__wrapper'})

    for imovel in imoveis:
        titulo = imovel.find('h2', attrs={'class': 'ui-search-item__title'})
        valor = imovel.find('span', attrs={'class': 'andes-money-amount'})
        endereco = imovel.find('span', attrs={'class': 'ui-search-item__location-label'})
        link = imovel.find('a', attrs={'class': 'ui-search-link'})['href']

        if titulo and valor and endereco and link:
            lista_imoveis.append([ 'Mercado Livre', titulo.text, valor.text, endereco.text, link])
        else:
            lista_imoveis.append([
                'Mercado Livre',
                titulo.text if titulo else 'N/A',
                valor.text if valor else 'N/A',
                endereco.text if endereco else 'N/A',
                link,
            ])

    return lista_imoveis

def buscar_quinto_andar():
    lista_imoveis = []
    url_base = 'https://www.quintoandar.com.br/comprar/imovel/belo-horizonte-mg-brasil'
    response = requests.get(url_base).content
    site = BeautifulSoup(response, 'html.parser')
    imoveis = site.findAll('div', attrs={'class': 'sc-740uoz-0'})
    

    for imovel in imoveis:
        titulo = imovel.find('h2', attrs={'class': 'Cozy__CardTitle-Metadata Dg2zLY'})
        valor = imovel.find('h3', attrs={'class': 'CozyTypography xih2fc EKXjIf EqjlRj'})
        endereco = imovel.find('div', attrs={'class': 'Cozy__CardContent-Container XBxUCJ'})
        link = imovel.find('a', attrs={'class': 'sc-1d0oyoa-0'})['href']

        if titulo and valor and endereco and link:
            lista_imoveis.append([ 'QuintoAndar', titulo.text, valor.text, endereco.text, link])
        else:
            lista_imoveis.append([
                'QuintoAndar',
                titulo.text if titulo else 'N/A',
                valor.text if valor else 'N/A',
                endereco.text if endereco else 'N/A',
                link,
            ])

    return lista_imoveis

imoveis_ml = buscar_mercado_livre()

imoveis_qa = buscar_quinto_andar()

lista_completa = imoveis_ml + imoveis_qa

colunas = ['Fonte', 'Titulo', 'Preco', 'Endereço', 'Link']
df = pd.DataFrame(lista_completa, columns=colunas)

df.to_excel('Imoveis_Belo_Horizonte.xlsx', index=False)

print('SALVO COM SUCESSO')