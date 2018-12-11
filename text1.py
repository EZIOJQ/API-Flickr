import requests
import json


# apply for a flickr authentication key at http://www.flickr.com/services/apps/create/apply/?
# paste the key (not the secret) as the value of the variable flickr_key
flickr_key = "9425b6c00bb87894456ae07ccd7489ca"
def get_flickr_data(tags_string):
    baseurl = "https://api.flickr.com/services/rest/"
    params_diction = {}
    params_diction["api_key"] = flickr_key # from the above global variable
    params_diction["tags"] = tags_string # Input must follow some rules in order to work properly
    params_diction["tag_mode"] = "all"
    params_diction["method"] = "flickr.photos.search"
    params_diction["per_page"] = 3
    params_diction["media"] = "photos"
    params_diction["format"] = "json"
    params_diction["nojsoncallback"] = 1
    flickr_resp = requests.get(baseurl, params = params_diction)
    # Useful for debugging: print the url! Uncomment the below line to do so.
    #print(flickr_resp.url) # Paste the result into the browser to check it out...
    flickr_text = flickr_resp.text # Access the text attribute of the response object
    # Then, transform it into a Python object, once you have valid JSON formatted text
    flickr_data_obj = json.loads(flickr_text)
    return flickr_data_obj # And return it

# A few different invocations to the get_flickr_data function
result_sunset_mountains = get_flickr_data("mountains, sunset")
result_river_mts = get_flickr_data("river,mountains")
result_just_mountains = get_flickr_data("mountains")

# And try printing one out to see what it's like... lots of data
# (Recall the nested data and nested iteration chapter!)

print(result_just_mountains)