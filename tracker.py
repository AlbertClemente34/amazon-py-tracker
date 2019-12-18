import db
import scraper
import time

URL = "https://www.amazon.es/Amazfit-GTS-Smartwatch/dp/B07YJWTCFM/ref=sr_1_1?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=amazfit+gts&qid=1575318278&s=computers&sr=1-1-catcorr"

def track():
    details = scraper.get_product_details(URL)
    result = ""
    if details is None:
        result = "not done"
    else:
        inserted = db.add_product_detail(details)
        if inserted:
            result = "done"
        else:
            result = "not done"
    return result

while True:
    print(track())
    time.sleep(60)