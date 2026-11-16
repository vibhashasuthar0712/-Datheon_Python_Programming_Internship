# Rule-Based Internship Support Chatbot

## 📌 Project Overview

The **Rule-Based Internship Support Chatbot** is a Python-based interactive chatbot developed as part of the Datheon Python Programming Internship.

The chatbot is designed to answer frequently asked internship-related questions using predefined responses stored in a JSON dataset. It processes user queries, identifies relevant keywords using regular expressions, and returns appropriate answers.

This project demonstrates how a rule-based conversational system can provide basic automated support without requiring machine learning or external AI APIs.

---

## 🎯 Problem Statement

Develop a rule-based customer support chatbot that can understand user queries through keyword detection and regular expressions.

The chatbot should:

- Handle greetings and conversational inputs.
- Answer frequently asked questions.
- Identify keywords and patterns in user messages.
- Support multiple-intent queries.
- Provide fallback responses for unrecognized questions.
- Handle errors gracefully.
- Allow users to end the conversation using commands such as `bye`, `exit`, and `quit`.

---

## ✨ Key Features

### 1. JSON-Based FAQ Management
- Stores predefined questions, keywords, and answers in `sample_faq.json`.
- Loads FAQ data dynamically when the chatbot starts.
- Validates the structure and content of the FAQ dataset.

### 2. Input Normalization
- Converts user input into lowercase.
- Removes unnecessary punctuation.
- Handles extra whitespace.
- Makes keyword matching more consistent.

### 3. Regular Expression Matching
- Uses Python's `re` module to identify keywords.
- Applies word-boundary matching to avoid partial-word matches.
- Detects relevant FAQ entries based on user input.

### 4. Greeting Detection
- Recognizes greetings such as `hello`, `hi`, and `good morning`.
- Provides an appropriate welcome response.

### 5. Multi-Intent Matching
- Identifies multiple FAQ topics in a single query.
- Returns all relevant answers instead of stopping at the first match.

### 6. Acknowledgement Handling
- Recognizes conversational responses such as `ok`, `thanks`, and `got it`.
- Provides suitable acknowledgement messages.

### 7. Smart Fallback Handling
- Responds appropriately when a query is not recognized.
- Requests additional details for very short or unclear inputs.
- Suggests topics the chatbot can help with.

### 8. Error Handling
- Handles missing JSON files.
- Detects invalid JSON formats.
- Validates FAQ data before starting.
- Handles empty user inputs.
- Supports graceful termination through keyboard interruption.

### 9. Exit Commands
Users can end the conversation using:

- `bye`
- `exit`
- `quit`

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| JSON | Storing and loading FAQ data |
| Regular Expressions (`re`) | Keyword and pattern matching |
| pathlib | File path management |
| Exception Handling | Managing runtime and file-related errors |

---

## 📂 Project Structure

```text
Rule-Based-Internship-Support-Chatbot/
│
├── chatbot.py
├── sample_faq.json
└── README.md
```

### File Description

- **chatbot.py:** Contains the complete chatbot implementation, including FAQ loading, input normalization, keyword matching, response generation, fallback handling, and conversation control.
- **sample_faq.json:** Stores greeting keywords and predefined internship-related FAQs with their corresponding answers.
- **README.md:** Provides project documentation, features, setup instructions, and usage details.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vibhashasuthar0712/Datheon_Python_Programming_Internship.git
```

### 2. Navigate to the Project Folder

```bash
cd Datheon_Python_Programming_Internship/Rule-Based-Internship-Support-Chatbot
```

### 3. Check Python Installation

Make sure Python 3 is installed.

```bash
python --version
```

### 4. Run the Chatbot

```bash
python chatbot.py
```

**Note:** This project uses Python's built-in libraries, so no additional package installation is required.

---

## 💬 Sample Interaction

```text
Welcome to Datheon Internship Support Chatbot!

You can ask questions about your internship.
Type 'bye', 'exit', or 'quit' to end the conversation.

You: hello

Chatbot: Hello! Welcome to Datheon Internship Support.
How can I help you?

You: when will I receive my certificate?

Chatbot: Certificates are reviewed and issued within
3-5 business days after your code review.

You: hours and certificate

Chatbot: We operate Monday through Friday from
9:00 AM to 6:00 PM IST.

Certificates are reviewed and issued within
3-5 business days after your code review.

You: thanks

Chatbot: You're welcome! Happy to help.

You: bye

Chatbot: Thank you for using our support chatbot. Goodbye!
```

---

## 🧠 How It Works

The chatbot follows a simple rule-based processing workflow:

1. **Load FAQ Data:** Reads greeting keywords and FAQ information from the JSON file.
2. **Validate Data:** Checks whether the loaded dataset has the expected structure.
3. **Receive User Input:** Accepts questions through the terminal.
4. **Normalize Input:** Converts text into a standardized format.
5. **Detect Intent:** Searches for matching keywords using regular expressions.
6. **Generate Response:** Returns the relevant predefined FAQ answers.
7. **Handle Fallbacks:** Provides an alternative response when no matching FAQ is found.
8. **Continue Conversation:** Waits for the next query until the user enters an exit command.

---

## 🧪 Testing

The chatbot was tested with different types of inputs to verify its functionality.

| Test Case | Expected Behaviour |
|---|---|
| Greeting (`hello`) | Displays a welcome message |
| Acknowledgement (`ok`) | Returns an acknowledgement |
| Certificate query | Provides certificate-related information |
| Working hours query | Displays working hours |
| Multiple-intent query | Returns multiple relevant answers |
| Unrecognized query | Displays a fallback response |
| Empty input | Requests the user to enter a question |
| Exit command (`bye`) | Terminates the conversation |

---

## 📚 Learning Outcomes

Through this project, I gained practical experience in:

- Building rule-based conversational applications.
- Working with JSON datasets.
- Applying regular expressions for text matching.
- Normalizing and processing user input.
- Implementing keyword-based intent identification.
- Handling multiple matching intents.
- Managing exceptions and invalid data.
- Organizing Python programs using functions.
- Designing interactive command-line applications.

---

## 🚀 Future Improvements

Some possible enhancements for this project include:

- Adding more FAQs and supported intents.
- Improving keyword matching with synonyms.
- Implementing more advanced conversational context management.
- Adding a graphical user interface.
- Storing conversation history for analysis.

---

## 👩‍💻 Author

**Vibhasha Suthar**

GitHub: [github.com/vibhashasuthar0712](https://github.com/vibhashasuthar0712)

**Project developed as part of the Datheon Python Programming Internship.**
