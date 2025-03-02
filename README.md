# Streszczacz Artykułów z Internetu (LangChain, Ollama, Streamlit)

Ten projekt to prosta aplikacja webowa, która pobiera artykuł z podanego adresu URL i generuje jego streszczenie, używając modelu językowego Ollama uruchomionego lokalnie i frameworka LangChain.

## Funkcjonalności

*   **Pobieranie treści artykułu:** Aplikacja pobiera treść artykułu z podanego adresu URL, korzystając z bibliotek `requests` i `BeautifulSoup4`.
*   **Streszczanie artykułu:** Wykorzystuje model językowy Ollama (domyślnie `llama2`) i LangChain do wygenerowania zwięzłego streszczenia artykułu.
*   **Interfejs użytkownika:** Prosty interfejs zbudowany za pomocą Streamlit, pozwalający na wprowadzenie adresu URL i wyświetlenie streszczenia.
*   **Obsługa błędów:** Podstawowa obsługa błędów, takich jak nieprawidłowy adres URL lub problemy z pobraniem strony.

## Wymagania

*   **Python 3.9+** (zalecane 3.10 lub nowszy)
*   **Ollama:** Zainstalowany i uruchomiony lokalnie (instrukcje: [https://ollama.com/](https://ollama.com/)).  Upewnij się, że masz pobrany model `llama2` (`ollama pull llama2`).
*   **Biblioteki Pythona:**
    *   `streamlit`
    *   `langchain-community`
    *   `requests`
    *   `beautifulsoup4`

## Instalacja

1.  **Zainstaluj Ollama:** Pobierz i zainstaluj Ollama ze strony [https://ollama.com/](https://ollama.com/).  Postępuj zgodnie z instrukcjami dla Twojego systemu operacyjnego.
2.  **Pobierz model `llama2`:**  W terminalu/wierszu poleceń uruchom:

    ```bash
    ollama pull llama2
    ```
3.  **Zainstaluj biblioteki Pythona:**

    ```bash
    pip install streamlit langchain-community requests beautifulsoup4
    ```

## Uruchomienie

1.  **Zapisz kod aplikacji:** Skopiuj kod aplikacji (podany w poprzedniej odpowiedzi) do pliku, np. `app.py`.
2.  **Uruchom aplikację Streamlit:** W terminalu/wierszu poleceń, przejdź do katalogu, w którym zapisałeś plik `app.py` i uruchom:

    ```bash
    streamlit run app.py
    ```

    Otworzy się strona aplikacji w Twojej przeglądarce internetowej.

3.  **Wklej adres URL artykułu** w polu tekstowym i poczekaj na wygenerowanie streszczenia.

## Struktura kodu

*   **`app.py`:**  Główny plik aplikacji, zawierający:
    *   **`get_llm()`:**  Inicjalizuje model Ollama.  Używa `@st.cache_resource`, aby model był ładowany tylko raz.
    *   **`prompt_template`:**  Szablon promptu przekazywanego do modelu Ollama.  Zawiera instrukcję streszczenia i miejsce na treść artykułu.
    *   **`get_article_text(url)`:**  Pobiera treść artykułu ze strony internetowej, parsując HTML za pomocą `BeautifulSoup`.
    *   **`summarize_article(article_text)`:**  Wysyła sformatowany prompt do modelu Ollama i zwraca wygenerowane streszczenie.
    *   **Interfejs Streamlit:**  Tworzy interfejs użytkownika z polem tekstowym na adres URL i miejscem na wyświetlenie streszczenia.

## Możliwe ulepszenia

*   **Bardziej zaawansowane parsowanie HTML:** Obecna implementacja `get_article_text` jest prosta i może nie działać poprawnie na wszystkich stronach.  Można ją ulepszyć, używając bardziej zaawansowanych selektorów CSS lub dedykowanych bibliotek do ekstrakcji treści (np. `trafilatura`, `goose3`).
*   **Wybór modelu Ollama:** Dodanie możliwości wyboru innego modelu Ollama (jeśli użytkownik ma zainstalowane inne modele).
*   **Wybór długości streszczenia:**  Dodanie opcji pozwalającej użytkownikowi określić, jak długie ma być streszczenie (np. liczba zdań, liczba słów).
*   **Wyświetlanie oryginalnego tekstu:**  Wyświetlanie oryginalnego tekstu artykułu obok streszczenia.
*   **Lepsza obsługa błędów:**  Bardziej szczegółowe komunikaty o błędach i obsługa większej liczby potencjalnych problemów (np. timeout przy pobieraniu strony, błędy parsowania HTML).
*   **Formatowanie streszczenia:**  Poprawa formatowania wygenerowanego streszczenia (np. dzielenie na akapity).
* **Dodanie testów jednostkowych.**

## Licencja

Ten projekt jest udostępniony na licencji MIT.  Zobacz plik [LICENSE](LICENSE) (który powinieneś utworzyć i umieścić w repozytorium) po szczegóły.

## Autor

Krzysztof Pika