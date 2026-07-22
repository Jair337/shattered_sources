import sqlite3

import ollama

from config import db_path_normalized


## Pulls the schema from the DB, the LLM needs this to generate a good query.
def get_db_scheme():
    with sqlite3.connect(db_path_normalized) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='events_normalized';")
        return cursor.fetchone()[0]


def generate_query(question, schema):
    ## Defines the prompt that is being sent to the LLM.
    prompt = f"""You are an expert assistant with two modes of response:

1. CONVERSATIONAL MODE: If the user greets you, says hello, or asks a general non-database question, respond naturally, warmly, and conversationally. Do NOT generate any SQL.
2. SQL GENERATION MODE: If the user asks a question that requires data from the database, write a valid SQLite query based on the schema below to answer the question. The query must return the title, description, and time_stamp.

For SQL GENERATION:
- Return ONLY the raw SQL query.
- Do NOT wrap it in markdown code blocks (no ```).
- Do NOT explain the query.
- Do not use chain-of-thought. Respond directly.

Schema:
{schema}

Question:
{question}
"""
    ## Generates the response from the LLM using the prompt.
    response = ollama.chat(
        model='gemma2:2b',
        messages=[
            {'role': 'system', 'content': prompt},
        ],
        ## Maximizes the amount of tokens the LLM is allowed to use to generate a response.
        ## This makes the LLM faster
        options={'num_predict': 512,
                 'temperature': 0.0,
                 'think': False,
                 'num_ctx': 2048,
                 'num_thread': 4}
    )
    return response['message']['content']



