var host = 'https://tag.raccoon.ag';
var store_id = 1;
var url = host + '/tag/remove-from-cart/' + String(store_id);
var payload = {
    'products': [{
        "sku": /* product_sku */
    }],
    'origin': /* traffic source */
};


var xhr = new XMLHttpRequest();
xhr.open("POST", url, true);
xhr.withCredentials = true;
xhr.setRequestHeader("Content-type", "application/json");
xhr.send(JSON.stringify(payload));
