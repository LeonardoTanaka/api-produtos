import requests
from bs4 import BeautifulSoup
import re


def eh_produto_principal(titulo, palavras_busca):
    titulo = titulo.lower()

    
    palavras_bloqueadas = [
        "capa", "case", "adesiv", "pelicul", "suporte",
        "teclado", "mouse", "kit", "combo", "protetor",
        "cabo", "carregador", "adaptador", "skin"
    ]

    if any(p in titulo for p in palavras_bloqueadas):
        return False

    # ✔ precisa conter pelo menos uma palavra da busca
    if not any(p in titulo for p in palavras_busca):
        return False

    # ✔ precisa parecer produto real (tem número)
    if not re.search(r"\d", titulo):
        return False

    return True


def buscar_produtos(nome):
    url = f"https://lista.mercadolivre.com.br/{nome}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Erro ao acessar página")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    itens = soup.select("li.ui-search-layout__item")

    print(f"Produtos encontrados (cards): {len(itens)}")

    produtos = []
    palavras_busca = nome.lower().split()

    for item in itens:
        try:
            titulo_tag = item.select_one("h2, h3")
            preco_tag = item.select_one(".andes-money-amount__fraction")
            link_tag = item.select_one("a")

            if not titulo_tag or not preco_tag or not link_tag:
                continue

            titulo = titulo_tag.get_text().strip()
            titulo_lower = titulo.lower()

            # 🔥 filtro inteligente
            if not eh_produto_principal(titulo_lower, palavras_busca):
                continue

            preco = preco_tag.get_text().replace(".", "").replace(",", ".")
            preco = float(preco)

            link = link_tag["href"]

            produtos.append({
                "nome": titulo,
                "preco": preco,
                "link": link
            })

        except Exception as e:
            print("Erro item:", e)
            continue

    print(f"Produtos válidos: {len(produtos)}")

    # ordena por menor preço
    produtos = sorted(produtos, key=lambda x: x["preco"])

    return produtos