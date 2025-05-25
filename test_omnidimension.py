from omnidimension import Client

# Replace with your actual API key
API_KEY = "2QkPorXpKTAosloCwtD6ELd8ZPUt59pGh5NWTYKlQes"

def main():
    """Initializes the OmniDimension client, lists agents, and prints the results."""
    try:
        # Initialize the client
        client = Client(api_key=API_KEY)
        print("Successfully initialized OmniDimension client.")

        # List agents
        response = client.agent.list()
        print("\nRaw response:")
        print(response) # Print the raw response to inspect its structure

        if response and response.get('status') == 200:
            agents_data = response.get('json', {})
            agents_list = agents_data.get('bots', [])
            total_records = agents_data.get('total_records', 0)

            print(f"\nFound {total_records} agents:")
            if agents_list:
                for agent in agents_list:
                    # Assuming agent is a dictionary now
                    agent_id = agent.get('id')
                    agent_name = agent.get('name')
                    print(f"- Agent ID: {agent_id}, Name: {agent_name}")
            else:
                print("No agents found in the 'bots' list.")
        else:
            print(f"Failed to retrieve agents. Status: {response.get('status')}")
            print(f"Response JSON: {response.get('json')}")


    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
