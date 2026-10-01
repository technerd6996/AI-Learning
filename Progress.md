# AI-Learning
This is Repository is the progress I make in my AI Learning journey

06-04-2026
* Added my initial basics on Python.
* Added my first AI API Call using Python.
* Command to set Environmental Variable setx GROQ_API_KEY ""

07-04-2026
* Understood basic concept of appending the data to List Dictionary.
* Added the logic and modified the code.

08-04-2026
 * Learnt about RAG
 * Learnt about File Handling, Reducing files to chunks
 * More on PIP and Packages
 * Vector DB Intros

09-04-2026

* Learnt about chunking and storing it in client session
* Faced problem while loading
* Hosted the app in Streamlit
* Added a github app_actual.py as code file

10-04-2026

* Added Persistent DB
* Built script to add the data to DB
* Made the web load instantly in Streamlit
* Added Expertise Level feature in the WebApp
* Practiced 3 HackerRank Questions
* Changed Readme to Progress

11-04-2026

* Identified 8 minute cold start problem
* Built build_db.py — separate indexing script
* Implemented PersistentClient — instant loading
* Deployed fix — cold start dropped to seconds

* Identified knowledge gaps — DevOps vs SRE, Agile vs SRE
* Added new documents — SRE_Intro.txt, SRE_DevOps.txt
* Built incremental indexing — add new docs without rebuilding
* Fixed encoding errors independently
* Final chunk count — 1063 chunks

* Built rag_utils.py — reusable core module
* Refactored app.py — 120 lines to 64 lines
* Built evaluate.py — automated test suite
* Implemented LLM-as-a-judge evaluation
* Added prompt injection guardrails
* Went from failing jailbreak tests to 10/10 pass rate

12-04-2026

* Fixed cold start performance
* Incremental indexing working
* Guardrails refined — 9/10 evaluation
* UI improvements — dropdown, welcome message
* Code refactored and cleaned 

01-10-2026

* Migrated from the unavailable Llama 4 Scout model to currently supported Groq models.
* Separated prompt-injection detection from RAG response generation.
* Explored Prompt Guard models for lightweight security classification.
* Explored GPT-OSS models for RAG response generation.
* Learned the difference between specialized security models and general-purpose instruct models.
* Improved the RAG pipeline: Security Check → Retrieval → Context Augmentation → LLM Generation.
* Fixed conversation history handling to prevent accidental mutation of Streamlit session state.
* Improved system prompt handling for maintaining the SRE assistant role.
* Added a floating Clear Chat History button to the Streamlit interface.
* Improved chat history management and automatic history trimming.
* Removed duplicate session-state initialization logic.
* Continued refactoring `app_actual.py` and `rag_utils.py` for cleaner separation of responsibilities.
* Improved understanding of prompt injection, jailbreak protection, RAG security, and model selection.
* Continued optimizing the application toward a more reliable and production-oriented AI architecture.
