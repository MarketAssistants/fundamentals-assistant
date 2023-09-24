from datetime import datetime, timedelta

def today_date(): 
    today_date = datetime.now()
    formatted_date = today_date.strftime("%Y-%m-%d")
    return formatted_date

def tomorrow_date(): 
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")
