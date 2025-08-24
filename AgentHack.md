
--- Your Personalised Travel Itinerary ---
## Paris Luxury Solo Trip: August 24-26, 2025

**Itinerary Overview**

This itinerary focuses on art and food, tailored for a luxurious solo experience.  Each day follows a similar structure, allowing for flexibility and spontaneity.

* **Day 1: Arrival & Exploration (August 24)**
    * 12:30: Local Food Tour (Fine Dining)
    * 15:00: Paris Art Gallery or Studio
    * 19:00: Sunset Viewing & Dinner

* **Day 2: Discover Paris (August 25)**
    * 12:30: Local Food Tour (Fine Dining)
    * 15:00: Paris Art Gallery or Studio
    * 19:00: Sunset Viewing & Dinner

* **Day 3: Final Adventures (August 26)**
    * 12:30: Local Food Tour (Fine Dining)
    * 15:00: Paris Art Gallery or Studio
    * 19:00: Sunset Viewing & Dinner

**Recommended Activities:**

* Paris Historic Center
* Famous Paris Landmark
* Local Paris Market

**Budget in EUR**

* **Total Estimated Budget:** €1840 (converted from $2000 USD)
* **Estimated Itinerary Budget:**  €1125 (based on provided USD breakdown and assuming similar EUR costs)
    * Accommodation: ~€540  (assumed equivalent to USD value)
    * Food: ~€300 (assumed equivalent to USD value)
    * Activities: ~€240 (assumed equivalent to USD value)
    * Transportation: ~€45 (assumed equivalent to USD value)


**Special Museum Exhibit to See**

* Mamluks. 1250-1517


**Fine Dining Recommendation**

* Hotel Regina Louvre (2 Place des Pyramides, Paris)


**Expense Log Confirmation**

* Dinner at Hotel Regina Louvre: €150


**Notes:**

* This is a suggested itinerary. Feel free to adjust timings and activities based on your preferences.
* Budget is an estimate and can vary.
* Consider pre-booking restaurants and attractions, especially for fine dining and popular exhibits.
* Check local weather and pack accordingly.
------------------------------------------

✨ A user-friendly view of this run is available in your Portia Dashboard:
https://app.portialabs.ai/dashboard/plan-runs?plan_run_id=prun-281a5cd3-d073-4828-8590-0906130d7ef1


GitHub Copilot: I'll help you modify the code to add weather results to your Paris travel itinerary. Here's how to update your plan:

````python
# ...existing code...
    .step(
        task="Add an estimated dinner expense of 150 EUR to the trip plan for the found restaurant.",
        tool_id="mcp:travel-assistant:add_expense",
        inputs=[
            Variable(name="$userId", description="The user's ID."),
            Variable(name="$restaurant_details", description="Details of the restaurant for the expense description."),
        ],
        output="$expense_confirmation",
    )
    .step(
        task="Get the weather forecast for Paris, France for August 24-26, 2025.",
        tool_id="browser_tool",
        output="$weather_forecast",
    )
    .step(
        task="""
        Synthesize all the information gathered into a single, clean, human-readable travel plan.
        Format the output in Markdown. Include sections for:
        - Itinerary Overview
        - Budget in EUR
        - Weather Forecast for August 24-26, 2025
        - Special Museum Exhibit to See
        - Fine Dining Recommendation
        - Expense Log Confirmation
        Make it look like a professional travel summary.
        """,
        # --- KEY CHANGE: Use our special, powerful summarization tool ---
        tool_id="summary_llm_tool",
        inputs=[
            Variable(name="$itinerary_details", description="The generated itinerary."),
            Variable(name="$local_budget", description="The budget converted to EUR."),
            Variable(name="$exhibit_name", description="The name of the Louvre exhibit."),
            Variable(name="$restaurant_details", description="Details of the recommended restaurant."),
            Variable(name="$expense_confirmation", description="Confirmation of the logged expense."),
            Variable(name="$weather_forecast", description="Weather forecast for Paris for the travel dates."),
        ],
        output="$trip_summary",
    )
    # ...existing code...
````

This change adds a new step that:

1. Uses the browser tool to search for and retrieve weather forecast information for Paris
2. Stores the results in a new variable `$weather_forecast`
3. Passes this information to the summary step
4. Updates the summary task description to explicitly include a Weather Forecast section

When executed, the browser will visit a weather website, fetch the forecast for your travel dates, and this information will be included in your final Markdown output.

Virtuoso633: get_weather

Get current weather and 5-day forecast for any location. Awards 5 points per check.





Parameters

locationRequired

string
Location to get weather for (e.g., "Paris, France", "New York, USA", "Tokyo")

userId

string
User ID for points tracking (optional)


get the weather update for location and userid it is tool in the given mcp only so add it

GitHub Copilot: I'll update your code to use the proper `get_weather` tool from the MCP service instead of adding a browser step. Here's the fix:

````python
# ...existing code...
    .step(
        task="Add an estimated dinner expense of 150 EUR to the trip plan for the found restaurant.",
        tool_id="mcp:travel-assistant:add_expense",
        inputs=[
            Variable(name="$userId", description="The user's ID."),
            Variable(name="$restaurant_details", description="Details of the restaurant for the expense description."),
        ],
        output="$expense_confirmation",
    )
    .step(
        task="Get the weather forecast for Paris, France for August 24-26, 2025.",
        tool_id="mcp:travel-assistant:get_weather",
        inputs=[
            Variable(name="$destination", description="The travel destination."),
            Variable(name="$userId", description="The user's ID for points tracking.")
        ],
        output="$weather_forecast",
    )
    .step(
        task="""
        Synthesize all the information gathered into a single, clean, human-readable travel plan.
        Format the output in Markdown. Include sections for:
        - Itinerary Overview
        - Budget in EUR
        - Special Museum Exhibit to See
        - Fine Dining Recommendation
        - Weather Forecast for Trip Dates
        - Expense Log Confirmation
        Make it look like a professional travel summary.
        """,
        # --- KEY CHANGE: Use our special, powerful summarization tool ---
        tool_id="summary_llm_tool",
        inputs=[
            Variable(name="$itinerary_details", description="The generated itinerary."),
            Variable(name="$local_budget", description="The budget converted to EUR."),
            Variable(name="$exhibit_name", description="The name of the Louvre exhibit."),
            Variable(name="$restaurant_details", description="Details of the recommended restaurant."),
            Variable(name="$expense_confirmation", description="Confirmation of the logged expense."),
            Variable(name="$weather_forecast", description="Weather forecast for Paris for the travel dates."),
        ],
        output="$trip_summary",
    )
    # ...existing code...
````

This implementation:

1. Uses the `mcp:travel-assistant:get_weather` tool directly from your MCP server
2. Passes both the destination and userId as inputs (the userId enables points tracking)
3. Stores the weather information in the `$weather_forecast` variable
4. Adds this variable to the input list for the summary step
5. Updates the summary task description to include a "Weather Forecast for Trip Dates" section

The summary tool will now incorporate the weather information into the final travel itinerary document.

Virtuoso633: can you make a good readme saying how i integrated mcp_server and the script for the hackathon 

GitHub Copilot: # Portia + MCP Travel Concierge Hackathon Project

## 🚀 Overview

This repository contains my submission for the Portia SDK Hackathon. I've built a sophisticated AI-powered travel concierge system that seamlessly integrates Portia's planning capabilities with a custom MCP (Model Control Platform) server offering specialized travel tools.

The system plans luxury trips by orchestrating multiple AI services, web scraping, currency conversion, weather forecasting, and more - all through a unified planning interface.

## 🔌 MCP Server Integration

The heart of this project is the integration between Portia SDK and a custom travel MCP server:

```python
travel_tools = McpToolRegistry.from_streamable_http_connection(
    server_name="travel-assistant",
    url="https://travel-assistant-mcp.virtuosoofcoding633.workers.dev/mcp",
)
```

This connects to a remote MCP server that exposes specialized travel planning tools:
- Itinerary creation
- Currency conversion
- Restaurant/event finding
- Expense tracking
- Weather forecasting

These remote tools are then combined with Portia's native tools:
```python
native_tools = ToolRegistry([
    BrowserTool(infrastructure_option=BrowserInfrastructureOption.REMOTE),
    default_llm_tool,
    summary_llm_tool,
    FileWriterTool()
])

combined_tools = travel_tools + native_tools
```

## 🛠️ Architecture

The project showcases several advanced integration patterns:

1. **Multi-Model LLM Approach** - Two different LLM configurations for different tasks:
   - Standard LLM for simple tasks
   - Specialized high-capacity model for comprehensive trip summarization

2. **User Verification Hooks** - Custom hook for expense confirmation:
   ```python
   def confirm_before_add_expense(tool: Tool, args: dict, plan_run: PlanRun, step: Step):
       # Implementation ensures user approval before adding expenses
   ```

3. **Cloud Storage Integration** - Results stored in Portia cloud for persistence and sharing:
   ```python
   config = Config.from_default(llm_provider="google", storage_class=StorageClass.CLOUD)
   ```

## ✨ Key Features

- **End-to-End Trip Planning** - From initial requirements to final itinerary document
- **Live Data Integration** - Currency rates, weather forecasts, museum exhibits
- **Budget Management** - Currency conversion and expense tracking
- **User Confirmation** - Interactive approval for financial transactions
- **Beautiful Output** - Professional Markdown summaries suitable for travelers

## 🚗 Workflow

The system implements an 8-step planning process:

1. Create a luxury itinerary focused on art and dining
2. Convert budget from USD to EUR
3. Research current museum exhibitions via web scraping
4. Find highly-rated restaurants near attractions
5. Add and track travel expenses
6. Get weather forecasts for trip dates
7. Synthesize all information into a comprehensive trip plan
8. Save as a shareable Markdown document

## 🔧 Setup & Usage

1. Clone this repository
2. Create a `.env` file with your API credentials (Google/Portia)
3. Install dependencies: `pip install -r requirements.txt`
4. Run the demo: `python hackathon_final_demo.py`

Example output:
```
✅ MCP server tools loaded.
✅ Specialized summarization tool created.
✅ Portia native tools created.
✅ Tool registries combined. Total tools: 10
✅ Portia instance created and configured for Cloud Dashboard.

--- Final Plan for Execution ---
// Plan details displayed
---------------------------------

▶️ Executing the final plan...

✅ Plan Complete!
📄 /path/to/trip_plan.md
```

## 🔮 Future Improvements

- Add photo suggestions for destinations
- Integrate flight and accommodation booking
- Support for multi-destination trips
- Real-time updates during travel

## 📝 Hackathon Learnings

Building this project demonstrated the power of combining:
- Remote MCP services with local tools
- Multiple LLM models with specialized roles
- Web scraping with structured data processing
- User approval flows with automated planning

The Portia SDK made it straightforward to orchestrate these diverse capabilities into a cohesive application with minimal code.