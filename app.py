import streamlit as st
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import requests
from bs4 import BeautifulSoup

# Inicjalizacja modelu Ollama
@st.cache_resource
def get_llm():
    return Ollama(model="llama3.2", temperature=0)  # Użyj llama2

llm = get_llm()

# Szablon promptu
prompt_template = """
Streszcz poniższy artykuł do maksymalnie 5 kluczowych zdań.  Zwróć TYLKO streszczenie, bez żadnych dodatkowych komentarzy, wstępu ani zakończenia.

Artykuł:
{article_text}

Streszczenie:
"""
prompt = PromptTemplate.from_template(prompt_template)

def get_article_text(url):
    """Pobiera treść artykułu ze strony internetowej."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Rzuć wyjątek dla kodów błędów (np. 404)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Prosty (i niedoskonały) sposób na wyciągnięcie tekstu:
        # Szukamy tagów <p> (paragrafów), które zwykle zawierają główny tekst.
        paragraphs = soup.find_all('p')
        text = '\n'.join([p.get_text() for p in paragraphs])
        return text

    except requests.exceptions.RequestException as e:
        st.error(f"Błąd pobierania strony: {e}")
        return None
    except Exception as e:
        st.error(f"Błąd przetwarzania strony: {e}")
        return None

def summarize_article(article_text):
    """Streszcza artykuł za pomocą Ollama."""
    formatted_prompt = prompt.format(article_text=article_text)
    summary = llm.invoke(formatted_prompt)
    return summary.strip()

# Interfejs Streamlit
st.title("Streszczacz Artykułów")

url = st.text_input("Wklej adres URL artykułu:", placeholder="https://...")

if url:
    with st.spinner("Pobieram i streszczam artykuł..."):
        article_text = get_article_text(url)
        if article_text:
            summary = summarize_article(article_text)
            if summary:
                st.write("### Streszczenie:")
                st.write(summary)
            else: #Na wszelki wypadek
                st.write("Przepraszam, nie udało się wygenerować streszczenia.")