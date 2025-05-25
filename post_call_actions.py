import csv
import os
from datetime import datetime

# --- Sample Data Structures ---

# Example based on output from offer_logic.get_top_offers()
mock_top_offers = [
    {
        "seller_name": "LimitedKicksCo",
        "product_name": "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'",
        "price": 330.00,
        "potential_negotiated_price": 320.00,
        "delivery_time_days": 6,
        "stock_available": True,
        "contact_number": "555-0105",
        "notes": "Slightly used, 9/10 condition.",
        "final_price": 320.00 # Added by get_top_offers
    },
    {
        "seller_name": "SneakerHeaven",
        "product_name": "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'",
        "price": 350.00,
        "potential_negotiated_price": 330.00,
        "delivery_time_days": 5,
        "stock_available": True,
        "contact_number": "555-0101",
        "notes": "Brand new, original box.",
        "final_price": 330.00 # Added by get_top_offers
    },
    {
        "seller_name": "KicksRUs",
        "product_name": "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'",
        "price": 360.00,
        "potential_negotiated_price": 350.00,
        "delivery_time_days": 3,
        "stock_available": True,
        "contact_number": "555-0102",
        "notes": "Fast shipping, collector's condition.",
        "final_price": 350.00 # Added by get_top_offers
    }
]

# Example for log_seller_interactions. This would include all attempts, not just top offers.
# 'final_price_achieved' refers to the price the agent secured (could be original or negotiated)
mock_interactions_data = [
    {
        "seller_name": "SneakerHeaven", "price": 350.00, "potential_negotiated_price": 330.00,
        "final_price_achieved": 330.00, "stock_available": True, "delivery_time_days": 5,
        "notes": "Brand new, original box."
    },
    {
        "seller_name": "KicksRUs", "price": 360.00, "potential_negotiated_price": 350.00,
        "final_price_achieved": 350.00, "stock_available": True, "delivery_time_days": 3,
        "notes": "Fast shipping, collector's condition."
    },
    {
        "seller_name": "ResellKingz", "price": 340.00, "potential_negotiated_price": 340.00,
        "final_price_achieved": 340.00, "stock_available": False, "delivery_time_days": 7, # Stock was false
        "notes": "Currently out of stock, restock expected next month."
    },
    {
        "seller_name": "SoleSource", "price": 375.00, "potential_negotiated_price": 360.00,
        "final_price_achieved": 360.00, "stock_available": True, "delivery_time_days": 4,
        "notes": "Includes authentication certificate."
    },
    {
        "seller_name": "LimitedKicksCo", "price": 330.00, "potential_negotiated_price": 320.00,
        "final_price_achieved": 320.00, "stock_available": True, "delivery_time_days": 6,
        "notes": "Slightly used, 9/10 condition."
    }
]

# --- Email Sending Function (Mock) ---
def send_recommendations_email(top_offers: list, recipient_email: str):
    """
    Formats and 'sends' a plain text email with top offers.
    Mocks sending by printing to console.
    """
    email_subject = "Your Top Sneaker Deals!"
    
    email_body = f"Hello,\n\nHere are your top sneaker recommendations:\n\n"
    if not top_offers:
        email_body += "No specific offers found this time. Please try again later.\n"
    else:
        for i, offer in enumerate(top_offers, 1):
            email_body += f"--- Offer {i} ---\n"
            email_body += f"Seller: {offer.get('seller_name', 'N/A')}\n"
            email_body += f"Product: {offer.get('product_name', 'N/A')}\n"
            email_body += f"Final Price: ${offer.get('final_price', 0.00):.2f}\n"
            email_body += f"Delivery Time: {offer.get('delivery_time_days', 'N/A')} days\n"
            email_body += f"Notes: {offer.get('notes', 'No additional notes.')}\n"
            if 'contact_number' in offer: # Include contact if available, as per agent flow
                email_body += f"Contact: {offer.get('contact_number')}\n"
            email_body += "\n"
            
    email_body += "Best regards,\nYour Sneaker Deal Finder Agent"

    print("--- Mock Email Sending ---")
    print(f"Recipient: {recipient_email}")
    print(f"Subject: {email_subject}")
    print("Body:")
    print(email_body)
    print("--- End of Mock Email ---")

# --- Data Logging Function ---
def log_seller_interactions(call_id: str, product_name: str, interactions: list, log_file_path: str = "seller_interactions.csv"):
    """
    Logs seller interaction data to a CSV file.
    Creates the file and writes headers if it doesn't exist.
    """
    headers = [
        "timestamp", "call_id", "product_name", "seller_name", 
        "price_queried", "negotiated_price_achieved", "stock_available", 
        "delivery_time_days", "seller_notes"
    ]
    
    file_exists = os.path.isfile(log_file_path)
    
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"DEBUG: Received interactions in log_seller_interactions: {interactions}") # DEBUG PRINT

    rows_to_write = []
    for interaction in interactions:
        row = {
            "timestamp": current_timestamp,
            "call_id": call_id,
            "product_name": product_name,
            "seller_name": interaction.get('seller_name', 'N/A'),
            "price_queried": interaction.get('price_queried', 0.00), # Corrected key
            "negotiated_price_achieved": interaction.get('negotiated_price_achieved', 0.00), # Corrected key
            "stock_available": interaction.get('stock_available', False),
            "delivery_time_days": interaction.get('delivery_time_days', 'N/A'),
            "seller_notes": interaction.get('seller_notes', '') # Corrected key
        }
        rows_to_write.append(row)
    
    if rows_to_write: # DEBUG PRINT
        print(f"DEBUG: First row to be written in log_seller_interactions: {rows_to_write[0]}")

    try:
        with open(log_file_path, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerows(rows_to_write)
        print(f"Successfully logged {len(rows_to_write)} interactions to {log_file_path}")
    except IOError as e:
        print(f"Error writing to CSV file {log_file_path}: {e}")

# --- Main block for testing ---
if __name__ == "__main__":
    print("--- Running Post Call Actions Tests ---")
    
    # Test email sending
    test_email_recipient = "test_user@example.com"
    send_recommendations_email(mock_top_offers, test_email_recipient)
    
    print("\n" + "="*30 + "\n") # Separator
    
    # Test data logging
    test_call_id = f"call_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    test_product_name = "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'"
    # Simulate logging one interaction, then another, to test appending
    log_seller_interactions(test_call_id, test_product_name, [mock_interactions_data[0]], "test_interactions_log.csv")
    log_seller_interactions(test_call_id, test_product_name, mock_interactions_data[1:], "test_interactions_log.csv") # Log remaining
    
    print("\n--- Post Call Actions Tests Completed ---")
    print("Mock email was 'sent' (printed to console).")
    print(f"Seller interactions were logged to 'test_interactions_log.csv'.")

    # Optional: Read the CSV to verify content (for testing purposes)
    try:
        with open("test_interactions_log.csv", mode='r', newline='', encoding='utf-8') as csvfile:
            print("\n--- Contents of test_interactions_log.csv ---")
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)
            print("--- End of CSV Content ---")
    except FileNotFoundError:
        print("\nLog file 'test_interactions_log.csv' was not created.")
