## SI 508 F18 - Project 1
## 1500 points

######################
## Import statements
######################
import json
import requests
import sys

####################################################################
##### THIS IS CODE TO SET UP TESTING FILE. DO NOT CHANGE IT. #######
import sys
orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f
#### END: THIS IS CODE TO SET UP TESTING FILE. DO NOT CHANGE IT. ###
####################################################################


#############################
## Setup code - DO NOT CHANGE
#############################

search_input = "landscapes" # DEFAULT
if len(sys.argv) > 1:
    if len(sys.argv) > 2:
        print("ERROR: Too many arguments.\nCHECK: Did you try to search for a term with spaces and no quotation marks?")
        exit()
    search_input = sys.argv[1]

#############################
#############################




######################
## Part 0: Preparation
######################

## We have provided a few files to help you practice, and a series of suggestions for how we recommend you practice and play around with code and data to prepare for the rest of this project.

## What is required for Part 0 is that you write code to investigate at least one of these files and do some investigation: indexing, at least one for loop, mutiple print statements.

## It is UP TO YOU how much of it you do beyond that, though I recommend you follow all of these instructions, because it will make the rest of the project much easier.

## -------

## We have provided a sample dictionary representing 1 Flickr photo in the format that Flickr returns it, saved in a JSON file, called sample_diction.json.

## We have also provided a file called sample_flickr_response.json.
## This file contains data that has been gotten from the Flickr API in response to a request for 25 photos tagged with the word "sunset", but the data from the API has been altered slightly so that it is properly formatted in a JSON way (as discussed in class).

## PREPARATION SUGGESTIONS FOLLOW:

## TODO: Write code to open the file and load its contents as a Python object into the variable sample_photo_rep. (We will refer to that variable name in hints later on.)

with open ("sample_diction.json")as f1:
    sample_photo_rep=json.loads(f1.read())

## Then close the file (that'll keep you from running into easily-avoidable errors later on!).

# TODO: Write code to access the nested data inside sample_photo_rep and create a list of all the TAGS of that photo. Save the list of tags in a variable -- say, called sample_tags_list.
sample_tags_list=[]
for item in sample_photo_rep["photo"]["tags"]["tag"]:
    sample_tags_list.append(item["_content"])



## You will need to do nested data investigation in order to manage this.

## Copying the contents of the sample_diction.json file into jsoneditoronline.org may help. Remember, go slowly and step-by-step; understand, then extract, then understand the next bit...

## If you do so, the tags list in sample_tags_list should look like this: ['nature','mist','mountain'] (or in some Python setups, [u'nature',u'mist',u'mountain'] -- this should be rare to nonexistent with Python 3).
## HINT: Check out the '_content' keys' values deep inside the nested dictionary...
## Don't use the "raw" key.
## TODO: Consider: Why do you think we recommend NOT using the "raw" key?


## TODO: Next, write code that will open the sample_flickr_response.json file and load the data inside that file into a variable called search_result_diction. The variable search_result_diction should now contain a very complex dictionary representing information about a bunch of photos that are tagged "sunset". Each photo has an id.
## TODO: Write code to create a list of all of the photo ids from each photo that the search_result_diction data represents, and save that list in a variable called sample_photo_ids.
with open("sample_flickr_response.json")as f2:
    search_result_diction=json.loads(f2.read())

sample_photo_ids=[]
for item in search_result_diction["photos"]["photo"]:
    sample_photo_ids.append(item["id"])

## Both these processes are things you'll need to do in Part 1 to proceed in this project -- except with real data that hasn't been provided for you. These provided files should show you what data representing 1 Flickr photo AND what data representing 1 Flickr *search* looks like. If the data you retrieve later for one of those is very different in structure, you'll know something's wrong. If it's not, then you'll know a bit about how to manage it already.

######################
## Part 1: Setup
######################

## The next part involves writing setup code so that you can access and cache code from Flickr.

## You will need a Yahoo!/Hotmail account in order to sign in to Flickr.
## You need such an account in order to complete this assignment. But it does not need to be a "real" account that you will use for anything else besides this, and you do not need to use your real name for it if you do not want to.

## TODO: Follow the instructions in the UsingRESTAPIs chapter of the provided textbook to get a key for the Flickr API, so that you can get data from Flickr and paste it below, inside the quotes.

## TODO: paste your flickr API key between the quotation marks below, such that the variable flickr_key will contain a string (your flickr key!).
FLICKR_KEY = "9425b6c00bb87894456ae07ccd7489ca"

## **** BEGIN PROVIDED CODE ****
## DO NOT CHANGE ANYTHING ELSE ABOUT THE CODE HERE.
## Normally you should not share API keys with others. But if you include your key in your problem set submission file here, we (graders) will not use it for anything nefarious. You can also regenerate the key if you want to keep it secret in the future (but do NOT regenerate it until AFTER you receive your grade on this project)!
if FLICKR_KEY == "" or not FLICKR_KEY:
    print("Your flickr key is missing from the file. Enter your flickr key where directed and save the program!")
    exit()
## **** END PROVIDED CODE ****


##### Write your caching code here. We suggest keeping the comments provided below and writing the code translations above / below / to the left of them...

CACHE_FNAME = "SAMPLE_SI508_project1_cached_data.json" # LINE PROVIDED FOR YOU, DO NOT CHANGE

## If you save data in this file that is wrong/not working, not a problem: just delete the file from the folder, or rename it if you want to refer back to it later, and run the code to see the new results!

# TODO: Write a try/except statement that does the following:
# Inside the try block:
## (1) Open a file with the CACHE_FNAME name.
## (2) Read the file into one big string.
## (3) Close the open file.
## (4) Load the string into a Python object, saved in a variable called CACHE_DICTION.
# Inside the except block:
## (1) Create a variable called CACHE_DICTION and give it the value of an empty dictionary.
try:
    with open(CACHE_FNAME,'r') as f3:
        _cache_diction=json.loads(f3.read())
except:
    _cache_diction={}



# In total, this should be five or six lines of code. ^
# We have also provided a file SAMPLE_SI508_project1_cached_data.json, which is SIMILAR to what your code should generate in format, etc. (You may end up with much more data in your cache file, and you will definitely end up with different data in your cache file, which is just fine.)

## Next, you'll need to define a function to get data from Flickr which uses the caching framework you just set up -- so it will only go request data from the Flickr API if you have not already made the same request! See below for more detail. You'll need the following utility function to do this in our case.

## Utility function provided for your use here (DO NOT CHANGE) -- to create a unique representation of each request without private data like API keys
def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)
## END UTILILTY FUNCTION

## TODO: Define a function called get_flickr_data which accepts 2 inputs:
## -- a REQUIRED parameter: a string representing a tag to search for on Flickr (e.g. if you wanted to search for data on photos tagged with "mountains", you would pass in "mountains" for this parameter)
## -- an OPTIONAL parameter: whose default value is 50 (representing how many photos you want in your response data)
def get_flickr_data(tag,num=50):
    baseurl="https://api.flickr.com/services/rest/"
    params_d={}
    params_d["api_key"]=FLICKR_KEY
    params_d["tags"]=tag
    params_d["tag_mode"]="all"
    params_d["per_page"] = num
    params_d["method"] = "flickr.photos.search"
    params_d["format"] = "json"
    params_d["media"] = "photos"
    unique_ident=params_unique_combination(baseurl,params_d)
    if unique_ident in _cache_diction:
        return _cache_diction[unique_ident]
    else:
        resp = requests.get(baseurl, params_d)
        _cache_diction[unique_ident] = json.loads(resp.text[14:-1])
        dumped_json_cache = json.dumps(_cache_diction)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return _cache_diction[unique_ident]


## The following is an EXTENDED description of what the function should do.

## This function should use the provided utility function params_unique_combination to get a unique identifier for the data request to the Flickr API.

## The function should check whether or not the unique identifier for each request exists in your cache data, and if it does, should access that data.

### If there is no such data in your cache, the function should make a request to the Flickr Photos Search API for photos tagged with your input string. Your request should use the tag_mode "all" so that if your query string represents multiple tags, it will search for photos with ALL of those tags.
## You must be careful to ensure that you are using ALL the required API parameters properly in the function, that that you are NOT depending on any global variables besides FLICKR_KEY.

### It should modify the string that is returned from the Flickr API so that it is properly JSON formatted. (You want a version of the string without the first 14 characters or the very last character -- see the textbook example!)

### Then, load that modified string into a Python object.

### Then, the function should add the new dictionary of data to your cache dictionary, associated with the unique identifier key, and save all the data in the cache dictionary to your cache file!

## The get_flickr_data function's RETURN VALUE, regardless of whether it got data from the cache, or made a new request and saved data to the cache, should be a big dictionary representing a bunch of search data from the Flickr Photos Search API.

## API docs here: flickr.com/services/api/flickr.photos.search.html

## The base URL for the Flickr API is: "https://api.flickr.com/services/rest/"

## Recall that all Flickr API endpoints have the same base url, but different values for the "method" parameter! For the Photos Search API, that value should be "flickr.photos.search"

## RECOMMENDED TODO once you have defined the function: Make an(other?) invocation to your get_flickr_data function with the input "mountains" (use the default second parameter). Save the result in the variable flickr_mountains_result, and check out what it's like. Is it like sample_flickr_response?

# flickr_mountains_result=get_flickr_data("mountains")
# print(flickr_mountains_result)

## Remember to comment this out later if it makes your output messy. This is a good test, but it's not necessary for your recommender!


## You'll need another function to complete this tag recommender.
## You also know about another endpoint of the Flickr API: Photo Info.
## https://www.flickr.com/services/api/flickr.photos.getInfo.html

## That documentation shows that you need a photo id, and a flickr key, to get info about a photo that is public, and also need to change the value of the method query parameter (that specifies which endpoint is being accessed!). So if you were to make a request to that endpoint of the API, you could get a response about each of these photos. You will be needing to do just that.

## TODO: Define a function called get_photo_data that takes 1 parameter: a photo id.

def get_photo_data(id):
    baseurl="https://api.flickr.com/services/rest/"
    params_d={}
    params_d["api_key"]=FLICKR_KEY
    params_d["photo_id"]=id
    params_d["tag_mode"]="all"
    params_d["per_page"] = 1
    params_d["method"] = "flickr.photos.getInfo"
    params_d["format"] = "json"
    params_d["media"] = "photos"
    unique_ident=params_unique_combination(baseurl,params_d)
    if unique_ident in _cache_diction:
        return _cache_diction[unique_ident]
    else:
        resp = requests.get(baseurl, params_d)
        _cache_diction[unique_ident] = json.loads(resp.text[14:-1])
        dumped_json_cache = json.dumps(_cache_diction)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return _cache_diction[unique_ident]



## It should have a similar structure to the get_flickr_data function you wrote in problem 6, but use different query parameters, of course.

## This function should cache data (in the same cache file! You don't need to change anything except for writing this brand new function).

## The get_photo_data function should return a complex dictionary that represents information about 1 photo on Flickr.

## Recommended TODO: Make an invocation to this function using one of the photo IDs from the data you've already gotten, just to see if it works.
## Make sure to comment out the the code after you try it out, since the result will be messy and confusing for the rest of your work here!

# print(get_photo_data("44448418044"))


##########################
## Part 2: Problem-Solving
##########################

## Now that you've practiced with the data and set up function definitions, now you'll need to invoke those functions AND write some code to build your tag recommender.

## Some of these steps will require more creativity on your part than others.

## Initially, you'll build this tag recommender as if you are recommending tags for photos based on the photo search "ocean". However, in the next part, you'll be editing some code in order to run your tag recommender program with ANY search.

## TODO: Invoke your get_flickr_data function on the term "ocean", with 50 results.
def sort_photo(name):
    ocean=get_flickr_data(name)

## TODO: From the result of the above function call, create a list of photo IDs and save it in a variable called photo_ids.
    photo_ids=[]
    for i in ocean["photos"]["photo"]:
        photo_ids.append(i["id"])
# print(photo_ids)



## TODO: Invoke your get_photo_data function on each ID in the photo_ids list, and accumulate a list of dictionaries, where each dictionary represents one photo.
    new_lst=[]
    for i in photo_ids:
        new_lst.append(get_photo_data(i))



## TODO: Using this list of dictionaries -- remember, each dictionary in this list represents one photo -- accumulate a count dictionary of ALL the tags used in ALL fifty of those photos, wherein the keys are the strings representing the tags, and their associated values are the number of times they appeared in the data (the list of dictionaries). This accumulated dictionary should be saved in a variable called tags_count.
    tags_count={}
    for item in new_lst:
        for i in item["photo"]["tags"]["tag"]:
            tag=i["_content"]
            if tag not in tags_count.keys():
                tags_count[tag]=1
            else:
                tags_count[tag]+=1
# print(tags_count)






## NOTE: It will be useful to refer back to your preparation work with sample_photo_rep for accessing tags in each photo!
## Careful about iteration... this is tricky! Go slow and make plans step by step, and then translate your ideas into code.

## NOTE: If any of those photos got deleted at some point, then this dictionary won't have useful data in it! You must set up your code in such a way that this is handled gracefully. So, for example, if one of the dictionaries in your list is {"error": "did not work"} or {102:"No"} or ANYTHING without the data you expect, your code will not break and will simply go on to the next dictionary to add its data to your accumulation.
### (Your code must account for ALL valid dictionaries in the list, and not stop upon the first problem dictionary you encounter.)

## TODO: Sort the tags in this count dictionary you accumulated by the number of times they have been seen among the data. You should find the top 5 -- NOT including the original thing you searched for! (e.g. if you originally searched on Flickr for "ocean", the tag "ocean" should NOT appear among your result top 5.)

    sor_tag=sorted(tags_count,key=lambda x: (-tags_count[x],x))
    sor_tag=sor_tag[1:6]
    return sor_tag
# print(sor_tag)

# print(sort_photo("ocean"))


## Ties should be broken alphabetically. (So if "apple" and "zoo" are tied for fifth place, among the top 5, you should ultimately see "apple" but not "zoo".) Since you are using the _content key and not the raw key, you should not see any variation in capitalization among the tags data!
## These top five tags are recommendations of what other tags you might like looking through on Flickr, if you like, e.g. photos that have the "ocean" tag.


##########################
## Part 3: Editing
##########################

## Now that you've built the bones of your program, you'll be editing it in the following ways. Remember, you've already done the hard work here -- in this portion you should be EDITING the code you wrote above to make this program work clearly and neatly.

## - TODO: Go back through your code and make sure you are not printing out anything you used for debugging. Don't delete it -- just comment it out.

## - TODO: Notice how, at the beginning of this file, you're given some provided code that assigns a value to a variable called search_term in a certain situation. This allows you to run this program as follows, with a command line argument, at the command prompt:

# python SI508_F18_project1.py mountains
# python SI508_F18_project1.py sunset
# python SI508_F18_project1.py farms
# python SI508_F18_project1.py "harry potter"

## ...and so on. The first example searches for mountains, the second for sunset, the third for farms, the fourth for harry potter etc. This comes from the variable search_term. (Note that a term with a space in it must be in quotes!)

## - TODO: Edit your program here so that it does print a couple more things.

get_flickr_data(search_input)
sor_tag = sort_photo(search_input)
print("You just searched for tag recommendations like {}...".format(search_input))
## - First, after you've run the program, it should print for the user to see: "You just searched for tag recommendations like [YOUR ORIGINAL SEARCH]..."
## For example, perhaps:
## You just searched for tag recommendations like ocean... (if you had run python SI508_F18_project1.py ocean)
## OR
## You just searched for tag recommendations like farms... (if you had run python SI508_F18_project1.py farms)

## This requires very little work -- just adding a print statement with the right variable! It does require making sure you understand what's happening in your code, but if you do, it can take less than ten seconds.
## (So: Don't spend time problem-solving this -- there's not much problem to solve -- instead, spend time talking through the code and asking questions so that it makes sense if you are confused! Confused is normal; talking through it is important.)

## - TODO: Add iteration and print statements at the very end of the program so that it prints out the 5 tag recommendations clearly, like so:

print("\"\"")
if len(sor_tag)==5:
    print("You searched for \"{}\". Your Flickr tag recommendations are:\n-{}\n-{}\n-{}\n-{}\n-{}".format(search_input,sor_tag[0],sor_tag[1],sor_tag[2],sor_tag[3],sor_tag[4]))

if len(sor_tag)<5 and len(sor_tag)>0:
    print("You searched for \"ocean\". Your Flickr tag recommendations are:")
    for i in sor_tag:
        print("-{}".format(i))
if len(sor_tag)==0:
    print("You searched for \"{}\". Unfortunately, there are no recommendations for this search! Try something else!".format(search_input))
print("\"\"")

# # """
# # You searched for "ocean". Your Flickr tag recommendations are:
# # - sea creatures
# # - beach
# # - shells
# # - water
# # - waves
# # """
# ### e.g. the term that was searched via the command line should show up, and each of the top 5 tags should also be listed like so.
# ### HINT: String formatting will be super helpful here!

# ## - TODO: If there are FEWER than five tags that appear BESIDES the original search, but, say, 1 or 3 or 4 can still be sorted, the output should be like so:

# """
# You searched for "ocean". Your Flickr tag recommendations are:
# - sea creatures
# - beach
# - shells

# There are fewer than 5 recommendations. Try searching for something else!
# """

# ## - And if there are ZERO tags that appear with the search, like so:

# """
# You searched for "ocean". Unfortunately, there are no recommendations for this search! Try something else!
# """

# ## You may certainly copy and paste these directly, though of course the first two examples will require some editing to work for any real situation.

# ## Be careful that your recommendations do NOT include the original search!