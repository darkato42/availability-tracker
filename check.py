import yaml
import requests
import argparse
from mailservice import MailService


def get_product_urls(config='product-urls.yml'):
    """
    Returns a list of product urls
    """

    if "http" in config:
        config_file = requests.get(config).text
        try:
            product_urls = yaml.safe_load(config_file).get("products")
        except yaml.YAMLError as exc:
            print(exc)

    with open(config, "r") as stream:
        try:
            product_urls = yaml.safe_load(stream).get("products")
        except yaml.YAMLError as exc:
            print(exc)

    return product_urls


def has_stock(product):
    """
    Checks if a product has stock
    """
    url = product.get("url")
    text = product.get("text")

    if url:
        product_page = requests.get(url).text
        if text in product_page:
            return False
        else:
            return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("from_add", help="sender email address")
    parser.add_argument("secret", help="Gmail App Secret")
    parser.add_argument("urls_yaml", help="yaml file with product urls")
    parser.add_argument("to_add", help="recipient email address")
    args = parser.parse_args()

    product_urls = get_product_urls(args.urls_yaml)
    products_with_stock = [product for product in product_urls if has_stock(product)]

    if not products_with_stock:
        print("No products with stock")
        exit(0)

    mail_service = MailService(args.from_add, args.secret)
    subject = "Products stock notification"
    body = "Products with stock: \n"
    for product in products_with_stock:
        body += f"{product['name']}: {product['url']}\n"

    mail_service.send(args.to_add, subject, body)
