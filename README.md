# TravelBuddy — AI Multi-Agent Travel Planner  
**Track:** Concierge Agents  
**Author:** Muhammed Asif t  
**Competition:** Kaggle – Agents Intensive Capstone Project (Nov 2025)

---
## 🔍 Overview  
TravelBuddy is an AI-powered Multi-Agent Travel Planner that automatically creates personalized itineraries.  
It researches attractions, filters top places, builds a day-by-day plan, and remembers user preferences for future trips.

This project demonstrates key concepts from the 5-Day AI Agents Intensive course:
- Multi-Agent System  
- Tools (Search Tool Stub, Geo Logic)  
- Memory & Sessions  
- Context Engineering  
- Logging / Observability  

---
## 🧠 Architecture  
### Agents Used  
1. **ResearchAgent**  
   - Finds attractions using Search Tool  
   - Filters, dedupes, compacts context  

2. **PlannerAgent**  
   - Builds daily itinerary  
   - Time slot allocation  
   - Creates structured travel plan  

3. **TravelBuddy Orchestrator**  
   - Manages memory  
   - Calls Research → Planner in sequence  
   - Saves trip to memory  

### Tools Used  
- Search Tool Stub  
- Geo-distance logic  
- Memory (JSON file)  

---
## 📂 Repository Structure  
travelbuddy-agent/
├── travelbuddy.py
├── requirements.txt
├── README.md
└── memory/
└── memory_bank.json

---
## ▶️ How to Run  
### Local 

1. Install dependencies
   
    pip install -r requirements.txt
   
3. Run demo:
    python travelbuddy.py
   
Kaggle Notebook Example:
```python
from travelbuddy import TravelBuddy

tb = TravelBuddy(memory_path="memory/memory_bank.json")
out = tb.plan_trip(
    user_id="kaggle_user",
    destination="Paris",
    start_date="2025-12-01",
    end_date="2025-12-03",
    interests=["museums","cafes"],
    preferences={"diet":"veg"}
)
out["summary"]

---
## ✍️ Submission Notes  

- No API keys are included in the repository.  
- The Search Tool is a mocked version (stub).  
- Memory is stored in a simple JSON file.  
- This README content can be reused for your Kaggle Writeup.  

---

## 📜 License  
MIT License

---

