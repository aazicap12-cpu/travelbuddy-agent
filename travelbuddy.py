"""
travelbuddy.py
TravelBuddy — Multi-Agent Travel Planner (Concierge Track)

Usage Example:
    from travelbuddy import TravelBuddy

    tb = TravelBuddy(store_path="memory/memory_bank.json")
    out = tb.plan_trip(
        user_id="muhammed123",
        destination="New York",
        start_date="2025-12-20",
        end_date="2025-12-22",
        interests=["museums", "parks", "markets"],
        preferences={"diet": "vegetarian", "max_walk_km": 5}
    )
    print(out["summary"])
"""

from __future__ import annotations
import json
import logging
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# ---------- Logging / Observability ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("travelbuddy")

# ---------- Memory Utilities ----------
def ensure_dir(path: str):
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

def read_json(path: str) -> Dict[str, Any]:
    if os.path.exists(path):
        with open(path, "r", encoding="utf8") as f:
            return json.load(f)
    return {}

def write_json(path: str, data: Dict[str, Any]):
    ensure_dir(path)
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- Memory Bank ----------
class MemoryBank:
    """
    Simple file-based memory.
    Stores user trip history and preferences.
    """
    def __init__(self, path: str):
        self.path = path
        self.data = read_json(self.path)

    def get_session(self, user_id: str) -> Dict[str, Any]:
        return self.data.get(user_id, {"preferences": {}, "trips": []})

    def save_session(self, user_id: str, session: Dict[str, Any]):
        self.data[user_id] = session
        write_json(self.path, self.data)
        logger.info("Memory saved for user %s", user_id)

# ---------- Search Tool (Stub Version) ----------
def search_tool_stub(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Mock search tool — replace with real Google Search or API if needed.
    """
    logger.info("Search Tool Query: %s", query)

    demo_places = [
        {"name": "City Museum", "description": "Popular museum", "rating": 4.6, "lat": 40.7794, "lon": -73.9632, "hours": "09:00-17:00"},
        {"name": "Central Park", "description": "Large urban park", "rating": 4.8, "lat": 40.785091, "lon": -73.968285, "hours": "24/7"},
        {"name": "Grand Market", "description": "Local market", "rating": 4.5, "lat": 40.7527, "lon": -73.9772, "hours": "08:00-20:00"},
        {"name": "Art Gallery", "description": "Contemporary art", "rating": 4.4, "lat": 40.7614, "lon": -73.9776, "hours": "10:00-18:00"},
    ]

    return demo_places[:top_k]

# ---------- Data Models ----------
@dataclass
class ItineraryItem:
    day: str
    time_range: str
    place: Dict[str, Any]

# ---------- Research Agent ----------
class ResearchAgent:
    def __init__(self, search_tool=search_tool_stub):
        self.search_tool = search_tool

    def run(self, destination: str, interests: List[str], top_k_each: int = 5) -> List[Dict[str, Any]]:
        logger.info("ResearchAgent: collecting places for %s", destination)

        results = []
        for interest in interests:
            query = f"{destination} top {interest}"
            hits = self.search_tool(query, top_k=top_k_each)
            results.extend(hits)

        unique = {}
        for r in results:
            unique[r["name"]] = r  # dedupe

        sorted_places = sorted(unique.values(), key=lambda x: x["rating"], reverse=True)

        compact = [{
            "name": p["name"],
            "description": p["description"],
            "rating": p["rating"],
            "lat": p["lat"],
            "lon": p["lon"],
            "hours": p["hours"]
        } for p in sorted_places[:20]]

        return compact

# ---------- Planner Agent ----------
class PlannerAgent:
    def build_itinerary(self, places: List[Dict[str, Any]], start: str, end: str) -> Dict[str, List[ItineraryItem]]:
        sd = datetime.fromisoformat(start)
        ed = datetime.fromisoformat(end)
        days = (ed - sd).days + 1

        logger.info("PlannerAgent: creating %d-day itinerary", days)

        itinerary = {}
        index = 0

        for d in range(days):
            day = sd + timedelta(days=d)
            day_str = day.date().isoformat()
            itinerary[day_str] = []

            for slot in range(3):  # 3 places per day
                if index >= len(places):
                    break

                time_block = ["09:00-12:00", "12:30-15:00", "15:30-18:00"][slot]
                itinerary[day_str].append(
                    ItineraryItem(
                        day=day_str,
                        time_range=time_block,
                        place=places[index]
                    )
                )
                index += 1

        # Convert dataclass → dict
        return {
            day: [asdict(item) for item in items]
            for day, items in itinerary.items()
        }

# ---------- Main Orchestrator ----------
class TravelBuddy:
    def __init__(self, store_path="memory/memory_bank.json", search_tool=search_tool_stub):
        self.memory = MemoryBank(store_path)
        self.research = ResearchAgent(search_tool)
        self.planner = PlannerAgent()
        logger.info("TravelBuddy ready (memory path: %s)", store_path)

    def plan_trip(self, user_id: str, destination: str, start_date: str, end_date: str,
                  interests: List[str], preferences: Optional[Dict[str, Any]] = None):

        if preferences is None:
            preferences = {}

        logger.info("Planning trip for user: %s", user_id)

        session = self.memory.get_session(user_id)
        session["preferences"].update(preferences)

        places = self.research.run(destination, interests)
        top_places = places[:12]  # context compaction

        itinerary = self.planner.build_itinerary(top_places, start_date, end_date)

        record = {
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "itinerary": itinerary,
            "preferences": session["preferences"],
            "timestamp": datetime.utcnow().isoformat()
        }

        session["trips"].append(record)
        self.memory.save_session(user_id, session)

        return {
            "itinerary": itinerary,
            "places": top_places,
            "session": session,
            "summary": {
                "destination": destination,
                "days": len(itinerary),
                "places_considered": len(top_places),
                "memory_saved": True
            }
        }

# ---------- CLI Demo ----------
def demo_run():
    tb = TravelBuddy()
    result = tb.plan_trip(
        user_id="demo_user",
        destination="Chennai",
        start_date="2025-12-10",
        end_date="2025-12-12",
        interests=["beaches", "markets"],
        preferences={"diet": "veg"}
    )
    print(json.dumps(result["summary"], indent=2))

if __name__ == "__main__":
    demo_run()
