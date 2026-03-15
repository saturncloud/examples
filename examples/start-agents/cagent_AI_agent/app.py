import streamlit as st
import subprocess
import os

# 1. Page Configuration
st.set_page_config(page_title="Docker Agent UI", page_icon="🐳", layout="centered")
st.title("🐳 Docker Multi-Agent Dashboard")
st.markdown("A production web UI wrapping a declarative Docker Agent hierarchy.")

# 2. Initialize Chat Memory in the Browser
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Render previous conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. Handle new web input
user_input = st.chat_input("Enter a task for the agent team...")

if user_input:
    # Display the user's prompt in the UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Execute the backend agent
    with st.chat_message("assistant"):
        
        # Determine execution command
        binary = "./docker-agent" if os.path.exists("./docker-agent") else "docker"
        args = ["agent", "run", "agent.yaml", user_input] if binary == "docker" else [binary, "run", "agent.yaml", user_input]
        env = os.environ.copy()

        # 5. The "Antigravity" UI: Real-time status streaming
        full_log = ""
        with st.status("Agent team is coordinating...", expanded=True) as status_box:
            
            # Popen allows us to read the terminal output line-by-line as it happens
            process = subprocess.Popen(
                args, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                env=env
            )
            
            for line in process.stdout:
                full_log += line
                
                # Intercept CLI events and turn them into UI notifications
                if line.startswith("Calling "):
                    tool_name = line.split("Calling ")[1].split("(")[0]
                    st.markdown(f"✅ Executing tool: **`{tool_name}`**")
                elif line.startswith("--- Agent:"):
                    agent_name = line.replace("--- Agent:", "").replace("---", "").strip()
                    st.markdown(f"🔄 Handing off to **{agent_name.capitalize()}**...")

            # Wait for the process to finish and collapse the status box
            process.wait()
            status_box.update(label="Tasks completed successfully!", state="complete", expanded=False)

        # 6. Extract and display ONLY the final text
        # Docker Agent tool logs always end with a closing parenthesis and a newline ")\n"
        if ")\n" in full_log:
            final_output = full_log.rpartition(")\n")[-1].strip()
        else:
            final_output = full_log.strip()
            
        # Display the clean result to the user
        st.write(final_output)
        st.session_state.messages.append({"role": "assistant", "content": final_output})