from geopy.geocoders import Nominatim
locator = Nominatim(user_agent='myapp')
latitude = 55.84489000000001
longitude = 37.487555237895194
address = locator.reverse(f'{latitude}, {longitude}')
print(latitude, longitude)
print(address.address)
# print(address.raw)
needed_address = address.raw.get('address')
print(needed_address.get('house_number'), needed_address.get('road'), needed_address.get('city'))
