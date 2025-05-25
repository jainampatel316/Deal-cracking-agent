import os
import json
from omnidimension import Client

# Initialize the OmniDimension client
api_key = os.environ.get('OMNIDIM_API_KEY', '2QkPorXpKTAosloCwtD6ELd8ZPUt59pGh5NWTYKlQes')
client = Client(api_key)

def load_agent_prompt():
    """Load the agent prompt from file"""
    with open('agent_prompt.txt', 'r') as file:
        return file.read()

def load_resellers():
    """Load the mock resellers data"""
    with open('mock_resellers.json', 'r') as file:
        return json.load(file)

def create_voice_agent():
    """Create a new voice agent for sneaker price comparison"""
    # Load the agent prompt
    prompt = load_agent_prompt()
    
    # Create the agent
    agent = client.agent.create(
        name="Sneaker Deal Finder",
        description="A voice agent that compares sneaker reseller prices and finds the best deals",
        prompt=prompt,
        voice_settings={
            "voice_id": "professional-male-1",  # Adjust based on available voices
            "speaking_rate": 1.0,
            "pitch": 0.0
        }
    )
    
    print(f"Created agent with ID: {agent.id}")
    return agent

def configure_webhook(agent_id):
    """Configure the post-call webhook for the agent"""
    # Set up the webhook URL
    webhook_url = "https://your-webhook-server.com/omnidimension-webhook"
    
    # Configure the webhook
    client.agent.update(
        agent_id=agent_id,
        webhook_settings={
            "enabled": True,
            "url": webhook_url,
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer your-webhook-auth-token"
            },
            "events": ["call.completed"]
        }
    )
    
    print(f"Configured webhook for agent {agent_id}")

def add_knowledge_base(agent_id):
    """Add reseller data as a knowledge base for the agent"""
    resellers = load_resellers()
    
    # Add the resellers data as a knowledge base
    knowledge_base = client.knowledge.create(
        agent_id=agent_id,
        name="Sneaker Resellers",
        description="Information about sneaker resellers, prices, and availability",
        data=resellers
    )
    
    print(f"Added knowledge base with ID: {knowledge_base.id}")

def main():
    # Create the voice agent
    agent = create_voice_agent()
    
    # Configure the webhook
    configure_webhook(agent.id)
    
    # Add knowledge base
    add_knowledge_base(agent.id)
    
    # Get the agent URL
    agent_url = f"https://omnidim.io/agent/{agent.id}"
    print(f"\nYour voice agent is ready! Access it at: {agent_url}")
    print("\nNext steps:")
    print("1. Deploy your webhook handler (webhook_handler.js)")
    print("2. Update the webhook URL in the configure_webhook function")
    print("3. Test your agent by making a call")

if __name__ == "__main__":
    main()