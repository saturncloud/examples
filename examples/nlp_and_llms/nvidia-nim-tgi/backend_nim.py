from openai import OpenAI
import os

# set it up in the key in the environment first
## sample free API key:  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
API_KEY = "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"

if not API_KEY:
    raise ValueError("❌ NVIDIA_API_KEY is not set. Export it first!")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=API_KEY,
)

def nim_chat(prompt, model="qwen/qwen3-next-80b-a3b-instruct", stream=False):
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        top_p=0.7,
        max_tokens=1024,
        stream=stream
    )

    if stream:
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content
    else:
        return completion.choices[0].message["content"]
