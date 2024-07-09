import csv
import time
from datetime import datetime
from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup

class CNBCScraper:
    def __init__(self, search_terms):
        self.search_terms = search_terms
        self.articles = []

    def accept_cookies(self, driver):
        try:
            # Attendre que le bouton de consentement apparaisse et cliquer dessus
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            )
            accept_button.click()
            print("Cookies accepted.")
        except Exception as e:
            print(f"Error accepting cookies: {e}")

    def extract_article_text(self, article_url, driver):
        # Exclure les articles vidéo
        if "/video/" in article_url:
            return ""  # Ne rien retourner pour les vidéos
    
        try:
            driver.get(article_url)
            
            # Attendre que le corps de l'article soit chargé
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ArticleBody-articleBody'))
            )
            
            # Extraire le contenu de la page une fois chargé
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            article_body = soup.find('div', class_='ArticleBody-articleBody')
            paragraphs = article_body.find_all('p') if article_body else []
            article_text = ' '.join([para.text for para in paragraphs])
            return article_text
        except Exception as e:
            print(f"Error extracting article text from {article_url}: {e}")
            return ""

    def get_pages(self, sleep_time=3):
        print('Running get_pages()...')
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver_path = r"C:\Users\yannp\Desktop\rcp209\projet\projet-RCP209\chromedriver-win64\chromedriver.exe"
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        search_url = f"https://www.cnbc.com/search/?query={'+'.join(self.search_terms)}"
        print(f"Navigating to URL: {search_url}")
        driver.get(search_url)
        time.sleep(sleep_time)

        # Accepter les cookies si nécessaire
        self.accept_cookies(driver)

        # Scroll to load more articles
        for scroll_count in range(100):  # Augmenté le nombre de scrolls pour charger plus d'articles
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"Scrolled {scroll_count + 1} times")
            time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Save the page source for debugging
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        articles = soup.find_all('div', class_='SearchResult-searchResult')
        print(f"Number of articles found: {len(articles)}")

        if not articles:
            print("No articles found. The structure of the page may have changed or the search terms may not match any articles.")
        else:
            print(f"Found {len(articles)} articles. Processing...")

        for article_index, article in enumerate(articles):
            try:
                title_element = article.find('div', class_='SearchResult-searchResultTitle').find('a')
                title = title_element.text.strip() if title_element else 'No title'
                link = title_element['href'].strip() if title_element else 'No link'
                category_element = article.find('div', class_='SearchResult-searchResultEyebrow').find('a')
                category = category_element.text.strip() if category_element else 'No category'
                author_element = article.find('a', class_='SearchResult-author')
                author = author_element.text.strip() if author_element else 'No author'
                date_element = article.find('span', class_='SearchResult-publishedDate')
                date = date_element.text.strip() if date_element else 'No date'

                article_text = self.extract_article_text(link, driver)

                self.articles.append({
                    'title': title,
                    'date_published': date,
                    'category': category,
                    'author': author,
                    'article_link': link,
                    'text': article_text
                })

                print(f"Article {article_index + 1} scraped: {title}")
            except Exception as e:
                print(f"Error processing article {article_index + 1}: {e}")

        driver.quit()


    def write_to_csv(self, file_name):
        if not self.articles:
            print("No articles to write to CSV.")
            return

        print('Writing to CSV...')
        keys = self.articles[0].keys()
        with open(file_name, 'w', encoding='utf-8', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.articles)
        print('Written to file')

def run_scraper(search_terms):
    scraper = CNBCScraper(search_terms)
    scraper.get_pages()
    if not scraper.articles:
        print('No articles found for the given search terms.')
        return

    save_to_csv = input('Do you want to save the data to a CSV file? (yes/no): ').strip().lower()
    if save_to_csv == 'yes':
        file_name = input('Enter the CSV file name: ').strip()
        scraper.write_to_csv(file_name)
    else:
        print('Data not saved.')

# Utilisation
terms = ["Apple"]
run_scraper(terms)
