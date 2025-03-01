# Instalacja potrzebnych bibliotek:
# pip install langchain langchain-community langchain-core langchain-sqlite pydantic streamlit ollama

import os
import streamlit as st
import pandas as pd
import sqlite3
from langchain_community.llms import Ollama
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_sqlite import SQLiteEngine
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.tools.render import format_tool_to_openai_function
from langchain_core.tools import Tool

# Konfiguracja aplikacji Streamlit
st.title("Agent do analizy danych z użyciem Ollama i LangChain")

# Inicjalizacja modelu Ollama
@st.cache_resource
def get_llm():
    return Ollama(model="llama3.2", temperature=0)

llm = get_llm()

# Tworzenie przykładowej bazy danych
def create_sample_database():
    conn = sqlite3.connect('sprzedaz.db')
    c = conn.cursor()
    
    # Tworzenie tabeli klientów
    c.execute('''
    CREATE TABLE IF NOT EXISTS klienci (
        id_klienta INTEGER PRIMARY KEY,
        imie TEXT,
        nazwisko TEXT,
        email TEXT,
        miasto TEXT
    )
    ''')
    
    # Tworzenie tabeli produktów
    c.execute('''
    CREATE TABLE IF NOT EXISTS produkty (
        id_produktu INTEGER PRIMARY KEY,
        nazwa TEXT,
        kategoria TEXT,
        cena REAL
    )
    ''')
    
    # Tworzenie tabeli zamówień
    c.execute('''
    CREATE TABLE IF NOT EXISTS zamowienia (
        id_zamowienia INTEGER PRIMARY KEY,
        id_klienta INTEGER,
        data TEXT,
        wartosc_calkowita REAL,
        FOREIGN KEY (id_klienta) REFERENCES klienci (id_klienta)
    )
    ''')
    
    # Tworzenie tabeli szczegółów zamówień
    c.execute('''
    CREATE TABLE IF NOT EXISTS szczegoly_zamowien (
        id INTEGER PRIMARY KEY,
        id_zamowienia INTEGER,
        id_produktu INTEGER,
        ilosc INTEGER,
        cena_jednostkowa REAL,
        FOREIGN KEY (id_zamowienia) REFERENCES zamowienia (id_zamowienia),
        FOREIGN KEY (id_produktu) REFERENCES produkty (id_produktu)
    )
    ''')
    
    # Wstawianie przykładowych danych
    # Klienci
    klienci = [
        (1, 'Jan', 'Kowalski', 'jan.kowalski@example.com', 'Warszawa'),
        (2, 'Anna', 'Nowak', 'anna.nowak@example.com', 'Kraków'),
        (3, 'Piotr', 'Wiśniewski', 'piotr.wisniewski@example.com', 'Wrocław'),
        (4, 'Alicja', 'Dąbrowska', 'alicja.dabrowska@example.com', 'Gdańsk'),
        (5, 'Tomasz', 'Lewandowski', 'tomasz.lewandowski@example.com', 'Poznań')
    ]
    c.executemany('INSERT OR REPLACE INTO klienci VALUES (?,?,?,?,?)', klienci)
    
    # Produkty
    produkty = [
        (1, 'Laptop Dell XPS 15', 'Elektronika', 6999.99),
        (2, 'Smartfon Samsung Galaxy S23', 'Elektronika', 3999.99),
        (3, 'Słuchawki Sony WH-1000XM5', 'Akcesoria', 1599.99),
        (4, 'Klawiatura mechaniczna Logitech', 'Akcesoria', 499.99),
        (5, 'Monitor Dell 27"', 'Elektronika', 1299.99),
        (6, 'Mysz bezprzewodowa Logitech', 'Akcesoria', 249.99),
        (7, 'Tablet Apple iPad Pro', 'Elektronika', 4499.99),
        (8, 'Głośnik Bluetooth JBL', 'Audio', 399.99),
        (9, 'Dysk SSD Samsung 1TB', 'Komponenty', 599.99),
        (10, 'Kamera internetowa Logitech', 'Akcesoria', 349.99)
    ]
    c.executemany('INSERT OR REPLACE INTO produkty VALUES (?,?,?,?)', produkty)
    
    # Zamówienia
    zamowienia = [
        (1, 1, '2024-01-15', 7499.98),
        (2, 2, '2024-01-20', 4499.98),
        (3, 3, '2024-02-05', 1849.98),
        (4, 4, '2024-02-10', 6299.98),
        (5, 5, '2024-02-15', 649.98),
        (6, 1, '2024-02-25', 4899.98),
        (7, 2, '2024-03-05', 5799.98),
        (8, 3, '2024-03-10', 949.98),
        (9, 4, '2024-03-15', 599.99),
        (10, 5, '2024-03-20', 3999.99)
    ]
    c.executemany('INSERT OR REPLACE INTO zamowienia VALUES (?,?,?,?)', zamowienia)
    
    # Szczegóły zamówień
    szczegoly = [
        (1, 1, 1, 1, 6999.99),
        (2, 1, 3, 1, 499.99),
        (3, 2, 2, 1, 3999.99),
        (4, 2, 3, 1, 499.99),
        (5, 3, 3, 1, 1599.99),
        (6, 3, 6, 1, 249.99),
        (7, 4, 7, 1, 4499.99),
        (8, 4, 8, 2, 399.99),
        (9, 5, 6, 1, 249.99),
        (10, 5, 10, 1, 399.99),
        (11, 6, 5, 1, 1299.99),
        (12, 6, 9, 6, 599.99),
        (13, 7, 1, 1, 5599.99),
        (14, 7, 6, 1, 199.99),
        (15, 8, 4, 1, 499.99),
        (16, 8, 6, 1, 249.99),
        (17, 8, 8, 1, 199.99),
        (18, 9, 9, 1, 599.99),
        (19, 10, 2, 1, 3999.99)
    ]
    c.executemany('INSERT OR REPLACE INTO szczegoly_zamowien VALUES (?,?,?,?,?)', szczegoly)
    
    conn.commit()
    conn.close()
    
    return 'sprzedaz.db'

# Tworzenie bazy danych
db_path = create_sample_database()

# Podłączenie do bazy danych
engine = SQLiteEngine(db_path)

# Narzędzie do wykonywania zapytań SQL
query_tool = QuerySQLDataBaseTool(db=engine)

# Narzędzie do generowania zapytań SQL na podstawie pytań w języku naturalnym
sql_chain = create_sql_query_chain(llm, engine)

def generate_and_execute_query(question):
    query = sql_chain.invoke({"question": question})
    st.code(query, language="sql")
    return query_tool.invoke({"query": query})

# Narzędzie do generowania opisowych analiz danych
def analyze_data(query_result):
    if not query_result or query_result.strip() == "":
        return "Brak danych do analizy."
    
    template = """
    Przeanalizuj poniższe dane i przedstaw wnikliwą, zwięzłą analizę. Wyjaśnij główne wzorce, trendy lub spostrzeżenia.
    
    Dane:
    {data}
    
    Twoja analiza powinna być profesjonalna i zawierać konkretne wnioski oparte na danych.
    """
    
    prompt = PromptTemplate(template=template, input_variables=["data"])
    chain = prompt | llm
    
    return chain.invoke({"data": query_result})

# Definiowanie narzędzi dla agenta
tools = [
    Tool(
        name="GenerateAndExecuteQuery",
        func=generate_and_execute_query,
        description="Generuje i wykonuje zapytanie SQL na podstawie pytania w języku naturalnym. Użyj tego narzędzia, gdy chcesz uzyskać dane z bazy."
    ),
    Tool(
        name="AnalyzeData",
        func=analyze_data,
        description="Analizuje wyniki zapytania i generuje wnikliwe wnioski. Użyj tego narzędzia do analizy danych otrzymanych z bazy."
    )
]

# Definiowanie templatki promptu dla agenta
prompt_template = """
Jesteś zaawansowanym agentem do analizy danych, który pomaga użytkownikom zrozumieć ich dane biznesowe.
Twoje zadanie to odpowiadanie na pytania o dane sprzedażowe firmy przy pomocy analizy bazy danych SQLite.

Baza danych zawiera następujące tabele:
- klienci (id_klienta, imie, nazwisko, email, miasto)
- produkty (id_produktu, nazwa, kategoria, cena)
- zamowienia (id_zamowienia, id_klienta, data, wartosc_calkowita)
- szczegoly_zamowien (id, id_zamowienia, id_produktu, ilosc, cena_jednostkowa)

Pytanie użytkownika: {input}

{agent_scratchpad}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

# Tworzenie agenta
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Interfejs użytkownika
pytanie = st.text_input("Zadaj pytanie o dane sprzedażowe:", placeholder="Np. Którzy klienci wydali najwięcej w ostatnim kwartale?")

if pytanie:
    with st.spinner("Analizuję dane..."):
        try:
            odpowiedz = agent_executor.invoke({"input": pytanie})
            st.write("### Odpowiedź:")
            st.write(odpowiedz["output"])
        except Exception as e:
            st.error(f"Wystąpił błąd: {str(e)}")

# Pokazanie schematu bazy danych
with st.expander("Schemat bazy danych"):
    conn = sqlite3.connect(db_path)
    
    st.write("### Tabela: klienci")
    df_klienci = pd.read_sql_query("SELECT * FROM klienci LIMIT 5", conn)
    st.dataframe(df_klienci)
    
    st.write("### Tabela: produkty")
    df_produkty = pd.read_sql_query("SELECT * FROM produkty LIMIT 5", conn)
    st.dataframe(df_produkty)
    
    st.write("### Tabela: zamowienia")
    df_zamowienia = pd.read_sql_query("SELECT * FROM zamowienia LIMIT 5", conn)
    st.dataframe(df_zamowienia)
    
    st.write("### Tabela: szczegoly_zamowien")
    df_szczegoly = pd.read_sql_query("SELECT * FROM szczegoly_zamowien LIMIT 5", conn)
    st.dataframe(df_szczegoly)
    
    conn.close()

# Przykładowe pytania
st.sidebar.header("Przykładowe pytania:")
example_questions = [
    "Którzy klienci wydali najwięcej w pierwszym kwartale 2024?",
    "Jakie są najpopularniejsze produkty według liczby sprzedanych sztuk?",
    "Jaki jest średni zakup w kategorii Elektronika?",
    "Porównaj sprzedaż miesięczną w pierwszym kwartale 2024.",
    "Którzy klienci kupili produkty z kategorii Audio?"
]

for q in example_questions:
    if st.sidebar.button(q):
        st.text_input("Zadaj pytanie o dane sprzedażowe:", value=q, key=f"example_{q}")
