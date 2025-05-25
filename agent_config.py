# agent_config.py

# This structure will be used to configure the OmniDimension voice agent.
# It's based on the interaction flow designed in Step 5.

agent_flow_config = [
    {
        "step_name": "Greeting",
        "type": "TTS_then_STT_Confirm", # Text-to-Speech, then Speech-to-Text for confirmation
        "prompt_text": "Hello! I'm your personal deal finder. I can help you get the best price on limited-edition items. Today, are you looking for the Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'?",
        "expected_input": {"type": "confirmation", "options": ["yes", "no", "yeah", "yep", "sure", "correct", "nope", "nah"]},
        "variables_to_set": "product_confirmation",
        "notes": "If confirmation is 'no', the agent should have a polite exit path (e.g., 'Okay, let me know when you're looking for something specific. Goodbye!'). This path is not detailed in this config."
    },
    {
        "step_name": "ExplainProcess",
        "type": "TTS", # Text-to-Speech only
        "prompt_text": "Great! I will now contact several resellers to check prices, availability, and try to negotiate the best deal for you. This might take a few moments as I need to make some (simulated) calls. Please wait, and I'll update you shortly.",
        "notes": "This step is conditional on 'product_confirmation' being 'yes'. Triggers the backend offer processing."
    },
    {
        "step_name": "SimulatedResellerInteractions",
        "type": "Logic_BackendCall_then_TTS", # This step implies a backend process happens, then TTS
        "prompt_text": "I'm now checking with various resellers for you... (Short pause) ...Just a moment more while I gather the latest information... (Short pause) ...Okay, I've contacted SneakerHeaven, KicksRUs, SoleSource, and LimitedKicksCo.",
        "notes": "This step simulates the agent 'working'. The actual calls to resellers are mocked by `offer_logic.py`. The TTS provides a summary of actions taken. The backend (webhook from Step 8) would have already processed `get_top_offers` from `offer_logic.py` before this step's TTS is finalized. The key is that the *results* of these interactions are used in the *next* step."
    },
    {
        "step_name": "PresentTop3Offers",
        "type": "TTS", # TTS only, content dynamically filled by backend.
        "prompt_text": "I've analyzed all the options and found some great deals! Here are the top three recommendations for the Nike Air Jordan 1: First, [Seller1Name] offers them for [Seller1Price] dollars, with delivery in [Seller1Delivery] days. They note: [Seller1Notes]. Second, [Seller2Name] has them for [Seller2Price] dollars, delivered in [Seller2Delivery] days. Their notes: [Seller2Notes]. And third, [Seller3Name] for [Seller3Price] dollars, delivery in [Seller3Delivery] days, with notes: [Seller3Notes].",
        "notes": "This TTS string needs to be populated dynamically using the data from `get_top_offers`. The placeholders [SellerXName], [SellerXPrice], [SellerXDelivery], [SellerXNotes] will be filled by the backend before TTS generation. If fewer than 3 offers, the text should adapt (e.g., 'Here are the top two...')."
    },
    {
        "step_name": "AskForEmail",
        "type": "TTS_then_STT_Confirm",
        "prompt_text": "These are the best deals I found. Would you like me to send these top recommendations to your email address so you have all the details?",
        "expected_input": {"type": "confirmation", "options": ["yes", "no", "please", "sure", "okay", "nope"]},
        "variables_to_set": "send_email_confirmation",
        "notes": "Proceed to 'CollectEmailAddress' if 'yes', otherwise proceed to 'Closing'."
    },
    {
        "step_name": "CollectEmailAddress",
        "type": "TTS_then_STT_Email", # TTS, then STT expecting an email format
        "prompt_text": "Great! What is your email address? Please spell it out if it's complex.",
        "expected_input": {"type": "email_address_pattern"}, # OmniDimension should have a built-in entity for email
        "variables_to_set": "user_email",
        "notes": "This step is conditional on 'send_email_confirmation' being 'yes'. Includes a prompt to spell out for better accuracy."
    },
    {
        "step_name": "ConfirmEmailAddress",
        "type": "TTS_then_STT_Confirm",
        "prompt_text": "Got it. I have your email as [UserEmail]. Is that correct?",
        "expected_input": {"type": "confirmation", "options": ["yes", "no", "correct", "incorrect"]},
        "variables_to_set": "email_is_correct",
        "notes": "Placeholder [UserEmail] will be filled with the value from 'user_email' variable. If 'no', ideally loop back to 'CollectEmailAddress' or have a specific correction step (not detailed further here)."
    },
    {
        "step_name": "NotifyEmailWillBeSent",
        "type": "TTS",
        "prompt_text": "Perfect. I will send the details of these offers to [UserEmail] shortly. The email will include contact numbers and notes for each seller.",
        "notes": "This step is conditional on 'email_is_correct' being 'yes'. This would be the point where a webhook is triggered to actually send the email."
    },
    {
        "step_name": "Closing",
        "type": "TTS",
        "prompt_text": "Thank you for using the deal finder! I hope this helps you get your sneakers. Have a great day!",
        "notes": "This is the final step. Could be reached after 'NotifyEmailWillBeSent', or if 'product_confirmation' was 'no', or if 'send_email_confirmation' was 'no'."
    }
]

# Placeholder for how this agent configuration would be used with the OmniDimension SDK
def create_omnidimension_agent(client, agent_name: str, flow_config: list, webhook_url: str):
    """
    Hypothetical function to create or update an OmniDimension agent.
    In a real scenario, this would use the OmniDimension SDK.
    """
    print(f"\n--- Simulating Agent Creation ---")
    print(f"Agent Name: {agent_name}")
    print(f"Webhook URL for backend logic: {webhook_url}")
    
    # Simulate checking the flow_config structure (very basic check)
    if not isinstance(flow_config, list) or not all(isinstance(step, dict) for step in flow_config):
        print("Error: flow_config is not a list of dictionaries.")
        return None
    
    print(f"Number of steps in flow: {len(flow_config)}")
    print("First step details:")
    if flow_config:
        for key, value in flow_config[0].items():
            print(f"  {key}: {value}")
            
    # Hypothetical SDK usage (actual SDK calls would be here)
    # Example:
    # agent = client.agent.create(
    #     name=agent_name,
    #     flow_configuration=flow_config, # This would likely need transformation to match SDK's expected format
    #     initial_prompt="Use the flow defined.", # Or specific initial prompt from flow_config
    #     tts_provider="eleven_labs", # Example
    #     voice_id="some_voice_id",   # Example
    #     llm_service="gpt-4",        # Example
    #     on_call_ended_webhook_url=webhook_url # Webhook for post-call processing or specific events
    # )
    # print(f"Agent '{agent_name}' would be created/updated with ID: {getattr(agent, 'id', 'mock_agent_123')}")
    
    print("\nTo actually create/update the agent, this configuration (potentially transformed) would be passed to the OmniDimension SDK/platform.")
    print("The SDK would handle validation and deployment of this agent flow.")
    
    # Return a mock agent link or ID
    mock_agent_id = f"agent_{agent_name.lower().replace(' ', '_')}_{sum(ord(c) for c in agent_name) % 1000}"
    return f"http://mock-od-platform.com/dashboard/agents/{mock_agent_id}"

if __name__ == "__main__":
    # client = Client(api_key="YOUR_ACTUAL_API_KEY_HERE") # Assuming client would be initialized
    
    # This is the webhook URL where OmniDimension would send events (e.g., call ended, specific triggers).
    # Our backend FastAPI app (from Step 8) would be listening at a similar URL.
    mock_call_webhook_url = "http://localhost:8000/webhook/omnidimension_call_event"
    
    agent_name = "Sneaker Deal Finder Agent V1"
    
    # Simulate creating the agent
    agent_link_or_id = create_omnidimension_agent(
        client=None, # Passing None as we don't have a live client object here
        agent_name=agent_name,
        flow_config=agent_flow_config,
        webhook_url=mock_call_webhook_url
    )
    
    if agent_link_or_id:
        print(f"\nMock agent link/ID for '{agent_name}': {agent_link_or_id}")
        print("\nFull Agent Flow Configuration:")
        for i, step in enumerate(agent_flow_config):
            print(f"\n--- Step {i+1}: {step['step_name']} ---")
            for key, value in step.items():
                print(f"  {key}: {value}")
    else:
        print(f"Failed to simulate creation for agent '{agent_name}'.")
