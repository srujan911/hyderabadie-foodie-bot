# database.py - Using different, potentially faster image URLs

restaurants_db = [
    {
        "name": "Paradise Biryani",
        "cuisine": ["Hyderabadi", "North Indian", "Biryani"],
        "location": "Secunderabad",
        "price_range": "₹₹ Theek Thaak",
        "rating": 4.1,
        "is_veg": False,
        "photo_url": "https://i.ytimg.com/vi/P8K3v9g3sL8/maxresdefault.jpg"
    },
  # In database.py, replace the Santosh Dhaba entry with this one:

    {
        "name": "Santosh Dhaba",
        "cuisine": ["North Indian", "Vegetarian"],
        "location": "Miyapur",
        "price_range": "₹ Light",
        "rating": 4.3,
        "is_veg": True,
        "photo_url": "https://b.zmtcdn.com/data/pictures/chains/1/90181/92f857477a32501a55091e4114457032.jpg"
    },
 # In database.py, find Pista House and change ONLY its photo_url
{
    "name": "Pista House",
    "cuisine": ["Hyderabadi", "Bakery"],
    "location": "Gachibowli",
    "price_range": "₹₹ Theek Thaak",
    "rating": 4.0,
    "is_veg": False,
    "photo_url": "https://i.imgur.com/2z42gJ9.jpeg"  # <-- Temporary Test URL
},
    {
        "name": "Chutneys",
        "cuisine": ["South Indian", "Vegetarian"],
        "location": "Banjara Hills",
        "price_range": "₹₹ Theek Thaak",
        "rating": 4.5,
        "is_veg": True,
        "photo_url": "https://img.etimg.com/thumb/width-1600,height-900,imgsize-206492,resizemode-75,msid-95693394/industry/services/hotels-/-restaurants/hyderabads-iconic-chutneys-restaurant-chain-now-in-the-uk.jpg"
    },
    {
        "name": "Farzi Cafe",
        "cuisine": ["Modern Indian", "Fusion"],
        "location": "Jubilee Hills",
        "price_range": "₹₹₹ Full Posh",
        "rating": 4.6,
        "is_veg": False,
        "photo_url": "https://b.zmtcdn.com/data/pictures/chains/4/18386464/73f27233519e4a6a578a1099684128f6.jpg"
    },
    {
        "name": "Olive Bistro & Bar",
        "cuisine": ["Italian", "Mediterranean"],
        "location": "Jubilee Hills",
        "price_range": "₹₹₹ Full Posh",
        "rating": 4.4,
        "is_veg": False,
        "photo_url": "https://im1.dineout.co.in/images/uploads/restaurant/sharpen/3/h/n/p322-166030953662f66e2098485.jpg?tr=tr:n-large"
    },
    {
        "name": "Conçu",
        "cuisine": ["Cafe", "Desserts", "Bakery"],
        "location": "Jubilee Hills",
        "price_range": "₹₹ Theek Thaak",
        "rating": 4.7,
        "is_veg": True,
        "photo_url": "https://res.cloudinary.com/purnesh/image/upload/w_1000,f_auto,q_auto:eco,c_limit/concu-cakes-jubilee-1.jpg"
    }
]



def find_restaurants(cuisine=None, location=None, is_veg=None, price_range=None, rating=None):
    """
    Finds restaurants that match ALL the given criteria.
    Any criteria left as None (not provided) will be ignored.
    """
    results = []
    for restaurant in restaurants_db:
        # We start by assuming it's a match, and then disqualify it if any check fails.
        is_a_match = True

        # --- Check Cuisine ---
        if cuisine and cuisine.lower() not in [c.lower() for c in restaurant["cuisine"]]:
            is_a_match = False
        
        # --- Check Location ---
        if location and location.lower() != restaurant["location"].lower():
            is_a_match = False

        # --- Check Veg/Non-Veg ---
        # "is_veg is not None" checks if the user actually provided this filter.
        if is_veg is not None and is_veg != restaurant["is_veg"]:
            is_a_match = False
        
        # --- Check Price Range ---
        if price_range and price_range != restaurant["price_range"]:
            is_a_match = False
        
        # --- Check Rating ---
        if rating and rating > restaurant["rating"]:
            is_a_match = False

        # If, after all checks, the restaurant is still a match, add it to our results.
        if is_a_match:
            results.append(restaurant)
            
    return results