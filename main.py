from api_utils import properties_search
from format_utils import sanitize_input, validate_location
print("🏡 Hello! Welcome to the Real Estate Project Helper Program.")

# Location input
print("\n📍 Location")
print("Please tell me the city and state you'd like to live in.")
print("Example: Houston, TX")
location = input("Your answer: ")
# Validate the locaiton by catching potential errors
while not validate_location(location):
    print("⚠️ Invalid format. Please enter in the form 'City, ST' (e.g., Houston, TX).")
    location = input("Your answer: ")


# Price range input
print("\n💰 Price Range")
print("If you have a price range, enter it in this format: (200000, 500000)")
print("Feel free to leave it blank if you're flexible.")
price_range = input("Your answer: ")

# Bathrooms input
print("\n🛁 Minimum Bathrooms")
print("Enter the minimum number of bathrooms you'd prefer.")
print("Leave it blank if you don't have a preference.")
bathrooms = sanitize_input(input("Your answer: "))


# Bedrooms input
print("\n🛌 Minimum Bedrooms")
print("Enter the minimum number of bedrooms you'd prefer.")
print("Leave it blank if you don't have a preference.")
bedrooms = sanitize_input(input("Your answer: "))

properties_search(location, price_range, bathrooms, bedrooms)
