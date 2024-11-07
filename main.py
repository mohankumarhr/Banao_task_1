from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import csv

# Initialize the Chrome WebDriver
browser = webdriver.Chrome()

# Open Amazon's homepage
browser.get('https://www.amazon.in')
# Wait for the page to load fully (you can adjust the sleep time if necessary)
sleep(10)
# Maximize the browser window
browser.maximize_window()

# Find the search input box and the search button
input_search = browser.find_element(By.ID, 'twotabsearchtextbox')
search_button = browser.find_element(By.XPATH, "(//input[@type='submit'])[1]")

# Type the search query into the search input field
input_search.send_keys("Mobile Portable Power Banks")
sleep(1)

# Click the search button to initiate the search
search_button.click()
sleep(3)
data = []



#Loop through the pages of search results (in this case, we are scraping the first 2 pages)
for i in range(2):
     # Find all the product links on the current page
    links = browser.find_elements(By.XPATH, '//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
    
    # Extract the 'href' attribute from each product link (this is the URL to the product page)
    for link in links:
        href = link.get_attribute('href')
        if href:  
            data.append(href)

    # Find the "Next" button to navigate to the next page of search results
    next_button = browser.find_element(By.XPATH, '//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')
    next_button.click()
    sleep(2)

print(len(data))
productDetails = []

# Loop through each product link and extract its details
for link in data:
    browser.get(link) # Open the product page
    browser.maximize_window()
    newdata = {}
    
    # Try to extract the product name,price,seller name, and rating and handle any errors if the element is not found
    try:
        newdata["Product Name"] = browser.find_element(By.XPATH, '//*[@id="productTitle"]').text
    except Exception as e:
        newdata["Product Name"] = ""  

    try:
        newdata["Price"] = browser.find_element(By.XPATH, '//*[@id="corePrice_feature_div"]/div/div/span[1]/span[2]/span[2]').text
    except Exception as e:
        newdata["Price"] = ""  

    try:
        newdata["Seller Name"] = browser.find_element(By.XPATH, '//*[@id="sellerProfileTriggerId"]').text
    except Exception as e:
        newdata["Seller Name"] = ""  

    try:
        newdata["Rating"] = browser.find_element(By.XPATH, '//*[@id="acrPopover"]/span[1]/a/span').text
    except Exception as e:
        newdata["Rating"] = ""  

    
    productDetails.append(newdata)

# Define the CSV file name
csv_file = 'products.csv'

# Define the fieldnames (column headers) for the CSV
fieldnames = ['Product Name', 'Price', 'Seller Name', 'Rating']


# Open the CSV file in write mode
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    
    writer.writeheader()

    # Write the product details to the CSV file
    writer.writerows(productDetails)

# Print a success message indicating that the CSV file has been created
print(f"CSV file '{csv_file}' created successfully!")

# Close the browser once all data is collected and saved
browser.quit()