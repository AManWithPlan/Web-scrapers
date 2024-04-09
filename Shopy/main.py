import math
import os
import requests
from bs4 import BeautifulSoup
import json
import time
import random
import numpy as np
# from discord_webhook import DiscordWebhook

def DiscordWebhook():
    pass

from dotenv import load_dotenv


load_dotenv()
mainWebHookUrl = os.getenv("mainWebHookUrl")
logWebHookUrl = os.getenv("logWebHookUrl")

czcPages = [0, 27, 54, 81]
datSorting = ['', '/filter/o:3', '/filter/o:9']
czcURL = random.choice(["https://www.czc.cz{}?q-first={}&dostupnost=skladem&stav-zbozi=nove&stitky=garance-skvele-ceny", "https://www.czc.cz{}?q-first={}&dostupnost=skladem&stav-zbozi=nove"])
# czcURL = "https://www.czc.cz{}?q-first={}&dostupnost=skladem&stav-zbozi=nove&stitky=garance-skvele-ceny"
alzaURL = "https://www.alza.cz{}#f&availabilityFilterValue=1&cst=1&cud=0&pg={}&pn={}&prod="
datURL = "https://www.datart.cz{}{}?limit=48"
failed = 0
checked = 0
faily = ""
slevy = []

dbCzc = {}
dbAlza = {}
dbDat = {}
dbMount = {}
prdel = 'nic'
remove = ''

AzlaHeaders = {
    'authority': 'www.alza.cz',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^^',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
}

AzlaCookies = {
}

with open("czc.json", "r") as read_file:
    dbCzc = json.load(read_file)
with open("azla2.json", "r") as read_file:
    dbAlza = json.load(read_file)
with open("dat.json", "r") as read_file:
    dbDat = json.load(read_file)
# with open("mount.json", "r") as read_file:
#     dbMount = json.load(read_file)


def send(msg, target):
    print(msg)
    if target == 'main':
        target = mainWebHookUrl
    elif target == 'log':
        target = logWebHookUrl
    i = 0
    while len(msg) - i*2000 > 0:
        webhook = DiscordWebhook(url=target, content=msg[i*2000:(i+1)*2000])
        response = webhook.execute()
        i += 1


def filler():
    temp = 1 + random.random() * 3
    # print('time.sleep', temp)
    time.sleep(temp)


def process(URL):
    print(URL, 'ok')


def checkPrice(name, price, oldPrice, supply, link):
    global checked, slevy
    checked += 1
    # text = "Dropnula sleva na {} za {}, místo {}, {}\n {}".format(
    #     name, price, oldPrice, supply, link)
    if price < 0.35 * oldPrice or (price < 0.7 * oldPrice and price < oldPrice - 500) or (price < oldPrice - 5000 and price < 0.8 * oldPrice):
        # if oldPrice - price > 250:
        #     text = "@everyone @slevaEnjoyers\nDropnula sleva na {} za {}, místo {}, {}\n {}".format(
        #         name, price, oldPrice, supply, link)
        # else:
        #     text = "@ everyone @slevaEnjoyers\nDropnula sleva na {} za {}, místo {}, {}\n {}".format(
        #         name, price, oldPrice, supply, link)

        # send(text, 'main')
        slevy.append([name, price, oldPrice, supply, link, price/oldPrice])
        # print(text)
    # if link[:21] == 'https://www.datart.cz':
    #     print(supply, link)


def generateCzcUrls(names):
    ret = []
    blacklist = ['/plysaci-geekultura/produkty', '/susene-ovoce-a-orechy/produkty', '/napoje/produkty', '/mixit/produkty', '/susene-ovoce-a-orechy/produkty', '/mixit/produkty', '/rozbalene-a-pouzite-zbozi/produkty', '/akcni-nabidky-fashion/produkty', '/abystyle-fashion/produkty', '/philips-hue-chytra-domacnost/produkty', '/lotr-czc-lab/produkty', '/abystyle-geekultura/produkty', '/game-of-thrones-czc-lab/produkty', '/czc-fashion/produkty', '/asus-rog-fashion/produkty', '/godlike-a-alchemistr-chutovky/produkty', '/18-plus-drogerie/produkty', '/chytre-zdravotni-hodinky/produkty', '/assassin-s-creed-czc-lab/produkty', '/nutrend-potravinove-doplnky/produkty', '/vedomostni-hry-zabava/produkty', '/smart-zubni-hygiena/produkty', '/kase-a-musli-zdrava-vyziva-a-doplnky-stravy/produkty', '/vysavace-smart-zarizeni/produkty', '/samsung-komponenty/produkty', '/ergonomie/produkty', '/oxymetry-zdravi/produkty', '/marvel-komiksy/produkty', '/dychaci-trenazery-zdravi/produkty', '/elektronicka-evidence-trzeb/produkty', '/obuv-fashion/produkty', '/mobilni-telefony-samsung/produkty', '/svetla-a-lampicky/produkty', '/tp-link-omada-cloudove-reseni/produkty', '/dezinfekcni-gely/produkty', '/lahve-hrnky-termosky-zdravi/produkty', '/robotime-zabava/produkty', '/kalhoty-fashion/produkty', '/rohozky-geekultura/produkty', '/xbox-series-gaming/produkty', '/grizly-mixit-a-zdrava-vyziva/produkty', '/akcni-nabidky-chutovky/produkty', '/polstare-zdravi/produkty', '/zvlhcovac-vzduchu-smart-spotrebice/produkty', '/venkovni-hry-zabava/produkty', '/ctecky-e-knih-a-digitalni-zapisniky/produkty', '/mechaniky/produkty', '/hrani-her-nejoblibenejsi-zajmy/produkty', '/virtualni-realita/produkty', '/svicky-relaxace-a-difuzery/produkty', '/lotr/produkty', '/elektrostimulatory-zdravi/produkty', '/modni-doplnky-fashion/produkty', '/energeticke-napoje/produkty', '/doplnky-stravy/produkty', '/intel-komponenty/produkty', '/novinky-zdrava-vyziva-a-doplnky-stravy/produkty', '/software/produkty', '/servery-servery-a-datova-uloziste/produkty', '/geek-tipy/produkty', '/skladove-systemy/produkty', '/procesory/produkty', '/software-microsoft/produkty', '/playstation-5-gaming/produkty', '/zdrave-mlsani/produkty', '/extra-sleva/produkty', '/rexhry-spolecenske-hry/produkty', '/mindok-spolecenske-hry/produkty', '/hry-pro-pc-gaming/produkty', '/space-protein/produkty', '/pece-o-plet-drogerie/produkty', '/parfemy-drogerie/produkty', '/rozvadece-servery/produkty', '/konfigurovatelne-nas-nas-servery/produkty', '/hubelino-zabava/produkty', '/puzzle-zabava/produkty', '/svetelne-terapeuticke-lampy-zdravi/produkty', '/bombus/produkty', '/monitory-spanku-zdravi/produkty', '/18plus-lab/produkty', '/teplomery/produkty', '/tlakomery-zdravi/produkty', '/iron-studios-figurky/produkty', '/hracky-zabava/produkty', '/hlasovy-asistent-smart-domacnost/produkty', '/pedro/produkty', '/geek-prislusenstvi-geekultura/produkty', '/vlasova-kosmetika/produkty', '/bundy-fashion/produkty', '/sportovni-sluchatka-a-mikrofony/produkty', '/dc-komiksy/produkty', '/respiratory-a-rousky/produkty', '/adc-blackfire-spolecenske-hry/produkty', '/mobilni-telefony-honor/produkty', '/zviratka-nejoblibenejsi-zajmy/produkty', '/realme-mobilni-telefony/produkty', '/gps-navigace/produkty', '/odvlhcovace-velke-spotrebice/produkty', '/small-foot-zabava/produkty', '/kancelarska-technika/produkty', '/mikiny-a-svetry-fashion/produkty', '/adventni-kalendare/produkty', '/stolni-hry-stolni-a-venkovni-hry/produkty', '/piatnik-spolecenske-hry/produkty', '/herni-tematika-komiksy/produkty', '/princezny-nejoblibenejsi-zajmy/produkty', '/komiksove-serie/produkty', '/herni-konzole-gaming/produkty', '/skolni-pomucky-pro-male-hrace/produkty', '/videokamery/produkty', '/se-zdravotnymi-funkcemi-chytre-hodinky/produkty', '/sezeni-u-pocitace-zdrava-kancelar/produkty', '/masazni-pistole-zdravi/produkty', '/penezenky-fashion/produkty', '/nas-servery/produkty', '/domaci-testy-zdravi/produkty', '/osobni-vahy-zdravi/produkty', '/czech-virus/produkty', '/fotovoltaika/produkty', '/cisticky-vzduchu-smart-spotrebice/produkty', '/video/produkty', '/slane-snacky/produkty', '/party-hry-zabava/produkty', '/xiaomi-mobilni-telefony/produkty', '/party-hry-spolecenske-hry/produkty', '/komiksy-pro-deti/produkty', '/zdrave-napoje/produkty', '/game-of-thrones/produkty', '/novinky-a-specialni-lego/produkty', '/fitness-naramky/produkty', '/metalearth-iconx-stavebnice/produkty', '/tycinky-mixit-a-zdrava-vyziva/produkty', '/lego-pro-dospele/produkty', '/sport/produkty', '/vedomostni-hry-spolecenske-hry/produkty', '/relaxacni-sluchatka-chytra-domacnost/produkty', '/knihy-pro-osobni-rozvoj-knihy/produkty', '/albi-spolecenske-hry/produkty', '/graficke-karty/produkty', '/telekomunikace-a-kamery/produkty', '/iphone-mobilni-telefony/produkty', '/super-hrdinove-nejoblibenejsi-zajmy/produkty', '/sportovni-chytre-hodinky/produkty', '/kulickove-drahy/produkty', '/knizni-serie-knihy/produkty', '/uv-lampy-zdravi/produkty', '/susene-maso/produkty', '/poco-mobilni-telefony/produkty', '/darkove-sady-drogerie/produkty', '/glukometry-zdravi/produkty', '/opticke-site/produkty', '/oshee-napoje/produkty']
    for name in names:
        if name in blacklist:
            url = czcURL.format(name, 0)
            ret.append(url)
        else:
            for page in czcPages:
                url = czcURL.format(name, page)
                ret.append(url)
    return ret


def getCzcCategories():
    page = requests.get("https://www.czc.cz/")
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("div", {"class": "main-menu__category"})
    ret = []
    for result in results:
        temp = result.find("a")
        if temp:
            href = temp.attrs['href']
            if href[-9:] == '/produkty':
                ret.append(href)
    # blacklist = ['/herni-konzole-gaming/produkty', '/konfigurovatelne-nas-nas-servery/produkty', '/servery-servery-a-datova-uloziste/produkty', '/czc-fashion/produkty', '/svetelne-terapeuticke-lampy-zdravi/produkty', '/monitory-spanku-zdravi/produkty', '/svetelne-terapeuticke-lampy-zdravi/produkty', '/polstare-zdravi/produkty', '/dychaci-trenazery-zdravi/produkty', '/dezinfekcni-gely/produkty', '/respiratory-a-rousky/produkty', ]
    # for t in blacklist:
    #     if t in ret:
    #         ret.remove(t)
    #     else:
    #         print("blacklist not in czc list: {}".format(t))
    return generateCzcUrls(ret[1:])


def processCzc(URL):
    for i in range(3):
        try:
            page = requests.get(URL)
            break
        except Exception as e:
            print(e)
            if i == 2:
                text = "<@313378412494585856>\nError in czc: {}\n{}".format(e, URL)
                send(text, 'log')
                return
            text = "Error in czc: {}\n{}".format(e, URL)
            send(text, 'log')
            time.sleep(6 + random.random() * 3)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="tiles")
    if results is None:
        if URL[-37] != '0' and URL[-63] != '0':
            global remove
            remove += "\nczc- {} {}".format(URL[-63], URL)
        return
        # log = DiscordWebhook(
        #     url=logWebHookUrl,)
        # content="<@313378412494585856>\nNo results for: {}".format(URL))
        # hook = log.execute()
    articles = results.find_all("div", class_="new-tile")

    for article in articles:
        temp = json.loads(article.attrs["data-ga-impression"])
        price = temp["price"]
        name = temp["name"]
        id = temp["id"]
        link = 'https://www.czc.cz' + article.contents[5].attrs["href"]
        if supply := article.find("span", class_="on-stock"):
            supply = ' '.join(supply.parent.contents[1].split())
        else:
            supply = "skladem <:ShrugMan:973117676748668951> kusů"

        oldPrice = dbCzc.get(id)
        if oldPrice is not None:
            checkPrice(name, price, oldPrice, supply, link)
        dbCzc[id] = price


def generateAlzaUrls(names):
    ret = []
    basic = ['/18844551-v12363.htm', '/levne-sport/sporttestery-na-behani/18867022.htm', ]
    for name in names:
        for page in range(1, 2):
            if name in basic:
                url = alzaURL.format(name, page, 0)
                ret.append(url)
            else:
                for sort in [0, 1]:
                    name2 = name
                    if sort == 7:
                        name2 = "/nejprodavanejsi-nejlepsi-" + name[1:]
                    elif sort == 1:
                        name2 = "/levne-" + name[1:]
                    url = alzaURL.format(name2, page, sort)
                    ret.append(url)
    return ret


def getAlzaCategories():
    page = requests.get("https://www.alza.cz", headers=AzlaHeaders)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("ul", {"class": "fmenu"})
    subs = results.find_all("a", {"class": "catLink"})
    list = set()
    interesting = ['/mobily/18843445.htm', '/notebooky/18842920.htm', '/pocitace/18852653.htm',
                   '/komponenty/18852654.htm', '/lcd-monitory/18842948.htm', '/prislusenstvi/18861668.htm',
                   '/sitove-prvky/18842916.htm', '/tiskarny-a-skenery/18851089.htm', '/televize/18849604.htm',
                   '/sluchatka/18843602.htm', '/priprava-jidla/18879690.htm', '/vysavace/18850975.htm',
                   '/spotrebice-na-pripravu-napoju/18850364.htm', '/kuchynske-potreby/18858834.htm',
                   '/hobby/nabytek/18871096.htm', '/elektroinstalace/18875780.htm',
                   '/smarthome-inteligentni-domacnost/18855843.htm', '/hobby/naradi/18858962.htm',
                   '/hobby/vybaveni-dilny/18862227.htm', '/alkohol/18872276.htm', '/nealkoholicke-napoje/18881193.htm',
                   '/sladkosti/18876397.htm', '/trvanlive-potraviny/18876335.htm',
                   '/smarthealth-chytre-zdravi/18855195.htm', '/pristroje-pro-peci-o-zdravi/18850366.htm', ]
    for t in subs:
        if t.attrs['href'] in interesting:
            list.update([t.attrs['href'] for t in [r for r in t.next_siblings][1].find_all("a", {"class": "subCat"})])
        else:
            # if random.randint(0, 10) < 3:
                list.add(t.attrs['href'])
    blacklist = ['/levne-darkova-baleni-alkoholu/18882368.htm', '/krasa-a-zdravi/18859693.htm', '/priprava-jidla/18879690.htm', '/media/knihy/18863041.htm', '/pet/chovatelske-potreby-pro-mala-zvirata/18884996.htm', '/pet/akvaristika/18895207.htm', '/pet/potreby-pro-kocky/18869016.htm', '/poukazy-sluzby/18848934.htm', '/pet/chovatelske-potreby-pro-ptaky/18899967.htm', '/hracky/vybava-pro-miminko/18855800.htm', '/media/audioknihy/18854370.htm', '/media/elektronicke-knihy/18853710.htm', '/pet/potreby-pro-psy/18869014.htm', '/pet/teraristika/18895221.htm', '/media/hudba-a-filmy/18881807.htm', '/maxi/vybava-pro-miminko/18855800.htm', '/bytovy-textil/18885735.htm', '/hobby/kuchyne/18889788.htm', '/pro-firmy', '/hobby/zahradni-nabytek/18855859.htm', '/hobby/bytovy-textil/18885735.htm', '/hobby/ulozne-prostory/18877953.htm', '/hobby/koupelna-a-wc/18884867.htm', '/vykup-mobilu/18894351.htm', '/hobby/jidelny/18884892.htm', '/zdravi/18874562.htm', '/hobby/loznice/18884810.htm', '/sestaveni-pc', '/hobby/obyvaci-pokoje/18884187.htm', '/18842948-e7.htm', '/stolovani/18858836.htm', '/ventilatory-a-chlazeni/18850974.htm', '/hobby/predsine-a-satny/18884803.htm', ]
    for t in blacklist:
        if t in list:
            list.remove(t)
        else:
            print("blacklist not in alza list: {}".format(t))
    # print("Alza categories: {}".format(len(list)))
    return generateAlzaUrls(list)


def processAlza(URL):
    results = None
    for i in range(5):
        try:
            page = requests.get(URL, headers=AzlaHeaders)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find("div", id="boxes")
            if results is None:
                with open("output1.html", "w", encoding="utf-8") as file:
                    file.write(str(soup))
                raise Exception("No results")
            break
        except Exception as e:
            print(e)
            if i == 4:
                text = "<@313378412494585856>\nError in alza: {}\n{}".format(e, URL)
                # send(text, 'log')
                print(text)
                return
            text = "Error in alza: {}\n{}".format(e, URL)
            # send(text, 'log')
            time.sleep(3 + random.random() * 3)

    if results is None:
        text = "<@313378412494585856>\nNo results for: {}".format(URL)
        # send(text, 'log')
        print(text)
        return

    # print(len(list(results.children)))
    for child in results.children:
        if child != '\n':
            article = child.find("a")
            if article:
                price = 999999
                name = "name"
                supply = "supply"
                link = 'link'
                try:
                    price = float(article.attrs["data-impression-metric2"].replace(',', '.'))
                    name = article.attrs["data-impression-name"]
                    supply = article.attrs["data-impression-dimension13"]
                    link = 'https://www.alza.cz/' + article.attrs["href"]
                    # print("Azala nasla:", price, name, supply, link)

                    oldPrice = dbAlza.get(link)
                    if oldPrice is not None:
                        checkPrice(name, price, oldPrice, supply, link)
                    dbAlza[name] = price
                except Exception as e:
                    oldPrice = dbAlza.get(link)
                    if oldPrice is not None:
                        checkPrice(name, price, oldPrice, supply, link)
                    global remove
                    remove += '\nazla- {}{}{}'.format(URL, name, e)
                    break


def generateDatUrls(names):
    ret = []
    for name in names:
        for sorting in datSorting:
            url = datURL.format(name, sorting)
            ret.append(url)
    return ret


def getDatCategories():
    page = requests.get("https://www.datart.cz/")
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("h3", {"class": "category-box-title"})
    ret = []
    noStrip = ['/susicky']
    for result in results:
        temp = result.find("a")
        if temp:
            href = temp.attrs['href']
            if href[-10:-5].isnumeric() and href[:-11] not in noStrip:
                # print(href, href[:-11])
                href = href[:-11] + href[-5:]
            ret.append(href)
    blacklist = ['/prislusenstvi-k-peci-o-zuby.html', '/komponenty.html', '/pece-o-zuby.html', '/skla-pro-mobilni-telefony.html', '/prislusenstvi-k-videokameram.html', '/herni-pocitace.html', '/herni-monitory.html', '/herni-sluchatka.html', '/herni-volanty.html', '/wi-fi-routery-a-komponenty.html', '/pece-o-ruce-a-nohy.html', '/notebooky-a-pc.html', '/chytra-domacnost.html', '/gamepady-pro-mobilni-telefony.html', '/kuchynske-vahy-krajece-a-mlynky.html', '/dtest-male-spotrebice.html', '/prislusenstvi-k-mobilnim-telefonum.html', '/meteostanice-digitalni-teplomery-hodiny-a-cas.html', '/vytapeni-a-chlazeni-domacnosti.html', '/baterie-a-nabijeni.html', '/gamepady-pro-konzole-a-pc.html', '/nintendo-konzole.html', '/virtualni-realita.html', '/elektricke-parni-a-fritovaci-hrnce.html', '/audio-na-doma.html', '/elektrovozitka.html', '/playstation-4.html', '/tv-prislusenstvi-k-televizorum.html', '/playstation-5.html', '/grily-topinkovace-sendvicovace.html', '/prislusenstvi-k-notebookum.html', '/prislusenstvi-k-fotoaparatum.html', '/prislusenstvi-k-domacim-spotrebicum.html', '/vysavace.html', '/sporaky.html', '/prislusenstvi-sluchatka.html', '/drony.html', '/zdravotni-pomucky.html', '/bazeny-a-virivky.html', '/pevne-a-ssd-disky.html', '/wifi-routery-a-komponenty.html', '/prislusenstvi.html', '/zarovky.html', '/chytre-hracky.html', '/kuchynske-a-domaci-potreby.html', '/xbox-series.html', '/prislusenstvi-k-tiskarnam.html', '/naradi-do-dilny.html', '/prislusenstvi-k-pc.html', '/technika-do-auta.html', '/kavovary.html', '/dtest-velke-spotrebice.html', '/hifi-komponenty.html', '/rychlovarne-konvice-napojove-automaty.html', '/zvlhcovace-odvhlcovace-cisticky-vzduchu-a-vune-do-bytu.html', '/odstavnovace-susicky-a-lisy-ovoce.html', '/zahradni-technika.html', '/ke-kavovarum.html', '/ukladani-dat.html', '/nositelna-elektronika.html', '/video.html', '/hracky.html', '/prislusenstvi-k-tabletum.html', '/vychytavky-do-kuchyne.html', '/jak-vybrat-kolobezku.html', '/tablety-a-ctecky-eknih.html', '/retro-spotrebice.html', '/satelitni-technika.html', '/herni-prislusenstvi.html', '/prislusenstvi-k-telefonum.html', '/foto-prislusenstvi-k-fotoaparatum.html', '/prislusenstvi-k-videokameram.html', '/mixery-roboty-mlynky.html', '/zvlhcovace-cisticky-vzduchu-a-vune-do-bytu.html', '/xbox-one.html', '/prislusenstvi-k-televizorum.html', '/vestavne-trouby-kavovary-a-zasuvky.html', '/auto-moto.html']

    # print(ret)
    for remove in blacklist:
        if remove in ret:
            ret.remove(remove)
        else:
            print("not found: {}".format(remove))

    whitelist = ['/pameti-ram.html', '/elektricke-zubni-kartacky.html', '/ustni-sprchy.html', '/smart-zubni-kartacky.html', '/elektronicke-zubni-kartacky-pro-deti.html', '/nahradni-hlavice-k-elektrickym-zubnim-kartackum.html', '/manualni-zubni-kartacky.html', '/audio-sluchatka.html', '/sady-rucniho-naradi.html', '/casovy-spinac.html', '/multibrusky.html', '/pily-lupinkove.html', '/odklepavace-na-kavu.html', '/drzaky-pro-mobilni-telefony-40130.html', '/vanocni-osvetleni.html', '/pily-okruzni.html', '/prislusenstvi-akumulatory-samostatne.html', '/adsl-vdsl-modemy.html', '/postrikovace.html', '/zvedaci-zarizeni.html', '/powerline.html', '/k-malym-spotrebicum.html', '/baterie.html', '/drazkovaci-frezy.html', '/ssd-disky.html', '/interni-disky.html', '/pily-ocasky.html', '/wifi-extender.html', '/externi-disky.html', '/postrikovace-37498.html', '/cisteni-pro-kuchynske-spotrebice.html', '/filtry-tukove.html', '/konvice-na-caj-a-kavu.html', '/powerbanky-externi-baterie.html', '/sklenice-na-kavu.html', '/dotykova-pera.html', '/priklopy.html', '/hobliky.html', '/konvicky-na-mleko.html', '/kavove-lzicky.html', '/foto-prislusenstvi-mobilni-telefony.html', '/vysokotlake-cistice-37474.html', '/filtry-uhlikove.html', '/zalozni-zdroje-a-prepetove-ochrany.html', '/apple-watch.html', '/prislusenstvi-fotoaparaty-objektivy.html', '/lasery.html', '/zavlazovaci-hodiny.html', '/ostatni-prislusenstvi-ke-sporakum.html', '/webkamery.html', '/vysavace-listi.html', '/klavesnice-pro-tablety.html', '/vertikutatory.html', '/nabijeci-kabely-stojanky-nositelna-elektronika.html', '/prislusenstvi-pro-monitory.html', '/kabely-pro-pc.html', '/k-zehleni.html', '/prislusenstvi-pro-instantni-fotoaparaty-a-fototiskarny.html', '/folie-na-tablety.html', '/autokompresory.html', '/prislusenstvi-pro-pily.html', '/gamepady-pro-mobilni-telefony-40173.html', '/pistole-lepici.html', '/plotostrihy.html', '/svitilny-do-dilny.html', '/prepetove-ochrany-k-tv.html', '/datove-uloziste-nas.html', '/razove-utahovaky.html', '/zasuvky.html', '/stavebni-radia.html', '/elektrocentraly.html', '/vrtacky-elektricke.html', '/prislusenstvi-k-ipadu.html', '/prislusenstvi-ke-kompresorum.html', '/vrtacky-akumulatorove.html', '/prislusenstvi-37475.html', '/tiskove-struny-pro-3d-tiskarny.html', '/cestovne-adaptery.html', '/pouzdra-pro-tablety.html', '/ostricky-na-pilove-retezy.html', '/konvice-na-caj-a-kavu.html', '/ostatni-osvetleni/1.html', '/pametove-karty.html', '/pokojove-anteny.html', '/chytre-hodinky.html', '/amazon-alexa-41311.html', '/rozdvojky.html', '/akumulatory-samostatne.html', '/powerbanky-externi-baterie.html', '/baterie-pro-notebooky.html', '/prislusenstvi-k-prackam-myckam-susickam.html', '/prislusenstvi-ke-kavovarum-ostatni.html', '/michadla.html', '/prislusenstvi-ke-cteckam-eknih.html', '/drevoobrabeci-stroje.html', '/brusky-kotoucove.html', '/prislusenstvi-pro-sponkovacky.html', '/kultivatory.html', '/prodluzovaci-privody.html', '/prislusenstvi-k-bazenum.html', '/pc-reproduktory.html', '/lampicky-a-svitilny.html', '/akumulatorove-sekacky.html', '/sprchy.html', '/pily-stolni.html', '/pily-pasove.html', '/stativy-pro-foto-a-video.html', '/ctecky-cipovych-karet.html', '/penice-mleka.html', '/dokovaci-stanice.html', '/herni-pocitace-39088.html', '/polarizacni-filtry.html', '/plechy.html', '/prislusenstvi-k-iphone.html', '/cerpadla.html', '/akumulatorove-nuzky-na-travu.html', '/autoprislusenstvi.html', '/mikrofony.html', '/predplacene-sim-karty-a-sady.html', '/prislusenstvi-37500.html', '/graficke-tablety.html', '/hevery.html', '/horni-frezy.html', '/google-home-41310.html', '/odvapnovace-kavovaru.html', '/hadice-a-boxy.html', '/baterie-pro-notebooky.html', '/mechaniky-cd-dvd-bd.html', '/pily-retezove.html', '/prislusenstvi-pametove-karty.html', '/prislusenstvi-pro-bezdratove-reproduktory.html', '/termosky.html', '/sponkovacky-37444.html', '/prislusenstvi-ostatni-prislusenstvi.html', '/prislusenstvi-prazdna-cd-media.html', '/drtice-vetvi.html', '/sporttestery.html', '/prislusenstvi-pro-horni-frezy.html', '/kvadrokoptery-drony-a-rc-modely.html', '/univerzalni-dalkova-ovladani-k-televizorum.html', '/chladici-podlozky-pod-notebook.html', '/stabilizatory-pro-mobilni-telefony.html', '/k-mikrovlnnym-troubam.html', '/zarovky-40113.html', '/brusky-vibracni.html', '/alternativni-tonery-naplne-a-cartridge-do-tiskaren.html', '/vypinace.html', '/vyhrivane-autopotahy.html', '/philips-hue.html', '/prislusenstvi-k-apple-watch.html', '/prislusenstvi-pro-macbook.html', '/prislusenstvi-kabely-pro-audio-video.html', '/napajeci-zdroje.html', '/usporadani-dilny.html', '/naplne-do-tiskaren.html', '/stojanky-na-kapsle.html', '/handsfree.html', '/usb-huby-a-doplnky.html', '/startovaci-boxy.html', '/strunove-sekacky.html', '/pripojovaci-material.html', '/rezacky-dlazdic.html', '/kapsle-kavovary.html', '/krovinorezy-37494.html', '/usb-sitove-adaptery.html', '/prislusenstvi-k-navigacim.html', '/sitova-karta.html', '/akumulatory-samostatne.html', '/roboticke-sekacky.html', '/prislusenstvi-k-bruskam.html', '/elektricke-sekacky.html', '/filtry-do-kavovaru.html', '/vodarny.html', '/stipace-drivi.html', '/el-nabijecky.html', '/herni-sluchatka-38595.html', '/napajeci-zdroje.html', '/prislusenstvi-37398.html', '/chladice-mleka.html', '/selfie-tyce.html', '/termohrnky.html', '/nabijecky-pro-mobilni-telefony.html', '/prislusenstvi-k-nositelne-elektronice.html', '/kladiva.html', '/ostatni-prislusenstvi-39440.html', '/volanty-pro-pc-37964.html', '/autovysavace-38839.html', '/lokatory.html', '/zebriky.html', '/fitness-naramky.html', '/nabijeci-stanice-a-solarni-panely.html', '/ostatni-prislusenstvi-37934.html', '/3d-pera.html', '/prislusenstvi-k-vysavacum.html', '/obrubniky.html', '/kompresory.html', '/autozarovky-37446.html', '/pametove-karty.html', '/cistici-prostredky-mobilni-telefony.html', '/switche.html', '/virivky.html', '/ostatni-prislusenstvi-k-chlazeni.html', '/hrnky-na-kavu.html', '/prislusenstvi-drony-a-kvadrakoptery.html', '/ostatni-prislusenstvi.html', '/rosty.html', '/wifi-routery.html', '/papiry-do-tiskaren-a-kopirek.html', '/termohrnky.html', '/konvicky-na-mleko.html', '/el-nabijecky.html', '/herni-bryle-k-pc.html', '/ip-kamery.html', '/minibrusky.html', '/odvetvovace.html', '/vretenove-sekacky.html', '/drzaky-pro-tv.html', '/pily-pokosove.html', '/prislusenstvi-pro-gramofony.html', '/prislusenstvi-prazdna-blu-ray-media.html', '/potrubi.html', '/prislusenstvi-k-merici-technice.html', '/cistici-prostredky-k-televizim.html', '/prislusenstvi-37433.html', '/pily-primocare.html', '/redukce-a-adaptery.html', '/pechovadlo-na-kavu.html', '/k-domacim-pekarnam.html', '/prumyslove-vysavace.html', '/ctecky-pametovych-karet.html', '/filtry-na-vodu-39429.html', '/bazeny.html', '/obrazove-a-foto-valce.html', '/cestovni-redukce.html', '/vrtacky-stojanove.html', '/zanovni-nositelna-elektronika.html', '/prislusenstvi-ke-sportovnim-kameram.html', '/brusky-excentricke.html', '/tv-karty.html', '/lampicky.html', '/apple-homekit-41309.html', '/datove-kabely-a-dokovaci-stanice.html', '/izolacni-pasky.html', '/brasny-a-pouzdra-pro-fotoaparaty.html', '/herni-bryle-k-pc.html', '/auto-prenosne-chladnicky.html', '/vysuvy.html', '/pristupovy-bod-ap.html', '/ke-kuchynskym-robotum.html', '/filtry-a-pohlcovace-pachu.html', '/prislusenstvi-pro-varne-desky.html', '/rozmetadla-hnojiv.html', '/datove-uloziste-nas.html', '/lte-modemy.html', '/brusky-pasove.html', '/gamepady-40171.html', '/drzaky-k-tabletum.html', '/menice-napeti.html', '/svarecky.html', '/mysi.html', '/el-menice-napeti.html', '/prislusenstvi-fotoaparaty-blesky.html', '/prislusenstvi-k-videokameram-akumulatory.html', '/sroubovaky-akumulatorove.html', '/prislusenstvi-fotoaparaty-ostatni.html', '/klavesnice.html', '/prislusenstvi-37495.html', '/termokonvice.html', '/led-pasky.html', '/merice.html', '/baterie-a-nabijeni-39417.html', '/prislusenstvi-prazdna-dvd-media.html', '/startovaci-boxy.html', '/pajky.html', '/brasny-a-batohy-na-notebooky-40174.html', '/brusky-uhlove.html', '/prislusenstvi-k-3d-a-smart-televizorum.html', '/nadobi-mlynky-na-kavu.html', '/pistole-horkovzdusne.html', '/motorove-sekacky.html', '/herni-monitory-38707.html']

    for add in whitelist:
        ret.append(add)
    return generateDatUrls(ret)


def processDat(URL):
    for i in range(3):
        try:
            page = requests.get(URL)
            break
        except Exception as e:
            print(e)
            if i == 2:
                text = "<@313378412494585856>\nError in Datart: {}\n{}".format(e, URL)
                send(text, 'log')
                return
            text = "Error in Datart: {}\n{}".format(e, URL)
            send(text, 'log')
            time.sleep(6 + random.random() * 3)

    soup = BeautifulSoup(page.content, "html.parser")
    soup.find_all("h3", {"class": "category-box-title"})
    results = soup.find("div", {"class": "product-box-list"})

    if results is None:
        # log = DiscordWebhook(
        # 	url=logWebHookUrl,
        # 	content="<@313378412494585856>\nNo results for: {}".format(URL))
        # hook = log.execute()


        results = soup.find("div", {"class": "category-tree-box-list"})
        articles = results.find_all("a", {})
        builder = ""
        for a in articles:
            temp = a.attrs['href']
            if temp[-10:-5].isnumeric():
                temp = (temp[:-11] + temp[-5:])

            builder += '\n+ ' + temp
        print('\ndat- {}{}'.format(URL, builder))
        global remove
        remove += 'dat- {}{}'.format(URL, builder)
        return

    articles = results.find_all("div", {"class": "product-box"})
    for article in articles:
        temp = article.find("h3", {"class": "item-title"})
        if not temp:
            # print("skipped", article)
            continue
        temp = temp.contents[0].attrs
        price = float(article.find("div", {"class": "item-price"}).attrs['data-product-price'])
        name = temp['data-lb-name']
        if article.find("div", {"class": "item-delivery"}).text != "\n":
            supply = article.find("div", {"class": "item-delivery"}).text.split()[0]
        else:
            supply = "???"
        link = 'https://www.datart.cz'+temp['href']
        id = article.find("button", {"class": "btn btn-link btn-compare"}).attrs['id'].split('-')[1]

        if supply != 'Není':
            oldPrice = dbDat.get(id)
            if oldPrice is not None:
                checkPrice(name, price, oldPrice, supply, link)
        dbDat[id] = price


def generateMountUrls(names):
    pass


def getMountCategories():
    ret = []
    blacklist = ['https://www.mountfield.cz/sezonni-dekorace', 'https://bazeny.mountfield.cz/', 'https://www.mountfield.cz/zrychleni-elektrokola', 'https://www.mountfield.cz/bazenove-prislusenstvi', 'https://www.mountfield.cz/elektrokola-s-motorem-bosch']
    page = requests.get("https://www.mountfield.cz/")
    soup = BeautifulSoup(page.content, "html.parser")
    bar = soup.find_all("div", {"class": "list-submenu__image"})
    for result in bar:
        if result != '\n':
            # print(result.contents[1].attrs['href'])
            category = result.contents[1].attrs['href']
            ret.append(category)

    for remove in blacklist:
        # print(remove)
        if remove in ret:
            ret.remove(remove)
        else:
            print("not found: {}".format(remove))
    return [*set(ret)]


def processMount(URL):
    for i in range(3):
        try:
            page = requests.get(URL)
            break
        except Exception as e:
            print(e)
            if i == 2:
                text = "<@313378412494585856>\nError in Mount: {}\n{}".format(e, URL)
                send(text, 'log')
                return
            text = "Error in Mount: {}\n{}".format(e, URL)
            send(text, 'log')
            time.sleep(6 + random.random() * 3)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", {"class": "list-products__in"}).contents[1].contents
    if results is None:
        text = "<@313378412494585856>\nNo results for: {}".format(URL)
        send(text, 'log')
        return

    for article in results:
        if article != '\n':
            temp = article.contents[1].contents[3].attrs
            link = temp['href']
            data = json.loads(temp['data-gtm'])['ecommerce']['click']['products'][0]
            price = data['priceWithTax']
            name = data['name']
            id = data['id']
            supply = data['availability']
            # print(name, price, supply, link)
            oldPrice = dbMount.get(id)
            if oldPrice is not None:
                checkPrice(name, price, oldPrice, supply, link)
            dbMount[id] = price


def main():
    global prdel
    text = "Scamování začalo z {}\n".format(os.getlogin())
    send(text, 'log')

    # try:
    #     alzaNames = getAlzaCategories()
    # except Exception as e:
    #     text = "Alza te zase blokla, stránka je v alza.html brouku \n{}\n".format(e)
    #     send(text, 'log')
    #     alzaNames = []
    #     page = requests.get("https://www.alza.cz", headers=AzlaHeaders)
    #     with open('alza.html', 'wb+') as f:
    #         f.write(page.content)
    # alzaNames = None
    czcNames = getCzcCategories()
    datNames = getDatCategories()
    # mountNames = getMountCategories()

    i = 0
    done = 0
    minWait = 2
    ins = [czcNames]  # ,
    fun = [processCzc]  #
    # ins = [datNames, ]
    # fun = [processDat, ]

    text = "Čeká mě {} stránek\n".format(sum(len(x) for x in ins))
    send(text, 'log')
    print(text)

    length = sum(len(j) for j in ins)
    cd = [0 for _ in ins]
    wait = [max((length / len(ins[j])), minWait) for j in range(len(ins))]
    order = np.argsort([len(j) for j in ins])[::-1]
    progress = [0 for _ in ins]

    print('Setup done')
    # print(wait)
    # print([len(j) for j in ins])

    while done < len(fun):
        if i % 100 == 0:
            print('done: {}/{}'.format(sum(progress), sum([len(j) for j in ins])))

        for j in order:
            if cd[j] <= i and progress[j] < len(ins[j]):
                URL = ins[j][progress[j]]
                try:
                    # print(URL)
                    prdel = fun[j], URL
                    fun[j](URL)
                except Exception as e:
                    text = "<@313378412494585856>\nError in: {}\n{}".format(URL, e)
                    send(text, 'log')
                    print("Error in: {}\n{}".format(URL, e))
                progress[j] += 1
                if progress[j] == len(ins[j])-1:
                    done += 1
                cd[j] = i + wait[j]
                break
        else:
            filler()
        i += 1

    # print(i)
    with open('czc.json', 'w') as convert_file:
        convert_file.write(json.dumps(dbCzc))
    with open('azla2.json', 'w') as convert_file:
        convert_file.write(json.dumps(dbAlza))
    with open('dat.json', 'w') as convert_file:
        convert_file.write(json.dumps(dbDat))
    # with open('mount.json', 'w') as convert_file:
    #     convert_file.write(json.dumps(dbMount))

    # send(slevy, 'main')
    if len(slevy) > 0:
        slevy.sort(key=lambda x: x[5])
        buider = "@ everyone @slevaEnjoyers\n"
        for s in slevy:
            name, price, oldPrice, supply, link, ratio = s
            text = "Dropnula sleva na {} za {}, místo {}, {}\n {}".format(
                name, price, oldPrice, supply, link)
            if len(buider) + len(text) > 2000:
                send(buider, 'main')
                buider = ""
            buider += text + "\n"

        send(buider, 'main')

    text = "Scamování skončilo, čeknul jsem {} z {} stránek\n{} produktů na Alze\n{} produktů na CZC\n{} produktů na Datartu\n{}".format(
            checked, length, len(dbAlza), len(dbCzc), len(dbDat), remove)
    send(text, 'log')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        text = "<@313378412494585856>\nError in main: {}\n{}".format(e, prdel)
        log = DiscordWebhook(url=logWebHookUrl, content=text)
        hook = log.execute()
        print(text)
        send(text, 'log')
        raise e
