## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)

## General info
This small project which I committed to learn a new skill.

* `streamlit run asking-about-file-content.py`

Ten projekt to lokalna aplikacja RAG (Retrieval-Augmented Generation) z interfejsem webowym w Streamlit, która działa jako asystent do zadawania pytań do własnych dokumentów PDF.

🧠 Co to w praktyce jest?

To jest:

ChatGPT działający na Twoich PDF-ach, uruchomiony lokalnie

📄 1. Wczytywanie dokumentów (PDF)
DirectoryLoader(DOCS_DIR, glob="./*.pdf", loader_cls=PyPDFLoader)
skanuje folder data/
ładuje wszystkie PDF-y
zamienia je na tekst

✂️ 2. Dzielenie tekstu na fragmenty (chunking)
RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
dzieli dokumenty na małe fragmenty
dzięki temu LLM może je później „przeszukiwać”

🧠 3. Embeddings + baza wektorowa
OllamaEmbeddings(model="nomic-embed-text")
Chroma(...)
każdy fragment PDF zamieniany jest na embedding (wektor)
zapisywany w bazie ChromaDB
umożliwia semantyczne wyszukiwanie (nie tylko słowa kluczowe)

🔍 4. Retrieval (wyszukiwanie kontekstu)
vector_db.as_retriever(search_kwargs={"k": 3})
przy pytaniu użytkownika
system szuka 3 najbardziej podobnych fragmentów dokumentów

🧠 5. LLM + RAG (ChatOllama)
ChatOllama(model="llama3")

Model:

dostaje pytanie użytkownika
kontekst z dokumentów
generuje odpowiedź

* `streamlit run get-summary-from-notes.py`

Ten projekt to lokalna aplikacja do automatycznego streszczania notatek z użyciem modeli LLM (Ollama) i Streamlit.

🧠 Co to jest w praktyce?

To jest:

AI notatnik, który zamienia długie teksty w streszczenia, listy punktów lub taski

🖥️ 1. Interfejs użytkownika (Streamlit)

Aplikacja daje prosty UI:

pole tekstowe na notatkę
panel boczny z ustawieniami
przycisk „Generuj podsumowanie”
wynik w czasie rzeczywistym

* `python ssh-guard.py`

Ten projekt to prosty system wykrywania anomalii w logach SSH / logach systemowych z użyciem lokalnego modelu AI (Ollama).

Co robi ten skrypt?

W skrócie: monitoruje logi systemowe i wykrywa podejrzane próby logowania, a potem wysyła je do modelu AI, który ocenia czy to atak.

🔍 1. Monitorowanie logów

Skrypt działa inaczej zależnie od systemu:

Windows → czyta logi Security przez PowerShell (Get-WinEvent)
Linux → śledzi logi SSH przez journalctl -u ssh -f

🚨 2. Wykrywanie podejrzanych zdarzeń

Ma listę wzorców (regex), np.:

Failed password
Invalid user
logon failure
unknown user
failure

Jeśli linia logu pasuje → trafia do bufora jako podejrzana aktywność.

🧠 3. Analiza przez AI (Ollama)

Gdy przez ~5 sekund nie pojawi się nowy podejrzany log:

zbiera wszystkie zgromadzone logi
wysyła je do lokalnego modelu AI (phi3)

Model ma odpowiedzieć:

czy to atak (Yes/No)
jaki IP jest źródłem
ocena ryzyka 1–10
krótkie wyjaśnienie

📦 4. Buffering zdarzeń

Skrypt nie analizuje pojedynczych logów od razu, tylko:

zbiera „burst” zdarzeń
dopiero potem robi analizę

To pomaga wykrywać np. brute force (wiele prób w krótkim czasie).

🎯 Cel projektu

To jest mini:

AI-based Intrusion Detection System (IDS)

czyli:

system wykrywania włamań
oparty o logi systemowe
wspierany przez lokalny model LLM
💡 W praktyce

Może wykrywać np.:

brute force SSH
skanowanie loginów
próby logowania na nieistniejących użytkowników
automatyczne boty próbujące hasła

* `python log-analyzer.py`

Ten projekt to narzędzie do analizy plików logów przy użyciu lokalnego modelu AI (Ollama).

🧠 Co robi ten skrypt?

W praktyce działa jak:

AI log analyzer / mini system analizy bezpieczeństwa i błędów systemowych

🔍 1. Wczytuje plik logów
LOG_FILE_PATH = "sample.log"
bierze plik tekstowy z logami systemowymi, aplikacyjnymi lub security
sprawdza czy istnieje

📦 2. Dzieli logi na porcje (chunking)
CHUNK_SIZE = 50
bierze 50 linii naraz
łączy je w jeden „blok analizy”

To ważne, bo modele LLM mają limit kontekstu.

🧠 3. Wysyła logi do AI (Ollama)
ollama.generate(model="phi3", prompt=...)

Model dostaje instrukcję:

szukaj:
ataków (brute force, SQL injection, unauthorized access)
błędów systemowych / hardware failure
anomalii

📊 4. AI zwraca analizę

Model odpowiada np.:

„No issues detected”
albo opis problemów:
podejrzane logowania
błędy systemu
anomalie

* `python chatbot.py`

## Technologies
* Python version: 3.5
* ollama
* phi3