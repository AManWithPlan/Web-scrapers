import requests
from bs4 import BeautifulSoup
import json
import time
import random
from discord_webhook import DiscordWebhook

import os
from dotenv import load_dotenv
load_dotenv()
mainWebHookUrl = os.getenv("mainWebHookUrl")
logWebHookUrl = os.getenv("logWebHookUrl")

# mainWebHookUrl = ""
# logWebHookUrl = ""


def main():
    log1 = DiscordWebhook(
        url=logWebHookUrl,
        content="Scamování CZC započíná")
    hook1 = log1.execute()
    failed = 0
    faily = ""
    db = {}
    with open("czc.json", "r") as read_file:
        db = json.load(read_file)
    czc = ["mobilni-telefony", "notebooky", "tablety", "prislusenstvi-mobilni-telefony", "prislusenstvi-tablety",
           "gps-navigace", "ctecky-e-knih-a-digitalni-zapisniky", "virtualni-realita", "pocitace",
           "prislusenstvi-pro-notebooky", "prislusenstvi_2", "pocitacove-vybaveni-a-doplnky", "disky",
           "rozsirujici-karty", "procesory", "graficke-karty", "skrine", "zakladni-desky", "operacni-pameti",
           "zdroje", "chladice", "prislusenstvi-digitalni-fotoaparaty", "prislusenstvi-videokamery",
           "prenosne-audio", "prislusenstvi-televize", "digitalni-fotoaparaty", "videokamery", "audio",
           "televize", "video", "reproduktory", "domacnost_3", "objektivy", "elektronika-do-auta",
           "sluchatka-a-mikrofony", "prijem-tv-signalu", "kancelarska-technika", "ergonomie", "projektory",
           "drzaky-a-stolky", "flash-disky", "sluchatka-a-mikrofony",
           "baterie-a-nabijecky-ostatni-prislusenstvi", "pametove-karty", "klavesnice", "tiskarny-a-naplne",
           "externi-disky", "mysi", "monitory", "vysavace-smart-zarizeni", "hlasovy-asistent-smart-domacnost",
           "fitness-naramky", "smart-zdravi", "sport", "drony", "chytre-hodinky", "chytra-domacnost",
           "zalozni-zdroje-a-prepetove-ochrany", "servery-servery-a-datova-uloziste", "nas-servery",
           "cloudove-reseni", "fotovoltaika", "bezpecnostni-kamerove-systemy", "sitove-prvky",
           "herni-zidle-a-stoly-herni-prislusenstvi-gaming", "herni-vybaveni-gaming", "herni-konzole-gaming", "lego-pro-dospele", "lego-technic"]
    # print(sorted(czc))

    pageRange = [0, 27, 54, 81]

    for category_name in czc:
        if db.get(category_name) is None:
            db[category_name] = {}
        category = db[category_name]
        # print(category_name)
        for page in pageRange:
            URL = "https://www.czc.cz/{}/produkty?q-first={}&dostupnost=skladem&stav-zbozi=nove&stitky=price-guarantee".format(
                category_name, page)
            for i in range(3):
                try:
                    page = requests.get(URL)
                except Exception as e:
                    print(e)
                    if i == 2:
                        log = DiscordWebhook(
                            url=logWebHookUrl,
                            content="<@313378412494585856>\nError in czc: {}\n{}".format(e, URL))
                        hook = log.execute()
                        continue
                    log = DiscordWebhook(
                        url=logWebHookUrl,
                        content="Error in czc: {}\n{}".format(e, URL))
                    hook = log.execute()
                    time.sleep(6 + random.random() * 3)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="tiles")
            if results is None:
                print("No results for {}".format(URL))
                if page == 0:
                    failed += 1
                    faily += " {}".format(category_name)
                break
            articles = results.find_all("div", class_="new-tile")

            for article in articles:
                temp = json.loads(article.attrs["data-ga-impression"])
                price = temp["price"]
                name = temp["name"]
                id = temp["id"]
                link = article.contents[5].attrs["href"]
                if supply := article.find("span", class_="on-stock"):
                    supply = supply.parent.contents[1]
                else:
                    supply = "<:ShrugMan:973117676748668951>"

                if db.get(category_name) is not None:
                    if category.get(id) is not None:
                        if category[id] > 2 * price:
                            if category[id] - price > 100:
                                text = "@everyone @slevaEnjoyers\nDropnula sleva na {} {} za {} místo {}, skladem je {}\n https://www.czc.cz{}".format(
                                    category_name, name, price, category[id], supply, link)
                            else:
                                text = "@ everyone @slevaEnjoyers\nDropnula sleva na {} {} za {} místo {}, skladem je {}\n https://www.czc.cz{}".format(
                                    category_name, name, price, category[id], supply, link)
                            webhook = DiscordWebhook(
                                url=mainWebHookUrl,
                                content=text)
                            response = webhook.execute()
                category[id] = price
            time.sleep(3 + random.random() * 3)

        db[category_name] = category

    category = None

    # %%

    with open('czc.json', 'w') as convert_file:
        convert_file.write(json.dumps(db))

    if failed > 0:
        print()
        log_fail = DiscordWebhook(
            url=logWebHookUrl,
            content="Failed to load {} czc\n{}".format(failed, faily))
        hook_fail = log_fail.execute()

    # print("hotovo lol")

    log2 = DiscordWebhook(
        url=logWebHookUrl,
        content="CZC prohledáno a nalezeno {} produktů".format(sum(len(db[key]) for key in db.keys())))
    hook2 = log2.execute()
    # time.sleep(60)
    # log1.delete(hook1)
    # log2.delete(hook2)

    # %%

    log1 = DiscordWebhook(
        url=logWebHookUrl,
        content="Scamování Azly započíná")
    hook1 = log1.execute()
    failed = 0
    faily = ""
    db = {}
    with open("azla.json", "r") as read_file:
        db = json.load(read_file)

    azla = ["/mobily/18843445.htm", "/chytre-hodinky-smartwatch/18854785.htm", "/tablety/18852388.htm",
            "/prislusenstvi-pro-mobilni-telefony/18844551.htm", "/prislusenstvi-k-chytrym-hodinkam/18855196.htm",
            "/prislusenstvi-pro-tablety/18852448.htm", "/notebooky/18842920.htm", "/pocitace/18852653.htm",
            "/komponenty/18852654.htm", "/lcd-monitory/18842948.htm", "/sitove-prvky/18842916.htm",
            "/software/18860415.htm", "/projektory/18843223.htm", "/gaming/playstation-5/18872471.htm",
            "/gaming/herni-konzole/playstation-4/18854416.htm", "/gaming/xbox/18892642.htm",
            "/gaming/nintendo-switch/18860896.htm", "/gaming/herni-pc/18848818.htm",
            "/gaming/herni-notebooky/18848814.htm", "/gaming/hry/18855143.htm",
            "/gaming/prislusenstvi-pro-hrace/18853697.htm", "/gaming/pc-gaming/18857155.htm",
            "/gaming/herni-telefony/18867506.htm", "/gaming/virtualni-realita/18856436.htm",
            "/gaming/herni-konzole/18855142.htm", "/gaming/merchandise/18862622.htm",
            "/hracky/spolecenske-hry-a-hlavolamy/18857192.htm", "/hracky/party-oslavy-a-kostymy/18878556.htm",
            "/televize/18849604.htm", "/sluchatka/18843602.htm", "/reproduktory/18843496.htm",
            "/digitalni-fotoaparaty/18843129.htm", "/digitalni-kamery/18843241.htm", "/mikrofony/18843339.htm",
            "/prehravace/18859887.htm", "/drony/18855539.htm", "/hudebni-nastroje/18855990.htm",
            "/audio-video/hi-fi-komponenty/18851356.htm", "/kuchynske-spotrebice/18890799.htm",
            "/elektricke-zubni-kartacky-a-sprchy/18861476.htm", "/vestavne-spotrebice/18853613.htm",
            "/uprava-vzduchu/18859694.htm", "/chlazeni-a-topeni/18890759.htm",
            "/smartappliances-chytre-spotrebice/18860900.htm", "/smarthome-inteligentni-domacnost/18855843.htm",
            "/usporne-spotrebice/18897587.htm", "/hobby/vybaveni-dilny/18862227.htm",
            "/hobby/zahradnicke-potreby/18867125.htm", "/hobby/bazeny/18861272.htm", "/hobby/pestovani/18861203.htm",
            "/hobby/zahradni-technika/18858970.htm", "/hobby/grily/18852352.htm", "/elektromobilita/18861977.htm",
            "/kancelarsky-nabytek/18875649.htm", "/kancelarska-technika/18875657.htm", "/kalkulacky/18851287.htm",
            "/prislusenstvi-pro-pocitac/18853152.htm", "/prislusenstvi-k-notebookum/18843112.htm",
            "/externi-datova-uloziste/18867065.htm", "/brasny-batohy-a-pouzdra/18857401.htm",
            "/baterie-a-nabijeni/18843926.htm", "/pouzdra/18861684.htm", "/pametove-karty/18843034.htm",
            "/drzaky/18861689.htm", "/bezpecnostni-tokeny/18894404.htm", "/ovladace/18862262.htm",
            "/usb-c/18861343.htm", "/cisteni-elektroniky/18876741.htm", "/dotykova-pera-stylusy/18885105.htm",
            "/mysi/18842900.htm", "/klavesnice/18842899.htm", "/prislusenstvi-k-tiskarnam/18842939.htm",
            "/baterie-a-nabijeni/nabijecky/18843927.htm", "/powerbanky/18854166.htm",
            "/ctecky-cipovych-karet/18867060.htm", "/privatni-filtry/18854610.htm", "/graficke-tablety/18843074.htm",
            "/bryle-pro-virtualni-realitu/18859989.htm", "/alzapower/v12363.htm",
            "/prislusenstvi-pro-apple/18855480.htm", "/prislusenstvi-pro-home-office/18894289.htm",
            "/tiskarny/18842929.htm", "/3d-tisk/18862952.htm", "/3d-pera/18868012.htm",
            "/filamenty-pro-3d-tiskarny/18854774.htm", "/uv-resin-pro-3d-tiskarny/18871691.htm",
            "/prislusenstvi-pro-3d-tisk/18877346.htm", "/susicky/18852767.htm", "/pracky/18852774.htm",
            "/vysavace/18850975.htm", "/male-kuchynske-spotrebice/18850363.htm", "/mixery/18850373.htm",
            "/toustovace/18852351.htm", "/grilovani/18879762.htm", "/domaci-pekarny/18850375.htm",
            "/ryzovary/18850461.htm", "/elektricke-hrnce/18850377.htm", "/fritezy/18850376.htm",
            "/food-procesory/18861796.htm", "/graficke-karty/18842862.htm", "/procesory/18842843.htm",
            "/pameti/18842853.htm", "/pevne-disky/18842851.htm", "/zakladni-desky/18842832.htm",
            "/skrine-a-zdroje/18850751.htm", "/chlazeni/18842845.htm", "/overclocking/18861850.htm",
            "/cd-a-dvd/18842867.htm", "/televizni-karty/18842886.htm", "/zvukove-karty/18842881.htm",
            "/sitove-prvky/sitove-karty/18843099.htm", "/programovatelne-stavebnice/18854857.htm",
            "/zaznamova-zarizeni/18855519.htm", "/mining/18862055.htm", "/hracky/lego/18851136.htm"]

    for category_name in azla:
        print(category_name)
        skip = False
        if db.get(category_name) is None:
            db[category_name] = {}
        category = db[category_name]
        for sort in range(4):
            if skip:
                break
            for page in range(1, 4):
                URL = "https://m.alza.cz{}?availabilityFilterValue=0&sort={}&wearType=new&page={}".format(
                    category_name, sort, page)
                for i in range(3):
                    try:
                        page = requests.get(URL)
                    except Exception as e:
                        print(e)
                        if i == 2:
                            log = DiscordWebhook(
                                url=logWebHookUrl,
                                content="<@313378412494585856>\nError in alza: {}\n{}".format(e, URL))
                            hook = log.execute()
                            continue
                        log = DiscordWebhook(
                            url=logWebHookUrl,
                            content="Error in alza: {}\n{}".format(e, URL))
                        hook = log.execute()
                        time.sleep(6 + random.random() * 3)

                soup = BeautifulSoup(page.content, "html.parser")
                results = soup.find("div", id="itemsContainer")

                if results is None:
                    print("No results for {}".format(URL))
                    if page == 0:
                        failed += 1
                        faily += " {}".format(category_name)
                    skip = True
                    break

                articles = results.find_all("a")
                for article in articles:
                    price = float(article.attrs["data-impression-metric2"].replace(',', '.'))
                    name = article.attrs["data-impression-name"]
                    supply = article.attrs["data-impression-dimension13"]
                    link = article.attrs["href"]

                    if db[category_name].get(link) is not None:
                        if db[category_name][link] > (2 * price):
                            if db[category_name][link] - price > 100:
                                text = "@everyone @slevaEnjoyers\n{} za {}, místo {}, {}\n https://www.alza.cz/{}".format(
                                    name, price, db[category_name][link], supply, link)
                            else:
                                text = "@ everyone @slevaEnjoyers\n{} za {}, místo {}, {}\n https://www.alza.cz/{}".format(
                                    name, price, db[category_name][link], supply, link)

                            webhook = DiscordWebhook(
                                url=mainWebHookUrl,
                                content=text)
                            response = webhook.execute()
                    category[name] = price
                time.sleep(3 + random.random() * 3)

        db[category_name] = category
        time.sleep(random.random() * 5)

    category = None

    with open('azla.json', 'w') as convert_file:
        convert_file.write(json.dumps(db))

    if failed > 0:
        print()
        log_fail = DiscordWebhook(
            url=logWebHookUrl,
            content="Failed to load {} alza\n{}".format(failed, faily))
        hook_fail = log_fail.execute()

    # print("hotovo lol")

    log2 = DiscordWebhook(
        url=logWebHookUrl,
        content="Azla prohledána a nalezeno {} produktů".format(sum(len(db[key]) for key in db.keys())))
    hook2 = log2.execute()
    # time.sleep(60)
    # log1.delete(hook1)
    # log2.delete(hook2)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        log = DiscordWebhook(
            url=logWebHookUrl,
            content="<@313378412494585856>\nError in main: {}".format(e))
        hook = log.execute()
