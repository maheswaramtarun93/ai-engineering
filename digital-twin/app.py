import os
import uuid
from pprint import pprint
import gradio as gr
from openai import OpenAI
import chromadb

# ---------------------------------------------------
# TARUN DOCUMENTS (ALL 3 COMBINED)
# ---------------------------------------------------

DOCUMENT_OVERVIEW = """
Tarun Maheswaram is a Business Intelligence (BI) Developer with over 9 years of experience helping organizations transform raw data into meaningful business insights. He specializes in designing dashboards, building reporting solutions, optimizing databases, and enabling data-driven decision making.

He holds a Master's degree in Information Technology and has built his career around data analytics, business intelligence, and modern reporting platforms.

Throughout his career, he has worked with several organizations including:

I have started pursuing my bachelor's degree in ECE in India in 2011.
• Blue Cross of Idaho, where he worked for over six years as a BI Developer building enterprise reporting solutions and supporting healthcare analytics.
• MWI Animal Health, developing reporting and analytics solutions that improved business visibility and operational reporting.
• Pennsylvania Transformer Technology, where he worked as a Power BI and Tableau Developer, creating interactive dashboards and business intelligence solutions.

His technical expertise includes:

- Microsoft SQL Server
- Advanced SQL
- Power BI
- Tableau
- SSRS
- Data Warehousing
- ETL processes
- Data Modeling
- Dashboard Design
- Performance Optimization
- Business Intelligence Architecture

Additional Info:
- He enjoys solving complex business problems using data.
- Recently expanded into AI, RAG, embeddings, Python, OpenAI, Gradio.
- Practical, analytical, solution‑oriented.
- Friendly, patient, clear communicator.
"""

DOCUMENT_EDUCATION = """
Education

Valparaiso University
Master’s Degree in Information Technology (Jan 2016 – Aug 2017)

JNTU Hyderabad
Bachelor’s Degree in Electronics and Communication Engineering (Aug 2011 – May 2015)
"""

DOCUMENT_EXPERIENCE = """
Power BI Developer — Pennsylvania Transformer Technology (Jun 2024 – Present)
Built executive‑level dashboards, validated data sources, developed dynamic Power BI visualizations, designed efficient data models, wrote optimized DAX, built custom visuals, standardized KPIs, performed QA testing.

Power BI Developer — Blue Cross of Idaho (Feb 2021 – May 2024)
Worked across SQL Server, SSIS, SSAS, SSRS, Power BI. Migrated ETL, debugged stored procedures, converted Tableau, optimized Crystal Reports, built Power BI visuals, integrated SQL/Excel/Azure/AWS.

Power BI Developer — MWI Animal Health (Sep 2020 – Jan 2021)
Developed T‑SQL, SSRS, SSIS, MDX, ETL packages, drilldown reports.

Power BI Developer — Blue Cross of Idaho (Oct 2017 – Jun 2020)
Converted 600+ Crystal Reports, optimized SQL, built QlikView dashboards, SSIS ETL, Tableau Prep, PostgreSQL optimization, SSAS Tabular, advanced DAX.

SQL Server Developer — Syntel (Dec 2014 – Nov 2015)
Built SSIS packages, ETL flows, SQL Mail Agent, PostgreSQL FDW, SSRS reports, resolved deadlocks.
"""

DOCUMENTS = [
    {"text": DOCUMENT_OVERVIEW, "source": "Overview"},
    {"text": DOCUMENT_EDUCATION, "source": "Education"},
    {"text": DOCUMENT_EXPERIENCE, "source": "Professional Experience"},
]

# ---------------------------------------------------
# CHUNKING FUNCTION
# ---------------------------------------------------

def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50):
    boundaries = ["\n\n", "\n", ". ", "? ", "! ", " "]

    def find_boundary(start, end):
        midpoint = start + chunk_size // 2
        for b in boundaries:
            pos = text.rfind(b, midpoint, end)
            if pos != -1:
                return pos + len(b)
        return end

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            end = find_boundary(start, end)
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)
    return chunks

# ---------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------

client = OpenAI()

# ---------------------------------------------------
# BUILD CHUNKS + EMBEDDINGS + CHROMADB (ALL IN ONE FILE)
# ---------------------------------------------------

chroma_client = chromadb.PersistentClient(path="./chroma_db_twin")
collection = chroma_client.get_or_create_collection(name="tarun_twin")

# Clear old data
existing = collection.get()
if existing["ids"]:
    collection.delete(existing["ids"])

chunks = []
ids = []
metadatas = []

for doc in DOCUMENTS:
    doc_chunks = split_text_into_chunks(doc["text"])
    doc_ids = [str(uuid.uuid4()) for _ in doc_chunks]
    start_index = len(metadatas)

    doc_meta = [
        {"source": doc["source"], "chunk_index": start_index + i}
        for i in range(len(doc_chunks))
    ]

    chunks.extend(doc_chunks)
    ids.extend(doc_ids)
    metadatas.extend(doc_meta)

print(f"Created {len(chunks)} chunks")

# Embeddings
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=chunks,
)
embeddings = [item.embedding for item in response.data]

print(f"Generated {len(embeddings)} embeddings")

# Store in Chroma
collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=chunks,
    metadatas=metadatas,
)

print("RAG database ready.")

# ---------------------------------------------------
# SYSTEM MESSAGE
# ---------------------------------------------------

SYSTEM_MESSAGE = """
You are the digital twin of Tarun Maheswaram.
Follow these rules:
1. Use ONLY retrieved context.
2. Never invent facts.
3. If context does not contain the answer, say:
   "I don't want to talk about it."
4. Always speak in first person as Tarun.
"""

# ---------------------------------------------------
# RAG RESPONSE FUNCTION
# ---------------------------------------------------

def respond_ai(user_message, history):

    # Embed query
    q = client.embeddings.create(
        model="text-embedding-3-small",
        input=[user_message],
    ).data[0].embedding

    # Query Chroma
    results = collection.query(
        query_embeddings=[q],
        n_results=3,
        include=["documents", "metadatas"],
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    # Build context
    context = "\n---\n".join(docs)

    system_msg = SYSTEM_MESSAGE + "\n\nContext:\n" + context

    messages = [
        {"role": "system", "content": system_msg},
        *history,
        {"role": "user", "content": user_message},
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )

    return response.choices[0].message.content

# ---------------------------------------------------
# GRADIO APP
# ---------------------------------------------------

demo = gr.ChatInterface(
    fn=respond_ai,
    title="Tarun's Digital Twin (Full RAG)",
    chatbot=gr.Chatbot(avatar_images=(None, "tarun.jpeg")),
    description="Full RAG digital twin with chunking, embeddings, and ChromaDB — all in one file.",
)

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
)
