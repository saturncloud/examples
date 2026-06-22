import asyncio
from metagpt.team import Team
from metagpt.roles import ProductManager, Architect, ProjectManager, Engineer

async def startup(idea: str):
    # Create the Software Company Team
    company = Team()
    
    # Hire the standard production roles
    company.hire([
        ProductManager(), 
        Architect(), 
        ProjectManager(), 
        Engineer()
    ])

    # Run the production line
    company.run_project(idea)
    await company.run(n_round=5)
    print(f"✅ Production Finished! Check your /workspace folder.")

if __name__ == "__main__":
    import sys
    idea = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("🚀 Project Idea: ")
    asyncio.run(startup(idea=idea))