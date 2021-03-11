from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    #-------------------------------------------------------------------------------------------
    # NASA Mars News
    #------------------------------------------------------------------------------------------- 
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    # Visit the page
    browser.visit(url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Retrieve the latest news title
    news_title=soup.find_all('div', class_='content_title')[1].text
    # Retrieve the latest news paragraph
    news_p=soup.find_all('div', class_='article_teaser_body')[0].text
    
    #-------------------------------------------------------------------------------------------
    # JPL Mars Space Images - Featured Image
    #------------------------------------------------------------------------------------------- 
    # URLs of page to be scraped
    space_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    space_image_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(space_image_url)
    # HTML object
    html=browser.html
    # Parse HTML
    soup=bs(html,"html.parser")
    # Retrieve anchor tag with the image url
    img_url=soup.find_all('a')[2]
    # Retrieve the image url
    img_url=soup.find('a', class_='showimg')['href']    
    # Display the full image url of the featured image
    featured_image_url = space_url+img_url
    
    #-------------------------------------------------------------------------------------------
    # Mars Facts
    #------------------------------------------------------------------------------------------- 
    # Visit the facts url and put it into a pandas dataframe
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    # Get the first item of the list which are the facts we are after
    mars_facts = tables[0]
    # Change the table headers
    mars_facts = mars_facts.rename(columns={0:"Description", 1:""})
    # Convert the dataframe to a HTML table
    mars_facts_html_table = mars_facts.to_html(index=False, classes="table table-sm table-striped font-weight-light")
    #-------------------------------------------------------------------------------------------
    # Mars Hemispheres
    #------------------------------------------------------------------------------------------- 
    # Store the url of the thumb images and get the browser to open it
    hemi_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    time.sleep(2)
    # Iterate through all thumbnails once
    for x in range(1):
        # Store the HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')
        # Retrieve all elements that contain images information
        thumbnails = soup.find_all('div', class_='item')        
        # Initialise the list to append to
        hemisphere_url = []        
        # Iterate through each thumbnail
        for thumb in thumbnails:
            # Use Beautiful Soup's find() method to navigate and retrieve attributes
            title = thumb.find('h3').text
            link = thumb.find('a', class_='itemLink product-item')
            href = link['href']
            # Open the site with the full image
            browser.visit('https://astrogeology.usgs.gov' + href)
            # Create the HTML Object parse with bs
            thumb_html = browser.html
            soup = bs( thumb_html, 'html.parser')
            # Partial url of the full images
            part_img_url = soup.find('img', class_='wide-image')['src']
            # Full image source 
            final_img_url = 'https://astrogeology.usgs.gov' + part_img_url
            # Append the retreived information into a list of dictionaries 
            hemisphere_url.append({"title" : title, "img_url" : final_img_url})
    
    #-------------------------------------------------------------------------------------------
    # Save the scrapped data in a dictionary
    #-------------------------------------------------------------------------------------------     
    scrapped_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": mars_facts_html_table, 
        "hemisphere_url": hemisphere_url
    }

    # Close the browser after scraping
    browser.quit()
    # Return results
    return scrapped_data
# if __name__ == "__main__":
#     scrape()