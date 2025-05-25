# webhook_server.py
# Implements a simple Flask web server to handle post-call webhooks from OmniDimension.

from flask import Flask, request, jsonify

# Assuming offer_logic.py and post_call_actions.py are in the same directory or accessible in PYTHONPATH
from offer_logic import get_top_offers, mock_reseller_data as all_reseller_data
from post_call_actions import send_recommendations_email, log_seller_interactions

# Create a Flask app instance
app = Flask(__name__)

# Define the webhook route for OmniDimension call ended events
@app.route('/webhook/omnidimension_call_ended', methods=['POST'])
def handle_omnidimension_webhook():
    """
    Handles post-call webhook from OmniDimension.
    Processes data to find top offers, log interactions, and send email.
    """
    # --- 1. Validate and Extract Data ---
    if not request.is_json:
        app.logger.error("Request was not JSON")
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    data = request.get_json()
    app.logger.info(f"Received webhook data: {data}")

    # Expected OmniDimension payload structure (simulated)
    # {
    #     "call_id": "some_unique_call_identifier",
    #     "user_email": "user@example.com", // Can be null if not provided
    #     "product_name": "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'",
    # }
    call_id = data.get('call_id')
    user_email = data.get('user_email') # This might be None or empty if not provided by user
    product_name = data.get('product_name')

    if not call_id or not product_name:
        app.logger.error(f"Missing call_id or product_name in request: {data}")
        return jsonify({"status": "error", "message": "Missing call_id or product_name"}), 400

    app.logger.info(f"Processing call_id: {call_id}, product: {product_name}, email: {user_email}")

    # --- 2. Process Offer Logic ---
    # We use the full mock_reseller_data imported from offer_logic.py
    # In a real system, this data might come from a database or live API calls.
    try:
        top_offers = get_top_offers(all_reseller_data, product_name)
        app.logger.info(f"Top offers for {product_name}: {top_offers}")
    except Exception as e:
        app.logger.error(f"Error calling get_top_offers: {e}")
        return jsonify({"status": "error", "message": f"Error processing offers: {str(e)}"}), 500


    # --- 3. Simulate and Log Seller Interactions ---
    # This reconstructs interaction data based on the full reseller data for the given product.
    # In a more advanced scenario, OmniDimension might send detailed interaction logs,
    # or this server might fetch them from a temporary cache related to the call_id.
    interactions_log_data = []
    for seller_data in all_reseller_data:
        if seller_data["product_name"] == product_name:
            # Calculate final_price for logging, similar to get_top_offers
            if seller_data.get("potential_negotiated_price", seller_data["price"]) < seller_data["price"]:
                final_price_achieved = seller_data.get("potential_negotiated_price")
            else:
                final_price_achieved = seller_data["price"]
            
            interaction_entry = {
                'seller_name': seller_data['seller_name'],
                'price_queried': seller_data['price'], # Use the key expected by log_seller_interactions
                'negotiated_price_achieved': final_price_achieved,
                'stock_available': seller_data['stock_available'],
                'delivery_time_days': seller_data['delivery_time_days'],
                'seller_notes': seller_data.get('notes', '') # Use the key expected by log_seller_interactions
            }
            interactions_log_data.append(interaction_entry)
    
    if interactions_log_data:
        try:
            log_seller_interactions(call_id, product_name, interactions_log_data)
            app.logger.info(f"Logged {len(interactions_log_data)} interactions for call_id: {call_id}")
        except Exception as e:
            app.logger.error(f"Error calling log_seller_interactions: {e}")
            # Continue processing even if logging fails, but flag it
            # In a production system, this might trigger an alert
    else:
        app.logger.info(f"No interactions to log for product: {product_name}")


    # --- 4. Send Email if Applicable ---
    if user_email and top_offers:
        try:
            send_recommendations_email(top_offers, user_email)
            app.logger.info(f"Sent recommendations email to: {user_email}")
        except Exception as e:
            app.logger.error(f"Error calling send_recommendations_email: {e}")
            # Continue processing, email failure shouldn't stop the webhook response
    elif not user_email:
        app.logger.info("No user_email provided, skipping email.")
    elif not top_offers:
        app.logger.info(f"No top offers found for {product_name}, skipping email.")

    # --- 5. Return Success Response ---
    return jsonify({"status": "success", "message": "Webhook actions processed"}), 200

# Main block to run the Flask development server
if __name__ == "__main__":
    # Note: Using a port like 5001 to avoid conflict with common ports.
    # debug=True is useful for development, shows detailed errors in browser and reloads on code change.
    # In a production environment, a proper WSGI server like Gunicorn or uWSGI would be used.
    app.run(port=5001, debug=True)
