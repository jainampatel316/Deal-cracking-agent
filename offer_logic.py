mock_reseller_data = [
    {
        "seller_name": "SneakerHeaven",
        "product_name": "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'",
        "price": 350.00,
        "potential_negotiated_price": 330.00,
        "delivery_time_days": 5,
        "stock_available": True,
        "contact_number": "555-0101",
        "notes": "Brand new, original box."
    },
    {
        "seller_name": "KicksRUs",
        "product_name": "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'",
        "price": 360.00,
        "potential_negotiated_price": 350.00,
        "delivery_time_days": 3,
        "stock_available": True,
        "contact_number": "555-0102",
        "notes": "Fast shipping, collector's condition."
    },
    {
        "seller_name": "ResellKingz",
        "product_name": "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'",
        "price": 340.00,
        "potential_negotiated_price": 340.00,
        "delivery_time_days": 7,
        "stock_available": False,
        "contact_number": "555-0103",
        "notes": "Currently out of stock, restock expected next month."
    },
    {
        "seller_name": "SoleSource",
        "product_name": "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'",
        "price": 375.00,
        "potential_negotiated_price": 360.00,
        "delivery_time_days": 4,
        "stock_available": True,
        "contact_number": "555-0104",
        "notes": "Includes authentication certificate."
    },
    {
        "seller_name": "LimitedKicksCo",
        "product_name": "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'",
        "price": 330.00,
        "potential_negotiated_price": 320.00,
        "delivery_time_days": 6,
        "stock_available": True,
        "contact_number": "555-0105",
        "notes": "Slightly used, 9/10 condition."
    }
]

def get_top_offers(reseller_data: list, product_name: str):
    # Filter for the product and stock availability
    filtered_offers = [
        offer for offer in reseller_data
        if offer["product_name"] == product_name and offer["stock_available"]
    ]

    processed_offers = []
    for offer in filtered_offers:
        # Determine final_price
        if offer["potential_negotiated_price"] < offer["price"]:
            final_price = offer["potential_negotiated_price"]
        else:
            final_price = offer["price"]
        
        # Add final_price to a copy of the offer dictionary
        processed_offer = offer.copy()
        processed_offer["final_price"] = final_price
        processed_offers.append(processed_offer)

    # Sort offers: primarily by final_price (asc), secondarily by delivery_time_days (asc)
    # The lambda function returns a tuple for multi-level sorting
    sorted_offers = sorted(
        processed_offers,
        key=lambda x: (x["final_price"], x["delivery_time_days"])
    )

    # Return top 3 offers, or all if fewer than 3
    return sorted_offers[:3]

if __name__ == "__main__":
    product_to_find = "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'"
    top_offers = get_top_offers(mock_reseller_data, product_to_find)

    print(f"Top offers for: {product_to_find}\n")
    if top_offers:
        for i, offer in enumerate(top_offers, 1):
            print(f"--- Offer {i} ---")
            print(f"Seller: {offer['seller_name']}")
            print(f"Final Price: ${offer['final_price']:.2f}")
            print(f"Original Price: ${offer['price']:.2f}")
            if offer['potential_negotiated_price'] < offer['price']:
                print(f"Potential Negotiated Price: ${offer['potential_negotiated_price']:.2f}")
            print(f"Delivery Time: {offer['delivery_time_days']} days")
            print(f"Contact: {offer['contact_number']}")
            print(f"Notes: {offer['notes']}")
            print("-" * 20)
    else:
        print("No available offers found for this product.")
