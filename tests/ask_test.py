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
    prompt = f"""You are an expert at making SQL queries. Given the following SQLite database schema, 
                  write a valid SQL query that answers the user's question and returns the event(s) name and description.
                  Return ONLY the raw SQL query. Do not wrap it in markdown code blocks, do not explain. 
                
                   Schema:
                   {schema}
                   
                   Question:
                   {question}                  
                   """
    ## Generates the response from the LLM using the prompt.
    response = ollama.chat(
        model='gemma4',
        messages=[
            {'role': 'system', 'content': prompt},
            ],
        ## Maximizes the amount of tokens the LLM is allowed to use to generate a response.
        ## This makes the LLM faster
        options={'num_predict': 50,
                 'temperature': 0.0}
    )

    return response['message']['content']


def retrieve_events_from_db():
    question = input("Please enter your question: ")
    sql_query = generate_query(question, get_db_scheme())
    with sqlite3.connect(db_path_normalized) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        return cursor.fetchall()

