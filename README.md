# 🚗 AI DDR Generator

AI-powered system that generates **Detailed Diagnostic Reports (DDR)** for vehicles using structured inspection data and LLM-based analysis.

> Converts raw vehicle inspection data into actionable insights in seconds.

---

## 🎬 Demo

![Demo](assets/demo.gif)

---

## 📌 Features

- ⚡ AI-powered DDR report generation  
- 🧠 Intelligent issue detection & severity classification  
- 🖼️ Optional image integration (thermal / inspection visuals)  
- 📊 Clean and structured output format  
- 🔌 Easy API integration (Groq / Gemini / OpenAI-compatible)  
- 🌍 Deployable for real-world usage  

---

## 🏗️ Architecture

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
ai-ddr-generator/
│
├── app/
│   ├── ddr_generator.py
│   ├── image_handler.py
│   └── utils.py
│
├── api/
│   └── groq_client.py
│
├── data/
│   ├── sample_input.json
│   └── sample_output.json
│
├── assets/
│   ├── demo.gif
│   ├── output.png
│   └── architecture.png
│
├── docs/
│   └── system_design.md
│
├── tests/
│   └── test_ddr.py
│
├── .env.example
├── requirements.txt
├── README.md
└── main.py

git clone https://github.com/your-username/ai-ddr-generator.git
cd ai-ddr-generator
pip install -r requirements.txt

python main.py
