import os
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
import markdown
from xhtml2pdf import pisa

# --- IMPOSTAZIONI DEL SITO WEB ---
st.set_page_config(page_title="Sintesi.ai - Motore Predittivo", page_icon="📊", layout="centered")

st.title("📊 Sintesi.ai - Executive Deep-Audit")
st.markdown("**Simulatore di Rischio ESG e Swarm Intelligence.** Incolla la bozza della campagna per generare un Memorandum per il Board of Directors.")

# Box dove l'utente incolla il testo
campagna_cliente = st.text_area("Testo della Campagna da analizzare:", height=150, placeholder="Es: La nostra nuova bottiglia è 100% amica dell'ambiente...")

# Bottone per avviare la magia
if st.button("🚀 Genera Report Esecutivo"):
    if non campagna_cliente:
        st.warning("Per favore, inserisci il testo della campagna prima di avviare.")
    else:
        with st.spinner("Inizializzazione Sciame Predittivo e Motori di Compliance in corso... (richiede circa 1 minuto)"):
            
            # 1. ATTIVA IL CERVELLO (Legge la chiave nascosta in modo sicuro)
            os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
            motore_ai = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.1)

            # 2. GLI AGENTI (Stessi di prima, compatti)
            nodo_demografico = Agent(role="Head of Consumer Insights", goal="Mappare l'attrito demografico e i driver di rigetto.", backstory="Segmenti le reazioni per coorti e fornisci percentuali secche di penetrazione e rigetto. Tono spietato e analitico.", allow_delegation=False, llm=motore_ai)
            nodo_legale = Agent(role="Chief Compliance & Risk Officer", goal="Calcolare esposizione finanziaria e rischi legali.", backstory="Cita precedenti antitrust UE (Green Claims). Calcola impatto economico su fatturato 10M€.", allow_delegation=False, llm=motore_ai)
            nodo_media = Agent(role="Director of Crisis Communication", goal="Prevedere il Fallout reputazionale.", backstory="Prevedi titoli di giornale d'inchiesta e Tasso di Viralità Negativa.", allow_delegation=False, llm=motore_ai)
            orchestratore = Agent(role="Managing Partner", goal="Sintetizzare i dati in un Executive Memorandum.", backstory="Usi framework strategici (MECE). Crea Matrice A/B/C di mitigazione.", allow_delegation=False, llm=motore_ai)

            # 3. I TASK
            task_demografico = Task(description=f"Analisi frizione demografica su: {campagna_cliente}.", expected_output="Metriche di rigetto per coorte.", agent=nodo_demografico)
            task_compliance = Task(description=f"Risk assessment legale su: {campagna_cliente}.", expected_output="Liability report.", agent=nodo_legale)
            task_media = Task(description=f"Previsione Fallout mediatico per: {campagna_cliente}.", expected_output="Titoli ostili.", agent=nodo_media)
            task_finale = Task(
                description="""Redigi l'EXECUTIVE BOARD MEMORANDUM in Markdown puro. 
                STRUTTURA:
                ## 1. EXECUTIVE SUMMARY & RISK EXPOSURE
                ## 2. CONSUMER INSIGHTS & SENTIMENT SHIFT
                ## 3. REGULATORY LIABILITY & FINANCIAL IMPACT (€)
                ## 4. BRAND EQUITY FALLOUT (Media Forecast)
                ## 5. MITIGATION STRATEGY & RISK/REWARD MATRIX (Opzioni A, B, C)""",
                expected_output="Documento strategico.", agent=orchestratore
            )

            # 4. ESECUZIONE
            sintesi_engine = Crew(agents=[nodo_demografico, nodo_legale, nodo_media, orchestratore], tasks=[task_demografico, task_compliance, task_media, task_finale], process=Process.sequential)
            risultato = sintesi_engine.kickoff()

            # 5. CREAZIONE DEL PDF
            html_body = markdown.markdown(str(risultato))
            html_styled = f"""
            <html><head><style>
                @page {{ size: A4; margin: 2.5cm; @frame footer {{ -pdf-frame-content: footer_content; bottom: 1cm; margin-left: 2.5cm; margin-right: 2.5cm; height: 1cm; }} }}
                body {{ font-family: Helvetica, sans-serif; font-size: 11pt; color: #2c3e50; line-height: 1.6; }}
                .cover {{ text-align: left; margin-top: 150px; }}
                .cover-title {{ font-size: 36pt; color: #002D62; font-weight: bold; margin-bottom: 20px; }}
                .cover-subtitle {{ font-size: 18pt; color: #7f8c8d; margin-bottom: 100px; border-left: 4px solid #002D62; padding-left: 15px; }}
                .cover-confidential {{ font-size: 10pt; color: #c0392b; font-weight: bold; margin-top: 20px; letter-spacing: 1px; }}
                h1 {{ color: #002D62; font-size: 20pt; border-bottom: 2px solid #002D62; padding-bottom: 8px; margin-top: 30px; page-break-before: always; }}
                h2 {{ color: #004080; font-size: 14pt; margin-top: 25px; margin-bottom: 15px; }}
            </style></head>
            <body>
                <div class="cover"><div class="cover-title">EXECUTIVE<br>BOARD MEMORANDUM</div>
                <div class="cover-subtitle">Predictive Deep-Audit: ESG & Compliance</div>
                <div class="cover-confidential">Strictly Confidential</div></div>
                <pdf:nextpage />
                {html_body}
                <div id="footer_content" style="text-align: right; font-size: 8pt; color: #95a5a6; border-top: 1px solid #bdc3c7; padding-top: 5px;">Sintesi.ai | Swarm Intelligence Model</div>
            </body></html>
            """
            
            pdf_filename = "Sintesi_Executive_Memorandum.pdf"
            with open(pdf_filename, "w+b") as result_file:
                pisa.CreatePDF(html_styled, dest=result_file)

            st.success("✅ Audit Generato con successo!")
            
            # Bottone per far scaricare il PDF all'utente
            with open(pdf_filename, "rb") as pdf_file:
                st.download_button(label="📥 Scarica il Memorandum (PDF)", data=pdf_file, file_name=pdf_filename, mime="application/pdf")
