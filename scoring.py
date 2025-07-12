#A ranking system to assign a score to each of the ten real estates
#The house represents the informations on row of the Excel profile
#While the remainings are the requirements of the user
def scoringSystem(house, price_range = None, min_bed = None, min_bath = None):
    score = 0
    try:
        price = float(house['Price'])
    except (TypeError, ValueError):
        price = None

    try:
        bedrooms = int(house['Bedrooms'])
    except (TypeError, ValueError):
        bedrooms = None

    try:
        bathrooms = int(house['Bathrooms'])
    except (TypeError, ValueError):
        bathrooms = None

    try:
        difference = float(house['Difference'])
    except (TypeError, ValueError):
        difference = None

    try:
        priceChange = float(house['Price Change'])
    except (ValueError, TypeError):
        priceChange = None

    # Below are the calculating rule for the scoring method
    if not price_range or "," not in price_range:
        min_price = max_price = price_range = None
    else:
        try:
            min_price_str, max_price_str = [p.strip() for p in price_range.split(",")]
            min_price = int(min_price_str)
            max_price = int(max_price_str)
        except ValueError:
            min_price = max_price = None


    #Price range
    if price_range is not None and price is not None:
        if min_price <= price <= max_price:
            score += 10
            if price <= (min_price + (max_price - min_price)/2):
                score += 5
    
    #Price change
    if priceChange is not None:
        if priceChange < 0:
            score +=5
        elif priceChange > 0:
            score -= 5

    #Bed and bath room
    if min_bed is not None and bedrooms is not None:
        if bedrooms > min_bed:
            score += 7
        elif bedrooms == min_bed:
            score += 5
        else:
            score -= 5
    
    if min_bath is not None and bathrooms is not None:
        if bathrooms > min_bath:
            score += 7
        elif bathrooms == min_bath:
            score += 5
        else:
            score -= 5



    #difference score
    if difference is not None and price:
        ratio = difference / price
        percent = round(ratio * 100)
        score -= percent

    return score



    