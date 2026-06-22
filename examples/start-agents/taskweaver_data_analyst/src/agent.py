import os
import shutil
from taskweaver.app.app import TaskWeaverApp
from .config import settings

class DataAnalystAgent:
    def __init__(self):
        project_path = os.path.join(os.getcwd(), "project")
        self.app = TaskWeaverApp(app_dir=project_path, config={
            "llm.api_key": settings.openai_api_key,
            "llm.model": settings.llm_model,
        })
        self.session = self.app.get_session()

    def run(self, query: str, files: list = None):
        # 1. Establish the Sandbox Path
        session_cwd = os.path.join(self.session.workspace, "cwd")
        os.makedirs(session_cwd, exist_ok=True)

        # 2. Move files and build a "Manifest"
        manifest = ""
        if files:
            uploaded_names = []
            for file_path in files:
                fname = os.path.basename(file_path)
                dest = os.path.join(session_cwd, fname)
                shutil.copy2(file_path, dest)
                uploaded_names.append(fname)
            
            # This manifest is prepended to the query
            manifest = f"SYSTEM NOTIFICATION: The following files are PRESENT in your current working directory: {uploaded_names}. Use these exact filenames. Do not guess filenames like 'data.xlsx'.\n\n"

        # 3. Prepend manifest to the user query
        full_query = manifest + "User Request: " + query
        
        response_round = self.session.send_message(full_query)
        
        final_output = []
        for post in response_round.post_list:
            # Capture tables/results
            for attachment in post.attachment_list:
                if attachment.type == "execution_result":
                    final_output.append(f"\n**[DATA OUTPUT]:**\n{attachment.content}")
            
            # Capture the analyst's final response
            if post.send_to.lower() == "user":
                final_output.append(f"\n{post.message}")
        
        return "\n".join(final_output) if final_output else "The analyst failed to respond. Check if the LLM is reaching its token limit."
