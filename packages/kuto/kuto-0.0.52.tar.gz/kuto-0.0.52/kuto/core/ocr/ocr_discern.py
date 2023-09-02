import os
import ssl
import time

import easyocr

from kuto.utils.log import logger

os.environ["CUDA_VISIBLE_DEVICES"] = "True"
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

ssl._create_default_https_context = ssl._create_unverified_context


class OCRDiscern:
    """
        通过OCR进行文字识别，获取相应坐标值
    """

    def __init__(self, image_path: str, grade=0.8) -> None:
        # self.image_path = os.path.join(os.path.abspath('image'), 'SourceImage.png')
        self.image_path = image_path
        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"文件: {self.image_path} 不存在")
        self.model = ['ch_sim', 'en']
        self.grade = grade
        # self.coordinate_set = self.__ocr_read_wording()
        # logger.debug(self.coordinate_set)

    # 进行OCR识别
    def __ocr_read_wording(self):
        # 实例化读取器
        reader = easyocr.Reader(self.model)
        # 读取图像
        result = reader.readtext(self.image_path)
        return result

    # 处理坐标数据
    def __handle_coordinate_data(self, coordinate_set, target_wording):
        search_res_coordinate = None
        logger.info(coordinate_set)
        for item in coordinate_set:
            if item[1] == target_wording:
                search_res_coordinate = item
                break
        if search_res_coordinate is None or search_res_coordinate[2] < self.grade:
            logger.warning(
                '没有搜索到元素「{0}」或元素「{0}」置信度过低'.format(target_wording))
            return False
        else:
            logger.info('识别到元素「{}」, 置信度为：{}'.format(
                search_res_coordinate[1], search_res_coordinate[2]))
            coordinates = search_res_coordinate[0]
            logger.info(coordinates)
            x_coordinate = coordinates[0][0] + \
                (coordinates[1][0] - coordinates[0][0]) / 2
            y_coordinate = coordinates[0][1] + \
                (coordinates[2][1] - coordinates[1][1]) / 2
            logger.info("X坐标：{}，Y坐标：{}".format(
                x_coordinate, y_coordinate))
            return x_coordinate, y_coordinate

    # 获取坐标信息
    def get_coordinate(self, target_wording: str):
        """get_coordinate 获取指定文字的坐标
        Args:
            target_wording (str): 目标文字
        Returns:
            tuple: x轴坐标 & y轴坐标
        """
        logger.info('开始进行OCR识别🔍')
        start = time.time()
        coordinate_set = self.__ocr_read_wording()
        res = self.__handle_coordinate_data(coordinate_set, target_wording)
        end = time.time()
        logger.info(f"识别耗时: {end -start}s")
        return res


if __name__ == '__main__':
    pass




