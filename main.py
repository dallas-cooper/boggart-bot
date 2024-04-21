import datetime
import json
import praw
import random
import string
import time
import urllib


def respond_to_comments(listen_to_all = False):
    DAILY_RESPONSE_LIMIT = 3 # The maximum number of responses we will allow our bot to make each day
    RESPONSE_RATE = 10 # The amount of time, in seconds, that we should wait before posting another comment

    # Subreddits that our bot will listen to
    SUBREDDITS = [
        "Eldenring", 
        "EldenRingMemes"
    ]

    # Words that will trigger an unsolicited response from our bot
    TRIGGER_WORDS = [
        "BLACKGUARD", 
        "BOGGART", 
        "PRAWN", 
        "CRAB", 
        "RYA", 
        "DUNG EATER", 
        "MARIKA", 
        "TITS",
        "UNGRY",
        "TARNISHED"
    ]

    responseCount = 0 # A running total of the number of unsolicted responses that we have made
    closingDay = None # When the bot reaches its daily response limit, we use this to track the day that it happened


    # Build the subreddits string
    subreddits = ""
    for subreddit in SUBREDDITS:
        subreddits = subreddits + subreddit + "+"
    subreddits = subreddits.rstrip(subreddits[-1])
    if listen_to_all == True:
        subreddits = "all"

    reddit = praw.Reddit("boggart_bot") # Create our Reddit instance

    # Loop runs indefinitely
    while 1 + 1 == 2:
        for comment in reddit.subreddit(subreddits).stream.comments(skip_existing = True):
            # Skip our own comments
            if comment.author.name == "boggart_bot":
                continue
            
            # Solicited responses
            #
            if "Biggie Boggart gimme lore:" in comment.body:
                try:
                    loreItem = comment.body.split(":", 1)[1].strip()
                except:
                    loreItem = "NOTHING!!!"
                else:
                    loreItem = string.capwords(loreItem)
                finally:
                    post_lore(comment, loreItem)
            
            elif "Biggie Boggart gimme prawns" in comment.body or "Biggie Boggart gimme crabs" in comment.body:
                if "prawns" in comment.body:
                    post_prawn_or_crab(comment, "prawns")
                elif "crabs" in comment.body:
                    post_prawn_or_crab(comment, "crabs")
            
            elif "Biggie Boggart" in comment.body:
                post_quote(comment)

            # Unsolicited responses
            #
            elif responseCount < DAILY_RESPONSE_LIMIT:
                # Find all the trigger words within the user's comment
                matches = is_string_from_array_present(comment.body, TRIGGER_WORDS, convertToUpper = True, returnMatches = True)

                # If the user's comment contains any of our trigger words, reply with a quote
                if len(matches) > 0:
                    post_quote(comment, random.choice(matches))
                    responseCount = responseCount + 1

                    if responseCount >= DAILY_RESPONSE_LIMIT:
                        closingDay = datetime.date.today()

            elif responseCount >= DAILY_RESPONSE_LIMIT:
                if datetime.date.today() > closingDay:
                    responseCount = 0
                    closingDay = None

            # Wait for some time before posting another comment
            time.sleep(RESPONSE_RATE)

def post_lore(comment, loreItem):
    comment.reply(use_api(loreItem))

def post_prawn_or_crab(comment, prawnsOrCrabs):
    if prawnsOrCrabs == "prawns":
        comment.reply("🦐 🦐 🦐")
    elif prawnsOrCrabs == "crabs":
        comment.reply("🦀 🦀 🦀")

def post_quote(comment, triggerWord = ""):
    # Quotes that our bot will respond with
    QUOTES = [
        "MARIKA'S TITS, YOU MUST BE 'UNGRY!", # 0
        "WHAT ARE YOU LOOKIN' AT? YOU TRYING TO START SOMETHING, MATE?", # 1
        "OH PISS OFF, WHAT IS IT NOW?", # 2
        "ALRIGHT, MATE. WANT SOME MORE PRAWN, DO YA?", # 3
        "ALRIGHT, MATE. WANT SOME MORE CRAB, DO YA?", # 4
        "YOU WANT SOME OF ME PRAWN?", # 5
        "YOU WANT SOME OF ME CRAB?", # 6
        "I'M NOT IN LOVE WITH IT OR NOTHING", # 7
        "WHAT THE HELL IS WRONG WITH YOU? YOU TRYING TO START SOMETHING? PISS OFF! BEFORE I CRACK YOU IN 'ALF!", # 8
        "YOU'RE A SHREWD ONE, CHIEF!", # 9
        "FIRST, YOU HAND ME THE RUNES! AND DON'T TRY NOTHIN', NEITHER!", # 10
        "THINK YOU'RE BLOODY CLEVER, DO YA? THEN HOW ABOUT YOU PISS OFF! FORE I CRACK YOU IN 'ALF!!!", # 11
        "THIS BLOODY SWINE...", # 12
        "THIS BLOODY SWINE... DECIDED TO PLAY BALL NOW, 'AVE YOU?", # 13
        "YOU'LL BE WANTIN' THE NECKLACE, THEN?", # 14
        "ALRIGHT, WELL, SOD THE PARTICULARS OF THE MATTER, BUT IT AIN'T MY FAULT SHE'S STUPID ENOUGH TO GET DUPED, IS IT?", # 15
        "SHE AIN'T ALRIGHT, THAT ONE!", # 16
        "LUCKY SHE AIN'T DIED ON THE BLOODY ROADSIDE, I RECKON!", # 17
        "YOU'RE TARNISHED TOO, AIN'TCHA?", # 18
        "CAN YOU SEE IT THEN? THE GUIDANCE OF GRACE, I MEAN!", # 19
        "MAKES NO BLOODY SENSE ANYWAY, WHY SOME NO-NAME SHITHEAD LIKE ME SHOULD GET CALLED TO THE LANDS BETWEEN!!!", # 20
        "MAYBE SOMETHING WENT TITS UP WITH IT!", # 21
        "MAYBE... IT'S BEEN BROKE FOR A GOOD LONG TIME! THE ERDTREE, I'M SAYIN'!", # 22
        "YOU 'EARD OF THE DUNG EATER?", # 23
        "E'S A MADMAN, 'AS IT OUT FOR EVERYONE.", # 24
        "E'S A MADMAN, 'AS IT OUT FOR EVERYONE. CURSES 'EM. GOES 'ROUND IN THIS RANK ARMOUR, AN' ALL.", # 25
        "E'S A GOD-FORSAKEN MONSTER. NOT JUST SOME PETTY THUG LIKE ME.", # 26
        "E'S A KILLER! KILLS PEOPLE AND CURSES THEIR SOULS... DOES ALL SORTS OF SHIT TO THEIR CORPSES, TO KEEP 'EM CURSED, FOREVER!", # 27
        "I AIN'T SEEN NOTHIN' MORE DISGUSTIN' IN ALL MY YEARS. I AIN'T NEVER BEEN MORE SCARED, NEITHER.", # 28
        "FITTING BLOODY END, FOR A JUMPED UP LITTLE SHIT WITH BIG IDEAS...", # 29
        "HELP ME OUT, WOULD YA MATE...", # 30
        "I DON'T WANNA GET CURSED. JUST LET ME DIE...", # 31
        "WHAT'S YOUR BLINKIN' PROBLEM?", # 32
        "WHAT'S YOUR BLINKIN' PROBLEM? YOU DON'T MESS WITH BIG BOGGART, MATE!", # 33
        "THAT BITCH PUT YOU UP TO THIS, EH? DAMN IT! I'LL RIP YOU TO SHREDS!", # 34
        "NOT SCARED, ARE YA?", # 35
        "YOU FEEL THAT, EH? THAT'S THE FISTS OF BIG BOGGART!", # 36
        "GODDAMN IT. WHY AIN'T IT ME, WHY AIN'T IT EVER...", # 37
        "NEVER MET SOMEONE WITH A TASTE FOR PRAWNS I COULDN'T TRUST!", # 38
        "NEVER MET SOMEONE WITH A TASTE FOR CRAB I COULDN'T TRUST!", # 39
        "WE'D MAKE GOOD MATES, I RECKON. I'LL BE SEEING YA!", # 40
        "WE'VE GOT A REAL THING HERE, EH, AND IT'S ONLY GETTIN' BETTER!", # 41
        "MARIKA'S TITS!" # 42
    ]
        
    match triggerWord:
        case "BLACKGUARD" | "BOGGART":
            comment.reply(random.choice(QUOTES))
        case "PRAWN":
            comment.reply(QUOTES[random.choice([3, 5, 38])])
        case "CRAB":
            comment.reply(QUOTES[random.choice([4, 6, 39])])
        case "RYA":
            comment.reply(QUOTES[random.choice([14, 15, 16, 17, 34])])
        case "DUNG EATER":
            comment.reply(QUOTES[random.choice([23, 24, 25, 26, 27, 28, 31])])
        case "MARIKA" | "TITS" | "UNGRY":
            comment.reply(QUOTES[random.choice([0, 42])])
        case "TARNISHED":
            comment.reply(QUOTES[random.choice([18, 19])])
        case _:
            comment.reply(random.choice(QUOTES))

def curate_content(foo):
    raise NotImplementedError("CUSTOM ERROR: 'curate_content' has not been implemented!!!")

def post_git_gud_count(foo):
    raise NotImplementedError("CUSTOM ERROR: 'post_git_gud_count' has not been implemented!!!")

# Helper functions
#
#
def is_string_from_array_present(stringToTest, arrayToCheck, convertToUpper = False, returnMatches = False):
    matches = []

    # Convert the string to uppercase
    if convertToUpper == True:
        stringToTest = stringToTest.upper()

    # Check each string in the arrayToCheck against stringToTest
    for string in arrayToCheck:
        if string in stringToTest:
            matches.append(string)

    # Return either a bool or an array of matches
    if returnMatches == True:
        return matches
    else:
        return len(matches) > 0

def use_api(itemName):
    REQUEST_RATE = 1 # The amount of time, in seconds, we should wait before making another request to the API

    # API endpoints that can be accessed by our bot
    CATEGORIES = [
        "ammos",
        "armors",
        "ashes",
        "bosses",
        "classes",
        "creatures",
        "incantations",
        "items",
        "locations",
        "npcs",
        "shields",
        "sorceries",
        "spirits",
        "talismans",
        "weapons"
    ]

    for category in CATEGORIES:
        request = urllib.request.urlopen("https://eldenring.fanapis.com/api/" + category + "?limit=1000")
        response = json.loads(request.read())
        for thing in response["data"]:
            if thing["name"] == itemName:
                return thing["description"]
        time.sleep(REQUEST_RATE) 
    return "Sorry! I couldn't find that!"

def is_authenticated(instance):
    print(instance.user.me()) 

# Main
#
#
respond_to_comments()