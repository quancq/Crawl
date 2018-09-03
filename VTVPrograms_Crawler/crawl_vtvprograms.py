import utils
from datetime import datetime, timedelta
from lxml import html
import requests, os
import pandas as pd
from utils import DEFAULT_DELIMITER


def crawl_vtvprograms(start_date, end_date):
    url_fmt = "https://vtv.vn/lich-phat-song-ngay-{}-thang-{}-nam-{}.htm"
    title_prefix = "Xem truyền hình trực tiếp kênh"
    data = {}

    for date in utils.generate_datetime_objs(start_date, end_date):
        data_by_date = {}
        # Crawl single page
        day, month, year = utils.get_specific_fmt_time(date)
        # print("(day={}, month={}, year={})".format(day, month, year))

        url = url_fmt.format(day, month, year)
        root = html.document_fromstring(requests.get(url).content)

        # Find channels
        titles = root.xpath("//ul[@class = 'list-channel']//a/@title")
        channels = [title[len(title_prefix) + 1:] for title in titles]
        # print(channels)

        # Find programs
        program_elms = root.xpath("//div[@id = 'wrapper']/ul[@class = 'programs']")
        for program_elm, channel in zip(program_elms, channels):
            # print("Channel = ", channel)
            li_elms = program_elm.xpath("./li")
            program_list = []
            for li in li_elms:
                duration = li.xpath("@duration")[0] or ''
                start_time = li.cssselect("span.time")[0].text or ''
                program_name = li.cssselect("span.title")[0].text or ''
                program_genre = li.cssselect("a.genre")

                if program_genre is None or len(program_genre) == 0:
                    program_genre = ''
                else:
                    # print(html.tostring(program_genre[0], encoding='utf-8'))
                    program_genre = program_genre[0].text
                    # print(program_genre)


                # print("Start time = {}, duration = {}, program = {}".format(start_time, duration, program))
                program_list.append(DEFAULT_DELIMITER.join([start_time, program_name, program_genre]))

            data_by_date.update({channel: program_list})

        date_str = utils.get_time_str(date)
        data.update({date_str: data_by_date})
        print("Crawl broadcast schedule of date {} done".format(date_str))
        # break

    return data


def print_data(data):
    for date, data_by_date in data.items():
        print("\n=====================")
        print("Start date : ", date)
        for channel, program_list in data_by_date.items():
            print("\nChannel : ", channel)
            print("Programs: ", program_list)

        print("End date : ", date)


def save_crawled_data(data):
    base_dir = "./Data"
    utils.mkdirs(base_dir)

    # Save total data
    save_path = os.path.join(base_dir, "BroadSchedule.json")

    # Load exist data
    if os.path.exists(save_path):
        exist_data = utils.load_json(save_path)
    exist_data = {}
    exist_data.update(data)
    data = exist_data
    utils.save_json(data, save_path)

    for date, data_by_date in data.items():
        # Create data frame from arrays not same length
        df = pd.DataFrame.from_dict(data=data_by_date, orient='index').transpose()
        sorted_columns = sorted(df.columns.tolist())
        df = df[sorted_columns]

        # Save data by date
        save_path = os.path.join(base_dir, "{}.csv".format(date))
        df.to_csv(save_path, index=False)
        print("Save data to {} done".format(save_path))


def find_info_by_program(data, program_name_search="Thời sự"):
    info = []
    for date, data_by_date in data.items():
        for channel, program_list in data_by_date.items():
            for program_name in program_list:
                program_name = program_name.split(DEFAULT_DELIMITER)
                start_time = program_name[0]
                program_name = DEFAULT_DELIMITER.join(program_name[1:])

                if program_name_search in program_name:
                    # Find info needed
                    info.append({
                        "Date": date,
                        "Start_Time": start_time,
                        "Channel": channel
                    })
    info = pd.DataFrame(info)
    columns = ["Date", "Start_Time", "Channel"]
    info = info[columns]
    info.sort_values(by=["Date", "Start_Time"], inplace=True)
    return info


if __name__ == "__main__":
    # start_date = datetime(day=1, month=1, year=2019)
    # end_date = datetime(day=1, month=1, year=2018)
    # data = crawl_vtvprograms(start_date, end_date)
    # save_crawled_data(data)

    # Load scrapped data
    data_path = "./Data/BroadSchedule.json"
    data = utils.load_json(data_path)

    # Find info by program name
    program_name = "Thương vụ bạc tỷ"
    info = find_info_by_program(data, program_name)
    info = info[info["Channel"] == "VTV6"]
    print(info)
    print("Number results : ", info.shape[0])



