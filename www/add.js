// Get url field.
var urlField = document.getElementsByClassName("URL-entry")[0];

// get add button.
var addBtn = document.getElementsByClassName("ADD-button")[0];
// var removeBtn = document.getElementsByClassName("REMOVE-button")[0];

/**
 * Passes the value of url field to the exposed function in python add_product.
 */
function add_product(){
    eel.add_product(urlField.value);
}

// When user clicks add button, it calls add_product() and clear the url field.
addBtn.addEventListener("click", function(){
    add_product();
    urlField.value = '';
});