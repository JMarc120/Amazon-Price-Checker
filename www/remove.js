/**
 * This function removes a stored product.
 */
async function get_products(){
    let productsString = await eel.get_products()();    // String with format '{product name}\n{product name}\n{product name}\n{product name} ... \n'.
    var arr = productsString.split(/\r?\n/);
    arr.pop();  // Last list item is empty, so we erase it.
    for (let step = 0; step < arr.length; step++) {
        addProduct(arr[step]);   // Weadd products one by one to HTML.
    }
    getButtons(arr=arr);
}

/**
 * This function adds in HTML format all the products productName stored.
 * @param {string} productName The productName of the product we want to show.
 */
function addProduct(productName) {
    // Creating HTML elements.
    let li = document.createElement('li');
    li.className = 'statement';
    let div = document.createElement('div');
    div.className = 'product';
    div.id = 'productName';
    let a = document.createElement('a');
    a.className = 'button';

    // Adding values to the components.
    div.innerHTML = `
        ${productName}
    `;

    a.innerHTML = `
        DELETE
    `;
    li.appendChild(div);
    li.appendChild(a);

    document.getElementById('addProducts').appendChild(li);
}

get_products();

/**
 * This function listens if the user press the remove button, in that case it removes the HTML product and calls in Python the function to remove the product from the JSON file.
 */
function getButtons() {
    let buttons = document.querySelectorAll(".button"); // array of all buttons generated.
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", function(){    // Listening for every button.
            productName = this.parentNode.querySelector('#productName').innerHTML;
            eel.remove_product_ByName(productName);
            this.parentNode.remove();
        });
}
    
    
}
