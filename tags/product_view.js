var host = 'https://tag.raccoon.ag';
var store_id = 1;
var url = host + '/tag/pageview/' + String(store_id) + '/product';
var payload = {
    'products': [{
        "sku": /* product_sku */,
        "price": /* product_price */,
        "image": /* product_image */,
        "name": /* product_name */,
        "url": document.location.href.split('?')[0]
    }],
    'origin': /* traffic source */
};


var xhr = new XMLHttpRequest();
xhr.open("POST", url, true);
xhr.withCredentials = true;
xhr.setRequestHeader("Content-type", "application/json");
xhr.send(JSON.stringify(payload));
