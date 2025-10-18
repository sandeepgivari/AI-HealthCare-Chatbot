# 🏥 AI Healthcare Chatbot

A simple yet functional **AI-powered Healthcare Chatbot** built using **HTML, CSS, JavaScript**, and a **Flask backend** with **MongoDB** integration.

This project allows users to:
1. Enter their details (Name, Age, Place, Mobile Number).
2. Chat with an AI healthcare assistant through a simple two-page interface.
3. Automatically store user details and chat history in a **MongoDB NoSQL database**.
4. When the same user visits again, their previous data and chats are updated under the same record.

---

## ⚙️ Features

- 🧑‍💻 **Two-step user interface**
  - Step 1: Collects user details.  
  - Step 2: Opens chatbot interface for interaction.

- 💬 **AI Chat Integration**
  - Simple 2–3 line responses.
  - Handles text and optional file input.

- 🗄️ **MongoDB Integration**
  - Stores user data and conversation history.
  - Updates old records for returning users.

- 🌐 **Flask Backend**
  - Connects front-end with MongoDB.
  - Handles form data and chat messages.

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-------------|
| Frontend | HTML, CSS, JavaScript (TailwindCSS) |
| Backend | Flask (Python) |
| Database | MongoDB (NoSQL) |

---

## 🚀 How to Run

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/healthcare_chatbot.git
cd healthcare_chatbot

###🧑‍⚕️ **About**

This project demonstrates how AI and simple frontend design can combine to create a basic healthcare assistant interface.
It can be expanded to include:

AI model integration (e.g., OpenAI or Gemini)

Better UI/UX animations

Real medical API support
