import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI

# 1. Initialize environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Environment Error: OPENAI_API_KEY is not defined.")

def initialize_task_assistant(data_dir="./data"):
    """Loads local documents and builds the LlamaIndex vector store."""
    print(f"Initializing LlamaIndex RAG pipeline. Reading from {data_dir}...")
    
    # Configure the LLM globally (Temperature 0.1 for strict, factual retrieval)
    Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    
    try:
        # Ingest data from the target directory
        documents = SimpleDirectoryReader(data_dir).load_data()
        
        # Build the vector index
        index = VectorStoreIndex.from_documents(documents)
        
        # Return the query engine interface
        return index.as_query_engine()
        
    except ValueError as e:
        print(f"Initialization Error: {e}. Please ensure the '{data_dir}' directory exists and contains text files.")
        exit(1)

if __name__ == "__main__":
    print("--- LlamaIndex Task Manager ---")
    
    # Initialize the query engine
    query_engine = initialize_task_assistant()
    
    print("\nTask Assistant is ready. (Type 'exit' to quit)")
    
    # Standard interactive execution loop
    while True:
        user_query = input("\nQuery your tasks: ")
        
        if user_query.lower() in ['exit', 'quit']:
            print("Terminating process.")
            break
        
        if user_query.strip():
            try:
                # Query the vector index
                response = query_engine.query(user_query)
                print(f"\nAssistant: {response}")
            except Exception as e:
                print(f"\nAPI Execution Error: {e}")