def calculate_score(price, reviews, rating):
    if price <= 0:
        return 0

    score = (reviews * rating) / price
    return round(score, 2)