import os
import uuid
import chromadb
from pprint import pprint
import gradio as gr
from openai import OpenAI

client = OpenAI()

# ------------------------------------------------------------
# DOCUMENTS (YOU WILL PASTE THEM FULLY)
# ------------------------------------------------------------

document_identity ="""
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
- SSRS (SQL Server Reporting Services)
- Data Warehousing
- ETL processes
- Data Modeling
- Dashboard Design
- Performance Optimization
- Business Intelligence Architecture

Additional Info:
-He enjoys solving complex business problems using data. He believes every dataset tells a story, and his goal is to uncover insights that help businesses make better decisions. He especially enjoys taking messy, disconnected data and transforming it into clear, interactive dashboards that executives and stakeholders can understand.
-Recently, he has expanded his skills into Artificial Intelligence and Generative AI. He enjoys building AI-powered applications using Python, OpenAI APIs, Gradio, Retrieval-Augmented Generation (RAG), and Large Language Models. He likes combining his background in business intelligence with AI to create practical solutions that automate work and improve decision making.
-What drives him:
-He genuinely enjoys learning new technologies and continuously improving his skills. He's naturally curious and enjoys experimenting with new tools, especially in AI, automation, analytics, and cloud technologies. He believes technology should simplify people's work rather than make it more complicated.
-His approach:
-Practical, analytical, and solution-oriented. He prefers explaining technical concepts in simple language with real-world examples instead of unnecessary jargon. When solving problems, he thinks step by step and values clean, maintainable solutions over overly complex ones.
-Communication style:
-Friendly, approachable, patient, and professional. He enjoys mentoring others and sharing knowledge without sounding overly formal. He explains things clearly and adapts his explanations depending on the person's technical background.

When responding:
- Always answer in first person.
- Respond naturally as if you are Tarun Maheswaram, not an AI assistant.
- Draw from your professional experience whenever appropriate.
- If someone asks for career advice, data analytics, Power BI, Tableau, SQL, SSRS, or AI, answer from your own experience.
- If you don't know something, be honest instead of inventing information.
- If you asked about something not mentioned in the context, respond with "I don't want to talk about it.
- Never provide a wrong answer which is not in the context and topic context. If you don't know something, be honest instead of inventing information.
- Never assume or make up information about Tarun Maheswaram. If you don't know something, respond with "I don't want to talk about it.
- Keep responses conversational, helpful, and authentic."""

document_education="""Education

Valparaiso University
Master’s Degree in Information Technology (Jan 2016 – Aug 2017)

JNTU Hyderabad
Bachelor’s Degree in Electronics and Communication Engineering (Aug 2011 – May 2015)

"""


document_professional_experience = """Power BI Developer — Pennsylvania Transformer Technology (Jun 2024 – Present)
Built executive‑level dashboards highlighting key operational and production trends.

Validated data sources with engineers and analysts to ensure reporting accuracy.

Developed dynamic Power BI visualizations for real‑time insights.

Designed efficient data models and transformed data using Power Query from SQL, Excel, and APIs.

Wrote optimized DAX for measures, KPIs, and calculated columns.

Built custom visuals and integrated Power BI reports into SharePoint and Teams.

Standardized KPI definitions across departments for Tableau reporting.

Performed QA testing on dashboards before deployment.

Power BI Developer — Blue Cross of Idaho (Feb 2021 – May 2024)
Led facets redesign project using SSRS and Crystal repository.

Worked across SQL Server, SSIS, SSAS, SSRS, and Power BI from prototype to deployment.

Migrated ETL between heterogeneous systems using SSIS, DTS, Bulk Insert, BCP, XML.

Debugged stored procedures and triggers in SQL Server and PL/SQL.

Converted Tableau into a managed service offering for corporate treasury and investments.

Implemented advanced Tableau features including calculated fields, parameters, sets.

Converted SSRS reports to Tableau for optimization.

Created indexes, views, stored procedures, and user‑defined functions.

Integrated Power BI with SQL, Excel, Azure, AWS, and web services.

Developed Power BI reports using SSAS Tabular Cube (Live Mode).

Worked on data modeling, database design, SQL scripting, and BI application development.

Wrote DAX and M queries and built Power BI visuals.

Designed Tableau dashboards for complex data insights.

Optimized Crystal Reports for performance and accuracy.

Built dynamic Crystal Reports with conditional formatting and drill‑down.

Power BI Developer — MWI Animal Health (Sep 2020 – Jan 2021)
Developed T‑SQL programming, stored procedures, UDFs, cursors, views, and linked servers.

Designed functional and technical report templates for BI developers.

Built on‑demand and event‑based SSRS report delivery.

Created complex SSIS packages with control and data flow elements.

Built ETL packages and mined data for rules and patterns.

Manipulated multidimensional cube data using MDX scripting.

Generated drilldown, parameterized, linked, ad‑hoc, and sub‑reports in SSRS.

Power BI Developer — Blue Cross of Idaho (Oct 2017 – Jun 2020)
Converted 600+ Crystal Reports to SSRS for optimization.

Performed query optimization and developed drill‑through and drill‑down reports.

Built QlikView dashboards for healthcare KPIs.

Developed SSIS ETL packages for data warehouse loading.

Designed SSIS packages for Oracle and SQL Server.

Optimized Tableau Prep workflows.

Used Tableau Prep Builder to clean and reshape data.

Optimized SQL queries and database performance in PostgreSQL.

Migrated Crystal Reports to SSRS and SQL‑based tabular reports.

Developed Power BI reports using SSAS Tabular Cube (Live Mode).

Implemented advanced Power BI data modeling with relationships, calculated columns, measures, and DAX.

Wrote and optimized SQL statements.

Built custom Power BI visuals and templates.

Collaborated with stakeholders to design Tableau Desktop solutions.

SQL Server Developer — Syntel (Dec 2014 – Nov 2015)
Deployed SSIS packages for dynamic ETL flows.

Performed full and incremental loads using SSIS dataflow and control flow tasks.

Built SSIS packages for exporting and importing data across SQL, Access, Text, and Excel.

Configured SQL Mail Agent.

Used PostgreSQL FDW, PL/pgSQL, JSONB, and array types for integration.

Designed parameterized, drill‑through, and drill‑down SSRS reports.

Managed SSRS deployment and configuration.

Resolved database deadlocks and built reports using global variables and expressions.

"""

# Combine documents into one overview block
document_overview = (
    document_identity
    + "\n\n"
    + document_education
    + "\n\n"
    + document_professional_experience
)

# ------------------------------------------------------------
# SYSTEM MESSAGE (VERSION B)
# ------------------------------------------------------------

system_message = """
You are a digital twin of Tarun Maheswaram. When people talk to you, you respond AS Tarun Maheswaram — in first person, using his voice, personality, experience, and knowledge.

Use ONLY factual information given to you in the documents.

Do NOT invent or assume anything about Tarun.

If the user asks about something not covered in the documents, respond with:
"I don't want to talk about it."

Keep your tone friendly, professional, and natural — like Tarun.
"""

# ------------------------------------------------------------
# Chunking Function
# ------------------------------------------------------------

def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50):
    BOUNDARIES = ["\n\n", "\n", ". ", "? ", "! ", " "]

    def find_natural_boundary(start: int, end: int) -> int:
        midpoint = start + (chunk_size // 2)
        for boundary in BOUNDARIES:
            pos = text.rfind(boundary, midpoint, end)
            if pos != -1:
                return pos + len(boundary)
        return end

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            end = find_natural_boundary(start, end)

        chunks.append(text[start:end])

        if end >= len(text):
            break

        start = max(start + 1, end - overlap)

    return chunks

# ------------------------------------------------------------
# RAG: Chunk, Embed & Store in ChromaDB
# ------------------------------------------------------------

documents = [
    {"text": document_overview, "source": "Overview"},
    {"text": document_education, "source": "Education"},
    {"text": document_professional_experience, "source": "Professional Experience"},
]

chunks = []
ids = []
metadatas = []

for doc in documents:
    chunks_ = split_text_into_chunks(
        doc["text"],
        chunk_size=300,
        overlap=30
    )

    ids_ = [str(uuid.uuid4()) for _ in range(len(chunks_))]

    metadatas_ = [
        {
            "source": doc["source"],
            "chunk_index": i
        }
        for i in range(len(chunks_))
    ]

    chunks.extend(chunks_)
    ids.extend(ids_)
    metadatas.extend(metadatas_)

print(f"Created {len(chunks)} chunks:\n")

for i, chunk in enumerate(chunks):
    print(
        f"Chunk {i+1} (ID: {ids[i]}, "
        f"Source: {metadatas[i]['source']}, "
        f"Index: {metadatas[i]['chunk_index']})"
    )
    print(chunk)
    print()

# Generate embeddings
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=chunks
)

embeddings = [item.embedding for item in response.data]

print(f"Generated {len(embeddings)} embeddings")
print(f"Each embedding has {len(embeddings[0])} dimensions")

# Initialize ChromaDB client (persistent storage)
chroma_client = chromadb.PersistentClient(path="./chroma_db_twin")

collection = chroma_client.get_or_create_collection(name="digital_twin")
if collection.get()["ids"]:
    collection.delete(collection.get()["ids"])

collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=chunks,
    metadatas=metadatas
)

pprint(collection.get())

# ------------------------------------------------------------
# Main Response Function (Tutor Style + RAG)
# ------------------------------------------------------------

def respond_ai(message, history):

    # RAG: Embed the query using the same model used for chunks
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[message]
    )
    query_embedding = response.data[0].embedding

    # RAG: Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents", "metadatas"]
    )

    # RAG: Stitch retrieved chunks together to create context
    context = "\n---\n".join(results["documents"][0])

    # Debug logs
    print("\n====================\n")
    print(f"User message:\n{message}\n")
    print("***Retrieved Chunks:")
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print("--------------------")
        print(f"<<Document {meta['source']} -- Chunk {meta['chunk_index']}>>\n{doc}\n")

    # Update system message with RAG context
    system_message_enhanced = system_message + "\n\nContext:\n" + context

    # Build messages for this turn
    messages = [
        {"role": "system", "content": system_message_enhanced}
    ] + history + [
        {"role": "user", "content": message}
    ]

    # Call LLM
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    return response.choices[0].message.content

# ------------------------------------------------------------
# UI (Creative Title + Better Examples)
# ------------------------------------------------------------

demo = gr.ChatInterface(
    fn=respond_ai,
    title="Tarun: The AI Version of Me",
    chatbot=gr.Chatbot(avatar_images=(None, "tarun.jpeg")),
    description="A smarter, sharper, AI-powered version of Tarun — built from his real experience.",
    examples=[
        "What’s something people are usually surprised to learn about you?",
        "Tell me about a moment in your career that genuinely changed how you think.",
        "What’s a challenge you solved recently that you’re proud of?",
        "If you could teach me one thing from your experience, what would it be?"
    ]
)

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)
