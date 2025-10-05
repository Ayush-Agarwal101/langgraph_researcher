# FILE: main.py

from dotenv import load_dotenv
load_dotenv()

from graph import app
import pprint
import sys

def main():
    """
    Main function to run the autonomous researcher graph.
    It can take a research topic as a command-line argument,
    or it will prompt the user for one if none is provided.
    """
    topic = ""
    
    # Check if a topic was passed as a command-line argument
    if len(sys.argv) > 1:
        # Join all arguments to form the topic string
        topic = " ".join(sys.argv[1:])
        print(f"🔬 Topic provided via command-line: '{topic}'")
    else:
        # If no command-line argument is given, prompt the user for input
        topic = input("❓ Please enter the research topic you want to investigate: ")

    if not topic:
        print("❌ No topic provided. Exiting.")
        return

    # Initial state for the graph
    inputs = {"topic": topic, "loop_count": 0}

    print("🚀 Starting the Autonomous Scientific Researcher...")
    print(f"▶️  Topic: {inputs['topic']}")
    print("-" * 50)

    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"✅ Output from node '{key}':")
            pprint.pprint(value, indent=2, width=120, depth=None)
        print("-" * 50)

    print("🏁 Research process finished.")

if __name__ == "__main__":
    main()