from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def buscar_produtos(nome):
    options = Options()

    # 👉 deixar visível pra debug (depois pode comentar)
    # options.add_argument("--headless=new")

    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)

    url = f"https://lista.mercadolivre.com.br/{nome}"
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    # 🔥 fechar cookies
    try:
        btn_cookie = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceitar')]"))
        )
        btn_cookie.click()
        print("Cookies aceitos")
    except:
        print("Sem popup de cookies")

    # 🔥 fechar CEP
    try:
        btn_cep = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Entendi')]"))
        )
        btn_cep.click()
        print("Popup de CEP fechado")
    except:
        print("Sem popup de CEP")

    # 🔥 esperar produtos carregarem
    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.ui-search-layout__item"))
        )
    except:
        print("Produtos não carregaram")
        driver.quit()
        return []

    # 🔥 scroll (garante carregamento completo)
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    itens = soup.select("li.ui-search-layout__item")

    print(f"Produtos encontrados (cards): {len(itens)}")

    produtos = []

    for item in itens:
        try:
            # 🔥 NOVO TÍTULO (baseado no seu HTML)
            titulo_el = item.select_one("a.poly-component__title")

            # 🔥 PREÇO
            preco_el = item.select_one(".andes-money-amount__fraction")

            if not titulo_el or not preco_el:
                continue

            titulo = titulo_el.get_text(strip=True)
            preco_texto = preco_el.get_text(strip=True)

            preco = float(preco_texto.replace(".", "").replace(",", "."))

            produtos.append({
                "nome": titulo,
                "preco": preco
            })

        except Exception as e:
            print("Erro item:", e)
            continue

    print(f"Produtos válidos: {len(produtos)}")
    print("Exemplo:", produtos[:3])

    return produtos