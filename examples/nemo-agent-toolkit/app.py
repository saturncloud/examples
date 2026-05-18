import gradio as gr
from nat.runtime.loader import load_workflow


async def predict(message, history):
    try:
        async with load_workflow("workflow.yml") as session:
            response = await session.run(input=message)
            return response.result
    except Exception as e:
        return f"Error: {str(e)}"


demo = gr.ChatInterface(
    fn=predict,
    title="NeMo Agent — Research Assistant",
    description="Ask any question. The agent searches Wikipedia and reasons step-by-step.",
    theme="soft",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8000)
