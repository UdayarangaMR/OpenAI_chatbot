from flask import Flask, render_template, request
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.5,
    openai_api_key="Your_OpenAI_API_Key"  # replace with your key
)

# Prompt template for Daily Life Companion
prompt_template = PromptTemplate(
    input_variables=["user_input"],
    template="""
You are a helpful Daily Life Companion. You can give advice, motivation, reminders, and answer daily questions. 
Be friendly and concise.

User: {user_input}
Assistant:
"""
)

# Create a runnable chain
llm_chain = prompt_template | llm

# Flask app
app = Flask(__name__)

def ask_companion(question):
    """Send user input to LLM and get response"""
    response = llm_chain.invoke({"user_input": question})
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    if request.method == "POST":
        question = request.form.get("question")
        answer = ask_companion(question)
    return render_template("index.html", question=question, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
