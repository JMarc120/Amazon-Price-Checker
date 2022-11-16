/**
 * This function checks for the new prices of the stored items and shows it.
 */
async function get_products(){
    let productsString = await eel.get_products()();    // String with format '{product name}\n{product name}\n{product name}\n{product name} ... \n'.
    var arr = productsString.split(/\r?\n/);
    arr.pop();  // Last list item is empty, so we erase it.
    for (let step = 0; step < arr.length; step++) {
        checkProducts(arr[step]);   // We check products one by one.
    }
}

function getFloat(number) {
    var priceTrad = ''
    for (var i = 0; i < number.length; i++) {
      if (number[i] == ','){
          priceTrad = priceTrad + number[i] + number[i+1] + number[i+2]
          break
      } else{
          priceTrad = priceTrad + number[i]
      }
    }
    return priceTrad
}

/**
 * This function writes (in HTML) the old and new price of the product passed.
 * 
 * @param {string} productName The productName we want to check prices of.
 */
async function checkProducts(productName) {
    // Creating HTML elements.
    let li = document.createElement('li');
    li.className = 'statementInfo';

    let divName = document.createElement('div');
    let divOP = document.createElement('div');
    divOP.className = 'oldPrice';

    let divNP = document.createElement('div');
    
    // Getting the price values.
    let OldPrice = await eel.getOldPrice(productName)();
    let NewPrice = await eel.getNewPrice(productName)();

    // If the new price is lower than the old one, the HTML component will be green; if is higher, red.
    var loadProduct = 0;
    if (getFloat(OldPrice) > getFloat(NewPrice)) {
        li.className = 'statementInfo bg-green';
        loadProduct = 1;
    } else if (getFloat(OldPrice) < getFloat(NewPrice)){
        li.className = 'statementInfo bg-red';
        loadProduct = 1;
    }

    // Adding values to the components.
    divName.innerHTML = `
        ${productName}
    `;

    divOP.innerHTML = `
        ${OldPrice}
    `;

    divNP.innerHTML = `
        ${NewPrice}€
    `;
    li.appendChild(divName);
    li.appendChild(divOP);
    li.appendChild(divNP);

    document.getElementById('addProducts').appendChild(li);

    // If there is a price difference, it uploads the new price.
    if (loadProduct == 1) {
        await eel.reloadProductPrice(productName, NewPrice)();
    }
}

get_products();