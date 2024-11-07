import requests
from bs4 import BeautifulSoup
import streamlit as st
from urllib.parse import urlparse, urljoin

# Function to get all the internal links of a website
def get_internal_links(url):
    internal_links = set()  # Using a set to avoid duplicates
    try:
        # Sending a GET request to the provided URL
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the content of the page with BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find all anchor tags with href attributes
            for anchor in soup.find_all("a", href=True):
                link = anchor.get("href")
                # Ensure it's an internal link (same domain)
                if link.startswith('/'):  # Relative URLs
                    link = urljoin(url, link)  # Convert to absolute URL
                parsed_link = urlparse(link)
                if parsed_link.netloc == urlparse(url).netloc:
                    internal_links.add(link)
        else:
            st.error(f"Failed to retrieve the page: {url}. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    
    return internal_links

# Streamlit UI
def main():
    st.title("Website Page Finder")
    st.write(
        "This app helps you find all the pages within a given website. "
        "Simply enter a website URL, and the app will crawl it to find all internal links."
    )
    
    # Input field to get website URL
    website_url = st.text_input("Enter a website URL (e.g., https://www.youtube.com):", "")
    
    if website_url:
        if not website_url.startswith("http"):
            website_url = "http://" + website_url
        
        with st.spinner("Crawling the website..."):
            internal_links = get_internal_links(website_url)
            
            # Display results
            if internal_links:
                st.subheader("Found Internal Pages:")
                for link in internal_links:
                    st.write(link)
            else:
                st.write("No internal links found or failed to crawl the website.")
    
if __name__ == "__main__":
    main()

