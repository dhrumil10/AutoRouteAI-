````markdown
# AutoRoute AI

**AI-Powered Smart Route Optimizer with Real-Time Detours and Conversational Assistant**

---

## Overview

AutoRoute AI is an advanced route optimization system developed in just **2 days**. It leverages AI, real-time traffic data, and natural language processing to deliver personalized, energy-efficient, and adaptive navigation solutions.

Key highlights:

- Multi-route navigation with energy consumption estimates  
- Real-time traffic and incident-aware dynamic rerouting  
- Seamless detour integration with POI search (e.g., coffee shops)  
- Conversational AI assistant powered by OpenAI GPT for route explanations and tips  
- Vehicle mode selection: economy, normal, emergency  
- Supports EV and gasoline vehicles with tailored suggestions  

---

## Features

- **Multiple route alternatives** with detailed travel time and energy estimates  
- **Dynamic detours** allowing users to add stops and update routes seamlessly  
- **Real-time traffic incident detection** to avoid delays and optimize routes  
- **Interactive conversational assistant** for personalized driving advice and route info  
- **Energy-efficient routing** optimized for battery or fuel saving  
- **Modern tech stack** with FastAPI backend and Streamlit frontend  

---

## Tech Stack

- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **AI:** OpenAI GPT API  
- **Mapping & Routing:** Mapbox Directions & Geocoding APIs  
- **Traffic Data:** TomTom Traffic API  
- **Containerization:** Docker  

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/AutoRouteAI.git
   cd AutoRouteAI
````

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   Create a `.env` file in the project root with:

   ```
   MAPBOX_ACCESS_TOKEN=your_mapbox_token
   OPENAI_API_KEY=your_openai_key
   TOMTOM_API_KEY=your_tomtom_key
   ```

---

## Running the Application

### Backend

```bash
uvicorn autoroute-ai.api.main:app --reload
```

Backend will run at: `http://localhost:8000`

### Frontend

```bash
streamlit run autoroute-ai/frontend/dashboard.py
```

Frontend will run at: `http://localhost:8501`

---

## Usage

* Enter origin and destination addresses in the frontend.
* Search for nearby points of interest (like coffee shops) to add as detours.
* Select preferred vehicle type and travel priority (economy, normal, emergency).
* Get multiple optimized routes with energy consumption estimates.
* Chat with the AI assistant for personalized tips and route explanations.
* Enjoy real-time dynamic rerouting based on traffic incidents.

---

## Future Improvements

* Integrate weather data for smarter routing.
* Advanced energy modeling with elevation and driving behavior.
* User profiles with adaptive personalized recommendations.
* Multi-modal routing including public transit and biking.
* Mobile app support for on-the-go use.

---

## License

[MIT License](LICENSE)

---

## Contact

Built by \[Dhrumil Patel] — feel free to reach out!
GitHub: [https://github.com/yourusername](https://github.com/dhrumil10)


```
```
