function getProductsList() {
    return new Promise((resolve, reject) => {
        var products = [];
        fetch('../PHP/getProducts.php')
            .then(response => response.text())
            .then(data => {
                var parser = new DOMParser();
                var doc = parser.parseFromString(data, 'text/html');
                var bodyText = doc.body.innerText.trim().split('\n');
                for (let index = 0; index < bodyText.length - 1; index++) {
                    const product = bodyText[index];
                    products.push(product);
                }
                resolve(products);
            })
            .catch((error) => {
                console.error('Error:', error);
                reject(error);
            });
    });
}


function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getFeaturedProducts(allProducts) {
    var featuredProducts = new Array();
    var lastElement = allProducts.pop();
    featuredProducts.push(lastElement);
    console.log(featuredProducts);
    var lastElement = allProducts.pop();
    featuredProducts.push(lastElement);
    console.log(featuredProducts);
    var randomIndex = getRandomInt(0, allProducts.length - 1);
    var randElement = allProducts[randomIndex];
    featuredProducts.push(randElement);
    console.log(featuredProducts);
    return featuredProducts;
}

async function displayFeaturedProducts() {
    var allProducts = await getProductsList();
    console.log(allProducts);
    var featuredProducts = getFeaturedProducts(allProducts);
    console.log(featuredProducts);
    var currentId = 0
    for (let index = 0; index < featuredProducts.length; index++) {
        var product = featuredProducts[index].split(';');
        console.log(product);
        // Get product name, description, image source, and price
        var name = product[1];
        currentId++;
        var description = product[2];
        var price = product[3];
        var imageSrc = product[4];

        displayProduct(currentId, name, description, price, imageSrc);
    }
}

function displayProduct(prodID, prodTitle, prodDesc, prodPrice, prodImg) {
    var productID = "prod" + prodID.toString();
    console.log(productID);

    // Update the product title
    var titleElements = document.getElementById(productID).getElementsByClassName("prodTitle");
    for (var i = 0; i < titleElements.length; i++) {
        titleElements[i].textContent = prodTitle;
    }

    // Update the product description
    var descElements = document.getElementById(productID).getElementsByClassName("prodDesc");
    for (var i = 0; i < descElements.length; i++) {
        descElements[i].textContent = prodDesc;
    }

    // Update the product price
    var priceElements = document.getElementById(productID).getElementsByClassName("prodPrice");
    for (var i = 0; i < priceElements.length; i++) {
        priceElements[i].textContent = "£" + prodPrice.toString();
    }

    // Update the product image
    var imgElements = document.getElementById(productID).getElementsByTagName("img");
    for (var i = 0; i < imgElements.length; i++) {
        imgElements[i].src = prodImg;
    }
}