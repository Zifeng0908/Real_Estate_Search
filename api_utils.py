from requests import get
import json
import pandas as pd
from dotenv import load_dotenv
import os
from format_utils import format_timestamp, column_adjust
from scoring import scoringSystem

# Load API key securely from .env file
load_dotenv()
x_rapidapi_key = os.getenv("x_rapidapi_key")

# Search properties using Zillow's RapidAPI based on location and filters
def properties_search(location, price_range, min_bath, min_bed):
    # Define endpoint URL and base query parameters
    url = "https://zillow-com4.p.rapidapi.com/properties/search"
    query = {
        "location": location.strip(),
        "status": "forSale",
        "sort": "relevance",
        "sortType": "asc",
        "priceType": "listPrice",
        "listingType": "agent"
    }

    # Apply user-defined filters if provided
    if price_range:
        query["priceRange"] = price_range.strip()
    if min_bed:
        query["bedroom"] = str(min_bed).strip()
    if min_bath:
        query["bathroom"] = str(min_bath).strip()

    # Define request headers including RapidAPI credentials
    headers = {
        "x-rapidapi-key": x_rapidapi_key,
        "x-rapidapi-host": "zillow-com4.p.rapidapi.com"
    }

    # Make API call and parse response
    response = get(url, headers=headers, params=query)
    json_response = json.loads(response.content).get('data', [])

    # Store all ten housing information to this list
    properties = []

    # Extract key details for up to 10 properties
    for house in json_response[:10]:  # Limit to first 10 results
        price_info = house.get('price', {})
        address_info = house.get('address', {})
        listing_info = house.get('listing', {})
        estimate_info = house.get('estimates', {})
        price = price_info.get('value', 'N/A')
        # A Zestimate is Zillow’s automated estimate of a home’s market value. 
        zestimate = estimate_info.get('zestimate', 'N/A')

        # Calculate price difference from Zestimate if available.
        # Therefore, a positive difference means that the list price of the house is more than its actual value according to zillow
        # On the other hand, a negative difference value means exactly the opposite. 
        # If the zestimate value is lacking, then the difference would also be "N/A"
        if zestimate == 'N/A':
            difference = 'N/A'
        else:
            difference = price - zestimate

        zpid = house.get('zpid')

        # Aggregate property details into a dictionary
        property_info = {
            "Address": f"{address_info.get('streetAddress', 'N/A')}, {address_info.get('city', 'N/A')}, {address_info.get('state', 'N/A')} {address_info.get('zipcode', 'N/A')}",
            "Price": price,
            "Price per sqrt" : price_info.get('pricePerSquareFoot', 'N/A'),
            "Price Change": price_info.get('priceChange', 'N/A'),
            "Price Change Date": format_timestamp(price_info.get('changedDate', 'N/A')),
            "Zestimate": zestimate,
            "Difference" : difference,
            "Bedrooms": house.get('bedrooms', 'N/A'),
            "Bathrooms": house.get('bathrooms', 'N/A'),
            "Living Area (sqft)": house.get('livingArea', 'N/A'),
            "Listing Status": listing_info.get('listingStatus', 'N/A'),
            "Zillow Url" : f"https://www.zillow.com/homedetails/{zpid}_zpid/" if zpid else "N/A"
        }
        properties.append(property_info)

    # Convert property data to DataFrame for analysis
    df = pd.DataFrame(properties)
    # Generate safe Excel filename by replacing problematic characters
    safe_location = ''.join(c if c.isalnum() or c == '_' else '_' for c in location)
    excel_path = f"zillow_properties_{safe_location}.xlsx"
    # Apply custom scoring system to each property
    df['Score'] = df.apply(lambda house: scoringSystem(house, price_range, min_bed, min_bath), axis = 1)
    # Export to Excel
    df.to_excel(excel_path, index=False)
    # Auto-adjust columns with openpyxl
    column_adjust(excel_path)
    return df