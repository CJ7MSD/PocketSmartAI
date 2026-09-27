from dataclasses import dataclass
from urllib.parse import quote_plus
@dataclass(frozen=True)
class Item: name:str; category:str; platform:str; price:float; url:str; tags:tuple
CATALOG=[
Item("Minimal LED Ceiling Light","lighting","IKEA",2499,"https://www.ikea.com/in/en/search/?q=",("modern","minimal","living room")),Item("Wood Finish Study Table","furniture","Amazon",5999,"https://www.amazon.in/s?k=",("modern","wood","bedroom")),Item("Compact 4-Seater Dining Table","furniture","Flipkart",11999,"https://www.flipkart.com/search?q=",("modern","dining","wood")),Item("Cotton Cushion Set","decor","Amazon",1299,"https://www.amazon.in/s?k=",("minimal","living room","decor")),Item("Wall Art Set of 3","decor","IKEA",1799,"https://www.ikea.com/in/en/search/?q=",("modern","decor")),Item("Energy Efficient Ceiling Fan","appliance","Amazon",3299,"https://www.amazon.in/s?k=",("bedroom","living room","modern")),Item("Warm Ambient Floor Lamp","lighting","IKEA",3999,"https://www.ikea.com/in/en/search/?q=",("warm","modern")),Item("Birthday Catering Package","catering","Zomato",450,"https://www.zomato.com/search?query=",("birthday","food")),Item("Party Snack Combo","catering","Swiggy",300,"https://www.swiggy.com/search?query=",("birthday","corporate","food")),Item("Budget Event Venue","venue","OYO",8000,"https://www.oyorooms.com/search/?q=",("birthday","corporate","venue")),Item("Basic Party Decoration Kit","decoration","Amazon",2499,"https://www.amazon.in/s?k=",("birthday","decor")),Item("Corporate Buffet Package","catering","Zomato",700,"https://www.zomato.com/search?query=",("corporate","food")),Item("Wedding Decor Starter Set","decoration","Flipkart",7999,"https://www.flipkart.com/search?q=",("wedding","decor")),Item("Classic Gold-Tone Necklace","necklace","Amazon",2499,"https://www.amazon.in/s?k=",("wedding","elegant","traditional")),Item("Pearl Drop Earrings","earrings","Flipkart",1599,"https://www.flipkart.com/search?q=",("wedding","elegant","party")),Item("Minimal Stud Earrings","earrings","Amazon",899,"https://www.amazon.in/s?k=",("casual","minimal","elegant")),Item("Statement Kundan Set","necklace set","Flipkart",4999,"https://www.flipkart.com/search?q=",("wedding","traditional","festive")),Item("Silver-Tone Bracelet","bracelet","Amazon",1299,"https://www.amazon.in/s?k=",("casual","minimal"))]
def product_url(item):
    base={
        "Amazon":"https://www.amazon.in/s?k=",
        "Flipkart":"https://www.flipkart.com/search?q=",
        "IKEA":"https://www.ikea.com/in/en/search/?q=",
        "Zomato":"https://www.zomato.com/search?query=",
        "Swiggy":"https://www.swiggy.com/search?query=",
        "OYO":"https://www.oyorooms.com/search/?q=",
    }.get(item.platform, item.url)
    return base + quote_plus(item.name)

def search(tags,cats=None,limit=10):
    tags={x.lower() for x in tags}; rows=[]
    for x in CATALOG:
        if cats and x.category not in cats: continue
        rows.append((len(tags.intersection(x.tags)),x))
    return [x for _,x in sorted(rows,key=lambda z:(-z[0],z[1].price))[:limit]]
