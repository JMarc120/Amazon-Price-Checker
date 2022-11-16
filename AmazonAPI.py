import requests
from bs4 import BeautifulSoup
import lxml
import json
import time

class Connection:
    '''
    Functions in this class are used to get responses from a webpage or getting HTML content.
    '''
    def getResponse(url: str) -> requests.models.Response:
        '''
        This function returns the response to an url using a headers User-Agent.
        :arg url: String, url you want to get the response of.
        :return: Returns the response connection.
        '''
        return requests.get(url=url, headers={"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'})

    def getHTML(response: requests.models.Response) -> BeautifulSoup:
        '''
        This function returns the HTML content of a given webpage response.
        :arg response: Response from requests class.
        :return: BeautifulSoup object.
        '''
        return BeautifulSoup(response.content, 'lxml')

class AmazonElements:
    '''
    Functions in this class are used to get HTML Amazon elements.
    '''
    def getPrice(soup: BeautifulSoup) -> tuple:
        '''
        This function get the price objects of the given webpage soup.
        :arg soup: BeautifulSoup object.
        :return: tuple with the whole price, the fraction price and the symbol of the price.
        '''
        try:
            price = soup.find("span", {"id":"priceblock_ourprice"}).text.strip()
        except:
            try:
                price = soup.find("span", {"id":"sns-base-price"}).text.strip()
            except:
                try:
                    price = soup.find("span", {"class":"a-offscreen"}).text.strip()
                    if '0%' in price:
                        price = soup.find("strong", {"class":"priceLarge"}).text.strip()
                except:
                    try:
                        price = soup.find("strong", {"class":"priceLarge"}).text.strip()
                    except:
                        try:
                            price = soup.find("span", {"class":"a-size-base a-color-price a-color-price"}).text.strip()
                        except:
                            print('There is a problem getting this product price.')
                            price = None
            
        return AmazonElements.cleanPrice(price)

    def cleanPrice(price: str):
        '''
        This function cleans the price format.
        :arg price: String with format {00 ... 0,00}.
        :return: cleaned price format and it's symbol.
        '''
        price = price.strip()
        final_price = str()
        for character in range(len(price)):
            if (price[character] == ','):
                final_price = final_price + price[character] + price[character+1] + price[character+2]
                return final_price
            final_price = final_price + price[character]
        
        return final_price + '€'

    def getName(soup: BeautifulSoup) -> str:
        '''
        This function get the product name object of the given webpage soup.
        :arg soup: BeautifulSoup object of Amazon product url.
        :return: The product name.
        '''
        try:
            return AmazonElements.cleanText(soup.find("span", {"id":"titleSection"}).text)
        except:
            return AmazonElements.cleanText(soup.find("span", {"id":"productTitle"}).text)
    
    def cleanText(name: str):
        '''
        This function returns a given string without whitespaces at start or end or character errors.
        :arg name: String that we want to clean.
        :return: Name cleaned.
        '''
        return name.replace('\\','').strip()

class ListsUtilities:
    '''
    Functions in this class are utilities used for testing.
    '''
    def txtListToDictionary(filename: str):
        '''
        This function converts a text file of format '{Name}\n{URL}\n{Category}\n=======\n{Name}\n{URL} ...' to a dicitonary.
        :arg filename: String that represents the file name we want to pass to dictionary.
        :return: Dictionary that contains the data from text file.
        '''
        with open(file=filename, mode='r', encoding='UTF8') as f:
            productsList = f.read().split('\n')
            productsList = [product for product in productsList if product !='']
            products_dict = dict()
            productIndex = 0
            while(productIndex*4 < len(productsList)):
                products_dict[productIndex] = {'Name':f'{productsList[productIndex*4]}',
                                               'URL':f'{productsList[productIndex*4+1]}', 
                                               'Category':f'{productsList[productIndex*4+2]}'}
                productIndex += 1

        return products_dict

class Test:
    '''
    This class executes a test.
    '''
    def __init__(self) -> None:
        '''
        This function opens a products text file and gets products elements to test if all works fine.
        '''
        products_dict = ListsUtilities.txtListToDictionary('Example products list.txt')
        i = 0
        for product in products_dict:
            print(products_dict[product]['URL'])
            try:
                soup = Connection.getHTML(Connection.getResponse(products_dict[product]['URL']))
            except requests.exceptions.ChunkedEncodingError:
                time.sleep(10)
                soup = Connection.getHTML(Connection.getResponse(products_dict[product]['URL']))
            
            priceItem = AmazonElements.getPrice(soup=soup)
            products_dict[i]['Price'] = priceItem
            i += 1
        with open(f'products Test.json', 'w') as f:
            json.dump(products_dict, f)


class AmazonUtilities:
    '''
    Functions in this class are used to organize the data of the products.
    '''
    def check_JSON_exists(filename: str) -> None:
        '''
        This function checks if a JSON file {filename}.json exists, if not, it creates it.
        :arg filename: String that contains the file name that we want to check.
        '''
        try:
            with open(f'{filename}.json', 'r') as file_object:
                pass
        except FileNotFoundError:
            open(f'{filename}.json', 'w').close()
    
    def load_JSON_data(filename: str):
        '''
        This funciton loads the data in the wanted JSON file.
        :arg filename: String that contains the file name that we want to check.
        :return: It returns a dictionary containing the JSON data or 0 if it couldn't return anything.
        '''
        with open(f'{filename}.json', 'r') as file_object:
            try:
                return json.load(file_object)
            except json.decoder.JSONDecodeError:
                return 0

    def update_json(filename: str, data: dict):
        '''
        This function uploads the wanted JSON file with the passed data.
        :arg filename: String that contains the file name that we want to check.
        :arg data: Dictionary with the data we want to upload on the JSON file.
        '''
        with open(f'{filename}.json', 'w') as file_object:
            json.dump(data, file_object)

    def addProduct(url: str):
        '''
        This function adds a product to the JSON file where products are located.
        :arg url: String that contains the URL of the product we want to add.
        :return: Integer 0 if something failed.
        '''
        ## Establish conneciton.
        try:
            soup = Connection.getHTML(Connection.getResponse(url=url))
        except:
            print('Error trying to get product. Try again.')
            return 0

        ## Get product price
        priceItem = AmazonElements.getPrice(soup=soup)
        if priceItem == None:
            print('Problem getting this product price.')
            return 0

        ## Creating json file in case it doesn't exist.
        AmazonUtilities.check_JSON_exists(filename='Products List')

        ## Getting the data written on the json file and adding the new product.
        with open(f'Products List.json', 'r') as file_object:
            try:
                data = json.load(file_object)
                if (len(data) == 0):                ## Case that the file is empty.
                    data[ 0 ] = {'Name':AmazonElements.getName(soup=soup),
                                 'URL':url,
                                 'price':priceItem}
                else:                               ## Case that the file is empty with curly braces.
                    dictValues = [int(x) for x in list(data)]
                    dictName = [i for i in range(len(dictValues)+1) if i not in dictValues]
                    data[ dictName[0] ] = {'Name':AmazonElements.getName(soup=soup),
                                           'URL':url,
                                           'price':priceItem}
            except json.decoder.JSONDecodeError:    ## Fail loading the content from json file.
                data = dict()
                data[ 0 ] = {'Name':AmazonElements.getName(soup=soup),
                             'URL':url,
                             'price':priceItem}

        ## Updating the json file.
        AmazonUtilities.update_json(filename='Products List', data=data)
    
    def removeProductByIndex(productIndex: int):
        '''
        This function removes a product to the JSON file where products are located.
        :arg productIndex: Integer that contains the key from the dictionary element we want to remove.
        :return: Integer 0 if something failed.
        '''
        ## Creating JSON file in case it doesn't exist.
        AmazonUtilities.check_JSON_exists(filename='Products List')

        ## Loading the data from the JSON file.
        data = AmazonUtilities.load_JSON_data(filename='Products List')

        ## Deletes the product index passed from data dictionary.
        try:
            del data[str(productIndex)]
        except:
            return 0
            
        ## Updating the json file.
        AmazonUtilities.update_json(filename='Products List', data=data)

    def removeProductByName(name: str):
        '''
        This function removes a product to the JSON file where products are located.
        :arg name: String that contains the product name we want to remove.
        :return: Integer 0 if something failed.
        '''
        name = name.strip()

        ## Creating JSON file in case it doesn't exist.
        AmazonUtilities.check_JSON_exists(filename='Products List')

        ## Loading the data from the JSON file.
        data = AmazonUtilities.load_JSON_data(filename='Products List')
        
        ## Finds the dictionary key that contains the wanted product name.
        productObjective = 0
        for product in data:
            if data[product]['Name'].strip() == name:
                productObjective = product
        del data[str(productObjective)]

        ## Updating the json file.
        AmazonUtilities.update_json(filename='Products List', data=data)

    def readProducts():
        '''
        This function makes a string that contains all product names stores in the JSON file.
        :return: Integer 0 if something failed. String of products if execution was successfull.
        '''
        ## Creating JSON file in case it doesn't exist.
        AmazonUtilities.check_JSON_exists(filename='Products List')

        ## Loading the data from the JSON file.
        data = AmazonUtilities.load_JSON_data(filename='Products List')

        ## Creates a String of type format '{product name}\n{product name}\n{product name}\n{product name}' of all data stored in JSON file.
        postConent = str()
        for i in data:
            postConent = postConent + data[i]['Name'] + '\n'

        return postConent

    def getOldPrice(name: str):
        '''
        This function gets the stored price of a given product name.
        :arg name: String that contains the product name.
        :return: Integer 0 if something failed. String of the stored price if execution was successfull.
        '''
        name = name.strip()

        ## Creating JSON file in case it doesn't exist.
        AmazonUtilities.check_JSON_exists(filename='Products List')

        ## Loading the data from the JSON file.
        data = AmazonUtilities.load_JSON_data(filename='Products List')
        
        ## Searches the price stored in JSON from a product name
        for product in data:
            if data[product]['Name'].strip() == name:
                return data[product]['price']
        return 0    ## Name not found case.
    
    def getNewPrice(name: str):
        '''
        This function gets the current price of a given product name.
        :arg name: String that contains the product name.
        :return: Integer 0 if something failed. String of the current price if execution was successfull.
        '''
        name = name.strip()

        ## Creating JSON file in case it doesn't exist.
        AmazonUtilities.check_JSON_exists(filename='Products List')

        ## Loading the data from the JSON file.
        data = AmazonUtilities.load_JSON_data(filename='Products List')

        ## Searches the URL from the wanted product name in the JSON file.
        actualURL = str()
        for product in data:
            if data[product]['Name'].strip() == name:
                actualURL = data[product]['URL']

        ## Establish connection
        try:
            soup = Connection.getHTML(Connection.getResponse(url=actualURL))
        except:
            print('Error trying to get product. Try again.')

        priceItem = AmazonElements.getPrice(soup=soup)
        if priceItem == None:
            print('Problem getting this product price.')
            return 0
        return priceItem    ## Product price located case.
    
    def addProductPrice(name: str, price: str):
        '''
        This function uploads the stored price of the product wanted.
        :arg name: String that contains the product name.
        :arg price: String that contains the price we want to upload.
        :return: Integer 0 if something failed.
        '''
        name = name.strip()

        ## Creating JSON file in case it doesn't exist.
        AmazonUtilities.check_JSON_exists(filename='Products List')

        ## Loading the data from the JSON file.
        data = AmazonUtilities.load_JSON_data(filename='Products List')

        ## Uploads the price of a selected product name.
        for product in data:
            if data[product]['Name'].strip() == name:
                data[product]['price'] = price

        ## Updating the json file.
        AmazonUtilities.update_json(filename='Products List', data=data)