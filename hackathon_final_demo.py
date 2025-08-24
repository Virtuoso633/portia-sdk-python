# hackathon_final_demo.py

from dotenv import load_dotenv
from portia import (
    Config, Portia, PlanBuilder, Variable, Tool, ToolRegistry,
    ExecutionHooks, Clarification, UserVerificationClarification, PlanRun, Step, PlanInput,
    StorageClass
)
from portia.cli import CLIExecutionHooks
from portia.open_source_tools.browser_tool import BrowserTool, BrowserInfrastructureOption
from portia.open_source_tools.llm_tool import LLMTool
from portia.open_source_tools.local_file_writer_tool import FileWriterTool
from portia.tool_registry import McpToolRegistry

load_dotenv(override=True)

# --- The Custom Hook (Same as before) ---
def confirm_before_add_expense(
    tool: Tool, args: dict, plan_run: PlanRun, step: Step
) -> Clarification | None:
    if tool.id == "mcp:travel-assistant:add_expense":
        for c in plan_run.outputs.clarifications:
            if (isinstance(c, UserVerificationClarification) and
                c.step == plan_run.current_step_index and c.resolved and c.response is True):
                return None
        expense_description = args.get("description", "unknown item")
        amount = args.get("amount", 0)
        currency = args.get("currency", "EUR")
        return UserVerificationClarification(
            plan_run_id=plan_run.id,
            user_guidance=f"CONFIRM: Add expense of {amount} {currency} for '{expense_description}'?",
            source="ExpenseConfirmationHook",
        )
    return None

print("--- The End-to-End Luxury Travel Concierge ---")

# --- Configuration ---
try:
    travel_tools = McpToolRegistry.from_streamable_http_connection(
        server_name="travel-assistant",
        url="https://travel-assistant-mcp.virtuosoofcoding633.workers.dev/mcp",
    )
    print("✅ MCP server tools loaded.")

    # --- THIS IS THE KEY CHANGE ---
    # We create two versions of the LLMTool.
    # 1. A standard one for simple tasks.
    # 2. A powerful one specifically for our big summarization task.
    
    # This uses the default model, good for simple tasks.
    default_llm_tool = LLMTool() 
    
    # We give this one a unique ID and tell it to use a more powerful model.
    summary_llm_tool = LLMTool(
        id="summary_llm_tool", 
        model="google/gemini-1.5-pro-latest" # A model with a huge context window
    )
    print("✅ Specialized summarization tool created.")
    # -----------------------------

    native_tools = ToolRegistry([
        BrowserTool(infrastructure_option=BrowserInfrastructureOption.REMOTE),
        default_llm_tool, # Add the default one
        summary_llm_tool, # Add our special one
        FileWriterTool()
    ])
    print("✅ Portia native tools created.")

    combined_tools = travel_tools + native_tools
    print(f"✅ Tool registries combined. Total tools: {len(combined_tools.get_tools())}")

    config = Config.from_default(llm_provider="google", storage_class=StorageClass.CLOUD)
    portia = Portia(
        config=config,
        tools=combined_tools,
        execution_hooks=ExecutionHooks(
            clarification_handler=CLIExecutionHooks().clarification_handler,
            before_tool_call=confirm_before_add_expense,
        ),
    )
    print("✅ Portia instance created and configured for Cloud Dashboard.")
except Exception as e:
    print(f"❌ Setup failed. Error: {e}")
    exit()

# --- The New, More Ambitious Plan ---
print("\n📝 Building the ambitious, multi-tool plan...")
final_plan = (
    PlanBuilder("Plan a 3-day luxury trip to Paris...")
    .plan_input(name="$userId", description="The unique identifier for the user.")
    .plan_input(name="$destination", description="The travel destination.")
    .plan_input(name="$budget_usd", description="The total budget in USD.")
    .step(
        task="Create a 3-day luxury itinerary for a solo traveler in Paris, focusing on art and fine dining.",
        tool_id="mcp:travel-assistant:create_itinerary",
        inputs=[
            Variable(name="$userId", description="The user's ID."),
            Variable(name="$destination", description="The destination city.")
        ],
        output="$itinerary_details",
    )
    .step(
        task="Convert the total budget from USD to EUR.",
        tool_id="mcp:travel-assistant:convert_currency_live",
        inputs=[Variable(name="$budget_usd", description="The budget in USD.")],
        output="$local_budget",
    )
    .step(
        task="Go to the Louvre Museum's official website (louvre.fr/en/) and find the name of a major current temporary exhibition.",
        tool_id="browser_tool",
        output="$exhibit_name",
    )
    .step(
        task="Find a highly-rated Michelin-star restaurant near the Louvre Museum in Paris.",
        tool_id="mcp:travel-assistant:find_events",
        inputs=[Variable(name="$destination", description="The destination city.")],
        output="$restaurant_details",
    )
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
        ],
        output="$trip_summary",
    )
    .step(
        task="Save the final trip summary to a file named 'trip_plan.md'.",
        tool_id="file_writer_tool",
        inputs=[Variable(name="$trip_summary", description="The final Markdown summary of the trip.")],
        output="$file_confirmation",
    )
    .build()
)

print("\n--- Final Plan for Execution ---")
print(final_plan.pretty_print())
print("---------------------------------")

# --- Execution ---
print("\n▶️  Executing the final plan...")
plan_run_inputs = {
    "$userId": "hackathon_demo_user",
    "$destination": "Paris, France",
    "$budget_usd": 2000,
}
plan_run = portia.run_plan(final_plan, plan_run_inputs=plan_run_inputs)

# --- Final Result ---
if plan_run.state == "COMPLETE":
    final_summary = plan_run.outputs.step_outputs.get("$trip_summary").get_value()
    file_path = plan_run.outputs.step_outputs.get("$file_confirmation").get_value()
    
    print("\n\n✅ Plan Complete!")
    print(f"📄 {file_path}")
    print("\n--- Your Personalised Travel Itinerary ---")
    print(final_summary)
    print("------------------------------------------")
    print(f"\n✨ A user-friendly view of this run is available in your Portia Dashboard:")
    print(f"https://app.portialabs.ai/dashboard/plan-runs?plan_run_id={plan_run.id}")
else:
    print(f"\n❌ Plan finished with state: {plan_run.state}")
    if plan_run.outputs.final_output:
        print("Final Output / Error:")
        print(plan_run.outputs.final_output.get_value())