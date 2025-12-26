# Django Chatbot with LangChain & Gmail Integration

This project is a Django-based AI chatbot application. It allows users to register, log in, and interact with an AI assistant. The project has been extended from its original tutorial to include modern AI frameworks and partial Google integration.

## 📚 Project Origin

This codebase is based on the **"Django ChatGPT Clone Tutorial"** from [FreeCodeCamp.org](https://www.freecodecamp.org/), created by **@Code With Tomi**.

* **Original Tutorial:** [Watch on YouTube](https://www.youtube.com/watch?v=qrZGfBBlXpk&list=LL&index=5)
* **Original Creator:** [Code With Tomi](https://www.youtube.com/@CodeWithTomi)

## 🚀 Features

### Core Features (from Tutorial)
* **User Authentication:** Full Login, Register, and Logout functionality.
* **Chat Interface:** Clean, responsive UI for sending and receiving messages.
* **Chat History:** Saves user conversations to a local database (SQLite) so history persists across sessions.
* **AJAX Integration:** Seamless messaging without page reloads using JavaScript Fetch API.

### 🛠 Custom Modifications
I have extended the original project with the following enhancements:

* **LangChain Integration:** Replaced/Augmented standard OpenAI API calls with **LangChain**. This allows for more advanced logic, prompt templates, and potential for future agent-based capabilities.
* **Google Mail (Gmail) Integration (WIP):** * Added OAuth2 authentication flow for Google.
    * Currently enables the OAuth consent page to authorize access (Full email reading/sending capabilities are in progress).

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name
