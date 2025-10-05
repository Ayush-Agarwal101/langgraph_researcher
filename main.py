# FILE: main.py

from dotenv import load_dotenv
# Load environment variables from .env file at the very start
load_dotenv()

from graph import app
import pprint

def main():
    """
    Main function to run the autonomous researcher graph.
    """
    # Define the input for the graph
    inputs = {"topic": "The role of attention mechanisms in transformer models"}

    print("🚀 Starting the Autonomous Scientific Researcher...")
    print(f"▶️  Topic: {inputs['topic']}")
    print("-" * 50)

    # Invoke the graph and stream the results, printing each step's output
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"✅ Output from node '{key}':")
            pprint.pprint(value, indent=2, width=80, depth=None)
        print("-" * 50)

    print("🏁 Research process finished.")

if __name__ == "__main__":
    main()