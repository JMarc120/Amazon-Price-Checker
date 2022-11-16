import eel
from AmazonAPI import AmazonUtilities as AU

# Setting the web files
eel.init('www')


# Exposing these functions to Javascript
@eel.expose
def add_product(url: str):
    AU.addProduct(url=url)

@eel.expose
def remove_product(index: int):
    AU.removeProduct(productIndex=index)

@eel.expose
def remove_product_ByName(name: str):
    AU.removeProductByName(name=name)

@eel.expose
def get_products():
    return AU.readProducts()

@eel.expose
def getOldPrice(name: str):
    return AU.getOldPrice(name=name)

@eel.expose
def getNewPrice(name: str):
    return AU.getNewPrice(name)

@eel.expose
def reloadProductPrice(name: str, price: float):
    AU.addProductPrice(name=name, price=price)

# Starting server
eel.start('index.html', size=(1920, 1080))