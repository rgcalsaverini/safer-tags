var host = 'https://tag.raccoon.ag';
var store_id = 1;
var transaction_id = /* transaction_id */;
var transaction_total = /* transaction_total */;

var url = host + '/tag/purchase/' + String(store_id)+ '/' + String(transaction_id)
    + '/' + String((Number(transaction_total) * 100)|0);

var purchased_products = /*

    Assemble a list of all purchased products, with every
    product in the following form:

    {
        "sku": ,
        "price": ,
        "image": ,
        "name": ,
        "url":
    }
*/

var payload = {
    'products': purchased_products,
    'origin': /* traffic source */
};


var xhr = new XMLHttpRequest();
xhr.open("POST", url, true);
xhr.withCredentials = true;
xhr.setRequestHeader("Content-type", "application/json");
xhr.send(JSON.stringify(payload));