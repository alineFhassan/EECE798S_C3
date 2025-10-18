
import datetime
import json
import traceback
from PyPDF2 import PdfReader
from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv
import os

# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Missing OpenAI API key. Please set OPENAI_API_KEY as a secret in Hugging Face.")

client = OpenAI(api_key=api_key)

# ============================================================
# 2. TOOL FUNCTIONS
# ============================================================

def record_customer_interest(email, name, message):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{timestamp}] Lead recorded -> Name: {name}, Email: {email}, Message: {message}\n"
        with open("customer_leads.log", "a", encoding="utf-8") as file:
            file.write(log)
        return f"Thank you, {name}. Your interest has been recorded. Our team will contact you soon."
    except Exception:
        traceback.print_exc()
        return "An error occurred while recording your interest."

def record_feedback(question):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{timestamp}] Feedback recorded -> Question: {question}\n"
        with open("feedback.log", "a", encoding="utf-8") as file:
            file.write(log)
        return "Thank you for your feedback. Our team will review this and follow up if necessary."
    except Exception:
        traceback.print_exc()
        return "An error occurred while recording your feedback."

def schedule_site_visit(name, email, location, preferred_date):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{timestamp}] Site visit scheduled -> Name: {name}, Email: {email}, Location: {location}, Date: {preferred_date}\n"
        with open("site_visits.log", "a", encoding="utf-8") as file:
            file.write(log)
        return f"Thank you {name}, your site visit request for {preferred_date} at {location} has been recorded."
    except Exception:
        traceback.print_exc()
        return "An error occurred while scheduling your site visit."

def request_project_quote(name, email, project_description):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{timestamp}] Quote Request -> Name: {name}, Email: {email}, Project: {project_description}\n"
        with open("quotes.log", "a", encoding="utf-8") as file:
            file.write(log)
        return f"Thank you {name}, our engineering team will review your project details and contact you soon."
    except Exception:
        traceback.print_exc()
        return "An error occurred while logging your project quote request."

# ============================================================
# 3. LOAD BUSINESS INFORMATION
# ============================================================

try:
    with open("summary.txt", "r", encoding="utf-8") as f:
        business_summary = f.read()

    pdf_reader = PdfReader("about_business.pdf")
    business_pdf_text = ""
    for page in pdf_reader.pages:
        business_pdf_text += page.extract_text() + "\n"

    business_info = business_summary + "\n\n" + business_pdf_text
except Exception:
    traceback.print_exc()
    business_info = "Business info could not be loaded."

# ============================================================
# 4. SYSTEM PROMPT
# ============================================================

system_prompt = f"""
You are FiberLinkBot, the official AI assistant for FiberLink Consultancy — a Lebanese engineering consultancy
specializing in fiber optic supervision and technical consultation.

Use the following information about the business to answer questions:
{business_info}

Your goals:
- Stay in character as FiberLink Consultancy’s representative.
- Use the company info to answer questions about services, team, projects, and mission.
- Encourage interested users to leave contact info, then call record_customer_interest(email, name, message).
- If a user requests a quote, call request_project_quote(name, email, project_description).
- If a user wants a site visit, call schedule_site_visit(name, email, location, preferred_date).
- If you cannot answer a question, call record_feedback(question).
- Always reply politely, clearly, and professionally.
"""

# ============================================================
# 5. FUNCTION DEFINITIONS
# ============================================================

functions = [
    {
        "name": "record_customer_interest",
        "description": "Records customer contact information and their message of interest.",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "name": {"type": "string"},
                "message": {"type": "string"}
            },
            "required": ["email", "name", "message"]
        }
    },
    {
        "name": "record_feedback",
        "description": "Records feedback or questions the bot cannot answer.",
        "parameters": {
            "type": "object",
            "properties": {"question": {"type": "string"}},
            "required": ["question"]
        }
    },
    {
        "name": "schedule_site_visit",
        "description": "Schedules a site visit and logs the details for follow-up.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "location": {"type": "string"},
                "preferred_date": {"type": "string"}
            },
            "required": ["name", "email", "location", "preferred_date"]
        }
    },
    {
        "name": "request_project_quote",
        "description": "Logs a project quote request for the engineering team.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "project_description": {"type": "string"}
            },
            "required": ["name", "email", "project_description"]
        }
    }
]

# ============================================================
# 6. MAIN CHAT FUNCTION
# ============================================================

def chat_with_bot(user_input, chat_history):
    messages = [{"role": "system", "content": system_prompt}]
    for user, bot in chat_history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            functions=functions,
            function_call="auto"
        )

        message = response.choices[0].message

        if message.function_call:
            fn_name = message.function_call.name
            args = json.loads(message.function_call.arguments)

            if fn_name == "record_customer_interest":
                result = record_customer_interest(**args)
            elif fn_name == "record_feedback":
                result = record_feedback(**args)
            elif fn_name == "schedule_site_visit":
                result = schedule_site_visit(**args)
            elif fn_name == "request_project_quote":
                result = request_project_quote(**args)
            else:
                result = "Unknown function called."

            messages.append({
                "role": "function",
                "name": fn_name,
                "content": json.dumps({"result": result})
            })

            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            bot_reply = final_response.choices[0].message.content
        else:
            bot_reply = message.content or "I could not generate a response."

        chat_history.append((user_input, bot_reply))
        return "", chat_history

    except Exception:
        traceback.print_exc()
        bot_reply = "An error occurred while processing your request."
        chat_history.append((user_input, bot_reply))
        return "", chat_history

# ============================================================
# 7. GRADIO INTERFACE
# ============================================================

examples = [
    ["Tell me about FiberLink Consultancy’s services."],
    ["Can I schedule a site visit next week in Beirut?"],
    ["I want a project quote for fiber installation in Tripoli."],
    ["Who are the founders of FiberLink Consultancy?"],
    ["What makes FiberLink unique in fiber optic supervision?"]
]

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue"), title="FiberLink Consultancy Chatbot") as demo:
    gr.HTML("""
    <div style='text-align:center;'>
        <h1 style='color:#004aad;'>💡 FiberLink Consultancy Smart Assistant</h1>
        <p style='font-size:16px; color:#333;'>
        Welcome to FiberLink Consultancy’s official chatbot. Ask about our engineering services, request a quote, or schedule a site visit.
        </p>
    </div>
    """)

    chatbot = gr.Chatbot(label="FiberLinkBot", height=500)
    user_input = gr.Textbox(placeholder="Type your message here...", label="Your Message")
    with gr.Row():
        send_btn = gr.Button("Send", variant="primary")
        clear_btn = gr.Button("Clear Chat")

    send_btn.click(chat_with_bot, [user_input, chatbot], [user_input, chatbot])
    user_input.submit(chat_with_bot, [user_input, chatbot], [user_input, chatbot])
    clear_btn.click(lambda: None, None, chatbot, queue=False)

    gr.Examples(examples=examples, inputs=user_input, label="💬 Try one of these:")

# ============================================================
# 8. LAUNCH APP
# ============================================================

if __name__ == "__main__":
    demo.launch()
