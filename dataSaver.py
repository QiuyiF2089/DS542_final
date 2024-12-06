import os
from datetime import datetime


class DataSaver:
    def __init__(self, folder_name="title"):
        # 初始化文件夹名称，并确保文件夹存在
        self.folder_name = folder_name
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)

    def save_data(self, data_list):
        # 获取当前日期作为文件名
        current_date = datetime.now().strftime("%Y%m%d")
        file_name = f"{self.folder_name}/{current_date}.txt"

        # 将所有数据写入同一个文件
        with open(file_name, "w", encoding="utf-8") as file:
            for data in data_list:
                file.write(str(data) + "\n")  # 将每个数据项转换为字符串再写入

        print(f"数据已成功保存到 {file_name}")


# 使用示例
hot_search_data = ["title1", "title2", "title3"]  # 或者 ["title1", ["title2", "title3"], "title4"]
data_saver = DataSaver()
data_saver.save_data(hot_search_data)
