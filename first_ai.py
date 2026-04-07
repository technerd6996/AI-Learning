from groq import Groq
import os

# Adding Groq API Key + Groq Manual

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY not found. Please set it.")
    exit()

client=Groq(api_key=api_key)

# Adding history List Dictionary to make it remember of the previous conversations

history = []

history.append({
    "role":"system",
    "content": "You are an expert SRE Engineer. Answer questions clearly and technically deep."
})

# Function to ask the AI Anything


def ask_ai(question):
    history.append({"role":"user", "content": question})

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=history
    )
    return response.choices[0].message.content
    history.append({"role":"assistant", "content": answer})
    return answer

#Ask Actual Question 

answer1 = ask_ai("What is SLI?")
print(answer1)

answer2 = ask_ai("Give me an example of what you just explained")
print(answer2)