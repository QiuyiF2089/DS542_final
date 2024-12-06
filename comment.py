import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


class WeiboScraper:
    def __init__(self):
        # Initialize Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def scrape_comments(self, url, required_comments=100):
        """
        Scrapes comments from the given URL on Weibo and returns all comments as a string
        :param url: URL of the Weibo page to scrape
        :param required_comments: Number of comments to extract (default is 100)
        :return: A single string of all collected comments
        """
        try:
            self.driver.get(url)
            time.sleep(5)  # Wait for the initial page load

            collected_comments = 0
            all_comments_text = []

            while collected_comments < required_comments:
                # Get the page source HTML
                html = self.driver.page_source

                # Parse the page with BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')

                # Find all divs with the class 'content'
                content_divs = soup.find_all('div', class_='content')

                # Extract text from span tags within content divs
                new_comments_found = False  # Flag to check if new comments are found
                for div in content_divs:
                    spans = div.find_all('span')
                    for span in spans:
                        comment_text = span.get_text(strip=True)
                        if comment_text and comment_text not in all_comments_text:  # Avoid duplicates
                            all_comments_text.append(comment_text)
                            collected_comments += 1
                            new_comments_found = True  # Mark that we found new comments
                            if collected_comments >= required_comments:
                                break
                    if collected_comments >= required_comments:
                        break

                # Check if new comments were found; if not, break the loop
                if not new_comments_found:
                    print("没有找到新评论，结束抓取。")
                    break

                # Scroll down to load more comments if needed
                if collected_comments < required_comments:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)  # Wait for new content to load

            # Return all comments joined into a single string
            return ' '.join(all_comments_text)

        except Exception as e:
            print(f"Error occurred while scraping: {e}")
            return ''

    def save_comments_to_file(self, comments, custom_filename):
        """
        Saves the comments to a file in a time-stamped folder structure.
        :param comments: The string of comments to save
        :param custom_filename: The custom name for the comments file
        """
        # Create the main comments folder if it doesn't exist
        main_folder = "comments"
        os.makedirs(main_folder, exist_ok=True)

        # Create a subfolder for the current date (e.g., 1026 for October 26)
        current_date = datetime.now().strftime("%m%d")  # Format as MMDD
        date_folder = os.path.join(main_folder, current_date)
        os.makedirs(date_folder, exist_ok=True)

        # Set full path with the date folder and custom filename
        file_path = os.path.join(date_folder, f"{custom_filename}.txt")

        # Write comments to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(comments)
        print(f"Comments saved to {file_path}")


# Example usage with link_dict
if __name__ == "__main__":
    link_dict = {
        1: 'https://ai.s.weibo.com/web/other/ai/blogs2?dt=1729880246&query=%E7%BD%91%E6%9B%9D%E5%A1%94%E6%96%AF%E6%B1%80%E6%B1%89%E5%A0%A1%E5%90%83%E5%87%BA%E7%94%9F%E8%82%89&tab=',
        2: 'https://ai.s.weibo.com/web/other/ai/blogs2?dt=1729880246&query=%E5%9B%BD%E4%B9%92%E6%B3%95%E5%9B%BD%E5%86%A0%E5%86%9B%E8%B5%9B0%E5%86%A0%E6%94%B6%E5%9C%BA&tab=',
        3: 'https://ai.s.weibo.com/web/other/ai/blogs2?dt=1729880246&query=%E8%BF%99%E4%BB%B6%E7%93%B7%E5%A3%B6%E9%9D%99%E9%9D%99%E7%BE%8E%E4%BA%86700%E5%A4%9A%E5%B9%B4&tab=',
        4: 'https://ai.s.weibo.com/web/other/ai/blogs2?dt=1729880246&query=%E6%98%AF%E8%B0%81%E5%9C%A8%E5%91%A8%E4%B8%80%E9%80%97%E6%88%91%E5%BC%80%E5%BF%83&tab=',
        5: 'https://ai.s.weibo.com/web/other/ai/blogs2?dt=1729880246&query=%E5%9B%BD%E4%B9%92%E4%B8%A4%E5%90%8D%E7%8B%AC%E8%8B%97%E5%9D%87%E6%97%A0%E7%BC%98%E5%86%B3%E8%B5%9B&tab='
    }

    Weibo_Scraper = WeiboScraper()
    for index, url in link_dict.items():
        print(f"Processing {index}...")
        comments = Weibo_Scraper.scrape_comments(url, required_comments=100)
        if comments:
            Weibo_Scraper.save_comments_to_file(comments, str(index))
