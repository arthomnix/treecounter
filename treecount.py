# Go TeamTrees!
# TreeCounter 0.0.2 (Commented Version) by arthomnix 
from lxml import html
import requests
from pypercard import CardApp, Card

url = "https://teamtrees.org"

def grabData(d, f): # d = data_store, f = form_value
    # don't crash if there is no internet connection
    try:
        treepage = requests.get(url).content
        pagetree = html.fromstring(treepage) # 'pagetree' means the HTML tree of the page and has nothing to do with real trees.
        # Make a list of all the 'data-count' properties of div elements with a class of 'counter' and take the first item in the list.
        trees = pagetree.xpath('//div[@class="counter"]/@data-count')[0]
        # Store the number of trees in the data_store
        d['trees'] = str(trees)
        # Target = 20 million trees. Store remaining trees in the data_store
        d['remaining'] = str(20000000 - int(trees))
        return 'displayTrees'
    except:
        # go to the 'error' card if there is no internet
        return 'error'

AppCards = [
            # The first card has a very short auto-advance and just runs the grabData() function.
            Card("init", auto_advance=0.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001, auto_target=grabData, background="green"),
            # Displays trees planted and trees remaining, with a lot of extra BBcode. (Human readable: "Trees planted: {trees} Trees remaining: {remaining} Donate at teamtrees.org $1 = 1 tree
            # Reloads the 'init' card to get the latest number of trees every 2.5 seconds.
            Card("displayTrees", text="[font=assets/JFWilwod][size=80]Trees planted:[/size]\n[size=120]{trees}[/size]\n[size=55]Trees left to plant:[/size]\n[size=120]{remaining}[/size]\n[size=30]Donate at teamtrees[/font].[font=assets/JFWilwod]org\n[/font]$[font=assets/JFWilwod]1 [/font]=[font=assets/JFWilwod] 1 tree[/size][/font]", background="green", text_color="black", auto_advance=2.5, auto_target='init'),
            # The card that is displayed if there is an Internet error. Tries again after 5 seconds.
            Card("error", text="Error getting trees", background="red", auto_advance=5, auto_target='init')
]

# Run the app
app = CardApp(stack=AppCards)
app.run()
