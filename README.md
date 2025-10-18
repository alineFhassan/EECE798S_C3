# 💡 FiberLink Consultancy Smart Chatbot

An AI-powered assistant for **FiberLink Consultancy**, a Lebanese engineering firm specializing in **fiber optic supervision** and **technical consultation**.  
This chatbot uses **OpenAI’s GPT models**, **Gradio** for the web interface, and can be deployed directly to **Hugging Face Spaces**.

---

## 📘 Overview

FiberLinkBot acts as a professional representative for FiberLink Consultancy.  
It can:
- Answer company-related questions based on uploaded business documents.
- Record customer interests and leads.
- Handle feedback automatically.
- Schedule site visits and log details.
- Accept project quote requests and store them for follow-up.

---

## 🧩 Project Structure
```bash
EECE798S_C3/
│
├── app.py # Main app for Hugging Face Spaces deployment
├── business_agent.ipynb # Colab / Jupyter notebook version
├── requirements.txt # Dependencies list
├── me
    ├── business_summary.txt # Text summary about the company
    ├── about_business.pdf # Detailed company info
├── .env # Contains the OpenAI API key (not uploaded)
├── customer_leads.log # Automatically created when leads are recorded (available after askign a question that requires to crete it)
├── feedback.log # Automatically created when feedback is logged (available after askign a question that requires to crete it)
├── site_visits.log # Automatically created when site visits are logged (available after askign a question that requires to crete it)
├── quotes.log # Automatically created when quotes are logged (available after askign a question that requires to crete it)
├── c3.mp4 #
└── README.md # Project documentation
```
## ⚙️ Installation and Setup (Local or Colab)

### 1. Clone or upload the project
```bash
git clone https://github.com/yourusername/fiberlink-chatbot.git
cd EECE798S_C3
```
### 2. Install requirements
```bash
pip install -r requirements.txt
```
### 3. Set your OpenAI API key

Create a file named .env in the root folder and add:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```
### 4. Running app
Run all cells
The chatbot will launch with a public Gradio link.

## 🚀 Deploying to Hugging Face Spaces

Go to Hugging Face Spaces
 and click New Space

Choose:
SDK: Gradio
Visibility: Public or Private
Name: fiberlink-chatbot
Upload these files:
app.py
requirements.txt
business_summary.txt
about_business.pdf

Go to Settings → Repository secrets and add:
Name: OPENAI_API_KEY
Value: your_actual_api_key

The Space will build automatically and your chatbot will be live in a few minutes. 
(I did this step but for api usage purposes, I kept the space private)


## 🧠 Example Prompts

You can try these in the chatbot:
“Tell me about FiberLink Consultancy’s services.”
“Can I schedule a site visit in Beirut next week?”
“Who are the founders of FiberLink Consultancy?”
“What makes FiberLink unique in fiber optic supervision?”
“I need a project quote for a fiber installation in Tripoli.”


## Done by: Aline Hassan