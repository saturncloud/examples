from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from composio import Composio
from composio_langchain import LangchainProvider
from .config import settings

class GitHubReviewer:
    def __init__(self):
        # 1. Setup the LLM
        self.llm = ChatOpenAI(
            model=settings.model_name, 
            openai_api_key=settings.openai_api_key,
            temperature=0
        )
        
        # 2. Setup the Composio Bridge
        self.composio = Composio(
            api_key=settings.composio_api_key, 
            provider=LangchainProvider()
        )
        
        # 3. Fetch Tools - Curated for Review, Comment, and Merge
        self.tools = self.composio.tools.get(
            tools=[
                # Discovery Tools
                "GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER",
                "GITHUB_LIST_PULL_REQUESTS",
                "GITHUB_GET_PULL_REQUEST",
                
                # Review Tools (Reading code)
                "GITHUB_GET_REPOSITORY_CONTENT",  # To read specific file contents
                "GITHUB_COMPARE_TWO_COMMITS",     # Useful for seeing diffs
                
                # Action Tools (Commenting & Merging)
                "GITHUB_CREATE_AN_ISSUE_COMMENT", # PRs are issues; used for general comments
                "GITHUB_CREATE_A_PULL_REQUEST_REVIEW", # To submit an official Approval/Request Changes
                "GITHUB_MERGE_A_PULL_REQUEST"     # The final step to merge
            ],
            user_id=settings.composio_user_id
        )
                
        # 4. Instructions to handle the 'Abwonder' single-word repo issue
        system_instructions = (
            "You are an Elite GitHub Reviewer Agent. Your workflow is:\n"
            "1. LIST repositories and PRs to find your target.\n"
            "2. READ the pull request details and file contents to perform a code review.\n"
            "3. COMMENT with your feedback or use 'GITHUB_CREATE_A_PULL_REQUEST_REVIEW' for formal approvals.\n"
            "4. MERGE the PR only if it meets all safety standards and you have confirmed the user wants you to merge it.\n\n"
            "Never guess file content; always fetch it using your tools."
        )

        # 5. Create the Agent
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=system_instructions
        )

    def run(self, query: str):
        response = self.agent.invoke({
            "messages": [("user", query)]
        })
        return response["messages"][-1].content
