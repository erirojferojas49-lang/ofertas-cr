STORES = {
    "ekono": {
        "url_base": "https://www.ekono.co.cr",
        "tipo_extraccion": "scraping_html",
        "selectors": {
            "price": ".price-now",
            "name": ".product-title",
            "sku": ".product-sku"
        }
    },
    "aliss": {
        "url_base": "https://www.aliss.cr",
        "tipo_extraccion": "scraping_html",
        "selectors": {
            "price": ".precio",
            "name": ".nombre"
        }
    }
}
