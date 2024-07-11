import requests

def get_ride_price(api_base_url, token, origin_lat, origin_lng, destination_lat, destination_lng):
    url = f"{api_base_url}/api/v2/ride/price"
    headers = {
        "Authorization": f"{token}",
        "Content-Type": "application/json"
    }
    payload = {
        "origin_lat": origin_lat,
        "origin_lng": origin_lng,
        "destination_lat": destination_lat,
        "destination_lng": destination_lng,
        "extra_destination_lat": None,
        "extra_destination_lng": None,
        "destination_place_id": None,
        "voucher_code": None,
        "round_trip": False,
        "waiting": None,
        "tag": 0
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Example usage
api_base_url = "https://corporate.snapp.site"  # Replace with the actual base URL
token = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0eXAiOiJtYW5hZ2VyIiwidWlkIjo3MjE3MDI4NiwicGlkIjo3MjE3MDI4NiwiaWF0IjoxNzIwNTY0MTMzLCJpc3MiOjF9.ZF9mZPLgIpxuqkPysCfn3veMOt_E0UBtCoMnUcgJEIO9k-zIfgmJh1hmPVU3FnwRUH1l3qKZlHqIo6SC50iduqohGiATq3MVvAF9pE0uH0bVeYP5mFIBNt1Yp1bNP7wDw8WiiXFtTYl2cOq360DA9F8HYchN4J_YcQkrTtsQP7Ew1PQfKE2ILbygXL8Pt7-M8MDsMItXjr9VeT9Nft-X_3VWZ5T5OxYpU4tDf9DJBG-CGvOasgXCCTBiCdu8q3z-CI26Wt1PES_GW4dDZ1a3S5FRb6pp4Bac5tGMYS4QS1xKI4jf1F0SdJmH51vgs07rfpTSHkqM6i0Z6vFhtfNlwQ"
origin_lat = 35.7669841
origin_lng = 51.4318892
destination_lat = 35.7271734
destination_lng = 51.439585

ride_price_response = get_ride_price(api_base_url, token, origin_lat, origin_lng, destination_lat, destination_lng)
print(ride_price_response)

###& C:/Users/mhshi/AppData/Local/Programs/Python/Python311/python.exe c:/Users/mhshi/Videos/snapp_box_integration/main.py
#{'status': 200, 'data': {'prices': [{'final': 510000, 'service': {'type': '1', 'name': 'اسنپ', 
#'photo_url': 'https://downloads.snapp.site/Service-types/Eco.png', 'description': 'به صرفه', 'is_ride_options_enabled': True, 'can_use_voucher': True, 'is_enabled': True, 'need_additional_info': False, 'is_new': False, 'tooltip': '', 'long_description': ''}, 'is_free_ride': False, 'is_discounted_price': False, 'is_surged': False, 'is_hurry_enable': False, 'is_post_price': False, 'tag': '', 'texts': {'free_ride': '', 'free_ride_footer': '', 'discounted_price': 'تخفیف برای شما!', 'discounted_price_footer': 'تبریک، این سفر ۰٪ تخفیف دارد. از سفرتان لذت ببرید!', 'surge': '', 'surge_footer': '', 'surge_link': None, 'promotion_message': '', 'promotion_message_footer': '', 'post_price': '', 'post_price_footer': ''}, 'distance': 0, 'eta': '', 'items': [], 'promotion_error': '', 'voucher_type': 0}, {'final': 740000, 'service': {'type': '2', 'name': 'اسنپ اکوپلاس', 'photo_url': 'https://downloads.snapp.site/Service-types/Plus.png', 'description': 
#'ویژه', 'is_ride_options_enabled': True, 'can_use_voucher': True, 'is_enabled': True, 'need_additional_info': False, 'is_new': False, 'tooltip': '', 'long_description': ''}, 'is_free_ride': 
#False, 'is_discounted_price': False, 'is_surged': False, 'is_hurry_enable': False, 'is_post_price': False, 'tag': '', 'texts': {'free_ride': '', 'free_ride_footer': '', 'discounted_price': 'تخفیف برای شما!', 'discounted_price_footer': 'تبریک، این سفر ۰٪ تخفیف دارد. از سفرتان لذت ببرید!', 'surge': '', 'surge_footer': '', 'surge_link': None, 'promotion_message': '', 'promotion_message_footer': '', 'post_price': '', 'post_price_footer': ''}, 'distance': 0, 'eta': '', 'items': [], 'promotion_error': '', 'voucher_type': 0}, {'final': 910000, 'service': {'type': '7', 'name': 'اسنپ بایک', 'photo_url': 'https://downloads.snapp.site/Service-types/Bike.png', 'description': 'ویژهٔ مسافر', 'is_ride_options_enabled': True, 'can_use_voucher': True, 'is_enabled': T
#rue, 'need_additional_info': False, 'is_new': False, 'tooltip': '', 'long_description': ''}, 'is_free_ride': False, 'is_discounted_price': False, 'is_surged': False, 'is_hurry_enable': True, 'is_post_price': False, 'tag': '', 'texts': {'free_ride': '', 'free_ride_footer': '', 'discounted_price': 'تخفیف برای شما!', 'discounted_price_footer': 'تبریک، این سفر ۰٪ تخفیف دارد. از سفرتان لذت ببرید!', 'surge': '', 'surge_footer': '', 'surge_link': None, 'promotion_message': '', 
#'promotion_message_footer': '', 'post_price': '', 'post_price_footer': ''}, 'distance': 0, 'eta': '', 'items': [], 'promotion_error': '', 'voucher_type': 0}, {'final': 705000, 'service': {'type': '5', 'name': 'اسنپ باکس', 'photo_url': 'https://downloads.snapp.site/Service-types/Box.png', 'description': 'ویژهٔ مرسولات', 'is_ride_options_enabled': True, 'can_use_voucher': True, '
#is_enabled': True, 'need_additional_info': True, 'is_new': False, 'tooltip': '', 'long_description': ''}, 'is_free_ride': False, 'is_discounted_price': False, 'is_surged': False, 'is_hurry_enable': True, 'is_post_price': False, 'tag': '', 'texts': {'free_ride': '', 'free_ride_footer': '', 'discounted_price': 'تخفیف برای شما!', 'discounted_price_footer': 'تبریک، این سفر ۰٪ تخفیف دارد. از سفرتان لذت ببرید!', 'surge': '', 'surge_footer': '', 'surge_link': None, 'promotion_message': '', 'promotion_message_footer': '', 'post_price': '', 'post_price_footer': ''}, 'distance': 0, 'eta': '', 'items': [], 'promotion_error': '', 'voucher_type': 0}], 'tag': 0, 'confirm_before_ride': False, 'confirm_before_ride_message': '', 'waiting': [{'key': '0m-5m', 'price': 
#30000, 'text': '۰ تا ۵ دقیقه'}, {'key': '5m-10m', 'price': 60000, 'text': '۵ تا ۱۰ دقیقه'}, {'key': '10m-15m', 'price': 90000, 'text': '۱۰ تا ۱۵ دقیقه'}, {'key': '15m-20m', 'price': 120000, 
#'text': '۱۵ تا ۲۰ دقیقه'}, {'key': '20m-25m', 'price': 150000, 'text': '۲۰ تا ۲۵ دقیقه'}, {'key': '25m-30m', 'price': 180000, 'text': '۲۵ تا ۳۰ دقیقه'}, {'key': '30m-45m', 'price': 270000, 'text': '۳۰ تا ۴۵ دقیقه'}, {'key': '45m-1h', 'price': 360000, 'text': '۴۵ دقیقه تا ۱ ساعت'}, {'key': '1h-1h30m', 'price': 540000, 'text': '۱ تا ۱.۵ ساعت'}, {'key': '1h30m-2h', 'price': 720000, 'text': '۱.۵ تا ۲ ساعت'}, {'key': '2h-2h30m', 'price': 900000, 'text': '۲ تا ۲.۵ ساعت'}, {'key': '2h30m-3h', 'price': 1080000, 'text': '۲.۵ تا ۳ ساعت'}, {'key': '3h-3h30m', 'price': 1260000, 'text': '۳ تا ۳.۵ ساعت'}, {'key': '3h30m-4h', 'price': 1440000, 'text': '۳.۵ تا ۴ ساعت'}]}} 
#PS C:\Users\mhshi\Videos\snapp_box_integration> 