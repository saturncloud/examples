import argparse
from backend_tgi import tgi_chat
from backend_nim import nim_chat

parser = argparse.ArgumentParser(description="NIM/TGI CLI")
parser.add_argument("--backend", choices=["local", "nim"], required=True)
parser.add_argument("prompt", type=str)

args = parser.parse_args()

if args.backend == "local":
    print("\n🟢 Local TGI Response:")
    print(tgi_chat(args.prompt))

else:
    print("\n🟢 NVIDIA NIM Response:")
    for chunk in nim_chat(args.prompt, stream=True):
        print(chunk, end="", flush=True)
    print("\n")
