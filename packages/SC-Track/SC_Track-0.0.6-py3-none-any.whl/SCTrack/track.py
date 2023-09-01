# coding=utf-8

from __future__ import annotations

import glob
import logging
import os.path
import time

import numpy as np

from SCTrack import reclassification
from SCTrack.utils import mask_to_json


def start_track(fannotation: str | dict, fout, basename, track_range=None, fimage=None, fbf=None,
                export_visualization=True,
                track_to_json=True):
    """
     :param track_range: Track frame number range
     :param visualize_background_image: track background image
     :param basename:
     :param fannotation: segmentation output result, json file or dict
     :param fout: Tracking output folder path
     :param fimage: raw image path, can be empty
     :param fbf: Bright field image path, can be empty
     :param export_visualization: Whether to export the tracking visualization file, if yes, it will export a multi-frame tif file
     :param track_to_json: Whether to write the tracking result into fjson, if yes, a new json file will be generated
     :return: None
    """

    if type(fannotation) is str:
        if not fannotation.endswith('.json'):
            logging.info('convert mask to annotation file...')
            annotation = mask_to_json(fannotation, xrange=track_range)
        else:
            annotation = fannotation
    else:
        annotation = fannotation

    result_save_path = os.path.join(fout, 'tracking_output')
    if not os.path.exists(result_save_path):
        os.makedirs(result_save_path)
    reclassification.run(annotation=annotation, output_dir=result_save_path, track_range=track_range, dic=fbf,
                         mcy=fimage,
                         save_visualize=export_visualization, visualize_background_image=fimage,
                         track_to_json=track_to_json, basename=basename)

#
# def run():
#     """临时批处理函数，用完删除"""
#     # dirs = ['copy_of_1_xy01', 'copy_of_1_xy19', 'MCF10A_copy02', 'MCF10A_copy11', 'src06']
#     dirs = ['MCF10A_copy02_5min']
#     base = r'G:\paper\evaluate_data\5min'
#     for i in dirs:
#         image = glob.glob(rf"{base}\{i}\mcy*.tif")[0]
#
#         annotation = rf"{base}\{i}\5-result-GT.json"
#         print(image)
#         print(annotation)
#         output = rf"{base}\{i}"
#         start_track(annotation, output, os.path.splitext(os.path.basename(image))[0], None, image,
#                     export_visualization=False)
#         # cmd = fr"python main.py -p {image} -bf {image} -tp -ns -js {annotation}"
#         # print(cmd)
#
# def run_smooth():
#     image = r'G:\paper\evaluate_data\evaluate_smoothing\copy_of_1_xy19\mcy.tif'
#     ann = r"G:\paper\evaluate_data\evaluate_smoothing\copy_of_1_xy19\10%-GT.json"
#     out = r"G:\paper\evaluate_data\evaluate_smoothing\copy_of_1_xy19"
#     start_track(ann, out, os.path.splitext(os.path.basename(image))[0], None, image,
#                 export_visualization=False)


if __name__ == '__main__':
    # run()
    # run_smooth()
    # i = 8
    # annotation = rf"G:\paper\test\Data{i}\SEG.tif"
    # mcy_img = rf"G:\paper\test\Data{i}\01.tif"
    # start_track(annotation, rf"G:\paper\test\Data{i}", 'mcy', 1000,
    #             mcy_img)

    # image = r"G:\paper\evaluate_data\incorrect-data-test\normal-dataset\copy_of_1_xy19\mcy.tif"
    # annotation = r"G:\paper\evaluate_data\incorrect-data-test\normal-dataset\copy_of_1_xy19\result.json"
    #
    # outputdir = fr"G:\paper\evaluate_data\incorrect-data-test\normal-dataset\copy_of_1_xy19"
    # start_track(annotation, outputdir, os.path.splitext(os.path.basename(image))[0], None, image, export_visualization=True)

    # image = r"G:\paper\evaluate_data\evaluate_for_tracking\parameter_test_incorrect\!test_data\rpe19.tif"
    # annotation = r"G:\paper\evaluate_data\evaluate_for_tracking\parameter_test_incorrect\!test_data\result.json"
    #
    # outputdir = fr"G:\paper\evaluate_data\evaluate_for_tracking\parameter_test_incorrect\GAP_WINDOW_LEN\10"
    # start_track(annotation, outputdir, 'rpe19', None, image, export_visualization=False)
    # for i in [0]:
    #
    #     image = fr"G:\paper\evaluate_data\evaluate_noise_classification\group{i}\mcy.tif"
    #     annotation = fr"G:\paper\evaluate_data\evaluate_noise_classification\group{i}\GT.json"
    #
    #     outputdir = fr"G:\杂项\group{i}"
    #     start_track(annotation, outputdir, 'mcy', None, image, export_visualization=False)

    # break

    annotation = r"G:\raw data\demo\GT.json"
    mcy_img = r"G:\raw data\demo\mcy.tif"
    dic_img = r"G:\raw data\demo\mcy.tif"
    start_track(annotation, r"G:\raw data\demo", 'mcy', None,
                mcy_img)
