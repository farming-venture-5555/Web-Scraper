from playwright.sync_api import sync_playwright
import csv
from datetime import datetime
def scrape_kpn_fresh():
    with sync_playwright() as p:
        productBaseLoc = "//div[@class='browse-layout-section']//div[@class='w-4/5']//div[contains(@class,'relative bg-white opacity')]"
        productNameLoc = "//div[@class='px-[8px] py-[10px]']/div[1]"
        productQuantityLoc = "//div[@class='px-[8px] py-[10px]']/div[2]"
        productPriceLoc = "//div[@class='px-[8px] py-[10px]']/div[3]"
        noOfPagesLoc = "//div[@class='browse-layout-section']//li[@data-testid='testListItem']"
        nextPageLoc = "//div[@class='browse-layout-section']//img[@alt='Next']"

        output_file_name = f'kpn_fresh_items_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

        urls = ['https://www.kpnfresh.com/apples-pears/c/2_1010?category_id=1_10']

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        all_items = []

        for url in urls:

            page.goto(url)

            try:
                no_of_Pages = int(page.query_selector(noOfPagesLoc).inner_text().split("of")[1].strip())

            except AttributeError as e:
                no_of_Pages = 1

            for i in range(no_of_Pages):

                # Wait for the products to load
                page.wait_for_timeout(2000)

                # Extract product details using XPath
                products = page.query_selector_all(productBaseLoc)

                for product in products:

                    # Extract the price using XPath
                    price = product.query_selector(productPriceLoc).inner_text().replace("₹", "").replace("\n"," ").strip()
                    price_split = price.split(" ")
                    if (len(price_split)==2):
                        price = price.replace(price_split[1], '-'+price_split[1]+'-')

                    item = {
                    'CATEGORY' : url.split("/")[3],

                    # Extract the product name using XPath
                    'NAME' : product.query_selector(productNameLoc).inner_text(),

                    # Extract the quantity using XPath
                    'QUANTITY' : product.query_selector(productQuantityLoc).inner_text(),

                    'PRICE' : price
                    }
                    print(f"item: {item}")
                    all_items.append(item)

                if(i < no_of_Pages-1):
                    page.query_selector(nextPageLoc).click()

        # Save to CSV
        with open(output_file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=all_items[0].keys())
                writer.writeheader()
                writer.writerows(all_items)

        # Close the browser
        browser.close()

if __name__ == "__main__":
    scrape_kpn_fresh()