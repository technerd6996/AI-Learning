from groq import Groq
import os

# Adding Groq API Key + Groq Manual

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY not found. Please set it.")
    exit()

client=Groq(api_key=api_key)

# Function to ask the AI Anything

def ask_ai(question):
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role":"system",
                "content":"You are an expert SRE Engineer. Answer questions clearly and technically deep."
            },
            {
                "role":"user",
                "content":question
            }
        ]
    )
    return response.choices[0].message.content

#Ask Actual Question 

answer = ask_ai("List the possible reasons for High CPU utilization Linux Servers")
print(answer)