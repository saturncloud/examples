import os
import dspy
import streamlit as st
from dotenv import load_dotenv

# 1. Page Configuration
st.set_page_config(page_title="DSPy Agent UI", page_icon="🧠", layout="centered")

# 2. Load Environment Variables
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OPENAI_API_KEY is missing from your .env file.")
    st.stop()

# 3. Configure DSPy (Cached so it doesn't reload on every button click)
@st.cache_resource
def setup_dspy():
    lm = dspy.LM('openai/gpt-4o-mini', max_tokens=1000)
    dspy.configure(lm=lm)
    return lm

setup_dspy()

# 4. Define the DSPy Signature & Module (Mirroring the Notebook)
class BasicQA(dspy.Signature):
    """Answer questions with short, precise, and accurate fact-based answers."""
    question = dspy.InputField(desc="The user's query.")
    answer = dspy.OutputField(desc="A concise, factual answer.")

class CoTQA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought(BasicQA)
        
    def forward(self, question):
        return self.prog(question=question)

# Instantiate the agent
agent = CoTQA()

# 5. Streamlit UI Build
st.title("🧠 DSPy Agent Dashboard")
st.markdown("Test the reasoning and output capacity of your DSPy Chain-of-Thought agent.")

# Input Field
user_question = st.text_input("Ask a question:", placeholder="e.g., What is the heaviest naturally occurring element?")

# Execution Button
if st.button("🚀 Generate Answer", type="primary"):
    if user_question:
        with st.spinner("Agent is thinking..."):
            try:
                # Execute the DSPy agent
                response = agent(question=user_question)
                
                # Display Final Answer clearly at the top
                st.subheader("🎯 Final Answer")
                st.success(response.answer)
                
                # Display the hidden reasoning in an expandable box or text area
                st.subheader("🧠 Internal Reasoning Trace")
                st.info(response.reasoning)
                
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
    else:
        st.warning("Please enter a question first.")