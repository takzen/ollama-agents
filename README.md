# Agent Analizy Danych - Ollama + LangChain + SQLite

## Opis projektu
Agent Analizy Danych to aplikacja Streamlit demonstrująca wykorzystanie modeli językowych do analizy danych biznesowych. Projekt łączy moce LLM (Llama 3.2 uruchomionego lokalnie przez Ollama), LangChain do orkiestracji agenta i SQLite jako lekką bazę danych.

## Funkcjonalności
- Zadawanie pytań o dane biznesowe w języku naturalnym
- Automatyczne generowanie i wykonywanie zapytań SQL
- Analiza wyników i generowanie wniosków przez LLM
- Graficzny interfejs w Streamlit z podpowiedziami i przykładami pytań
- Przykładowa baza danych sprzedażowa z realistycznymi danymi

## Wymagania
- Python 3.8+
- Ollama z zainstalowanym modelem llama3.2
- Biblioteki wymienione w `requirements.txt`

## Instalacja

1. Klonowanie repozytorium
```bash
git clone https://github.com/twoj-login/agent-analizy-danych.git
cd agent-analizy-danych
```

2. Tworzenie i aktywacja wirtualnego środowiska (opcjonalnie)
```bash
python -m venv venv
source venv/bin/activate  # Na Windows: venv\Scripts\activate
```

3. Instalacja wymaganych bibliotek
```bash
pip install -r requirements.txt
```

4. Upewnij się, że Ollama jest zainstalowany i model llama3.2 jest dostępny
```bash
ollama pull llama3.2
```

## Uruchomienie aplikacji
```bash
streamlit run app.py
```

## Struktura bazy danych
Aplikacja używa prostej bazy danych SQLite z następującymi tabelami:
- **klienci** (id_klienta, imie, nazwisko, email, miasto)
- **produkty** (id_produktu, nazwa, kategoria, cena)
- **zamowienia** (id_zamowienia, id_klienta, data, wartosc_calkowita)
- **szczegoly_zamowien** (id, id_zamowienia, id_produktu, ilosc, cena_jednostkowa)

## Przykładowe pytania
- "Którzy klienci wydali najwięcej w pierwszym kwartale 2024?"
- "Jakie są najpopularniejsze produkty według liczby sprzedanych sztuk?"
- "Jaki jest średni zakup w kategorii Elektronika?"
- "Porównaj sprzedaż miesięczną w pierwszym kwartale 2024."
- "Którzy klienci kupili produkty z kategorii Audio?"

## Jak to działa?
1. Użytkownik zadaje pytanie w języku naturalnym
2. Agent przekształca pytanie na zapytanie SQL
3. Zapytanie jest wykonywane na bazie danych
4. LLM analizuje wyniki i generuje przydatne wnioski
5. Odpowiedź jest prezentowana użytkownikowi

## Technologie
- **LangChain** - framework do budowania aplikacji zasilanych przez LLM
- **Ollama** - narzędzie do lokalnego uruchamiania modeli językowych
- **Llama 3.2** - zaawansowany model językowy
- **SQLite** - lekka baza danych
- **Streamlit** - framework do tworzenia webowych aplikacji z Pythonem

## Licencja
MIT

## Autor
[Twoje Imię i Nazwisko]
