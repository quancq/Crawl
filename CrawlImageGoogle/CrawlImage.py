import requests
import os
import time
import shutil
import urllib

class ImageCrawler:
    def __init__(self):
        self.path_urls_dic = {}             # dictionary map url_file_path -> url image list

    def update_dic(self, path, urls):
        self.path_urls_dic.update({path: urls})

    def read_files(self, paths):
        for path in paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    urls = f.read().strip().split('\n')
                print("[ + ] Read file {} -> Collected {} urls ".format(path, len(urls)))
                self.update_dic(path, urls)
            else:
                print("[ - ] Path {} dont exist".format(path))

    def crawl_all_images(self, max_num_imgs = 20):
        for path, urls in self.path_urls_dic.items():
            # Crawl all url of 1 path
            start_time = time.clock()
            temp = os.path.split(path)
            dir_path = ''.join(temp[:-1])
            keyword = temp[-1].split('.')[0]

            num_dowloaded_urls = 0
            index = 0

            if max_num_imgs < len(urls):
                urls = urls[0: max_num_imgs]

            num_urls_length = len(str(len(urls)))
            with open(os.path.join(dir_path, keyword + '_ErrorURL.txt'), mode='a') as log_file:
                for url in urls:
                    index += 1
                    lst = list(urllib.parse.urlsplit(url))
                    lst = [urllib.parse.quote(elm) for elm in lst]
                    url_quote = urllib.parse.urlunsplit(lst)

                    img_file_name = keyword + '_{}.jpg'.format(str(num_dowloaded_urls).zfill(num_urls_length))
                    output_path = os.path.join(dir_path, img_file_name)
                    try:
                        data = urllib.request.urlopen(url_quote).read()
                        with open(output_path, 'wb') as img_file:
                            img_file.write(data)

                        # req.urlretrieve(url, output_path)

                        # response = requests.get(url, stream=True, timeout=30)
                        # response.raise_for_status()
                        # with open(output_path, "wb") as file:
                        #     shutil.copyfileobj(response.raw, file)
                        # del response

                        # with open(output_path, 'wb') as f:
                        #     f.write(response.content)

                        num_dowloaded_urls +=1
                        print("[ + ] Downloaded {} ({}/{}/{})".format(url_quote, num_dowloaded_urls, index, len(urls)))
                    except:
                        log_file.write(url_quote + '\n')
                        print("[ - ] Error downloading {} ... skipping".format(url_quote))

            end_time = time.clock()
            print("[ * ] Path {} : {}/{} urls downloaded, {} error urls => {} seconds".format(
                dir_path, num_dowloaded_urls, len(urls), len(urls) - num_dowloaded_urls, (end_time - start_time))
            )


if __name__ == "__main__":
    imgCrawler = ImageCrawler()

    paths = []
    # paths.append(os.path.abspath("./Data/Nhà hát lớn Hà Nội/Nhà hát lớn Hà Nội.txt"))
    # paths.append(os.path.abspath("./Data/Nhà thờ lớn Hà Nội/Nhà thờ lớn Hà Nội.txt"))
    # paths.append(os.path.abspath("./Data/Phủ Tây Hồ/Phủ Tây Hồ.txt"))


    # paths.append(os.path.abspath("./Data/Bảo tàng lịch sử quốc gia/Công viên nước hồ Tây.txt"))
    # paths.append(os.path.abspath("./Data/Công viên nước hồ Tây/Công viên nước hồ Tây.txt"))
    # paths.append(os.path.abspath("./Data/Cửa hàng bánh tôm hồ Tây/Cửa hàng bánh tôm hồ Tây.txt"))
    # paths.append(os.path.abspath("./Data/Cửa hàng kem tràng tiền/Cửa hàng kem tràng tiền.txt"))
    # paths.append(os.path.abspath("./Data/Khách sạn Diamond West Lake/Khách sạn Diamond West Lake.txt"))
    # paths.append(os.path.abspath("./Data/Khách sạn Điện Lực/Khách sạn Điện Lực.txt"))
    # paths.append(os.path.abspath("./Data/Khách sạn Hồ Gươm/Khách sạn Hồ Gươm.txt"))
    # paths.append(os.path.abspath("./Data/Khách sạn Intercontinental Hồ Tây/Khách sạn Intercontinental Hồ Tây.txt"))
    # paths.append(os.path.abspath("./Data/Khách sạn Metropole Hoàn Kiếm/Khách sạn Metropole Hoàn Kiếm.txt"))
    # paths.append(os.path.abspath("./Data/Khách sạn Pan Pacific/Khách sạn Pan Pacific.txt"))
    # paths.append(os.path.abspath("./Data/Khách sạn Sofitel Plaza Hà Nội/Khách sạn Sofitel Plaza Hà Nội.txt"))
    # paths.append(os.path.abspath("./Data/Khách sạn Thắng Lợi hồ Tây/Khách sạn Thắng Lợi hồ Tây.txt"))
    # paths.append(os.path.abspath("./Data/Rạp chiếu phim tháng 8/Rạp chiếu phim tháng 8.txt"))
    # paths.append(os.path.abspath("./Data/Khách sạn Sheraton Hà Nội/Khách sạn Sheraton Hà Nội.txt"))
    # paths.append(os.path.abspath("./Data/Thư viện quốc gia/Thư viện quốc gia.txt"))
    # paths.append(os.path.abspath("./Data/Tràng Tiền Plaza Hoàn Kiếm/Tràng Tiền Plaza Hoàn Kiếm.txt"))
    # paths.append(os.path.abspath("./Data/Vườn hoa con cóc/Vườn hoa con cóc.txt"))
    # paths.append(os.path.abspath("./Data/Vườn hoa đền Bà Kiệu/Vườn hoa đền Bà Kiệu.txt"))
    # paths.append(os.path.abspath("./Data/Vườn Hoa Hàng Đậu/Vườn Hoa Hàng Đậu.txt"))
    # paths.append(os.path.abspath("./Data/Vườn hoa hàng trống/Vườn hoa hàng trống.txt"))
    # paths.append(os.path.abspath("./Data/Vườn hoa hồ Tây/Vườn hoa hồ Tây.txt"))
    # paths.append(os.path.abspath("./Data/Vườn hoa Lý Thái Tổ/Vườn hoa Lý Thái Tổ.txt"))
    paths.append(os.path.abspath("./Data/Vườn quất Tứ Liên/Vườn quất Tứ Liên.txt"))
    # paths.append(os.path.abspath("./Data/.txt"))


    imgCrawler.read_files(paths)
    imgCrawler.crawl_all_images(max_num_imgs=100)