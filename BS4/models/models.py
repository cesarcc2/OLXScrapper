from dataclasses import dataclass
import json
from prettytable import PrettyTable
import uuid
import hashlib

@dataclass
class Search:
    id: str
    transcript: str
    minPrice: float
    maxPrice: float
    optimalPrice: float
    allowTradable: bool
    onlyNegotiables:bool
    def __init__(self,transcript, minPrice,maxPrice,optimalPrice,allowTradable,onlyNegotiables,id = None):
        self.id = id
        if(id == None):
            self.id = (str(uuid.uuid1().fields[-1])[:5]) + str(len(transcript))
        self.transcript = transcript
        self.minPrice = minPrice
        self.maxPrice = maxPrice
        self.optimalPrice = optimalPrice
        self.allowTradable = allowTradable
        self.onlyNegotiables = onlyNegotiables

    def toJSON(self) -> dict:
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))

@dataclass
class Product:
    id: str
    name: str
    price: float
    tradable: bool
    negotiable: bool
    date:str
    url: str
    img: str
    location: str

    def __init__(self, name,price,tradable,negotiable,date,url,img,location):
        self.id = hashlib.sha1(str.encode(name)+str.encode(img)).hexdigest()
        self.name = name
        self.price = price
        self.tradable = tradable
        self.negotiable = negotiable
        self.date = date
        self.url = url
        self.img = img
        self.location = location

    def toJSON(self) -> dict:
        return json.loads(json.dumps(self,default=lambda obj: obj.__dict__))


