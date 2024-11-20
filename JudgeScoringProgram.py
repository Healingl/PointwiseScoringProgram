# -*- coding: utf-8 -*-
# @Time : 2024/11/15 22:02
# @Author : Yuzhou Zhuang
# @Email : 605540375@qq.com


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/19 20:53
# @Author  : Yuzhou Zhuang
# @File    : demo2.py
# @License: (C) Copyright 2024-2034, OPLUS Mobile Comm Corp., Ltd.
# @Desc:

import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QScrollArea,
    QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QTextEdit, QGraphicsItem, QGraphicsPixmapItem, QGraphicsScene,
    QGraphicsView, QRadioButton, QMessageBox, QSplitter, QTextBrowser, QPlainTextEdit
)
from PyQt5.QtCore import QTimer, QDateTime, QSize, Qt, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap, QWheelEvent
from datetime import datetime
import pandas as pd
import numpy as np
import yaml
import json
import copy
import re

WINDOW_SIZE = (1280, 980)
RECORD_USER_DICT_LIST = []


class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Step1 配置文件选择")
        self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.center()

        # 获取当前窗口的宽度并计算按钮宽度（代码中的这部分可以考虑根据实际布局情况优化调整，暂时保留逻辑不变）
        self.__window_width = self.width()
        self.__window_height = self.height()

        # 创建一个中心部件来布局其他组件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)  # 减少间距

        # 用于放置文件选择相关组件的水平布局
        file_choose_widget = QWidget()
        file_choose_layout = QHBoxLayout()

        # 左右边距，可根据实际情况调整
        margin_size = 10
        # 用于显示文件路径的文本框
        self.file_path_edit = QLineEdit(self)
        self.file_path_edit.setPlaceholderText("选择需要打分的YAML文件路径")
        self.file_path_edit.setMinimumHeight(40)
        # 设置为只读
        self.file_path_edit.setReadOnly(True)
        file_choose_layout.addWidget(self.file_path_edit)

        # 按钮 "YAML配置文件选择"
        self.select_button = QPushButton("YAML配置文件选择", self)
        self.select_button.setMinimumSize(int(self.__window_width*0.15), 40)
        self.select_button.setStyleSheet("font-size: 16px;")
        self.select_button.clicked.connect(self.choose_yaml_file)
        file_choose_layout.addWidget(self.select_button)

        # 设置水平布局的左右边距
        file_choose_layout.setContentsMargins(margin_size, 0, margin_size, 0)
        file_choose_layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        file_choose_widget.setLayout(file_choose_layout)
        main_layout.addWidget(file_choose_widget)

        # 日志显示区域
        self.log_label = QTextEdit(self)
        self.log_label.setPlaceholderText("YAML文件加载日志")
        self.log_label.setReadOnly(True)
        self.log_label.setMaximumHeight(int(self.__window_height * 0.3))  # 设置日志区域的高度
        self.log_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        main_layout.addWidget(self.log_label)

        parse_button_widget = QWidget()
        parse_button_layout = QVBoxLayout()

        # 解析按钮
        self.parse_button = QPushButton("解析打分配置文件，并进入打分界面", self)
        self.parse_button.setEnabled(False)
        self.parse_button.setStyleSheet("font-size: 17px;font-weight: bold")
        self.parse_button.clicked.connect(self.open_window2)
        self.parse_button.setMinimumSize(int(self.__window_width * 0.9),int(self.__window_height * 0.04))  # 设置按钮的宽度
        parse_button_layout.addWidget(self.parse_button)  # 居中对齐
        parse_button_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        parse_button_widget.setLayout(parse_button_layout)
        main_layout.addWidget(parse_button_widget)

        self.__loaded_yaml_path = ''
        self.__loaded_yaml_dict = {}

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())

    def choose_yaml_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择YAML配置文件", "", "YAML Files (*.yaml)")
        if file_path:
            self.file_path_edit.setText(file_path)
            self.check_yaml_file(file_path)

    def check_yaml_file(self, file_path):
        if not os.path.exists(file_path):
            self.show_log_message(message_text='文件不存在！')
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)

                required_keys = ['dataset_json_path', 'dataset_image_dir', 'multiple_choice_questions']
                if all(key in data.keys() for key in required_keys):
                    if not os.path.exists(data['dataset_json_path']):
                        self.parse_button.setEnabled(False)
                        self.show_error_log_message(message_text="dataset_json_path路径不存在！")
                    elif not os.path.exists(data['dataset_image_dir']):
                        self.parse_button.setEnabled(False)
                        self.show_error_log_message(message_text="dataset_image_dir路径不存在！")
                    elif len(data['multiple_choice_questions']) <= 1:
                        self.parse_button.setEnabled(False)
                        self.show_error_log_message(message_text="multiple_choice_questions数量不足！（至少需要2个问题）")
                    else:
                        self.__loaded_yaml_path = file_path
                        self.__loaded_yaml_dict = data

                        self.show_success_log_message(message_text= yaml.dump(data, default_flow_style=False, allow_unicode=True))  # 将 yaml_dict 转换为字符串并显示
                        self.parse_button.setEnabled(True)

                else:
                    # 收集缺失的键
                    missing_keys = [key for key in required_keys if key not in data.keys()]
                    # 显示错误日志消息，包含缺失的键
                    self.parse_button.setEnabled(False)
                    self.show_error_log_message(message_text=f"YAML文件中关键字段缺失: {', '.join(missing_keys)}")

        except Exception as e:
            self.show_log_message(message_text=str(e))

    def show_success_log_message(self, message_text):
        current_text = 'YAML文件加载成功！文件内容为：'
        new_text = f"{current_text}\n{message_text}"
        self.log_label.setText(new_text)


    def show_error_log_message(self, message_text):
        current_text = 'YAML文件加载失败！错误原因为：'
        new_text = f"{current_text}\n{message_text}"
        self.log_label.setText(new_text)

    def open_window2(self):
        self.window2 = Window2(yaml_path=self.__loaded_yaml_path, yaml_dict=self.__loaded_yaml_dict)
        self.window2.show()
        self.close()


class Window2(QMainWindow):
    def __init__(self, yaml_path, yaml_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Step2 逐项标注数据")
        self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.center()

        self._current_yaml_path = yaml_path
        self._current_yaml_dict = yaml_dict

        # 从 YAML 字典中获取相关路径和多选题题目
        self.__dataset_json_path = self._current_yaml_dict['dataset_json_path']
        self.__dataset_image_dir = self._current_yaml_dict['dataset_image_dir']
        self.__multiple_choice_questions = self._current_yaml_dict['multiple_choice_questions']

        # 读取 JSON 文件内容
        try:
            with open(self.__dataset_json_path, 'r', encoding='utf-8') as f:
                self.dataset_json_data = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Load json file ({self.__dataset_json_path}) error: {e}.")

        global RECORD_USER_DICT_LIST


        self.dataset_total_num = len(self.dataset_json_data)
        self.dataset_labeled_num = 0

        # 获取当前窗口的宽度并计算按钮宽度（代码中的这部分可以考虑根据实际布局情况优化调整，暂时保留逻辑不变）
        self.__window_width = self.width()
        self.__button_width = self.__window_width // 3

        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建垂直布局管理器
        self.window2_layout = QVBoxLayout()

        self.first_line_layout = QHBoxLayout()

        # 按钮"返回YAML文件选择"
        self.return_yaml_select_button = QPushButton("返回YAML文件选择", self)
        self.return_yaml_select_button.setMinimumSize(self.__button_width, 40)
        self.return_yaml_select_button.clicked.connect(self.confirm_return)
        self.first_line_layout.addWidget(self.return_yaml_select_button)

        # 按钮“计算打分精度及时间”
        self.cal_result_button = QPushButton("计算打分精度及时间", self)
        self.cal_result_button.setMinimumSize(self.__button_width, 40)
        self.cal_result_button.clicked.connect(self.calculate_all_data_averages)

        self.first_line_layout.addWidget(self.cal_result_button)

        self.first_line_layout.setAlignment(Qt.AlignCenter)
        self.first_line_layout.setSpacing(self.__window_width // 3)
        self.window2_layout.addLayout(self.first_line_layout)

        # 页面标题
        self.window2_titile_label = QLabel("数据标注列表")
        self.window2_titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.window2_titile_label.setAlignment(Qt.AlignCenter)
        self.window2_layout.addWidget(self.window2_titile_label)

        # 添加统计信息标签
        self.stats_label = QLabel(f"已标注数据：{self.dataset_labeled_num}个，总数量：{self.dataset_total_num}个,剩余数据：{self.dataset_total_num - self.dataset_labeled_num}个")
        self.stats_label.setStyleSheet("font-size: 14px; font-weight: bold; color: red")
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.window2_layout.addWidget(self.stats_label)

        # 改进label_json_path的样式，使用QHBoxLayout实现左侧为QLabel右侧为QLineEdit并居中显示
        label_json_path_widget = self.create_label_lineedit_widget(label_text="当前json路径:",
                                                                   line_edit_text=self.__dataset_json_path)
        self.window2_layout.addWidget(label_json_path_widget)

        # 改进label_image_dir的样式，同样使用QHBoxLayout实现相应布局并居中显示
        label_image_dir_widget = self.create_label_lineedit_widget(label_text="当前图片文件夹:",
                                                                   line_edit_text=self.__dataset_image_dir)
        self.window2_layout.addWidget(label_image_dir_widget)

        # 创建滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 始终显示垂直滚动条
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 根据需要显示水平滚动条
        self.scroll_area.setWidgetResizable(True)  # 允许内部小部件调整大小
        self.scroll_content = QWidget()  # 滚动区域的内容
        self.scroll_layout = QVBoxLayout(self.scroll_content)  # 内容的布局
        self.scroll_area.setWidget(self.scroll_content)

        # 根据json内容添加按钮
        for data_idx, item in enumerate(self.dataset_json_data):

            # 定义需要检查的键列表
            required_keys = ["id", "image", "mllm_model_name", "mllm_response", "pointwise_score_gt"]
            # 使用lambda函数来判断字典是否包含所有需要的键
            check_dict = lambda d: all(key in d for key in required_keys)
            if check_dict(item):


                current_model_data_dict = item
                current_image_path = os.path.join(self.__dataset_image_dir, current_model_data_dict['image'])
                current_model_data_dict['image_path']  = current_image_path
                current_model_data_dict['pointwise_score_manual'] = -1
                current_model_data_dict['manual_time'] = -1

                # 初始化 RECORD_USER_DICT_LIST
                RECORD_USER_DICT_LIST.append(current_model_data_dict)

                current_multiple_choice_questions = self.__multiple_choice_questions

                if os.path.exists(current_image_path):
                    item['image_path'] = current_image_path

                    new_button_idx = data_idx
                    new_button_idx_label = QLabel(f"第{new_button_idx + 1}个数据")
                    new_button_idx_label.setMinimumSize(self.__button_width, 40)  # 设置标签的最小尺寸
                    new_button_idx_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

                    new_button = QPushButton(item['image'])
                    new_button.setMinimumSize(self.__button_width, 40)  # 设置按钮的最小尺寸
                    # new_button.clicked.connect(lambda: self.open_window3(current_model_data_dict, current_multiple_choice_questions))
                    new_button.clicked.connect(
                        lambda _, d=current_model_data_dict, q=current_multiple_choice_questions: self.open_window3(d, q))
                    status_label = QLabel("未标注")
                    status_label.setMinimumSize(self.__button_width, 40)  # 设置标签的最小尺寸

                    h_layout = QHBoxLayout()
                    h_layout.addWidget(new_button_idx_label)
                    h_layout.addWidget(new_button)
                    h_layout.addWidget(status_label)
                    h_layout.setAlignment(Qt.AlignCenter)  # 水平居中对齐
                    # h_layout.setSpacing(10)  # 设置间距

                    self.scroll_layout.addLayout(h_layout)

        # 将滚动区域添加到主布局
        self.window2_layout.addWidget(self.scroll_area)

        # 设置中心部件的布局
        self.central_widget.setLayout(self.window2_layout)

    def create_label_lineedit_widget(self, label_text, line_edit_text):
        label_lineedit_layout = QHBoxLayout()
        qlabel = QLabel(label_text)
        qline_edit = QLineEdit(line_edit_text)
        qline_edit.setReadOnly(True)
        label_lineedit_layout.addWidget(qlabel)
        label_lineedit_layout.addWidget(qline_edit)
        label_lineedit_layout.setAlignment(Qt.AlignCenter)
        label_lineedit_widget = QWidget()
        label_lineedit_widget.setLayout(label_lineedit_layout)
        return label_lineedit_widget

    def confirm_return(self):
        # 创建一个消息框
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("提醒")
        msg_box.setText("您确定要返回上一界面吗？\n这将导致当前标注数据丢失。")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        # 显示消息框并获取用户的选择
        response = msg_box.exec_()

        # 根据用户的选择执行相应的操作
        if response == QMessageBox.Yes:
            self.open_window1()
        else:
            # 如果用户选择“否”，则不进行任何操作
            pass

    def open_window1(self):
        self.window1 = Window1()
        self.window1.show()
        self.close()

    def open_window3(self, model_data_dict, multiple_choice_questions_list):
        # print(model_data_dict)
        self.window3 =  Window3(model_data_dict=model_data_dict, multiple_choice_questions_list=multiple_choice_questions_list)
        self.window3.submission_signal.connect(self.update_after_submission)  # 添加信号连接
        self.window3.show()

    def update_after_submission(self, model_dict, score, time_spent):
        for i in range(self.scroll_layout.count()):
            layout = self.scroll_layout.itemAt(i).layout()
            button = layout.itemAt(1).widget()  # 获取 QPushButton
            status_label = layout.itemAt(2).widget()  # 获取 QLabel

            # 不仅要当前button的名称为图片名，而且要保证顺序以及id符合
            if button.text() == model_dict['image'] and RECORD_USER_DICT_LIST[i]['id'] == model_dict['id']:
                status_label.setText(f"已标注，得分{score}分，耗时{time_spent}秒")
                status_label.setStyleSheet("color: red; font-weight: bold")
                button.setEnabled(False)
                self.dataset_labeled_num += 1

        self.stats_label.setText(
            f"已标注数据：{self.dataset_labeled_num}个，总数量：{self.dataset_total_num}个,剩余数据：{self.dataset_total_num - self.dataset_labeled_num}个"
        )

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())

    def calculate_all_data_averages(self):
        current_unlabeled_data_idx = [data_idx + 1 for data_idx, item in enumerate(RECORD_USER_DICT_LIST) if item['pointwise_score_manual'] == -1 or item['manual_time'] == -1]

        if len(current_unlabeled_data_idx) == 0:
            record_all_data_user_df = pd.DataFrame(RECORD_USER_DICT_LIST)

            pointwise_score_gt_array = record_all_data_user_df['pointwise_score_gt']
            pointwise_score_manual_array = record_all_data_user_df['pointwise_score_manual']
            manual_time_array = record_all_data_user_df['manual_time']

            average_gt_score = pointwise_score_gt_array.mean()
            average_manual_score = pointwise_score_manual_array.mean()
            average_time = manual_time_array.mean()

            mae_metric = self.mean_absolute_error(y_pred=pointwise_score_manual_array, y_gt=pointwise_score_gt_array)
            mse_metric = self.mean_squared_error(y_pred=pointwise_score_manual_array, y_gt=pointwise_score_gt_array)
            rmse_metric = self.root_mean_squared_error(y_pred=pointwise_score_manual_array, y_gt=pointwise_score_gt_array)

            current_experiment_time = datetime.now().strftime('%Y%m%d%H%M')

            metric_result_message = f'MAE:{mae_metric:.4f}\nMSE:{mse_metric:.4f}\nRMSE:{rmse_metric:.4f}'
            result_average_message = f'打标时间:{current_experiment_time}\n打标数据量:{len(RECORD_USER_DICT_LIST)}条\n打标总耗时:{manual_time_array.sum():.2f}秒\n当前人工打标平均得分:{average_manual_score:.2f}\n当前每条数据人工打标的平均耗时:{average_time:.2f}秒\n真实标注平均分:{average_gt_score:.2f}\n人工标注和真实标注之间指标评估:\n{metric_result_message}'

            msg_box = QMessageBox()
            msg_box.setWindowTitle("打分结果")  # 设置标题
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(result_average_message)
            save_button = msg_box.addButton("保存打分结果", QMessageBox.ActionRole)
            cancel_button = msg_box.addButton("取消", QMessageBox.RejectRole)  # 添加取消按钮
            msg_box.setDefaultButton(save_button)

            msg_box.exec_()

            if msg_box.clickedButton() == save_button:

                # 获取当前Python文件所在的目录
                current_script_path = os.path.dirname(os.path.abspath(__file__))

                save_folder_path = QFileDialog.getExistingDirectory(self, "选择保存文件夹", current_script_path)

                if save_folder_path is not None and os.path.exists(save_folder_path):
                    try:
                        record_all_data_user_save_dir = os.path.join(save_folder_path, f"{current_experiment_time}_judge_score_result")

                        if not os.path.exists(record_all_data_user_save_dir): os.makedirs(record_all_data_user_save_dir)

                        record_all_data_user_df_csv_path = os.path.join(record_all_data_user_save_dir, 'record_all_data_user_labeled.csv')
                        record_all_data_user_final_result_txt = os.path.join(record_all_data_user_save_dir, 'record_all_data_final_result.txt')

                        record_all_data_user_df.to_csv(record_all_data_user_df_csv_path, index=False, encoding='utf_8_sig')
                        with open(record_all_data_user_final_result_txt , 'w+', encoding='utf-8') as f: f.write(result_average_message)

                        QMessageBox.information(self, "提示", f"打分结果已成功保存！结果保存在:{record_all_data_user_save_dir}")

                    except Exception as e:
                        QMessageBox.warning(self,'提示', f"打分结果保存失败:{e}")

        else:
            QMessageBox.warning(self, "提示", f"还有{len(current_unlabeled_data_idx)}条数据尚未打分，具体为第{','.join(str(num) for num in current_unlabeled_data_idx)}条数据，请对所有数据打分后再计算结果！")


    @staticmethod
    def mean_absolute_error(y_pred, y_gt):
        """
        计算均方绝对误差 (Mean Absolute Error, MAE)

        参数:
        y_pred: 预测值数组
        y_gt: 真实值数组

        返回:
        mae: 均方绝对误差
        """

        # 检查输入数组的长度是否一致
        if len(y_pred) != len(y_gt):
            raise ValueError("预测值和真实值数组的长度必须相同")

        # 将输入转换为 NumPy 数组
        y_pred = np.array(y_pred)
        y_gt = np.array(y_gt)

        # 计算绝对误差
        absolute_errors = np.abs(y_pred - y_gt)

        # 计算均方绝对误差
        mae = np.mean(absolute_errors)

        return mae

    @staticmethod
    def mean_squared_error(y_pred, y_gt):
        """
        计算均方误差 (Mean Squared Error, MSE)

        参数:
        y_pred: 预测值数组
        y_gt: 真实值数组

        返回:
        mse: 均方误差
        """
        # 检查输入数组的长度是否一致
        if len(y_pred) != len(y_gt):
            raise ValueError("预测值和真实值数组的长度必须相同")

        # 将输入转换为 NumPy 数组
        y_pred = np.array(y_pred)
        y_gt = np.array(y_gt)

        # 计算平方误差
        squared_errors = (y_pred - y_gt) ** 2

        # 计算均方误差
        mse = np.mean(squared_errors)

        return mse

    @staticmethod
    def root_mean_squared_error(y_pred, y_gt):
        """
        计算均方根误差 (RMSE)

        参数:
        y_pred (numpy.ndarray): 预测值数组
        y_gt (numpy.ndarray): 真实值数组

        返回:
        float: RMSE值
        """
        # 检查输入数组的长度是否一致
        if len(y_pred) != len(y_gt):
            raise ValueError("预测值和真实值数组的长度必须相同")

        # 计算差值的平方
        squared_errors = (y_pred - y_gt) ** 2

        # 计算均方误差
        mean_squared_error = np.mean(squared_errors)

        # 计算均方根误差
        rmse = np.sqrt(mean_squared_error)

        return rmse

class Window3(QMainWindow):
    submission_signal = pyqtSignal(dict, int, int)

    def __init__(self, model_data_dict, multiple_choice_questions_list, *args, **kwargs):
        """

        :param model_data_dict:
        :param multiple_choice_questions_list:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)



        self.__model_data_dict = model_data_dict

        self.user_multiple_choice_questions_list = copy.deepcopy(multiple_choice_questions_list)
        self.is_early_end = False

        # 初始化self.user_multiple_choice_questions_list
        for item in self.user_multiple_choice_questions_list:
            item['select_answer_idx'] = -1
            item['select_answer_score'] = 0

        self.current_question_index = 0
        self.total_score = 0

        self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.setWindowTitle("数据打分窗口")

        self.__window_width = self.width()
        self.__button_width = self.__window_width // 2

        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.center()
        self.initUI()

        self.start_time = QDateTime.currentDateTime()
        self.total_seconds = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(100)  # 100毫秒更新一次

    def initUI(self):
        # 创建布局
        main_layout = QVBoxLayout()
        top_info_layout = QHBoxLayout()
        middle_img_response_layout = QHBoxLayout()

        # 第一行：题目编号、计时器、提交按钮
        self.label_question_number = QLabel(f"第{self.current_question_index + 1}/{len(self.user_multiple_choice_questions_list)}题")
        self.label_question_number.setStyleSheet('font-size: 16px; font-weight: bold')
        self.label_question_number.setAlignment(Qt.AlignCenter)
        self.label_question_number.setMaximumSize(self.__button_width, 40)

        self.text_timer = QLabel('计时:00分钟:00秒')
        self.text_timer.setStyleSheet('font-size: 16px; font-weight: bold; color: red')
        self.text_timer.setAlignment(Qt.AlignCenter)
        self.text_timer.setMaximumSize(self.__button_width, 40)

        self.total_score_label = QLabel(f'当前得分:{self.total_score}')
        self.total_score_label.setStyleSheet('font-size: 16px; font-weight: bold; color: orange')
        self.total_score_label.setAlignment(Qt.AlignCenter)
        self.total_score_label.setMaximumSize(self.__button_width, 40)

        self.button_submit = QPushButton('提交结果')
        self.button_submit.setStyleSheet('font-size: 18px')
        self.button_submit.setMaximumSize(self.__button_width, 40)

        top_info_layout.addWidget(self.label_question_number)
        top_info_layout.addWidget(self.text_timer)
        top_info_layout.addWidget(self.total_score_label)
        top_info_layout.addWidget(self.button_submit)

        ## 中间部分：图片名称、图片区域、MLLM名称输入框、MLLM回复文本框
        # 图片名称、图片区域
        self.image_name_text = QPlainTextEdit(f"图片名称: {self.__model_data_dict['image']}")
        self.image_name_text.setStyleSheet('font-size: 13px; border: 1px;background-color: rgba(0,0,0,0)')
        self.image_name_text.setReadOnly(True)
        self.image_name_text.setMaximumSize(int(self.__button_width * 0.8), 30)

        self.label_image = ImageViewer(image_path=self.__model_data_dict['image_path'])
        self.label_image.setMaximumSize(int(self.__button_width * 0.8), 850)  # 设置图片大小

        label_image_layout = QVBoxLayout()
        label_image_layout.addWidget(self.image_name_text)
        label_image_layout.addWidget(self.label_image)

        middle_img_response_layout.addLayout(label_image_layout)

        self.mllm_name_text_label = QLabel(
            f"当前MLLM名称为{self.__model_data_dict['mllm_model_name']}, 当前MLLM回复为:")
        self.mllm_name_text_label.setStyleSheet(
            'font-size: 18px; border: 1px;background-color: rgba(0,0,0,0);font-weight: bold;vertical-align: middle;')
        # self.mllm_name_text_label.setReadOnly(True)
        self.mllm_name_text_label.setAlignment(Qt.AlignVCenter)
        self.mllm_name_text_label.setMaximumSize(self.__button_width, 50)

        #
        input_mllm_response = str(self.__model_data_dict['mllm_response'])

        self.mllm_response_text_label = QPlainTextEdit(f"{input_mllm_response}")
        self.mllm_response_text_label.setStyleSheet('font-size: 18px;border: 0px;background-color: rgb(255,255,255);font-weight: normal')
        self.mllm_response_text_label.setReadOnly(True)
        self.mllm_response_text_label.setMaximumSize(self.__button_width, 250)

        chinese_count, _ = self.count_characters_and_words(input_mllm_response)

        self.mllm_response_count_label = QLabel(f"当前MLLM回复中的中文字数(除标点符号):{chinese_count}")
        self.mllm_response_count_label.setStyleSheet('font-size: 14px;background-color: rgba(0,0,0,0);font-weight: normal;vertical-align: middle')
        # self.mllm_response_count_label.setReadOnly(True)
        self.mllm_response_count_label.setMaximumSize(self.__button_width, 25)

        # 中间部分：当前多选题和选项
        self.label_question = QPlainTextEdit(
            f"{self.user_multiple_choice_questions_list[self.current_question_index]['question']}")
        self.label_question.setStyleSheet(
            'font-size: 17px; border: 0px;background-color: rgba(0,0,0,0);font-weight:bold')

        self.label_question.setMaximumSize(self.__button_width, 90)

        # 创建多选项按钮滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 始终显示垂直滚动条
        self.scroll_area.setWidgetResizable(True)  # 允许内部小部件调整大小
        self.scroll_area.setMaximumSize(self.__button_width, 300)

        # 上一题和下一题按钮
        self.button_previous = QPushButton('上一题')
        self.button_previous.setMaximumSize(self.__button_width, 50)
        self.button_previous.setStyleSheet("""
            QPushButton:enabled {
                font-size: 16px;font-weight:bold;
            };
            QPushButton:disabled {
                background-color: gray;  /* 背景颜色设为灰色 */
                color: darkgray;         /* 文字颜色设为深灰色 */
            }
            """)
        self.button_next = QPushButton('下一题')
        self.button_next.setMaximumSize(self.__button_width, 50)
        self.button_next.setStyleSheet("""
            QPushButton:enabled {
                font-size: 16px;font-weight:bold;
            };
            QPushButton:disabled {
                background-color: gray;  /* 背景颜色设为灰色 */
                color: darkgray;         /* 文字颜色设为深灰色 */
            }
        """)

        mllm_response_layout = QVBoxLayout()
        # model name and response
        mllm_response_layout.addWidget(self.mllm_name_text_label)
        mllm_response_layout.addWidget(self.mllm_response_text_label)
        mllm_response_layout.addWidget(self.mllm_response_count_label)
        # question and answers
        mllm_response_layout.addWidget(self.label_question)
        mllm_response_layout.addWidget(self.scroll_area)
        mllm_response_layout.addWidget(self.button_previous)
        mllm_response_layout.addWidget(self.button_next)
        mllm_response_layout.setSpacing(5)

        middle_img_response_layout.addLayout(mllm_response_layout)

        # 绑定按钮点击事件
        self.button_previous.clicked.connect(self.previous_question)
        self.button_next.clicked.connect(self.next_question)
        self.button_submit.clicked.connect(self.submit_all)

        # 将所有布局组合在一起
        main_layout.addLayout(top_info_layout)
        main_layout.addLayout(middle_img_response_layout)
        # 设置主窗口布局
        self.central_widget.setLayout(main_layout)

        # 更新按钮和scroll area
        self.update_scroll_area()
        self.update_next_previous_button()

    def on_answer_selected(self):
        """
        {'question': 'xxx',
         'answers': [{'answer_content': '否（0分，结束）', 'is_end': True, 'score': 0},
                     {'answer_content': '是（10分）', 'is_end': False, 'score': 10}],
         'select_answer_idx': -1,
         'select_answer_score': 0
         }
        :return:
        """
        selected_answer = None
        selected_answer_idx = 0
        for button_idx, radio_button in enumerate(self.answers_group):
            if radio_button.isChecked():
                selected_answer = radio_button.text()
                selected_answer_idx=button_idx
                break

        # 计分、记录选项和提前结束逻辑
        if selected_answer:
            for answer in self.user_multiple_choice_questions_list[self.current_question_index]['answers']:
                if answer['answer_content'] == selected_answer:
                    self.user_multiple_choice_questions_list[self.current_question_index]['select_answer_idx'] = selected_answer_idx
                    self.user_multiple_choice_questions_list[self.current_question_index]['select_answer_score'] = int(answer['score'])
                    self.update_total_score()

                    if answer['is_end']:
                        self.button_previous.setEnabled(False)
                        self.button_next.setEnabled(False)
                        self.is_early_end= True
                        self.show_early_end_info()
                    else:
                        self.button_previous.setEnabled(True)
                        self.button_next.setEnabled(True)
                        self.is_early_end = False
                    break

    def next_question(self):
        """
        上一题按钮逻辑
        :return:
        """
        self.user_multiple_choice_questions_list[self.current_question_index]['select_answer_idx']

        if self.current_question_index < len(self.user_multiple_choice_questions_list) - 1:
            self.current_question_index += 1
            self.update_question()

    def previous_question(self):
        """
        下一题按钮逻辑
        :return:
        """
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.update_question()

    def update_question(self):
        # 更新问题显示
        self.label_question.setPlainText(f"{self.user_multiple_choice_questions_list[self.current_question_index]['question']}")
        # 更新多选项
        self.update_scroll_area()

        self.update_next_previous_button()

        self.label_question_number.setText(f'第{self.current_question_index + 1}/{len(self.user_multiple_choice_questions_list)}题')

    def update_next_previous_button(self):
        if self.current_question_index + 1 == len(self.user_multiple_choice_questions_list):
            self.button_previous.setEnabled(True)
            self.button_next.setEnabled(False)
        elif self.current_question_index == 0:
            self.button_previous.setEnabled(False)
            self.button_next.setEnabled(True)
        else:
            self.button_previous.setEnabled(True)
            self.button_next.setEnabled(True)

    def update_scroll_area(self):
        """
        {'question': 'xxx',
         'answers': [{'answer_content': '否（0分，结束）', 'is_end': True, 'score': 0},
                     {'answer_content': '是（10分）', 'is_end': False, 'score': 10}],
         'select_answer_idx': -1,
         'select_answer_score': 0
         }
        :return:
        """

        current_question_answer_dict = self.user_multiple_choice_questions_list[self.current_question_index]

        # 多选项更新逻辑
        self.scroll_content = QWidget()  # 滚动区域的内容
        self.scroll_layout = QVBoxLayout(self.scroll_content)  # 内容的布局
        self.scroll_area.setWidget(self.scroll_content)
        self.answers_group = []

        # 更新内容
        current_answers_list = current_question_answer_dict['answers']
        for answer in current_answers_list:
            current_radio_button = QRadioButton(answer['answer_content'])
            current_radio_button.setMaximumSize(self.__button_width, 30)
            current_radio_button.setStyleSheet('font-size: 16px;font-weight:bold')
            current_radio_button.clicked.connect(self.on_answer_selected)
            self.scroll_layout.addWidget(current_radio_button)
            self.answers_group.append(current_radio_button)

        # 更新radio_button状态
        for button_idx, radio_button in enumerate(self.answers_group):
            if button_idx == current_question_answer_dict['select_answer_idx']:
                radio_button.setChecked(True)
            else:
                radio_button.setChecked(False)

    def submit_all(self):
        current_select_answer_idx_list = [int(item['select_answer_idx']) for item in self.user_multiple_choice_questions_list]
        current_unlabeled_questions_idx = [question_idx+1 for question_idx, item in enumerate(current_select_answer_idx_list) if item==-1]

        if len(current_unlabeled_questions_idx) == 0 or self.is_early_end:
            # self.update_timer()
            self.timer.stop()

            self.update_total_score()
            self.show_result()
        else:
            QMessageBox.warning(self, "提示", f"还有题目{','.join(str(num) for num in current_unlabeled_questions_idx)}尚未回答，请回答完所有题目后再提交！")


    def show_result(self):
        # # previous
        # elapsed_time = self.start_time.secsTo(QDateTime.currentDateTime())
        elapsed_time = self.total_seconds

        # 更新 RECORD_USER_DICT_LIST 信息
        global RECORD_USER_DICT_LIST
        for item in RECORD_USER_DICT_LIST:
            if item["id"] ==self.__model_data_dict['id']:
                item["pointwise_score_manual"] = self.total_score
                item["manual_time"] = elapsed_time


        # 发出信号传递信息给 Window2 更新 UI 和逻辑处理
        self.submission_signal.emit(self.__model_data_dict, self.total_score, elapsed_time)

        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        result_message = f"总得分: {self.total_score} 分\n耗时: {minutes} 分钟 {seconds} 秒"
        QMessageBox.information(self, "结果", result_message)
        self.close()

    def show_early_end_info(self):
        result_message = f"选择了具有提前终止条件的选项，请提交结果或重新选择！"
        QMessageBox.information(self, "提示", result_message)

    def update_timer(self):
        current_time = QDateTime.currentDateTime()
        elapsed_time = self.start_time.secsTo(current_time)
        self.total_seconds = elapsed_time
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        self.text_timer.setText(f'计时:{minutes:02}分钟{seconds:02}秒')

    def update_total_score(self):
        self.total_score = sum([int(item['select_answer_score']) for item in self.user_multiple_choice_questions_list])
        self.total_score_label.setText(f'当前得分:{self.total_score}')

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())

    @staticmethod
    def count_characters_and_words(text):
        # 定义正则表达式模式，用于匹配中文字符、英文单词以及标点符号
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')  # 匹配所有中文字符
        english_word_pattern = re.compile(r'\b[a-zA-Z]+\b')  # 匹配所有英文单词
        punctuation_pattern = re.compile(r'[^\w\s]')  # 匹配所有非字母数字字符（即标点符号）

        # 移除文本中的标点符号
        text_without_punctuation = punctuation_pattern.sub('', text)

        # 查找所有的中文字符
        chinese_matches = chinese_pattern.findall(text_without_punctuation)
        chinese_count = sum(len(match) for match in chinese_matches)

        # 查找所有的英文单词
        english_word_matches = english_word_pattern.findall(text_without_punctuation)
        english_word_count = len(english_word_matches)

        return chinese_count, english_word_count

class ImageViewer(QGraphicsView):
    """ 图片查看器 """

    def __init__(self, image_path, parent=None):
        super().__init__(parent=parent)
        self.zoomInTimes = 0
        self.maxZoomInTimes = 22

        # 创建场景
        self.graphicsScene = QGraphicsScene()

        # 图片
        self.pixmap = QPixmap(image_path)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.displayedImageSize = QSize(0, 0)

        # 初始化小部件
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        #

        # 隐藏滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 以鼠标所在位置为锚点进行缩放
        self.setTransformationAnchor(self.AnchorUnderMouse)

        # 平滑缩放
        self.pixmapItem.setTransformationMode(Qt.SmoothTransformation)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform)

        # 设置场景
        self.graphicsScene.addItem(self.pixmapItem)
        self.setScene(self.graphicsScene)

    def wheelEvent(self, e: QWheelEvent):
        """ 滚动鼠标滚轮缩放图片 """
        if e.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    def resizeEvent(self, e):
        """ 缩放图片 """
        super().resizeEvent(e)

        if self.zoomInTimes > 0:
            return

        # 调整图片大小
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size() * ratio
        if ratio < 1:
            self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)
        else:
            self.resetTransform()

    def setImage(self, imagePath: str):
        """ 设置显示的图片 """
        self.resetTransform()

        # 刷新图片
        self.pixmap = QPixmap(imagePath)
        self.pixmapItem.setPixmap(self.pixmap)

        # 调整图片大小
        self.setSceneRect(QRectF(self.pixmap.rect()))
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size() * ratio
        if ratio < 1:
            self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)

    def resetTransform(self):
        """ 重置变换 """
        super().resetTransform()
        self.zoomInTimes = 0
        self.__setDragEnabled(False)

    def __isEnableDrag(self):
        """ 根据图片的尺寸决定是否启动拖拽功能 """
        v = self.verticalScrollBar().maximum() > 0
        h = self.horizontalScrollBar().maximum() > 0
        return v or h

    def __setDragEnabled(self, isEnabled: bool):
        """ 设置拖拽是否启动 """
        self.setDragMode(
            self.ScrollHandDrag if isEnabled else self.NoDrag)

    def __getScaleRatio(self):
        """ 获取显示的图像和原始图像的缩放比例 """
        if self.pixmap.isNull():
            return 1

        pw = self.pixmap.width()
        ph = self.pixmap.height()
        rw = min(1, self.width() / pw)
        rh = min(1, self.height() / ph)
        return min(rw, rh)

    def fitInView(self, item: QGraphicsItem, mode=Qt.KeepAspectRatio):
        """ 缩放场景使其适应窗口大小 """
        super().fitInView(item, mode)
        self.displayedImageSize = self.__getScaleRatio() * self.pixmap.size()
        self.zoomInTimes = 0

    def zoomIn(self, viewAnchor=QGraphicsView.AnchorUnderMouse):
        """ 放大图像 """
        if self.zoomInTimes == self.maxZoomInTimes:
            return

        self.setTransformationAnchor(viewAnchor)

        self.zoomInTimes += 1
        self.scale(1.1, 1.1)
        self.__setDragEnabled(self.__isEnableDrag())

        # 还原 anchor
        self.setTransformationAnchor(self.AnchorUnderMouse)

    def zoomOut(self, viewAnchor=QGraphicsView.AnchorUnderMouse):
        """ 缩小图像 """
        if self.zoomInTimes == 0 and not self.__isEnableDrag():
            return

        self.setTransformationAnchor(viewAnchor)

        self.zoomInTimes -= 1

        # 原始图像的大小
        pw = self.pixmap.width()
        ph = self.pixmap.height()

        # 实际显示的图像宽度
        w = self.displayedImageSize.width() * 1.1 ** self.zoomInTimes
        h = self.displayedImageSize.height() * 1.1 ** self.zoomInTimes

        if pw > self.width() or ph > self.height():
            # 在窗口尺寸小于原始图像时禁止继续缩小图像比窗口还小
            if w <= self.width() and h <= self.height():
                self.fitInView(self.pixmapItem)
            else:
                self.scale(1 / 1.1, 1 / 1.1)
        else:
            # 在窗口尺寸大于图像时不允许缩小的比原始图像小
            if w <= pw:
                self.resetTransform()
            else:
                self.scale(1 / 1.1, 1 / 1.1)

        self.__setDragEnabled(self.__isEnableDrag())

        # 还原 anchor
        self.setTransformationAnchor(self.AnchorUnderMouse)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # start 1
    main_window = Window1()
    main_window.show()

    signal = app.exec_()

    sys.exit(signal)
