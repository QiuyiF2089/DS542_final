import requests
from datetime import datetime
from urllib.parse import quote


class WeiboHotSearchScraper:
    def __init__(self, num_results=60):
        """
        Initializes the scraper with the number of hot search results to retrieve.
        :param num_results: Number of hot search entries to retrieve (default is 20)
        """
        self.num_results = num_results
        self.base_url = 'https://weibo.com/ajax/side/hotSearch'
        self.hot_search_data = []
        self.link_dict = {}
        self.sentiment_dict = {}

    def hot_search(self):
        """
        Fetches the hot search JSON data from Weibo.
        :return: JSON data if successful, None otherwise
        """
        response = requests.get(self.base_url)
        if response.status_code != 200:
            print('Failed to fetch hot search data')
            return None
        return response.json()['data']

    def display_hot_searches(self):
        """
        Fetches the top hot search results from Weibo and stores the links and sentiment URLs in dictionaries.
        """
        data = self.hot_search()
        if not data:
            print('Unable to retrieve hot search data from Weibo.')
            return

        # Display the top 'hotgov' item
        print(f"Top Official Trending: {data['hotgov']['word'].strip('#')}")

        # Store each hot search item in dictionaries for links and sentiment URLs
        for i, rs in enumerate(data['realtime'][:self.num_results], 1):
            title = rs['word']
            hot = rs['num']
            link = f"https://ai.s.weibo.com/web/other/ai/blogs2?dt=1729880246&query={quote(title)}&tab="
            sentiment_url = f"https://ai.s.weibo.com/web/other/ai/content?ua=OPPO-PFZM10__weibo__14.3.2__android__android14&from=10E3295010&query={quote(title)}&from=3004"

            # Append each item as a sublist [index, title, popularity]
            self.hot_search_data.append([i, title, hot])

            # Store link and sentiment URL in separate dictionaries
            self.link_dict[i] = link
            self.sentiment_dict[i] = sentiment_url

        return self.hot_search_data, self.link_dict, self.sentiment_dict


# Usage example
if __name__ == '__main__':
    scraper = WeiboHotSearchScraper(num_results=20)
    hot_search_data, link_dict, sentiment_dict = scraper.display_hot_searches()

    for entry in hot_search_data:
        index = entry[0]
        title = entry[1]
        popularity = entry[2]
        print(f"{index}. {title} - Popularity: {popularity}")
        print(f"Link: {link_dict[index]}")
        print(f"Sentiment Analysis: {sentiment_dict[index]}")
        print()
