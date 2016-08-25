import os
from hotelSeeds import HotelSeeds
# filename = 'backend/hotelSeeds.get_seeds_url() cannot concatenate 'str' and 'NoneType' objectsSeeds/seeds_url.csv'
# if os.path.exists(filename):
#     message = 'OK, the file exists.'
# else:
#     message = "Sorry, I cannot find the  file."
# print message
hotelSeeds = HotelSeeds('ss', 'english', 'beijing')
hotelSeeds.get_seeds_url()