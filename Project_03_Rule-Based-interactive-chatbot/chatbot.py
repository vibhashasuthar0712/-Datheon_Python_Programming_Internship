
import json
import re
from pathlib import Path


# ============================================================
# 1. LOAD AND VALIDATE FAQ DATA
# ============================================================

def load_faq_data():

    try:

        file_path = Path(__file__).parent / "sample_faq.json"

        with open(file_path, "r", encoding="utf-8") as file:

            faq_data = json.load(file)

        # Validate JSON structure
        if not isinstance(faq_data, dict):
            raise ValueError("FAQ data must be a JSON object.")

        if not isinstance(faq_data.get("greetings"), list):
            raise ValueError("Greetings must be a list.")

        if not isinstance(faq_data.get("faqs"), list):
            raise ValueError("FAQs must be a list.")

        # Validate greeting entries
        if not all(
            isinstance(item, str) and item.strip()
            for item in faq_data["greetings"]
        ):
            raise ValueError("Invalid greeting entries.")

        # Validate FAQ entries
        if not faq_data["faqs"]:
            raise ValueError("FAQ dataset is empty.")

        for faq in faq_data["faqs"]:

            if not isinstance(faq, dict):
                raise ValueError("Each FAQ must be an object.")

            if not isinstance(faq.get("keywords"), list):
                raise ValueError("FAQ keywords must be a list.")

            if not faq["keywords"] or not all(
                isinstance(keyword, str) and keyword.strip()
                for keyword in faq["keywords"]
            ):
                raise ValueError("Invalid FAQ keywords.")

            if not isinstance(faq.get("answer"), str) or not faq["answer"].strip():
                raise ValueError("FAQ answer is missing or invalid.")

        return faq_data

    except FileNotFoundError:

        print("Error: sample_faq.json file not found.")
        return None

    except json.JSONDecodeError:

        print("Error: Invalid JSON format.")
        return None

    except (ValueError, TypeError) as error:

        print(f"Error: Invalid FAQ data. {error}")
        return None

    except OSError as error:

        print(f"Error loading FAQ file: {error}")
        return None


# ============================================================
# 2. NORMALIZE USER INPUT
# ============================================================

def normalize_input(user_input):

    user_input = user_input.lower().strip()

    user_input = re.sub(r"[^\w\s]", "", user_input)

    user_input = re.sub(r"\s+", " ", user_input)

    return user_input


# ============================================================
# 3. FIND MATCHING FAQs USING REGEX
# ============================================================

def find_matching_faqs(user_input, faq_data):

    normalized_input = normalize_input(user_input)

    matched_faqs = []

    for faq in faq_data["faqs"]:

        for keyword in faq["keywords"]:

            normalized_keyword = normalize_input(keyword)

            pattern = rf"\b{re.escape(normalized_keyword)}\b"

            if re.search(pattern, normalized_input):

                matched_faqs.append(faq)

                # Avoid duplicate matches
                break

    return matched_faqs


# ============================================================
# 4. GREETING DETECTION
# ============================================================

def is_greeting(user_input, faq_data):

    normalized_input = normalize_input(user_input)

    for greeting in faq_data["greetings"]:

        normalized_greeting = normalize_input(greeting)

        pattern = rf"\b{re.escape(normalized_greeting)}\b"

        if re.search(pattern, normalized_input):

            return True

    return False


# ============================================================
# 5. ACKNOWLEDGEMENT HANDLING
# ============================================================

def handle_acknowledgement(user_input):

    normalized_input = normalize_input(user_input)

    acknowledgements = {

        "ok": "Alright! Let me know if you need any more help.",

        "okay": "Alright! Let me know if you need any more help.",

        "thanks": "You're welcome! Happy to help.",

        "thank you": "You're welcome! Happy to help.",

        "got it": "Great! Let me know if you have any questions.",

        "understood": "Glad that helped!"

    }

    return acknowledgements.get(normalized_input)


# ============================================================
# 6. SMART FALLBACK RESPONSE
# ============================================================

def smart_fallback(user_input):

    normalized_input = normalize_input(user_input)

    if len(normalized_input.split()) <= 2:

        return (
            "I'm not sure what you mean. "
            "Could you please provide more details?"
        )

    return (
        "Sorry, I couldn't find an answer to your question. "
        "I can help you with internship working hours, "
        "project submission, GitHub uploads, certificates, "
        "and code reviews."
    )


# ============================================================
# 7. GENERATE CHATBOT RESPONSE
# ============================================================

def generate_response(user_input, faq_data):

    responses = []

    # Check greeting
    if is_greeting(user_input, faq_data):

        responses.append(
            "Hello! Welcome to Datheon Internship Support. "
            "How can I help you?"
        )

    # Find matching FAQs
    matched_faqs = find_matching_faqs(user_input, faq_data)

    # Collect all matching answers
    for faq in matched_faqs:

        responses.append(faq["answer"])

    # Return greeting and FAQ responses
    if responses:

        return "\n".join(responses)

    # Handle acknowledgement
    acknowledgement = handle_acknowledgement(user_input)

    if acknowledgement:

        return acknowledgement

    # Smart fallback
    return smart_fallback(user_input)


# ============================================================
# 8. EXIT COMMAND DETECTION
# ============================================================

def is_exit_command(user_input):

    exit_commands = ["bye", "exit", "quit"]

    normalized_input = normalize_input(user_input)

    return normalized_input in exit_commands


# ============================================================
# 9. MAIN CHATBOT FUNCTION
# ============================================================

def chatbot():

    faq_data = load_faq_data()

    # Stop if FAQ data could not be loaded
    if faq_data is None:

        print("Chatbot could not start because FAQ data is unavailable.")
        return

    # Initial conversational state
    conversation_state = "greeting"

    print("\nWelcome to Datheon Internship Support Chatbot!")

    print("You can ask questions about your internship.")

    print("Type 'bye', 'exit', or 'quit' to end the conversation.\n")

    # Move to intent identification state
    conversation_state = "intent_identification"

    while conversation_state != "exit":

        try:

            user_input = input("You: ").strip()

            # Handle empty input
            if not user_input:

                print("Chatbot: Please enter a question.")
                continue

            # Check exit command
            if is_exit_command(user_input):

                conversation_state = "exit"

                print(
                    "Chatbot: Thank you for using our support chatbot. Goodbye!"
                )

                break

            # Identify intent and generate response
            conversation_state = "intent_identification"

            response = generate_response(user_input, faq_data)

            # Move to resolution state
            conversation_state = "resolution"

            print("Chatbot:", response)

            # Wait for the next user query
            conversation_state = "intent_identification"

        except (EOFError, KeyboardInterrupt):

            conversation_state = "exit"

            print(
                "\nChatbot: Conversation ended. Goodbye!"
            )

            break


# ============================================================
# 10. PROGRAM EXECUTION
# ============================================================

if __name__ == "__main__":

    chatbot()
