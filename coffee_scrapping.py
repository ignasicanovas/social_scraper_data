import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Configura Selenium con Chrome."""
    options = Options()
    options.add_argument("--headless")  # Ejecuta el navegador en modo sin interfaz gráfica
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_page_urls(base_url, num_pages=5):
    """Genera URLs de páginas de noticias en Intelligence Coffee."""
    return [f"{base_url}/page/{i}/" for i in range(1, num_pages + 1)]

def get_article_links(driver, page_url):
    """Extrae enlaces de artículos desde Intelligence Coffee usando Selenium."""
    article_links = []
    
    try:
        driver.get(page_url)
        time.sleep(3)  # Esperar a que la página cargue
        
        articles = driver.find_elements(By.CSS_SELECTOR, "div.latest-posts__post h3.entry-title a")
        
        for article in articles:
            link = article.get_attribute("href")
            if link and link.startswith("https://intelligence.coffee/"):
                article_links.append(link)
        
        print(f"Enlaces obtenidos en {page_url}: {article_links}")
    except Exception as e:
        print(f"Error en {page_url}: {e}")
    
    return article_links

def scrape_article(driver, url, output_folder):
    """Descarga y extrae el contenido de un artículo usando Selenium y lo guarda en un archivo .txt."""
    try:
        driver.get(url)
        
        # Esperar a que el título esté presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        
        title = driver.find_element(By.TAG_NAME, "h1").text.strip()
        
        # Esperar a que el contenido esté presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
        )
        
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p")
        content = "\n".join([p.text.strip() for p in paragraphs])
        
        print(f"Procesando: {url}")
        print(f"Título: {title}")
        print(f"Fragmento de contenido: {content[:200]}")  # Muestra una parte del contenido extraído
        
        # Guardar contenido en un archivo .txt
        safe_title = title.replace(" ", "_").replace("/", "-").replace("?", "")[:50]  # Asegurar nombres válidos
        article_path = os.path.join(output_folder, f"{safe_title}.txt")
        with open(article_path, "w", encoding="utf-8") as file:
            file.write(f"Título: {title}\nURL: {url}\n\n{content}")
        
        return title, article_path
    except Exception as e:
        print(f"Error al procesar {url}: {e}")
        return None, None

def main():
    base_url = "https://intelligence.coffee"
    num_pages = 5
    output_folder = "intelligence_coffee_articles"
    output_file = "intelligence_coffee_index.csv"
    
    os.makedirs(output_folder, exist_ok=True)  # Crear carpeta si no existe
    driver = setup_driver()
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "File Path", "URL"])
        
        for page_url in get_page_urls(base_url, num_pages):
            article_links = get_article_links(driver, page_url)
            
            for article_url in article_links:
                title, file_path = scrape_article(driver, article_url, output_folder)
                
                if title and file_path:
                    writer.writerow([title, file_path, article_url])
                    print(f"Guardado: {title}")
                    
                time.sleep(2)  # Evita bloqueos
    
    driver.quit()
    print("Scraping completado. Los artículos se guardaron en la carpeta", output_folder)

if __name__ == "__main__":
    main()
