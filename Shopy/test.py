import math
import requests
from bs4 import BeautifulSoup
import json
import time
import random
import numpy as np
from discord_webhook import DiscordWebhook


page = requests.get("https://www.mountfield.cz/")
soup = BeautifulSoup(page.content, "html.parser")
