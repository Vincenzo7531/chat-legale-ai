import os
import openai
import pytesseract
import pdfplumber
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from docx import Document
from datetime import datetime
# Configurazione delle API
OPENAI_API_KEY = "TUA_API_KEY_TECHONCLOUD"
CLADAI_API_KEY = "TUA_API_KEY_CLADAI"
NORMATTIVA_API_KEY = "TUA_API_KEY_NORMATTIVA"

openai.api_key = OPENAI_API_KEY

# Directory per tracciare i file analizzati
LOG_DIR = "log_analisi"
os.makedirs(LOG_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Estrae il testo da un PDF, anche se scannerizzato."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    
    if not text.strip():  # Se il testo non è stato estratto, utilizza OCR
        text = pytesseract.image_to_string(pdf_path)
    
    return text.strip()

def extract_text_from_docx(docx_path):
    """Estrae il testo da un file DOCX."""
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def chat_with_ai(prompt):
    """Simula una chat interattiva con GPT."""
    response = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "system", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

def send_message():
    """Invia un messaggio alla chat e mostra la risposta."""
    user_input = user_entry.get("1.0", tk.END).strip()
    if user_input:
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"\nUtente: {user_input}\n", "user")
        response = chat_with_ai(user_input)
        chat_history.insert(tk.END, f"ChatGPT: {response}\n", "bot")
        chat_history.config(state=tk.DISABLED)
        user_entry.delete("1.0", tk.END)

def create_chat_interface():
    """Crea l'interfaccia stile ChatGPT."""
    root = tk.Tk()
    root.title("Chat Legale con AI")
    root.geometry("600x500")
    
    global chat_history, user_entry
    chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=20, width=70)
    chat_history.pack(padx=10, pady=10)
    chat_history.tag_configure("user", foreground="blue")
    chat_history.tag_configure("bot", foreground="green")
    
    user_entry = tk.Text(root, height=3, width=70)
    user_entry.pack(padx=10, pady=5)
    
    send_button = tk.Button(root, text="Invia", command=send_message)
    send_button.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    create_chat_interface()
