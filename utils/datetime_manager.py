from datetime import datetime, timedelta    

def is_expired(stored_datetime_str: str) -> bool:
    try:
        format = "%Y-%m-%d %H:%M:%S.%f"
        stored_datetime = datetime.strptime(stored_datetime_str, format)
        
        expiration_time = stored_datetime + timedelta(minutes=3)
        
        return datetime.now() > expiration_time
    except Exception as e:
        print(f'is_expired e : {e}')
        return False