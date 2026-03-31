# 🚗 AI DDR Generator

AI-powered system that generates **Detailed Diagnostic Reports (DDR)** for vehicles using structured inspection data and LLM-based analysis.

> Converts raw vehicle inspection data into actionable insights in seconds.

---



## 📌 Features

- ⚡ AI-powered DDR report generation  
- 🧠 Intelligent issue detection & severity classification  
- 🖼️ Optional image integration (thermal / inspection visuals)  
- 📊 Clean and structured output format  
- 🔌 Easy API integration (Groq / Gemini / OpenAI-compatible)  
- 🌍 Deployable for real-world usage  

---


## 📥 Sample Input

```json
{
  "vehicle": "Royal Enfield Meteor 350",
  "date": "25 March 2026",
  "engine": {
    "inspection": "Oil leakage observed near engine casing"
  },
  "brakes": {
    "inspection": "Front brake worn out"
  },
  "battery": {
    "inspection": "Normal condition"
  }
}

