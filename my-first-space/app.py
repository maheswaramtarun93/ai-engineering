import os
import gradio as gr

# ---------------------------------------------------
# YOUR RESPOND_AI FUNCTION GOES HERE
# ---------------------------------------------------

def respond_ai(user_message, history):
    # temporary placeholder until you add OpenAI logic
    return f"Tarun's Digital Twin says: I heard you ask — '{user_message}'. I'm still warming up!"


# ---------------------------------------------------
# GRADIO APP FOR RENDER
# ---------------------------------------------------

demo = gr.ChatInterface(
    fn=respond_ai,
    title="Tarun's Digital Twin",
    chatbot=gr.Chatbot(avatar_images=(None, "tarun.jpeg")),  # <-- your JPEG here
    description="Chat with Tarun's AI twin — smart, curious, and always ready to help.",
    examples=[
        "Tell me something interesting about yourself.",
        "What motivates you the most?",
        "How would you describe your personality?",
        "What goals are you working on right now?"
    ]
)

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)
