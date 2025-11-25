import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from backend.controllers.chat_controller import ChatController

def test_chat():
    controller = ChatController()
    
    questions = [
        "Are there any buses from Dhaka to Rajshahi under 500 taka?",
        "What are the contact details of Hanif Bus?",
        "Can I cancel my booking for the bus from Dhaka to Barishal?"
    ]
    
    print("--- Starting Chat Test ---\n")
    
    for q in questions:
        print(f"User: {q}")
        response = controller.process_query(q)
        print(f"Bot: {response}\n")
        print("-" * 30 + "\n")

if __name__ == "__main__":
    test_chat()
