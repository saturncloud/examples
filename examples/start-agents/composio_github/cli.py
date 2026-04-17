import sys
from src.agent import GitHubReviewer

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py 'Your question about GitHub'")
        return

    query = sys.argv[1]
    print(f"--- Reviewer Agent is processing: {query} ---")
    
    try:
        agent = GitHubReviewer()
        result = agent.run(query)
        print("\n[AGENT RESPONSE]:")
        print(result)
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()