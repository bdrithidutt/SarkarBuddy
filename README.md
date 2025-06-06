<<<<<<< HEAD
# 🧠 Sarkar Buddy – Citizen Support Chatbot (Hackathon Prototype)

**Sarkar Buddy** is a bilingual AI-powered chatbot designed to bridge the communication gap between citizens and government services. Built for rapid prototyping in a hackathon setting, this project delivers real-time responses to common queries, tracks service statuses, and logs complaints through an intuitive chat interface.

---

## 🎯 Objective

To develop a **working prototype** of a chatbot within 24–48 hours that:
- Responds to common government-related queries
- Displays real-time service statuses (via sample/mock data)
- Accepts and logs public complaints with ticketing functionality

---

## ✅ Key Features

### 1. Intelligent Chatbot (Telugu + English)
- Handles 5–10 predefined queries such as:
  - Pension status
  - Ration card progress
  - Electricity bill reminders
  - Government scheme updates
  - Complaint registration
- Friendly and localized conversational tone

### 2. Service Tracking
- Queries mapped to a sample JSON-based database
- Returns relevant data within seconds

### 3. Complaint Logging
- User messages trigger complaint creation
- Generates and displays a sample ticket number
- (Optional) Allows photo upload for visual evidence

---

## 💻 Technology Stack

### 🤖 Chatbot Engine
- **Dialogflow** (Google NLP) for natural language understanding  
  *or*  
- **Python + Flask** with custom rule-based logic

### 🧑‍💻 Frontend (UI)
- **React.js** (web-based WhatsApp-style interface)  
- **Google Fonts** for Telugu and English support  
- **Web Speech API** (optional, for voice input)  

### 💾 Backend / Data
- **Mock JSON database** for simulating service records and ticket logs  
- **Local storage** for client-side prototype state management

### 🎨 Design & Tools
- **Figma** for UI/UX mockups and branding elements  
- **Visual Studio Code** for development  
- **GitHub** for version control and team collaboration  
- (Optional) **Firebase** for hosting the live prototype

---

## 📋 Hackathon Implementation Plan

| Phase | Task | Time Estimate |
|-------|------|---------------|
| 🧠 Plan | Role assignment, scope definition, tool selection | 2 hrs |
| 🔧 Build | Chatbot logic + Sample database integration | 8–10 hrs |
| 💬 UI Dev | Chat interface + Complaint form + Language support | 6–8 hrs |
| 🧪 Testing | Functional testing + UI refinement | 4–6 hrs |
| 🎤 Pitch Prep | Slide creation + Demo scripting & rehearsal | 2–4 hrs |

---

## 📌 Deliverables

1. **Prototype**  
   - Functional chatbot (with five core queries + one complaint flow)  
   - Responsive web/mobile UI supporting bilingual input  

2. **Mock Data**  
   - Sample citizen data in a structured JSON format  
   - Complaint logs with assigned ticket IDs  

3. **Demo Pitch**  
   - 2-minute presentation (Problem → Solution → Live Demo → Impact)  
   - 1-slide deck summarizing scope and benefits

---

## 🧠 Why This Solution?

- **Problem Addressed**: Citizens face delays and uncertainty when accessing public service updates.
- **Proposed Solution**: A conversational chatbot offering immediate responses in local languages with a friendly interface.
- **Potential Impact**: Reduces footfall at government offices, improves access to information, and builds digital trust—especially in rural and semi-urban areas.

---

## 🚀 Future Potential

- Real-time integration with government APIs  
- Support for additional languages and services  
- Admin dashboards for monitoring complaint logs  
- Voice-based access and mobile app version  
- Scalable architecture for state or national use

---

## 📞 Sample Interaction (Demo Flow)

```text
User: What is my pension status?
Bot: Ramu, your pension has been approved and will be credited this Friday.

User: There is a pothole on Main Road.
Bot: Thank you for reporting. Complaint registered with Ticket ID #123.
=======
# SarkarBuddy
Prototype chatbot to bridge citizen-government communication gaps.
>>>>>>> 228e72eb574deec8dee994b09cecb8a486d3fa26
