from datetime import datetime
from crawler import WeiboHotSearchScraper
from image import CanvasScraper
from comment import WeiboScraper
from dataSaver import DataSaver
def main():
    scraper = WeiboHotSearchScraper(60)
    time=datetime.now().strftime('%Y%m%d ')
    hot_search_data, link_dict, sentiment_dict = scraper.display_hot_searches()
    canvas_scraper = CanvasScraper()
    for index, url in sentiment_dict.items():
        print(index)
        output_image_name = f"{index}.png"
        canvas_scraper.save_canvas_image(url=url,filename=output_image_name,timestamp=time)


    Weibo_Scraper = WeiboScraper()
    for index, url in link_dict.items():
        print(f"Processing {index}...")
        comments = Weibo_Scraper.scrape_comments(url, required_comments=100)
        if comments:
            Weibo_Scraper.save_comments_to_file(comments, str(index))
    data_saver = DataSaver()
    data_saver.save_data(hot_search_data)

main()












