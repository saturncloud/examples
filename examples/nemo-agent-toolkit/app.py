import gradio as gr
from langgraph.errors import GraphRecursionError
from nat.runtime.loader import load_workflow


async def predict(message, history):
    try:
        async with load_workflow("workflow.yml") as session:
            async with session.run(message) as runner:
                result = await runner.result()
                return str(result)
    except GraphRecursionError:
        return (
            "I searched Wikipedia but couldn't find enough information to answer "
            "this question within the search limit. Try rephrasing your question or "
            "asking about a more specific topic."
        )
    except Exception as e:
        return f"Error: {str(e)}"


demo = gr.ChatInterface(
    fn=predict,
    title="NeMo Agent — Research Assistant",
    description="Ask any question. The agent searches Wikipedia and reasons step-by-step.",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8000)
