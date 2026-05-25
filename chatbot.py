import ollama

messages = [
    {'role': 'system', 'content': 'Jesteś pomocnym asystentem.'},
    {'role': 'user', 'content': 'Jak masz na imię?'},
    {'role': 'assistant', 'content': 'Jestem modelem Llama 3.'},
    {'role': 'user', 'content': 'O czym rozmawialiśmy przed chwilą?'}
]

# Wewnątrz pętli:
response = ollama.chat(model='llama3', messages=messages, stream=True)
for chunk in response:
    print(chunk['message']['content'], end='', flush=True)