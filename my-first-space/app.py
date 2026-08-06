import os
import gradio as gr

# ---------------------------------------------------
# YOUR RESPOND_AI FUNCTION GOES HERE
# ---------------------------------------------------

def respond_ai(user_message, history):
    # paste your full function here
    return "working"


# ---------------------------------------------------
# GRADIO APP FOR RENDER
# ---------------------------------------------------

demo = gr.ChatInterface(
    fn=respond_ai,
    title="Sherlock's Digital Twin",
    chatbot=gr.Chatbot(avatar_images=(None, "sherlock.png")),
    description="Chat with an AI version of Sherlock Holmes, the world's greatest consultant.",
    examples=[
        "Tell me some interesting facts about you?",
        "Key Cases solved?",
        "Which unusual deductions are your specialty?"
    ]
)

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)
