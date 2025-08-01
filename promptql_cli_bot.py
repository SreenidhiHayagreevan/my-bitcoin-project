import requests

# ✅ Use your ngrok tunnel + correct PromptQL endpoint
PROMPTQL_API = "https://21a7f400b90c.ngrok-free.app/promptql"


print("🧠 Welcome to the PromptQL CLI Bot!")
print("Type your Bitcoin question or type 'exit' to quit.\n")

while True:
    user_input = input("🔍 Ask: ")
    if user_input.strip().lower() == "exit":
        print("👋 Goodbye!")
        break

    payload = {
        "prompt": user_input,
        "mode": "auto"
    }

    try:
        res = requests.post(PROMPTQL_API, json=payload)
        
        # 🐛 Print raw text for debugging
        print("\n🔁 Raw response:")
        print(res.text)

        # 👇 Try to parse it as JSON
        data = res.json()
        print("\n🧠 Answer:")
        print(data.get("response", "No response key in result."))
        print("-" * 40)

    except Exception as e:
        print(f"❌ Error: {e}")
        print("-" * 40)


