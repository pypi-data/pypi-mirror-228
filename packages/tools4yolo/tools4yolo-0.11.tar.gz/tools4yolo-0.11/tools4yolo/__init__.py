import multiprocessing
import traceback
from math import ceil, floor
from pathlib import Path
from time import sleep
import numexpr
from PIL import Image
from a_cv_imwrite_imread_plus import (
    add_imwrite_plus_imread_plus_to_cv2,
    open_image_in_cv,
)
from functools import lru_cache
from get_rectangle_infos import get_rectangle_information
from a_cv2_easy_resize import add_easy_resize_to_cv2
from fast_color_checker import ColorCheck
from getpartofimg import get_part_of_image as _get_part_of_image
import numpy as np
import shutil
import regex
from sklearn.model_selection import train_test_split
import random
import PILasOPENCV
import cv2
import torch
import pandas as pd
import os
import subprocess
from list_all_files_recursively import get_folder_file_complete_path
import ast
from collections import defaultdict
from configparser import ConfigParser
import re
from typing import Any
from flatten_any_dict_iterable_or_whatsoever import fla_tu, set_in_original_iter
from deepcopyall import deepcopy
import sys
from rembg import remove, new_session


add_imwrite_plus_imread_plus_to_cv2()
add_easy_resize_to_cv2()
allbackgrounds = []
allimages = []


def augment_needle_images(
    folder,
    outputfolder,
    width=640,
    height=640,
):
    def get_shape_information_from_picture(
        im,
        method_bw=2,
        method0_constant_subtracted=2,
        method0_block_size=11,
        method1_kernel=(5, 5),
        method1_startthresh=127,
        method1_endthresh=255,
        invert=False,
    ):
        image = open_image_in_cv(im, channels_in_output=4)
        grayImage_konvertiert = open_image_in_cv(image.copy(), channels_in_output=2)
        if invert:
            grayImage_konvertiert = cv2.bitwise_not(grayImage_konvertiert)
        if method_bw == 0:
            threshg = cv2.adaptiveThreshold(
                grayImage_konvertiert,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                method0_block_size,
                method0_constant_subtracted,
            )
        elif method_bw == 1:
            threshg = cv2.adaptiveThreshold(
                grayImage_konvertiert,
                255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                method0_block_size,
                method0_constant_subtracted,
            )
        else:
            blur = cv2.GaussianBlur(grayImage_konvertiert.copy(), method1_kernel, 0)
            _, threshg = cv2.threshold(
                blur,
                method1_startthresh,
                method1_endthresh,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU,
            )
        output_image = np.zeros_like(image)
        output_image[:, :, 0] = threshg
        output_image[:, :, 1] = threshg
        output_image[:, :, 2] = threshg
        output_image[:, :, 3] = image[:, :, 3]  # Copy the alpha channel
        return output_image

    def convert_to_random_color(
        im,
        method_bw=0,
        method0_constant_subtracted=2,
        method0_block_size=11,
        method1_kernel=(5, 5),
        method1_startthresh=127,
        method1_endthresh=255,
        invert=False,
    ):
        image = open_image_in_cv(im, channels_in_output=4)

        output_image = get_shape_information_from_picture(
            image.copy(),
            method_bw=method_bw,
            method0_constant_subtracted=method0_constant_subtracted,
            method0_block_size=method0_block_size,
            method1_kernel=method1_kernel,
            method1_startthresh=method1_startthresh,
            method1_endthresh=method1_endthresh,
            invert=invert,
        )
        random_numbers = [0, 1, 2]
        random.shuffle(random_numbers)
        output_image[
            np.where(output_image[:, :, random_numbers[0]] <= 127)
        ] = random.randint(20, 80)
        output_image[:, :, 3] = image[:, :, 3]
        return output_image

    def convert_to_grayscale_keep_transparency(image, invert=False):
        image = open_image_in_cv(image, channels_in_output=4)
        gray_image = open_image_in_cv(image, channels_in_output=2)
        if invert:
            gray_image = cv2.bitwise_not(gray_image)
        output_image = np.zeros_like(image)
        output_image[:, :, 0] = gray_image
        output_image[:, :, 1] = gray_image
        output_image[:, :, 2] = gray_image
        output_image[:, :, 3] = image[:, :, 3]  # Copy the alpha channel
        return output_image

    def convert_to_some_random_color(image, invert=False):
        image = open_image_in_cv(image, channels_in_output=4)
        gray_image = open_image_in_cv(image, channels_in_output=2)
        if invert:
            gray_image = cv2.bitwise_not(gray_image)
        output_image = np.zeros_like(image)
        random_numbers = [0, 0, random.randint(20, 80)]
        random.shuffle(random_numbers)
        output_image[np.where(gray_image >= 100)][:, 0] = 255  # random.randint(20, 80)
        output_image[:, :, 3] = image[:, :, 3]  # Copy the alpha channel
        return output_image

    folder_path = os.path.normpath(folder)
    outputfolderx = os.path.normpath(outputfolder)
    folders = [folder_path]
    for folderpath in folders:
        allfiles = get_folder_file_complete_path(str(folderpath))
        counter = 0

        for i in allfiles:
            outputfolder = os.path.normpath(
                os.path.join(
                    outputfolderx, i.folder.replace(folder_path, "").strip("\\/")
                )
            )

            if not os.path.exists(outputfolder):
                os.makedirs(outputfolder, exist_ok=True)
            try:
                image = i.path
                imagex = resize_to_certain_percentage(
                    image,
                    percentage=0.99,
                    width=width,
                    height=height,
                )
                f1 = os.path.join(outputfolder, str(counter).zfill(6) + ".png")
                cv2.imwrite(f1, imagex)
                counter += 1

                f1 = os.path.join(outputfolder, str(counter).zfill(6) + ".png")
                cv2.imwrite(f1, open_image_in_cv(imagex.copy(), bgr_to_rgb=True))
                counter += 1

                i1 = get_shape_information_from_picture(
                    imagex.copy(),
                    method_bw=2,
                    method0_constant_subtracted=2,
                    method0_block_size=11,
                    method1_kernel=(5, 5),
                    method1_startthresh=127,
                    method1_endthresh=255,
                )
                f2 = os.path.join(outputfolder, str(counter).zfill(6) + ".png")
                cv2.imwrite(f2, i1)
                counter += 1
                i1 = get_shape_information_from_picture(
                    imagex.copy(),
                    method_bw=2,
                    method0_constant_subtracted=2,
                    method0_block_size=11,
                    method1_kernel=(5, 5),
                    method1_startthresh=127,
                    method1_endthresh=255,
                    invert=True,
                )
                f2 = os.path.join(outputfolder, str(counter).zfill(6) + ".png")
                cv2.imwrite(f2, i1)
                counter += 1

                i1 = convert_to_random_color(
                    imagex,
                    method_bw=2,
                    method0_constant_subtracted=2,
                    method0_block_size=11,
                    method1_kernel=(5, 5),
                    method1_startthresh=127,
                    method1_endthresh=255,
                    invert=False,
                )
                f2 = os.path.join(outputfolder, str(counter).zfill(6) + ".png")
                cv2.imwrite(f2, i1)
                counter += 1

                i1 = get_shape_information_from_picture(
                    imagex,
                    method_bw=1,
                    method0_constant_subtracted=2,
                    method0_block_size=11,
                    method1_kernel=(5, 5),
                    method1_startthresh=127,
                    method1_endthresh=255,
                )
                f2 = os.path.join(outputfolder, str(counter).zfill(6) + ".png")
                cv2.imwrite(f2, i1)
                counter += 1
                i1 = get_shape_information_from_picture(
                    imagex,
                    method_bw=1,
                    method0_constant_subtracted=2,
                    method0_block_size=11,
                    method1_kernel=(5, 5),
                    method1_startthresh=127,
                    method1_endthresh=255,
                    invert=True,
                )
                f2 = os.path.join(outputfolder, str(counter).zfill(6) + ".png")
                cv2.imwrite(f2, i1)
                counter += 1
                i1 = get_shape_information_from_picture(
                    imagex,
                    method_bw=2,
                    method0_constant_subtracted=2,
                    method0_block_size=11,
                    method1_kernel=(5, 5),
                    method1_startthresh=127,
                    method1_endthresh=255,
                )
                f2 = os.path.join(outputfolder, str(counter).zfill(6) + ".png")
                cv2.imwrite(f2, i1)
                counter += 1
                i1 = get_shape_information_from_picture(
                    imagex,
                    method_bw=2,
                    method0_constant_subtracted=2,
                    method0_block_size=11,
                    method1_kernel=(5, 5),
                    method1_startthresh=127,
                    method1_endthresh=255,
                    invert=True,
                )
                f2 = os.path.join(outputfolder, str(counter).zfill(6) + ".png")
                cv2.imwrite(f2, i1)
                counter += 1

                i2 = convert_to_grayscale_keep_transparency(imagex.copy())
                f3 = os.path.join(outputfolder, str(counter).zfill(6) + ".png")
                cv2.imwrite(f3, i2)
                counter += 1

                i2 = convert_to_some_random_color(imagex.copy())
                f3 = os.path.join(outputfolder, str(counter).zfill(6) + ".png")
                cv2.imwrite(f3, i2)
                counter += 1

                i2 = convert_to_grayscale_keep_transparency(imagex.copy(), invert=True)
                f3 = os.path.join(outputfolder, str(counter).zfill(6) + ".png")
                cv2.imwrite(f3, i2)
                counter += 1
            except Exception as fe:
                pfehler()
                continue


def pfehler():
    etype, value, tb = sys.exc_info()
    traceback.print_exception(etype, value, tb)


def remove_background_and_resize(folder, folderout, maxwidth=640, maxheight=640):
    allsavedpics = []
    session = new_session()
    if not os.path.exists(folderout):
        os.makedirs(folderout, exist_ok=True)
    ini = 0
    for file in Path(folder).glob("*.*"):
        input_path = str(file)
        output_path = os.path.join(folderout, str(ini) + ".png")

        try:
            input = Image.open(input_path)
        except Exception as fe:
            pfehler()
            continue
        output = remove(input, session=session)
        try:
            input_path = cut_transparent_border(np.array(output))
        except Exception as fe:
            pfehler()

            continue
        image = resize_to_certain_percentage(
            input_path,
            percentage=1,
            width=maxwidth,
            height=maxheight,
        )
        imagex = cv2.imread_plus(image, bgr_to_rgb=False, channels_in_output=4)
        imagex = cut_transparent_border(imagex)
        imagenew = Image.fromarray(imagex)
        imagenew.save(output_path)
        allsavedpics.append(output_path)
        ini += 1
    return allsavedpics


def parse_data_from_config_file(cfgfile):
    nested_dict = lambda: defaultdict(nested_dict)

    def load_config_file_vars(
        cfgfile: str, onezeroasboolean: bool = False
    ) -> tuple[Any, list[Any]]:
        pars2 = ConfigParser()
        pars2.read(cfgfile)

        (
            cfgdictcopy,
            cfgdictcopyaslist,
        ) = copy_dict_and_convert_values(pars2, onezeroasboolean=onezeroasboolean)
        return (
            cfgdictcopy,
            cfgdictcopyaslist,
        )

    def copy_dict_and_convert_values(
        pars: ConfigParser, onezeroasboolean: bool = False
    ):
        copieddict = deepcopy(pars.__dict__["_sections"])
        flattli = fla_tu(pars.__dict__["_sections"])
        for value, keys in flattli:
            if not re.search(r"^(?:[01])$", str(value)):
                try:
                    valuewithdtype = pars.getboolean(*keys)
                except Exception:
                    try:
                        valuewithdtype = ast.literal_eval(pars.get(*keys))
                    except Exception:
                        valuewithdtype = pars.get(*keys)
            else:
                if onezeroasboolean:
                    valuewithdtype = pars.getboolean(*keys)
                else:
                    valuewithdtype = ast.literal_eval(pars.get(*keys))

            set_in_original_iter(iterable=copieddict, keys=keys, value=valuewithdtype)

        g = list(fla_tu(copieddict))
        return copieddict, g

    (
        cfgdictcopy,
        cfgdictcopyaslist,
    ) = load_config_file_vars(cfgfile=cfgfile, onezeroasboolean=False)
    allto = []
    for key, item in cfgdictcopy.items():
        allto.append(list(item.values()))
    return allto, cfgdictcopyaslist


def start_yolov5_training(
    cfgfile,
    ptfile,
    generate_images=True,
    train_model=True,
    model_file="yolov5s.yaml",
    hypfile="hyp.scratch-low.yaml",
    batch=5,
    epochs=4,
    workers=2,
    save_period=10,
    cache="disk",
):
    allto, cfgdictcopyaslist = parse_data_from_config_file(cfgfile=cfgfile)
    outputfolder = ([x[0] for x in cfgdictcopyaslist if x[-1][-1] == "outputfolder"])[0]
    yamlfile = ([x[0] for x in cfgdictcopyaslist if x[-1][-1] == "personal_yaml_file"])[
        0
    ]
    image_size_width = (
        [x[0] for x in cfgdictcopyaslist if x[-1][-1] == "image_size_width"]
    )[0]
    yolovyamel = os.path.normpath(
        os.path.join(outputfolder, "dataset", "splitset", yamlfile)
    )
    name_for_set = yolovyamel.split(".")[0]
    if generate_images:
        psw(allto)
    if train_model:
        start_training(
            model_file=model_file,
            hypfile=hypfile,
            yolovyamel=yolovyamel,
            ptfile=ptfile,
            name_for_set=name_for_set,
            resolutionsize=image_size_width,
            batch=batch,
            epochs=epochs,
            workers=workers,
            save_period=save_period,
            cache=cache,
        )


def get_results_as_df(path_or_np, models, confidence_thresh):
    asnumpy = open_image_in_cv(path_or_np, channels_in_output=3)
    allresu = []
    for model in models:
        try:
            results = model(asnumpy)
            df = pd.concat(results.pandas().xywhn)
            df = df.rename(
                columns={
                    "xcenter": "aa_center_x",
                    "ycenter": "aa_center_y",
                    "width": "aa_width",
                    "height": "aa_heigth",
                    "confidence": "aa_confidence",
                    "class": "aa_id",
                    "name": "aa_name",
                }
            )
            df["aa_img_width"] = asnumpy.shape[1]
            df["aa_img_height"] = asnumpy.shape[0]
            df["aa_img_abs_center_y"] = df.aa_img_height * df.aa_center_y
            df["aa_img_abs_center_y"] = df["aa_img_abs_center_y"].astype("int")
            df["aa_img_abs_center_x"] = df.aa_img_width * df.aa_center_x
            df["aa_img_abs_center_x"] = df["aa_img_abs_center_x"].astype("int")
            df["aa_img_abs_width"] = df.aa_img_width * df.aa_width
            df["aa_img_abs_width"] = df["aa_img_abs_width"].astype(int)
            df["aa_img_abs_height"] = df.aa_img_height * df.aa_heigth
            df["aa_img_abs_height"] = df["aa_img_abs_height"].astype(int)
            df["aa_haystack_start_x"] = (
                df.aa_img_abs_center_x - df.aa_img_abs_width // 2
            )
            df["aa_haystack_end_x"] = df.aa_img_abs_center_x + df.aa_img_abs_width // 2
            df["aa_haystack_start_y"] = (
                df.aa_img_abs_center_y - df.aa_img_abs_height / 2
            )
            df["aa_haystack_end_y"] = df.aa_img_abs_center_y + df.aa_img_abs_height // 2
            df.aa_haystack_start_y = df.aa_haystack_start_y.astype(int)
            df = df.loc[df.aa_confidence >= confidence_thresh].copy()
            allresu.append(df.copy())
        except Exception as fe:
            pfehler()

    try:
        df = (
            pd.concat(allresu, ignore_index=True, axis=0)
            .drop_duplicates()
            .reset_index()
        )
    except Exception as fe:
        df = allresu[0].drop_duplicates().reset_index()
        pfehler()

    return df


def yolov5_detection(
    models, images, confidence_thresh=0.05, bgr_to_rgb=True, draw_output=True
):
    if not isinstance(images, (list, tuple)):
        images = [images]
    allresults = []
    for indi, image in enumerate(images):
        try:
            sshot = open_image_in_cv(image, channels_in_output=3, bgr_to_rgb=bgr_to_rgb)
            df = get_results_as_df(
                path_or_np=sshot.copy(),
                models=models,
                confidence_thresh=confidence_thresh,
            )

            if draw_output:
                bi = PILasOPENCV.fromarray(
                    open_image_in_cv(
                        sshot.copy(), channels_in_output=3, bgr_to_rgb=not bgr_to_rgb
                    )
                )
                ba = PILasOPENCV.ImageDraw(bi)

                for key, item in df.iterrows():
                    if item.aa_confidence < confidence_thresh:
                        continue
                    r_, g_, b_ = (
                        random.randrange(50, 255),
                        random.randrange(50, 255),
                        random.randrange(50, 255),
                    )
                    print(df)
                    ba.rectangle(
                        xy=(
                            (item.aa_haystack_start_x, item.aa_haystack_start_y),
                            (item.aa_haystack_end_x, item.aa_haystack_end_y),
                        ),
                        outline="black",
                        width=4,
                    )
                    ba.rectangle(
                        xy=(
                            (item.aa_haystack_start_x, item.aa_haystack_start_y),
                            (item.aa_haystack_end_x, item.aa_haystack_end_y),
                        ),
                        outline=(r_, g_, b_),
                        width=2,
                    )
                    ba.text(
                        xy=((item.aa_haystack_start_x, item.aa_haystack_start_y + 10)),
                        text=f"{str(item.aa_confidence)} - {item.aa_name}",
                        fill="black",
                        font=cv2.FONT_HERSHEY_SIMPLEX,
                        scale=0.50,
                        thickness=3,
                    )
                    ba.text(
                        xy=((item.aa_haystack_start_x, item.aa_haystack_start_y + 10)),
                        text=f"{str(item.aa_confidence)} - {item.aa_name}",
                        fill=(r_, g_, b_),
                        font=cv2.FONT_HERSHEY_SIMPLEX,
                        scale=0.50,
                        thickness=1,
                    )
                allresults.append([df, bi.getim()])
            else:
                allresults.append([df, sshot])
        except Exception as fe:
            pfehler()

    return allresults


def load_torchmodel(ptfiles, repo_or_dir="./yolov5", model="custom", source="local"):
    if not isinstance(ptfiles, (list, tuple)):
        ptfiles = [ptfiles]
    models = []
    for ptfile in ptfiles:
        models.append(
            torch.hub.load(
                repo_or_dir,
                model,
                ptfile,
                source=source,
            )
        )
    return models


class Yolov5Detect:
    def __init__(
        self, modelfiles, repo_or_dir="./yolov5", model="custom", source="local"
    ):
        self.models = load_torchmodel(
            ptfiles=modelfiles, repo_or_dir=repo_or_dir, model=model, source=source
        )

    def detect(
        self,
        images,
        confidence_thresh=0.01,
        bgr_to_rgb=True,
        draw_output=True,
        save_folder=None,
    ):
        allimsresults = yolov5_detection(
            models=self.models,
            images=images,
            confidence_thresh=confidence_thresh,
            bgr_to_rgb=bgr_to_rgb,
            draw_output=draw_output,
        )
        if save_folder:
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            for ini, b in enumerate(allimsresults):
                df, bi = b
                cv2.imwrite(os.path.join(save_folder, str(ini).zfill(8) + ".png"), bi)

        return allimsresults


def start_training(
    model_file,
    hypfile,
    yolovyamel,
    ptfile,
    name_for_set,
    resolutionsize=640,
    batch=20,
    epochs=25,
    workers=2,
    save_period=10,
    cache="disk",
):
    allyolofiles = [
        x.path
        for x in get_folder_file_complete_path(os.path.dirname(sys.executable))
        if "yolo" in x.path.lower()
    ]

    trainpy = [x for x in allyolofiles if rf"yolov5{os.sep}train.py" in x][0]
    nanomodel = [x for x in allyolofiles if rf"models{os.sep}{model_file}" in x][0]
    hypfile = [x for x in allyolofiles if hypfile in x][0]
    wholec = [
        trainpy,
        "--img",
        str(resolutionsize),
        "--cfg",
        nanomodel,
        "--hyp",
        hypfile,
        "--batch",
        str(batch),
        "--epochs",
        str(epochs),
        "--data",
        yolovyamel,
        "--weights",
        ptfile,
        "--workers",
        str(workers),
        "--name",
        name_for_set,
        "--save-period",
        str(save_period),
        "--cache",
        str(cache),
    ]
    cmd = subprocess.list2cmdline(wholec)
    wholecommand = f'start "" "{sys.executable}" {cmd}'
    print(wholecommand)
    p = subprocess.Popen(
        wholecommand, shell=True, env=os.environ.copy(), cwd=os.getcwd()
    )


def distort_image(image, percentx=0.05, percenty=0.05):
    image = cv2.imread_plus(image, channels_in_output=4)
    format_1x4 = (0, 0, image.shape[1], image.shape[0])
    rec = get_rectangle_information(rect=format_1x4)
    recfor = rec.format_4x2
    format_1x41 = format_1x4
    rec2 = get_rectangle_information(rect=format_1x41)
    recfor2 = rec2.format_4x2
    original_points = np.float32(recfor)
    nfloa = np.float32(recfor2)
    distorted_points = nfloa * (1 - (percentx + percenty) * 2)
    distorted_points[0][0] += random.randint(0, int(image.shape[1] * percentx))
    distorted_points[0][1] += random.randint(0, int(image.shape[1] * percenty))
    distorted_points[1][0] += random.randint(0, int(image.shape[1] * percentx))
    distorted_points[1][1] += random.randint(0, int(image.shape[1] * percenty))
    distorted_points[2][0] += random.randint(0, int(image.shape[1] * percentx))
    distorted_points[2][1] += random.randint(0, int(image.shape[1] * percenty))
    distorted_points[3][0] += random.randint(0, int(image.shape[1] * percentx))
    distorted_points[3][1] += random.randint(0, int(image.shape[1] * percenty))
    perspective_matrix = cv2.getPerspectiveTransform(original_points, distorted_points)
    distorted_image = cv2.warpPerspective(
        image, perspective_matrix, (image.shape[1], image.shape[0])
    )
    box = (
        floor(np.min(distorted_points[..., 0])),
        ceil(np.min(distorted_points[..., 1])),
        floor(np.max(distorted_points[..., 0])),
        ceil(np.max(distorted_points[..., 1])),
    )
    distorted_imagecropped = distorted_image[box[1] : box[3], box[0] : box[2]]
    return box, distorted_imagecropped


def add_transparency_distortion(
    img,
    min_tranparency,
    max_tranparency,
):
    cv2.imread_plus(img, channels_in_output=4)
    im = img.copy()
    im[..., 3:4] = np.random.randint(
        min_tranparency, max_tranparency, im[..., 3:4].shape
    )

    bu = img[..., 3]

    im[..., 3][(numexpr.evaluate("(bu==0)", global_dict={}, local_dict={"bu": bu}))] = 0
    return im


def overlay_pic(background, overlay):
    background = cv2.imread_plus(background, channels_in_output=4)

    overlay = cv2.imread_plus(overlay, channels_in_output=4)

    if overlay.shape[0] >= background.shape[0]:
        background = cv2.easy_resize_image(
            background,
            width=None,
            height=overlay.shape[0] * 2,
            percent=None,
            interpolation=cv2.INTER_AREA,
        )
    if overlay.shape[1] >= background.shape[1]:
        background = cv2.easy_resize_image(
            background,
            width=overlay.shape[1] * 2,
            height=None,
            percent=None,
            interpolation=cv2.INTER_AREA,
        )
    for _ in range(10):
        overlay_height, overlay_width, _ = overlay.shape
        x_position = random.randint(0, background.shape[1] - overlay.shape[1])
        y_position = random.randint(0, background.shape[0] - overlay.shape[0])

        x_end = x_position + overlay_width
        y_end = y_position + overlay_height

        o1 = overlay[:, :, :3]
        o2 = background[y_position:y_end, x_position:x_end, :3]

        meancolor0 = o1[..., 0]
        meancolor1 = o1[..., 1]
        meancolor2 = o1[..., 2]

        meancolor1_0 = o2[..., 0]
        meancolor1_1 = o2[..., 1]
        meancolor1_2 = o2[..., 2]
        ll1 = numexpr.evaluate(
            r"((abs(meancolor0-meancolor1_0))< 80) & ((abs(meancolor1-meancolor1_1))< 80) & ((abs(meancolor2-meancolor1_2))< 80)",
            global_dict={},
            local_dict={
                "meancolor0": meancolor0,
                "meancolor1": meancolor1,
                "meancolor2": meancolor2,
                "meancolor1_0": meancolor1_0,
                "meancolor1_1": meancolor1_1,
                "meancolor1_2": meancolor1_2,
            },
        )
        l1 = len(np.where(ll1)[0])
        l2 = (o2.shape[0] * o2.shape[1]) // 10
        if l1 > l2:
            continue
        else:
            break
    else:
        return (None, None, None, None), None

    o0 = overlay[:, :, 3:4]
    alpha_front = numexpr.evaluate("o0 / 255", global_dict={}, local_dict={"o0": o0})
    alpha_ba = background[y_position:y_end, x_position:x_end, 3:4]
    alpha_back = numexpr.evaluate(
        "alpha_ba / 255", global_dict={}, local_dict={"alpha_ba": alpha_ba}
    )

    background[y_position:y_end, x_position:x_end, :3] = numexpr.evaluate(
        """alpha_front * o1 + (1 - alpha_front) * o2""",
        global_dict={},
        local_dict={"alpha_front": alpha_front, "o1": o1, "o2": o2},
    )

    background[y_position:y_end, x_position:x_end, 3:4] = numexpr.evaluate(
        """(alpha_front + alpha_back) / (1 + alpha_front * alpha_back) * 255""",
        global_dict={},
        local_dict={"alpha_front": alpha_front, "alpha_back": alpha_back},
    )

    x_center = (x_position + x_end) / (2 * background.shape[1])
    y_center = (y_position + y_end) / (2 * background.shape[0])
    width = overlay_width / background.shape[1]
    height = overlay_height / background.shape[0]

    return (x_center, y_center, width, height), background


def canny_edge_blur(image, threshold1=10, threshold2=90, blur=((55, 55), 0)):
    image = cv2.imread_plus(image, channels_in_output=4)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray_image, threshold1=threshold1, threshold2=threshold2)

    blurred_image = cv2.GaussianBlur(image, *blur)

    mask = np.zeros_like(image)
    mask[
        numexpr.evaluate("""edges != 0""", global_dict={}, local_dict={"edges": edges})
    ] = 255
    ma1 = cv2.bitwise_and(image, cv2.bitwise_not(mask))
    ma2 = cv2.bitwise_and(blurred_image, mask)
    result = numexpr.evaluate(
        """ma1 + ma2""", global_dict={}, local_dict={"ma1": ma1, "ma2": ma2}
    )
    return result


def add_pixxelborder(img, loop=10, add_each_loop=2):
    image = cv2.imread_plus(img, channels_in_output=4)
    imageold = image.copy()
    looppercentage = loop
    loop = int(img.shape[0] / 100 * loop)
    if loop < 2:
        loop = 2
    image0 = img.copy()
    ending = ceil(255 / loop)
    try:
        for x in range(loop):
            x = x + add_each_loop
            bord = image0[:, :, 3][x : x + 1]
            test = random.randrange(x, x * ending) * np.random.random_sample(
                bord.shape
            ) + random.randrange(x, x * ending) * np.random.random_sample(bord.shape)
            test[
                numexpr.evaluate(
                    "test > 255", global_dict={}, local_dict={"test": test}
                )
            ] = 255
            test = test.astype(np.uint8)
            image0[:, :, 3][x : x + 1] = test
            image0[:, :, 3][image0.shape[0] - x - 1 : image0.shape[0] - x] = test
        image0 = np.rot90(image0)
        loop = looppercentage
        loop = int(image0.shape[0] / 100 * loop)
        if loop < 2:
            loop = 2
        ending = ceil(255 / loop)
        for x in range(loop):
            x = x + add_each_loop
            bord = image0[:, :, 3][x : x + 1]
            test = random.randrange(x, x * ending) * np.random.random_sample(
                bord.shape
            ) + random.randrange(x, x * ending) * np.random.random_sample(bord.shape)
            test[
                numexpr.evaluate(
                    "test > 255", global_dict={}, local_dict={"test": test}
                )
            ] = 255
            test = test.astype(np.uint8)
            image0[:, :, 3][x : x + 1] = test
            image0[:, :, 3][image0.shape[0] - x - 1 : image0.shape[0] - x] = test
        image0 = np.rot90(image0, k=3)
        imol = imageold[..., 3]
        image0[..., 3][
            (numexpr.evaluate("imol == 0", global_dict={}, local_dict={"imol": imol}))
        ] = 0
        image0[:, :, 3][..., :2] = 0
        image0[:, :, 3][..., -2:] = 0
        image0[:, :, 3][:2] = 0
        image0[:, :, 3][-2:] = 0

        return image0

    except ValueError:
        return add_pixxelborder(
            img=imageold, loop=looppercentage - 1, add_each_loop=add_each_loop
        )


def blur_borders_keep_transparency(
    im,
    y0=0.11,
    y1=0.21,
    x0=0.20,
    x1=0.30,
    blur=((55, 55), 0),
    borderType=cv2.BORDER_DEFAULT,
):
    imageall = cv2.imread_plus(im, channels_in_output=4)
    image = imageall[:, :, :3]
    alpha_channel = imageall[:, :, 3]

    mask = np.zeros_like(image, dtype=np.uint8)
    mask[: ceil(image.shape[0] * y0), :, :] = 255
    mask[-ceil(image.shape[0] * y1) :, :, :] = 255
    mask[:, : ceil(image.shape[1] * x0), :] = 255
    mask[:, -ceil(image.shape[1] * x1) :, :] = 255

    blurred_borders = cv2.GaussianBlur(image, *blur, borderType=borderType)

    ma1 = cv2.bitwise_and(image, cv2.bitwise_not(mask))
    ma2 = cv2.bitwise_and(blurred_borders, mask)
    result = numexpr.evaluate(
        """ma1 + ma2""", global_dict={}, local_dict={"ma1": ma1, "ma2": ma2}
    )

    return np.dstack((result, alpha_channel))


def blur_borders(
    im,
    y0=0.11,
    y1=0.21,
    x0=0.20,
    x1=0.30,
    blur=((55, 55), 0),
    borderType=cv2.BORDER_DEFAULT,
):
    image = cv2.imread_plus(im, channels_in_output=4)

    mask = np.zeros_like(image, dtype=np.uint8)
    mask[: ceil(image.shape[0] * y0), :, :] = 255
    mask[-ceil(image.shape[0] * y1) :, :, :] = 255
    mask[:, : ceil(image.shape[1] * x0), :] = 255
    mask[:, -ceil(image.shape[1] * x1) :, :] = 255

    blurred_borders = cv2.GaussianBlur(image, *blur, borderType=borderType)

    ma1 = cv2.bitwise_and(image, cv2.bitwise_not(mask))
    ma2 = cv2.bitwise_and(blurred_borders, mask)
    result = numexpr.evaluate(
        """ma1 + ma2""", global_dict={}, local_dict={"ma1": ma1, "ma2": ma2}
    )

    return result


def blur_image_keep_transparency(image, blur=((55, 55), 0)):
    image = cv2.imread_plus(image, channels_in_output=4)
    rgb_channels = image[:, :, :3]
    alpha_channel = image[:, :, 3]
    blurred_image = cv2.GaussianBlur(rgb_channels, *blur)
    return np.dstack((blurred_image, alpha_channel))


def blur_image(image, blur=((55, 55), 0)):
    image = cv2.imread_plus(image, channels_in_output=4)
    blurred_image = cv2.GaussianBlur(image, *blur)
    return blurred_image


def random_crop(
    image,
    min_y=0.001,
    max_y=0.008,
    min_x=0.001,
    max_x=0.008,
):
    image = cv2.imread_plus(image, channels_in_output=4)

    random_percentage_x = random.uniform(min_x, max_x)
    random_percentage_y = random.uniform(min_y, max_y)

    crop_height = ceil(abs(image.shape[0] - (image.shape[0] * random_percentage_y)))
    crop_width = ceil(abs(image.shape[1] - (image.shape[1] * random_percentage_x)))

    max_x = image.shape[1] - crop_width
    max_y = image.shape[0] - crop_height

    start_x = np.random.randint(0, max_x + 1)
    start_y = np.random.randint(0, max_y + 1)

    cropped_image = image[
        start_y : start_y + crop_height, start_x : start_x + crop_width
    ]
    return cropped_image


def hue_shift_keep_transparency(image, hue_shift=20):
    image = cv2.imread_plus(image, channels_in_output=4)
    alpha_channel = image[:, :, 3]
    hsv_image = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2HSV)
    hsvi = hsv_image[:, :, 0]
    hsv_image[:, :, 0] = numexpr.evaluate(
        "(hsvi + hue_shift) % 180",
        global_dict={},
        local_dict={"hsvi": hsvi, "hue_shift": hue_shift},
    )

    color_adjusted_bgr = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    return np.dstack((color_adjusted_bgr, alpha_channel))


def hue_shift(image, hue_shift=20):
    image = cv2.imread_plus(image, channels_in_output=4)

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hsvi = hsv_image[:, :, 0]
    hsv_image[:, :, 0] = numexpr.evaluate(
        "(hsvi + hue_shift) % 180",
        global_dict={},
        local_dict={"hsvi": hsvi, "hue_shift": hue_shift},
    )

    color_adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return color_adjusted_image


def random_resize(image, addtox=0.1, addtoy=0.3):
    image = cv2.imread_plus(image, channels_in_output=4)
    return cv2.easy_resize_image(
        image,
        width=image.shape[1] + int(image.shape[1] * addtox),
        height=image.shape[0] + int(image.shape[0] * addtoy),
        percent=None,
        interpolation=cv2.INTER_AREA,
    )


def cut_transparent_border(image):
    image = cv2.imread_plus(image, channels_in_output=4)

    bu = image[:, :, 3]
    non_transparent_coords = np.argwhere(
        numexpr.evaluate("bu > 100", global_dict={}, local_dict={"bu": bu})
    )

    min_row, min_col = np.min(non_transparent_coords, axis=0)
    max_row, max_col = np.max(non_transparent_coords, axis=0)

    return image[min_row : max_row + 1, min_col : max_col + 1]


def rotate_image(image, rotation_angle=45):
    image = cv2.imread_plus(image, channels_in_output=4)

    height, width = image.shape[:2]

    rotation_matrix = cv2.getRotationMatrix2D(
        (width / 2, height / 2), rotation_angle, 1
    )

    cos_theta = np.abs(rotation_matrix[0, 0])
    sin_theta = np.abs(rotation_matrix[0, 1])
    new_width = int((width * cos_theta) + (height * sin_theta))
    new_height = int((width * sin_theta) + (height * cos_theta))

    rotation_matrix[0, 2] += (new_width - width) / 2
    rotation_matrix[1, 2] += (new_height - height) / 2

    rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height))

    return rotated_image


def change_contrast(image, contrast_factor=1.5):
    image = cv2.imread_plus(image, channels_in_output=4)
    contimage = numexpr.evaluate(
        "image * contrast_factor",
        global_dict={},
        local_dict={"image": image, "contrast_factor": contrast_factor},
    )
    adjusted_image = np.clip(contimage, 0, 255).astype(np.uint8)
    bu = image[..., 3]
    adjusted_image[..., 3][
        numexpr.evaluate("bu==0", global_dict={}, local_dict={"bu": bu})
    ] = 0
    return adjusted_image


def sharpen_image(image, blur=((55, 55), 0), add_weighted=(4.5, -1.05)):
    image = cv2.imread_plus(image, channels_in_output=4)

    blurred_image = blur_image_keep_transparency(image, blur=blur)

    sharpened_image = cv2.addWeighted(
        image, add_weighted[0], blurred_image, add_weighted[1], 0
    )
    bu = image[..., 3]
    sharpened_image[..., 3][
        numexpr.evaluate("bu==0", global_dict={}, local_dict={"bu": bu})
    ] = 0
    return sharpened_image


def get_part_of_image(image, width=640, height=640):
    image = cv2.imread_plus(image, channels_in_output=4)

    return _get_part_of_image(
        image=image, width=width, height=height, allow_resize=True
    )


def get_random_size_between(
    width,
    height,
    min_width=500,
    max_width=640,
    min_height=500,
    max_height=640,
):
    if height <= max_height or width <= max_width:
        while height <= random.uniform(
            min_height, max_height
        ) or width <= random.uniform(min_width, max_width):
            height = height * 1.01

            width = width * 1.01

    while height >= random.uniform(min_height, max_height) or width >= random.uniform(
        min_width, max_width
    ):
        height = height * 0.99

        width = width * 0.99
    return int(width), int(height)


def resize_to_certain_percentage(
    image,
    percentage=0.3,
    width=640,
    height=640,
):
    image = cv2.imread_plus(image, channels_in_output=4)

    newwidth, newheight = get_random_size_between(
        image.shape[1],
        image.shape[0],
        min_width=int(percentage * width),
        max_width=width,
        min_height=int(percentage * height),
        max_height=height,
    )

    image = cv2.easy_resize_image(
        image.copy(),
        width=newwidth,
        height=newheight,
        percent=None,
        interpolation=cv2.INTER_AREA,
    )

    return image


def create_folder_structure(outputfolder):
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)
    datasetfolder = os.path.join(outputfolder, "dataset")
    if not os.path.exists(datasetfolder):
        os.makedirs(datasetfolder)
    imagefolder = os.path.join(datasetfolder, "images")
    if not os.path.exists(imagefolder):
        os.makedirs(imagefolder)
    labelsfolder = os.path.join(datasetfolder, "labels")
    if not os.path.exists(labelsfolder):
        os.makedirs(labelsfolder)
    backgroundfolder = os.path.join(outputfolder, "background")
    if not os.path.exists(backgroundfolder):
        os.makedirs(backgroundfolder)
    return [
        os.path.normpath(p)
        for p in [datasetfolder, imagefolder, labelsfolder, backgroundfolder]
    ]


def open_image_cached(path, cut_border=False, count_cors=False):
    image = cv2.imread_plus(path, channels_in_output=4)
    if cut_border:
        image = cut_transparent_border(image)
    if not count_cors:
        return image
    return image, count_colors(image)


@lru_cache(maxsize=4096)
def open_image_cached2(
    path, image_size_width, image_size_height, cut_border=False, count_cors=False
):
    image = cv2.imread_plus(path, channels_in_output=4)
    if cut_border:
        image = cut_transparent_border(image)
    newwidth, newheight = get_random_size_between(
        image.shape[1],
        image.shape[0],
        min_width=int(0.98 * image_size_width),
        max_width=image_size_width,
        min_height=int(0.98 * image_size_width),
        max_height=image_size_height,
    )

    image = cv2.easy_resize_image(
        image,
        width=newwidth,
        height=newheight,
        percent=None,
        interpolation=cv2.INTER_AREA,
    )
    if not count_cors:
        return image
    return image, count_colors(image)


def crop_list_of_images(qty, input_folder, outputfolder, width=640, height=640):
    (
        datasetfolder,
        imagefolder,
        labelsfolder,
        backgroundfolder,
    ) = create_folder_structure(outputfolder)
    allims = get_folder_file_complete_path(folders=input_folder)
    i = 0
    allbackgrounds = []
    backgroundthere = 1
    while qty > i:
        try:
            img = random.choice(allims)
            image = open_image_cached(img.path)
            imgc = get_part_of_image(image, width=width, height=height)
            p = os.path.normpath(
                os.path.join(backgroundfolder, str(backgroundthere) + ".png")
            )
            while os.path.exists(p):
                backgroundthere += 1
                p = os.path.normpath(
                    os.path.join(backgroundfolder, str(backgroundthere) + ".png")
                )
            cv2.imwrite(p, imgc)
            i = i + 1
            allbackgrounds.append(p)
        except Exception:
            continue
    return allbackgrounds


def do_or_dont(percentage):
    neg = 100 - percentage
    return random.choice([True] * percentage + [False] * neg)


def needle_blur_image_kernel_function(x1min, x1max):
    x = (
        (q := random.randint(x1min, x1max), q),
        0,
    )
    while x[0][0] % 2 == 0:
        x = (
            (q := random.randint(x1min, x1max), q),
            0,
        )
    return x


def count_colors(img):
    img = cv2.imread_plus(img, channels_in_output=4)
    pic = ColorCheck(img)
    alc = pic.count_all_colors()
    return alc


def replace_color(
    img,
    alc,
    percentage,
    colors_to_change_r_min,
    colors_to_change_r_max,
    colors_to_change_g_min,
    colors_to_change_g_max,
    colors_to_change_b_min,
    colors_to_change_b_max,
):
    img = cv2.imread_plus(img, channels_in_output=4)
    image = img.copy()
    allpix = np.multiply(*img.shape[:2])
    minpixl = int((allpix / 100) * percentage)
    colorstochange = []
    totalv = 0
    for pix in alc:
        if pix[1] > 1000:
            colorstochange.append(pix[0])
        totalv = totalv + pix[1]
        if totalv >= minpixl:
            break
    for color in colorstochange:
        randomcolor = (
            random.randint(colors_to_change_b_min, colors_to_change_b_max),
            random.randint(colors_to_change_g_min, colors_to_change_g_max),
            random.randint(colors_to_change_r_min, colors_to_change_r_max),
            255,
        )
        r = img[..., 2]
        g = img[..., 1]
        b = img[..., 0]
        r1, g1, b1 = color
        (
            img[
                numexpr.evaluate(
                    """(r == r1) & (g == g1) & (b == b1)""",
                    global_dict={},
                    local_dict={"r": r, "r1": r1, "g": g, "g1": g1, "b": b, "b1": b1},
                )
            ]
        ) = randomcolor
    img[..., 3] = image[..., 3]
    return img


def move_files_to_folder(list_of_files, destination_folder, concatfolder):
    destination_folder = os.path.join(concatfolder, destination_folder)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except Exception as fe:
            pfehler()
            print(f"{fe}", end="\r")
            continue
    return regex.sub(r"[\\/]+", "/", destination_folder).rstrip("/") + "/"


def flip_image_left_right(img):
    img = cv2.imread_plus(img, channels_in_output=4)
    mirrored_image = cv2.flip(img, 1)
    return mirrored_image


def flip_image_up_down(img):
    img = cv2.imread_plus(img, channels_in_output=4)
    mirrored_image = cv2.flip(img, 1)
    return mirrored_image


def generate_args(
    outputfolder,
    image_size_width,
    image_size_height,
    needle_size_percentage_min,
    needle_size_percentage_max,
    blur_image_kernel_min,
    blur_image_kernel_max,
    blur_image_frequency,
    sharpen_image_kernel_min,
    sharpen_image_kernel_max,
    sharpen_image_frequency,
    distorted_resizing_add_min_x,
    distorted_resizing_add_max_x,
    distorted_resizing_add_min_y,
    distorted_resizing_add_max_y,
    distorted_resizing_frequency,
    blur_borders_min_x0,
    blur_borders_max_x0,
    blur_borders_min_x1,
    blur_borders_max_x1,
    blur_borders_min_y0,
    blur_borders_max_y0,
    blur_borders_min_y1,
    blur_borders_max_y1,
    blur_borders_kernel_min,
    blur_borders_kernel_max,
    blur_borders_frequency,
    pixelborder_min,
    pixelborder_max,
    pixelborder_loop_min,
    pixelborder_loop_max,
    pixelborder_frequency,
    perspective_distortion_min_x,
    perspective_distortion_max_x,
    perspective_distortion_min_y,
    perspective_distortion_max_y,
    perspective_distortion_percentage,
    transparency_distortion_min,
    transparency_distortion_max,
    transparency_distortion_frequency,
    canny_edge_blur_thresh_lower_min,
    canny_edge_blur_thresh_lower_max,
    canny_edge_blur_thresh_upper_min,
    canny_edge_blur_thresh_upper_max,
    canny_edge_blur_kernel_min,
    canny_edge_blur_kernel_max,
    canny_edge_blur_frequency,
    random_crop_min_x,
    random_crop_max_x,
    random_crop_min_y,
    random_crop_max_y,
    random_crop_frequency,
    hue_shift_min,
    hue_shift_max,
    hue_shift_frequency,
    change_contrast_min,
    change_contrast_max,
    change_contrast_frequency,
    rotate_image_min,
    rotate_image_max,
    rotate_image_frequency,
    classnumber,
    classname,
    random_background_folder,
    class_pictures,
    personal_yaml_file,
    colors_to_change_frequency,
    colors_to_change_percentage_max,
    colors_to_change_percentage_min,
    colors_to_change_r_min,
    colors_to_change_r_max,
    colors_to_change_g_min,
    colors_to_change_g_max,
    colors_to_change_b_min,
    colors_to_change_b_max,
    flip_image_left_right_frequency,
    flip_image_up_down_frequency,
    background_qty,
    bloom_kernel_min,
    bloom_kernel_max,
    bloom_sigmaX_min,
    bloom_sigmaX_max,
    bloom_intensity_min,
    bloom_intensity_max,
    bloom_frequency,
    fish_distortion_min1,
    fish_distortion_max1,
    fish_distortion_min2,
    fish_distortion_max2,
    fish_distortion_min3,
    fish_distortion_max3,
    fish_distortion_min4,
    fish_distortion_max4,
    fish_divider_1_min,
    fish_divider_1_max,
    fish_divider_2_min,
    fish_divider_2_max,
    fish_divider_3_min,
    fish_divider_3_max,
    fish_divider_4_min,
    fish_divider_4_max,
    fish_border_add,
    fish_frequency,
):
    try:
        while True:
            hackstack_image = random.choice(allbackgrounds)
            needle_image = random.choice(allimages)
            color_counted = None

            yield (
                color_counted,
                hackstack_image,
                needle_image,
                outputfolder,
                image_size_width,
                image_size_height,
                needle_size_percentage_min,
                needle_size_percentage_max,
                blur_image_kernel_min,
                blur_image_kernel_max,
                blur_image_frequency,
                sharpen_image_kernel_min,
                sharpen_image_kernel_max,
                sharpen_image_frequency,
                distorted_resizing_add_min_x,
                distorted_resizing_add_max_x,
                distorted_resizing_add_min_y,
                distorted_resizing_add_max_y,
                distorted_resizing_frequency,
                blur_borders_min_x0,
                blur_borders_max_x0,
                blur_borders_min_x1,
                blur_borders_max_x1,
                blur_borders_min_y0,
                blur_borders_max_y0,
                blur_borders_min_y1,
                blur_borders_max_y1,
                blur_borders_kernel_min,
                blur_borders_kernel_max,
                blur_borders_frequency,
                pixelborder_min,
                pixelborder_max,
                pixelborder_loop_min,
                pixelborder_loop_max,
                pixelborder_frequency,
                perspective_distortion_min_x,
                perspective_distortion_max_x,
                perspective_distortion_min_y,
                perspective_distortion_max_y,
                perspective_distortion_percentage,
                transparency_distortion_min,
                transparency_distortion_max,
                transparency_distortion_frequency,
                canny_edge_blur_thresh_lower_min,
                canny_edge_blur_thresh_lower_max,
                canny_edge_blur_thresh_upper_min,
                canny_edge_blur_thresh_upper_max,
                canny_edge_blur_kernel_min,
                canny_edge_blur_kernel_max,
                canny_edge_blur_frequency,
                random_crop_min_x,
                random_crop_max_x,
                random_crop_min_y,
                random_crop_max_y,
                random_crop_frequency,
                hue_shift_min,
                hue_shift_max,
                hue_shift_frequency,
                change_contrast_min,
                change_contrast_max,
                change_contrast_frequency,
                rotate_image_min,
                rotate_image_max,
                rotate_image_frequency,
                classnumber,
                classname,
                random_background_folder,
                class_pictures,
                personal_yaml_file,
                colors_to_change_frequency,
                colors_to_change_percentage_max,
                colors_to_change_percentage_min,
                colors_to_change_r_min,
                colors_to_change_r_max,
                colors_to_change_g_min,
                colors_to_change_g_max,
                colors_to_change_b_min,
                colors_to_change_b_max,
                flip_image_left_right_frequency,
                flip_image_up_down_frequency,
                background_qty,
                bloom_kernel_min,
                bloom_kernel_max,
                bloom_sigmaX_min,
                bloom_sigmaX_max,
                bloom_intensity_min,
                bloom_intensity_max,
                bloom_frequency,
                fish_distortion_min1,
                fish_distortion_max1,
                fish_distortion_min2,
                fish_distortion_max2,
                fish_distortion_min3,
                fish_distortion_max3,
                fish_distortion_min4,
                fish_distortion_max4,
                fish_divider_1_min,
                fish_divider_1_max,
                fish_divider_2_min,
                fish_divider_2_max,
                fish_divider_3_min,
                fish_divider_3_max,
                fish_divider_4_min,
                fish_divider_4_max,
                fish_border_add,
                fish_frequency,
            )
    except KeyboardInterrupt:
        return


def add_bloom_effect(image, kernel=(15, 15), sigmaX=240, bloom_intensity=4.5):
    image = open_image_in_cv(image, channels_in_output=4).copy()
    bloa = image[..., 3]
    nottrans = np.where(
        numexpr.evaluate("bloa > 100", global_dict={}, local_dict={"bloa": bloa})
    )
    blurred = cv2.GaussianBlur(image, kernel, sigmaX=sigmaX)
    bloom = cv2.addWeighted(image, 1, blurred, bloom_intensity, 0)
    bloom = np.clip(bloom, 0, 255).astype(np.uint8)
    rands = [random.randint(0, 100), random.randint(100, 150), random.randint(150, 230)]
    random.shuffle(rands)
    bloom[..., 0] = np.clip(bloom[..., 0], 0, rands[0]).astype(np.uint8)
    bloom[..., 1] = np.clip(bloom[..., 1], 0, rands[1]).astype(np.uint8)
    bloom[..., 2] = np.clip(bloom[..., 2], 0, rands[2]).astype(np.uint8)

    bloom[nottrans] = image[nottrans]
    return bloom


def make_image(arg):
    try:
        (
            color_counted,
            hackstack_image,
            needle_image,
            outputfolder,
            image_size_width,
            image_size_height,
            needle_size_percentage_min,
            needle_size_percentage_max,
            blur_image_kernel_min,
            blur_image_kernel_max,
            blur_image_frequency,
            sharpen_image_kernel_min,
            sharpen_image_kernel_max,
            sharpen_image_frequency,
            distorted_resizing_add_min_x,
            distorted_resizing_add_max_x,
            distorted_resizing_add_min_y,
            distorted_resizing_add_max_y,
            distorted_resizing_frequency,
            blur_borders_min_x0,
            blur_borders_max_x0,
            blur_borders_min_x1,
            blur_borders_max_x1,
            blur_borders_min_y0,
            blur_borders_max_y0,
            blur_borders_min_y1,
            blur_borders_max_y1,
            blur_borders_kernel_min,
            blur_borders_kernel_max,
            blur_borders_frequency,
            pixelborder_min,
            pixelborder_max,
            pixelborder_loop_min,
            pixelborder_loop_max,
            pixelborder_frequency,
            perspective_distortion_min_x,
            perspective_distortion_max_x,
            perspective_distortion_min_y,
            perspective_distortion_max_y,
            perspective_distortion_percentage,
            transparency_distortion_min,
            transparency_distortion_max,
            transparency_distortion_frequency,
            canny_edge_blur_thresh_lower_min,
            canny_edge_blur_thresh_lower_max,
            canny_edge_blur_thresh_upper_min,
            canny_edge_blur_thresh_upper_max,
            canny_edge_blur_kernel_min,
            canny_edge_blur_kernel_max,
            canny_edge_blur_frequency,
            random_crop_min_x,
            random_crop_max_x,
            random_crop_min_y,
            random_crop_max_y,
            random_crop_frequency,
            hue_shift_min,
            hue_shift_max,
            hue_shift_frequency,
            change_contrast_min,
            change_contrast_max,
            change_contrast_frequency,
            rotate_image_min,
            rotate_image_max,
            rotate_image_frequency,
            classnumber,
            classname,
            random_background_folder,
            class_pictures,
            personal_yaml_file,
            colors_to_change_frequency,
            colors_to_change_percentage_max,
            colors_to_change_percentage_min,
            colors_to_change_r_min,
            colors_to_change_r_max,
            colors_to_change_g_min,
            colors_to_change_g_max,
            colors_to_change_b_min,
            colors_to_change_b_max,
            flip_image_left_right_frequency,
            flip_image_up_down_frequency,
            background_qty,
            bloom_kernel_min,
            bloom_kernel_max,
            bloom_sigmaX_min,
            bloom_sigmaX_max,
            bloom_intensity_min,
            bloom_intensity_max,
            bloom_frequency,
            fish_distortion_min1,
            fish_distortion_max1,
            fish_distortion_min2,
            fish_distortion_max2,
            fish_distortion_min3,
            fish_distortion_max3,
            fish_distortion_min4,
            fish_distortion_max4,
            fish_divider_1_min,
            fish_divider_1_max,
            fish_divider_2_min,
            fish_divider_2_max,
            fish_divider_3_min,
            fish_divider_3_max,
            fish_divider_4_min,
            fish_divider_4_max,
            fish_border_add,
            fish_frequency,
        ) = arg
        hackstack_image = open_image_cached(hackstack_image).copy()
        needle_image, color_counted = open_image_cached2(
            needle_image,
            image_size_width,
            image_size_height,
            cut_border=True,
            count_cors=True,
        )
        needle_image = needle_image.copy()
        if do_or_dont(colors_to_change_frequency):
            try:
                needle_image = replace_color(
                    needle_image,
                    color_counted,
                    random.randint(
                        colors_to_change_percentage_min, colors_to_change_percentage_max
                    ),
                    colors_to_change_r_min,
                    colors_to_change_r_max,
                    colors_to_change_g_min,
                    colors_to_change_g_max,
                    colors_to_change_b_min,
                    colors_to_change_b_max,
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(flip_image_left_right_frequency):
            try:
                needle_image = flip_image_left_right(needle_image)
            except Exception as fe:
                pfehler()

        if do_or_dont(flip_image_up_down_frequency):
            try:
                needle_image = flip_image_up_down(needle_image)
            except Exception as fe:
                pfehler()

        new_resize_width = int(
            random.uniform(needle_size_percentage_min, needle_size_percentage_max)
            * image_size_width
        )
        im = cv2.easy_resize_image(
            needle_image,
            width=new_resize_width,
            height=None,
            percent=None,
            interpolation=cv2.INTER_AREA,
        )

        if do_or_dont(blur_image_frequency):
            try:
                im = blur_image_keep_transparency(
                    im,
                    blur=needle_blur_image_kernel_function(
                        blur_image_kernel_min,
                        blur_image_kernel_max,
                    ),
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(sharpen_image_frequency):
            try:
                im = sharpen_image(
                    im,
                    blur=(
                        needle_blur_image_kernel_function(
                            blur_image_kernel_min,
                            blur_image_kernel_max,
                        )
                    ),
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(distorted_resizing_frequency):
            try:
                im = random_resize(
                    im,
                    addtox=random.uniform(
                        distorted_resizing_add_min_x, distorted_resizing_add_max_x
                    ),
                    addtoy=random.uniform(
                        distorted_resizing_add_min_y, distorted_resizing_add_max_y
                    ),
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(blur_borders_frequency):
            try:
                im = blur_borders_keep_transparency(
                    im,
                    y0=random.uniform(blur_borders_min_x0, blur_borders_max_x0),
                    y1=random.uniform(blur_borders_min_x1, blur_borders_max_x1),
                    x0=random.uniform(blur_borders_min_y0, blur_borders_max_y0),
                    x1=random.uniform(blur_borders_min_y1, blur_borders_max_y1),
                    blur=needle_blur_image_kernel_function(
                        blur_borders_kernel_min,
                        blur_borders_kernel_max,
                    ),
                    borderType=cv2.BORDER_DEFAULT,
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(pixelborder_frequency):
            try:
                im = add_pixxelborder(
                    im,
                    loop=random.randint(pixelborder_min, pixelborder_max),
                    add_each_loop=random.randint(
                        pixelborder_loop_min, pixelborder_loop_max
                    ),
                )
            except Exception as fe:
                pfehler()

        if (
            do_or_dont(perspective_distortion_percentage)
            and new_resize_width / image_size_width > 0.2
        ):
            try:
                box, im = distort_image(
                    im,
                    percentx=random.uniform(
                        perspective_distortion_min_x, perspective_distortion_max_x
                    ),
                    percenty=random.uniform(
                        perspective_distortion_min_y, perspective_distortion_max_y
                    ),
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(transparency_distortion_frequency):
            try:
                im = add_transparency_distortion(
                    im,
                    min_tranparency=transparency_distortion_min,
                    max_tranparency=transparency_distortion_max,
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(canny_edge_blur_frequency):
            try:
                im = canny_edge_blur(
                    im,
                    threshold1=random.randint(
                        canny_edge_blur_thresh_lower_min,
                        canny_edge_blur_thresh_lower_max,
                    ),
                    threshold2=random.randint(
                        canny_edge_blur_thresh_upper_min,
                        canny_edge_blur_thresh_upper_max,
                    ),
                    blur=(
                        needle_blur_image_kernel_function(
                            canny_edge_blur_kernel_min,
                            canny_edge_blur_kernel_max,
                        )
                    ),
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(random_crop_frequency):
            try:
                im = random_crop(
                    im,
                    min_y=random_crop_min_y,
                    max_y=random_crop_max_y,
                    min_x=random_crop_min_x,
                    max_x=random_crop_min_x,
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(hue_shift_frequency):
            try:
                im = hue_shift_keep_transparency(
                    im, hue_shift=random.randint(hue_shift_min, hue_shift_max)
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(change_contrast_frequency):
            try:
                im = change_contrast(
                    im,
                    contrast_factor=random.uniform(
                        change_contrast_min, change_contrast_max
                    ),
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(rotate_image_frequency):
            try:
                im = rotate_image(
                    im,
                    rotation_angle=random.randint(rotate_image_min, rotate_image_max),
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(bloom_frequency):
            try:
                _ke = needle_blur_image_kernel_function(
                    bloom_kernel_min, bloom_kernel_max
                )[:-1]
                im = add_bloom_effect(
                    im,
                    kernel=_ke[0],
                    sigmaX=random.randint(bloom_sigmaX_min, bloom_sigmaX_max),
                    bloom_intensity=random.uniform(
                        bloom_intensity_min, bloom_intensity_max
                    ),
                )
            except Exception as fe:
                pfehler()

        if do_or_dont(fish_frequency) and new_resize_width / image_size_width > 0.2:
            try:
                im = fish_warp_image(
                    im,
                    fish_distortion_min1,
                    fish_distortion_max1,
                    fish_distortion_min2,
                    fish_distortion_max2,
                    fish_distortion_min3,
                    fish_distortion_max3,
                    fish_distortion_min4,
                    fish_distortion_max4,
                    fish_divider_1_min,
                    fish_divider_1_max,
                    fish_divider_2_min,
                    fish_divider_2_max,
                    fish_divider_3_min,
                    fish_divider_3_max,
                    fish_divider_4_min,
                    fish_divider_4_max,
                    fish_border_add,
                )
            except Exception as fe:
                pfehler()

        try:
            im = cut_transparent_border(im)
        except Exception as fe:
            pfehler()

        try:
            (x_center, y_center, width, height), background = overlay_pic(
                hackstack_image, im
            )
            return (
                classnumber,
                classname,
                x_center,
                y_center,
                width,
                height,
            ), background
        except Exception:
            return (None, None, None, None, None, None), None
    except KeyboardInterrupt:
        return (None, None, None, None, None, None), None


def fish_eye(
    img,
    distortion_coefficients=(0.2, -0.27, 0.25, -0.08),
    camera_intrinsic_parameters=((100, 0, 100), (0, 100, 500), (0, 0, 1)),
):
    img = open_image_in_cv(img, channels_in_output=4)
    K = np.array(camera_intrinsic_parameters, dtype=np.float32)
    d = np.array(distortion_coefficients, dtype=np.float32)
    maxim = img.max()
    img = numexpr.evaluate(
        "img / maxim", global_dict={}, local_dict={"img": img, "maxim": maxim}
    )
    # img = img / img.max()
    indic0 = (
        np.array(np.meshgrid(np.arange(img.shape[0]), np.arange(img.shape[1])))
        .T.reshape(np.prod(img.shape[:2]), -1)
        .astype(np.float32)
    )

    Kinv = np.linalg.inv(K)
    indices1 = Kinv @ np.array(
        [indic0[..., 0], indic0[..., 1], np.ones(len(indic0[..., 1]))]
    )
    indices1 = np.expand_dims(indices1.T[..., :2], axis=0)
    indic1 = cv2.fisheye.distortPoints(indices1, K, d)
    indic0, indic1 = indic0.squeeze(), indic1.squeeze()
    indic1 = indic1.astype(np.uint32)
    indic0 = indic0.astype(np.uint32)
    distorted_img = np.zeros_like(img)
    a1 = indic1[..., 0]
    s1 = img.shape[0]
    a2 = indic1[..., 1]
    s2 = img.shape[1]
    indi = np.where(
        numexpr.evaluate(
            "(a1 < s1) & (a2 < s2)",
            global_dict={},
            local_dict={"a1": a1, "s1": s1, "a2": a2, "s2": s2},
        )
    )
    indi0 = indic1[indi]
    indi1 = indic0[indi]
    x, y = indi0[..., 0], indi0[..., 1]
    x1, y1 = indi1[..., 0], indi1[..., 1]
    distorted_img[x, y] = img[x1, y1]
    return (
        numexpr.evaluate(
            "255 * distorted_img",
            global_dict={},
            local_dict={"distorted_img": distorted_img},
        )
    ).astype(np.uint8)


def fish_warp_image(
    img,
    fish_distortion_min1=0.01,
    fish_distortion_max1=0.4,
    fish_distortion_min2=0.01,
    fish_distortion_max2=0.4,
    fish_distortion_min3=0.01,
    fish_distortion_max3=0.4,
    fish_distortion_min4=0.01,
    fish_distortion_max4=0.04,
    fish_divider_1_min=1,
    fish_divider_1_max=2,
    fish_divider_2_min=1,
    fish_divider_2_max=4,
    fish_divider_3_min=1,
    fish_divider_3_max=2,
    fish_divider_4_min=2,
    fish_divider_4_max=6,
    fish_border_add=0.1,
):
    img = open_image_in_cv(img, channels_in_output=4)

    top_border = int(img.shape[0] * fish_border_add)
    bottom_border = int(img.shape[0] * fish_border_add)
    left_border = int(img.shape[1] * fish_border_add)
    right_border = int(img.shape[1] * fish_border_add)

    border_color = [0, 0, 0, 0]

    img = cv2.copyMakeBorder(
        img,
        top_border,
        bottom_border,
        left_border,
        right_border,
        cv2.BORDER_CONSTANT,
        value=border_color,
    )

    dico1 = (
        -random.uniform(fish_distortion_min1, fish_distortion_max1),
        random.uniform(fish_distortion_min2, fish_distortion_max2),
        random.uniform(fish_distortion_min3, fish_distortion_max3),
        random.uniform(fish_distortion_min4, fish_distortion_max4),
    )

    dico2 = (
        -random.uniform(fish_distortion_min1, fish_distortion_max1),
        random.uniform(fish_distortion_min2, fish_distortion_max2),
        random.uniform(fish_distortion_min3, fish_distortion_max3),
        -random.uniform(fish_distortion_min4, fish_distortion_max4),
    )
    dico3 = (
        random.uniform(fish_distortion_min1, fish_distortion_max1),
        -random.uniform(fish_distortion_min2, fish_distortion_max2),
        random.uniform(fish_distortion_min3, fish_distortion_max3),
        -random.uniform(fish_distortion_min4, fish_distortion_max4),
    )
    dico = random.choice([dico1, dico2, dico3])

    para = (
        (
            img.shape[0] // random.randint(fish_divider_1_min, fish_divider_1_max),
            0,
            img.shape[0] // random.randint(fish_divider_2_min, fish_divider_2_max),
        ),
        (
            0,
            img.shape[1] // random.randint(fish_divider_3_min, fish_divider_3_max),
            img.shape[1] // random.randint(fish_divider_4_min, fish_divider_4_max),
        ),
        (0, 0, 1),
    )

    return fish_eye(
        img=img, distortion_coefficients=dico, camera_intrinsic_parameters=para
    )


def psw(data):
    totalcounter = 0
    imagefolder = None
    labelsfolder = None
    generated_pic_folder = None
    personal_yaml_file = None
    all_classes = {}
    backgroundfolder = ""
    for (
        classnumber,
        classname,
        random_background_folder,
        class_pictures,
        personal_yaml_file,
        outputfolder,
        howmany,
        background_qty,
        processes,
        image_size_width,
        image_size_height,
        needle_size_percentage_min,
        needle_size_percentage_max,
        blur_image_kernel_min,
        blur_image_kernel_max,
        blur_image_frequency,
        sharpen_image_kernel_min,
        sharpen_image_kernel_max,
        sharpen_image_frequency,
        distorted_resizing_add_min_x,
        distorted_resizing_add_max_x,
        distorted_resizing_add_min_y,
        distorted_resizing_add_max_y,
        distorted_resizing_frequency,
        blur_borders_min_x0,
        blur_borders_max_x0,
        blur_borders_min_x1,
        blur_borders_max_x1,
        blur_borders_min_y0,
        blur_borders_max_y0,
        blur_borders_min_y1,
        blur_borders_max_y1,
        blur_borders_kernel_min,
        blur_borders_kernel_max,
        blur_borders_frequency,
        pixelborder_min,
        pixelborder_max,
        pixelborder_loop_min,
        pixelborder_loop_max,
        pixelborder_frequency,
        perspective_distortion_min_x,
        perspective_distortion_max_x,
        perspective_distortion_min_y,
        perspective_distortion_max_y,
        perspective_distortion_percentage,
        transparency_distortion_min,
        transparency_distortion_max,
        transparency_distortion_frequency,
        canny_edge_blur_thresh_lower_min,
        canny_edge_blur_thresh_lower_max,
        canny_edge_blur_thresh_upper_min,
        canny_edge_blur_thresh_upper_max,
        canny_edge_blur_kernel_min,
        canny_edge_blur_kernel_max,
        canny_edge_blur_frequency,
        random_crop_min_x,
        random_crop_max_x,
        random_crop_min_y,
        random_crop_max_y,
        random_crop_frequency,
        hue_shift_min,
        hue_shift_max,
        hue_shift_frequency,
        change_contrast_min,
        change_contrast_max,
        change_contrast_frequency,
        rotate_image_min,
        rotate_image_max,
        rotate_image_frequency,
        colors_to_change_percentage_max,
        colors_to_change_percentage_min,
        colors_to_change_frequency,
        colors_to_change_r_min,
        colors_to_change_r_max,
        colors_to_change_g_min,
        colors_to_change_g_max,
        colors_to_change_b_min,
        colors_to_change_b_max,
        flip_image_left_right_frequency,
        flip_image_up_down_frequency,
        verbose,
        bloom_kernel_min,
        bloom_kernel_max,
        bloom_sigmaX_min,
        bloom_sigmaX_max,
        bloom_intensity_min,
        bloom_intensity_max,
        bloom_frequency,
        fish_distortion_min1,
        fish_distortion_max1,
        fish_distortion_min2,
        fish_distortion_max2,
        fish_distortion_min3,
        fish_distortion_max3,
        fish_distortion_min4,
        fish_distortion_max4,
        fish_divider_1_min,
        fish_divider_1_max,
        fish_divider_2_min,
        fish_divider_2_max,
        fish_divider_3_min,
        fish_divider_3_max,
        fish_divider_4_min,
        fish_divider_4_max,
        fish_border_add,
        fish_frequency,
    ) in data:
        # allbackgrounds.clear()
        allimages.clear()
        (
            datasetfolder,
            imagefolder,
            labelsfolder,
            backgroundfolder,
        ) = create_folder_structure(outputfolder)
        allbackgrounds.extend(
            crop_list_of_images(
                qty=background_qty,
                input_folder=random_background_folder,
                outputfolder=outputfolder,
                width=image_size_width,
                height=image_size_height,
            )
        )
        allimages.extend(
            [x.path for x in get_folder_file_complete_path(folders=class_pictures)]
        )

        gener = generate_args(
            outputfolder,
            image_size_width,
            image_size_height,
            needle_size_percentage_min,
            needle_size_percentage_max,
            blur_image_kernel_min,
            blur_image_kernel_max,
            blur_image_frequency,
            sharpen_image_kernel_min,
            sharpen_image_kernel_max,
            sharpen_image_frequency,
            distorted_resizing_add_min_x,
            distorted_resizing_add_max_x,
            distorted_resizing_add_min_y,
            distorted_resizing_add_max_y,
            distorted_resizing_frequency,
            blur_borders_min_x0,
            blur_borders_max_x0,
            blur_borders_min_x1,
            blur_borders_max_x1,
            blur_borders_min_y0,
            blur_borders_max_y0,
            blur_borders_min_y1,
            blur_borders_max_y1,
            blur_borders_kernel_min,
            blur_borders_kernel_max,
            blur_borders_frequency,
            pixelborder_min,
            pixelborder_max,
            pixelborder_loop_min,
            pixelborder_loop_max,
            pixelborder_frequency,
            perspective_distortion_min_x,
            perspective_distortion_max_x,
            perspective_distortion_min_y,
            perspective_distortion_max_y,
            perspective_distortion_percentage,
            transparency_distortion_min,
            transparency_distortion_max,
            transparency_distortion_frequency,
            canny_edge_blur_thresh_lower_min,
            canny_edge_blur_thresh_lower_max,
            canny_edge_blur_thresh_upper_min,
            canny_edge_blur_thresh_upper_max,
            canny_edge_blur_kernel_min,
            canny_edge_blur_kernel_max,
            canny_edge_blur_frequency,
            random_crop_min_x,
            random_crop_max_x,
            random_crop_min_y,
            random_crop_max_y,
            random_crop_frequency,
            hue_shift_min,
            hue_shift_max,
            hue_shift_frequency,
            change_contrast_min,
            change_contrast_max,
            change_contrast_frequency,
            rotate_image_min,
            rotate_image_max,
            rotate_image_frequency,
            classnumber,
            classname,
            random_background_folder,
            class_pictures,
            personal_yaml_file,
            colors_to_change_frequency,
            colors_to_change_percentage_max,
            colors_to_change_percentage_min,
            colors_to_change_r_min,
            colors_to_change_r_max,
            colors_to_change_g_min,
            colors_to_change_g_max,
            colors_to_change_b_min,
            colors_to_change_b_max,
            flip_image_left_right_frequency,
            flip_image_up_down_frequency,
            background_qty,
            bloom_kernel_min,
            bloom_kernel_max,
            bloom_sigmaX_min,
            bloom_sigmaX_max,
            bloom_intensity_min,
            bloom_intensity_max,
            bloom_frequency,
            fish_distortion_min1,
            fish_distortion_max1,
            fish_distortion_min2,
            fish_distortion_max2,
            fish_distortion_min3,
            fish_distortion_max3,
            fish_distortion_min4,
            fish_distortion_max4,
            fish_divider_1_min,
            fish_divider_1_max,
            fish_divider_2_min,
            fish_divider_2_max,
            fish_divider_3_min,
            fish_divider_3_max,
            fish_divider_4_min,
            fish_divider_4_max,
            fish_border_add,
            fish_frequency,
        )

        generated_pic_folder = os.path.normpath(os.path.join(datasetfolder, "splitset"))
        counter = 0
        try:
            with multiprocessing.Pool(processes=processes) as pool:
                processed_results = pool.imap_unordered(make_image, gener)

                for pr in processed_results:
                    (
                        classnumber,
                        classname,
                        x_center,
                        y_center,
                        width,
                        height,
                    ), background = pr
                    if not x_center or not y_center:
                        continue
                    all_classes[classname] = classnumber
                    saveimagepath = os.path.join(
                        imagefolder, f"image{totalcounter}.jpg"
                    )
                    if verbose:
                        print(saveimagepath, end="\r")
                    cv2.imwrite(saveimagepath, background)
                    with open(
                        os.path.join(labelsfolder, f"image{totalcounter}.txt"),
                        mode="w",
                        encoding="utf8",
                    ) as fi:
                        fi.write(
                            f"{classnumber} {x_center} {y_center} {width} {height}"
                        )
                    counter = counter + 1
                    totalcounter = totalcounter + 1
                    if howmany < counter:
                        break
        except KeyboardInterrupt:
            try:
                print("quitting...")
                sleep(5)
            except:
                pass
            break
    images = [x.path for x in get_folder_file_complete_path(imagefolder)]
    annotationstxt = [x.path for x in get_folder_file_complete_path(labelsfolder)]

    train_images, val_images, train_annotations, val_annotations = train_test_split(
        images, annotationstxt, test_size=0.2, random_state=1
    )
    val_images, test_images, val_annotations, test_annotations = train_test_split(
        val_images, val_annotations, test_size=0.5, random_state=1
    )

    train_images_path = move_files_to_folder(
        train_images, "images/train", generated_pic_folder
    )
    val_images_path = move_files_to_folder(
        val_images, "images/val/", generated_pic_folder
    )
    test_images_path = move_files_to_folder(
        test_images, "images/test/", generated_pic_folder
    )
    move_files_to_folder(train_annotations, "labels/train/", generated_pic_folder)
    move_files_to_folder(val_annotations, "labels/val/", generated_pic_folder)
    move_files_to_folder(test_annotations, "labels/test/", generated_pic_folder)

    fileinfosmodel = rf"""
    train: {train_images_path} 
    val:  {val_images_path} 
    test: {test_images_path} 

    nc: {len(all_classes)}

    names: {repr(list(all_classes.keys())).replace("'", '"')}
    """
    yolovyamel = os.path.join(generated_pic_folder, personal_yaml_file)
    with open(yolovyamel, encoding="utf-8", mode="w") as f:
        for line in fileinfosmodel.splitlines():
            f.write(f"{line.strip()}\n")

    images = [x.path for x in get_folder_file_complete_path(backgroundfolder)]
    move_files_to_folder(images, "images/train", generated_pic_folder)


def generate_ini_file(allclasses):
    def _generate_ini_file(
        classnumber,
        classname,
        random_background_folder,
        class_pictures,
        personal_yaml_file,
        outputfolder,
        howmany=3000,
        background_qty=300,
        processes=4,
        image_size_width=640,
        image_size_height=640,
        needle_size_percentage_min=0.2,
        needle_size_percentage_max=0.8,
        blur_image_kernel_min=1,
        blur_image_kernel_max=5,
        blur_image_frequency=10,
        sharpen_image_kernel_min=1,
        sharpen_image_kernel_max=6,
        sharpen_image_frequency=10,
        distorted_resizing_add_min_x=0.01,
        distorted_resizing_add_max_x=0.15,
        distorted_resizing_add_min_y=0.01,
        distorted_resizing_add_max_y=0.15,
        distorted_resizing_frequency=30,
        blur_borders_min_x0=0.01,
        blur_borders_max_x0=0.1,
        blur_borders_min_x1=0.01,
        blur_borders_max_x1=0.1,
        blur_borders_min_y0=0.01,
        blur_borders_max_y0=0.1,
        blur_borders_min_y1=0.01,
        blur_borders_max_y1=0.1,
        blur_borders_kernel_min=1,
        blur_borders_kernel_max=6,
        blur_borders_frequency=10,
        pixelborder_min=1,
        pixelborder_max=20,
        pixelborder_loop_min=1,
        pixelborder_loop_max=2,
        pixelborder_frequency=20,
        perspective_distortion_min_x=0.01,
        perspective_distortion_max_x=0.15,
        perspective_distortion_min_y=0.01,
        perspective_distortion_max_y=0.15,
        perspective_distortion_percentage=10,
        transparency_distortion_min=150,
        transparency_distortion_max=255,
        transparency_distortion_frequency=40,
        canny_edge_blur_thresh_lower_min=10,
        canny_edge_blur_thresh_lower_max=20,
        canny_edge_blur_thresh_upper_min=80,
        canny_edge_blur_thresh_upper_max=90,
        canny_edge_blur_kernel_min=1,
        canny_edge_blur_kernel_max=6,
        canny_edge_blur_frequency=20,
        random_crop_min_x=0.01,
        random_crop_max_x=0.10,
        random_crop_min_y=0.01,
        random_crop_max_y=0.10,
        random_crop_frequency=20,
        hue_shift_min=1,
        hue_shift_max=180,
        hue_shift_frequency=90,
        change_contrast_min=0.8,
        change_contrast_max=1.2,
        change_contrast_frequency=30,
        rotate_image_min=2,
        rotate_image_max=359,
        rotate_image_frequency=90,
        colors_to_change_percentage_max=75,
        colors_to_change_percentage_min=1,
        colors_to_change_frequency=90,
        colors_to_change_r_min=5,
        colors_to_change_r_max=150,
        colors_to_change_g_min=5,
        colors_to_change_g_max=150,
        colors_to_change_b_min=5,
        colors_to_change_b_max=150,
        flip_image_left_right_frequency=2,
        flip_image_up_down_frequency=2,
        verbose=True,
        bloom_kernel_min=1,
        bloom_kernel_max=25,
        bloom_sigmaX_min=140,
        bloom_sigmaX_max=240,
        bloom_intensity_min=4.5,
        bloom_intensity_max=20.5,
        bloom_frequency=20,
        fish_distortion_min1=0.01,
        fish_distortion_max1=0.6,
        fish_distortion_min2=0.01,
        fish_distortion_max2=0.6,
        fish_distortion_min3=0.01,
        fish_distortion_max3=0.6,
        fish_distortion_min4=0.01,
        fish_distortion_max4=0.04,
        fish_divider_1_min=1,
        fish_divider_1_max=2,
        fish_divider_2_min=1,
        fish_divider_2_max=4,
        fish_divider_3_min=1,
        fish_divider_3_max=2,
        fish_divider_4_min=2,
        fish_divider_4_max=6,
        fish_border_add=0.1,
        fish_frequency=20,
    ):
        v = rf"""[class{classnumber}]
        classnumber:{classnumber}
        classname:{classname}
        random_background_folder:{random_background_folder}
        class_pictures:{class_pictures}
        personal_yaml_file:{personal_yaml_file}
        outputfolder:{outputfolder}
        howmany:{howmany}
        background_qty:{background_qty}
        processes:{processes}
        image_size_width:{image_size_width}
        image_size_height:{image_size_height}
        needle_size_percentage_min:{needle_size_percentage_min}
        needle_size_percentage_max:{needle_size_percentage_max}
        blur_image_kernel_min:{blur_image_kernel_min}
        blur_image_kernel_max:{blur_image_kernel_max}
        blur_image_frequency:{blur_image_frequency}
        sharpen_image_kernel_min:{sharpen_image_kernel_min}
        sharpen_image_kernel_max:{sharpen_image_kernel_max}
        sharpen_image_frequency:{sharpen_image_frequency}
        distorted_resizing_add_min_x:{distorted_resizing_add_min_x}
        distorted_resizing_add_max_x:{distorted_resizing_add_max_x}
        distorted_resizing_add_min_y:{distorted_resizing_add_min_y}
        distorted_resizing_add_max_y:{distorted_resizing_add_max_y}
        distorted_resizing_frequency:{distorted_resizing_frequency}
        blur_borders_min_x0:{blur_borders_min_x0}
        blur_borders_max_x0:{blur_borders_max_x0}
        blur_borders_min_x1:{blur_borders_min_x1}
        blur_borders_max_x1:{blur_borders_max_x1}
        blur_borders_min_y0:{blur_borders_min_y0}
        blur_borders_max_y0:{blur_borders_max_y0}
        blur_borders_min_y1:{blur_borders_min_y1}
        blur_borders_max_y1:{blur_borders_max_y1}
        blur_borders_kernel_min:{blur_borders_kernel_min}
        blur_borders_kernel_max:{blur_borders_kernel_max}
        blur_borders_frequency:{blur_borders_frequency}
        pixelborder_min:{pixelborder_min}
        pixelborder_max:{pixelborder_max}
        pixelborder_loop_min:{pixelborder_loop_min}
        pixelborder_loop_max:{pixelborder_loop_max}
        pixelborder_frequency:{pixelborder_frequency}
        perspective_distortion_min_x:{perspective_distortion_min_x}
        perspective_distortion_max_x:{perspective_distortion_max_x}
        perspective_distortion_min_y:{perspective_distortion_min_y}
        perspective_distortion_max_y:{perspective_distortion_max_y}
        perspective_distortion_percentage:{perspective_distortion_percentage}
        transparency_distortion_min:{transparency_distortion_min}
        transparency_distortion_max:{transparency_distortion_max}
        transparency_distortion_frequency:{transparency_distortion_frequency}
        canny_edge_blur_thresh_lower_min:{canny_edge_blur_thresh_lower_min}
        canny_edge_blur_thresh_lower_max:{canny_edge_blur_thresh_lower_max}
        canny_edge_blur_thresh_upper_min:{canny_edge_blur_thresh_upper_min}
        canny_edge_blur_thresh_upper_max:{canny_edge_blur_thresh_upper_max}
        canny_edge_blur_kernel_min:{canny_edge_blur_kernel_min}
        canny_edge_blur_kernel_max:{canny_edge_blur_kernel_max}
        canny_edge_blur_frequency:{canny_edge_blur_frequency}
        random_crop_min_x:{random_crop_min_x}
        random_crop_max_x:{random_crop_max_x}
        random_crop_min_y:{random_crop_min_y}
        random_crop_max_y:{random_crop_max_y}
        random_crop_frequency:{random_crop_frequency}
        hue_shift_min:{hue_shift_min}
        hue_shift_max:{hue_shift_max}
        hue_shift_frequency:{hue_shift_frequency}
        change_contrast_min:{change_contrast_min}
        change_contrast_max:{change_contrast_max}
        change_contrast_frequency:{change_contrast_frequency}
        rotate_image_min:{rotate_image_min}
        rotate_image_max:{rotate_image_max}
        rotate_image_frequency:{rotate_image_frequency}
        colors_to_change_percentage_max:{colors_to_change_percentage_max}
        colors_to_change_percentage_min:{colors_to_change_percentage_min}
        colors_to_change_frequency:{colors_to_change_frequency}
        colors_to_change_r_min:{colors_to_change_r_min}
        colors_to_change_r_max:{colors_to_change_r_max}
        colors_to_change_g_min:{colors_to_change_g_min}
        colors_to_change_g_max:{colors_to_change_g_max}
        colors_to_change_b_min:{colors_to_change_b_min}
        colors_to_change_b_max:{colors_to_change_b_max}
        flip_image_left_right_frequency:{flip_image_left_right_frequency}
        flip_image_up_down_frequency:{flip_image_up_down_frequency}
        verbose:{verbose}
        bloom_kernel_min:{bloom_kernel_min}
        bloom_kernel_max:{bloom_kernel_max}
        bloom_sigmaX_min:{bloom_sigmaX_min}
        bloom_sigmaX_max:{bloom_sigmaX_max}
        bloom_intensity_min:{bloom_intensity_min}
        bloom_intensity_max:{bloom_intensity_max}
        bloom_frequency:{bloom_frequency}
        fish_distortion_min1:{fish_distortion_min1}
        fish_distortion_max1:{fish_distortion_max1}
        fish_distortion_min2:{fish_distortion_min2}
        fish_distortion_max2:{fish_distortion_max2}
        fish_distortion_min3:{fish_distortion_min3}
        fish_distortion_max3:{fish_distortion_max3}
        fish_distortion_min4:{fish_distortion_min4}
        fish_distortion_max4:{fish_distortion_max4}
        fish_divider_1_min:{fish_divider_1_min}
        fish_divider_1_max:{fish_divider_1_max}
        fish_divider_2_min:{fish_divider_2_min}
        fish_divider_2_max:{fish_divider_2_max}
        fish_divider_3_min:{fish_divider_3_min}
        fish_divider_3_max:{fish_divider_3_max}
        fish_divider_4_min:{fish_divider_4_min}
        fish_divider_4_max:{fish_divider_4_max}
        fish_border_add:{fish_border_add}
        fish_frequency:{fish_frequency}"""
        resu = ""
        for vv in v.splitlines():
            resu += vv.strip() + "\n"
        resu += "\n\n"
        return resu

    maindict = {
        "classnumber": 0,
        "classname": r"",
        "random_background_folder": r"",
        "class_pictures": r"",
        "personal_yaml_file": "",
        "outputfolder": r"",
        "howmany": 3000,
        "background_qty": 300,
        "processes": 4,
        "image_size_width": 640,
        "image_size_height": 640,
        "needle_size_percentage_min": 0.2,
        "needle_size_percentage_max": 0.8,
        "blur_image_kernel_min": 1,
        "blur_image_kernel_max": 5,
        "blur_image_frequency": 10,
        "sharpen_image_kernel_min": 1,
        "sharpen_image_kernel_max": 6,
        "sharpen_image_frequency": 10,
        "distorted_resizing_add_min_x": 0.01,
        "distorted_resizing_add_max_x": 0.15,
        "distorted_resizing_add_min_y": 0.01,
        "distorted_resizing_add_max_y": 0.15,
        "distorted_resizing_frequency": 30,
        "blur_borders_min_x0": 0.01,
        "blur_borders_max_x0": 0.1,
        "blur_borders_min_x1": 0.01,
        "blur_borders_max_x1": 0.1,
        "blur_borders_min_y0": 0.01,
        "blur_borders_max_y0": 0.1,
        "blur_borders_min_y1": 0.01,
        "blur_borders_max_y1": 0.1,
        "blur_borders_kernel_min": 1,
        "blur_borders_kernel_max": 6,
        "blur_borders_frequency": 10,
        "pixelborder_min": 1,
        "pixelborder_max": 20,
        "pixelborder_loop_min": 1,
        "pixelborder_loop_max": 2,
        "pixelborder_frequency": 20,
        "perspective_distortion_min_x": 0.01,
        "perspective_distortion_max_x": 0.15,
        "perspective_distortion_min_y": 0.01,
        "perspective_distortion_max_y": 0.15,
        "perspective_distortion_percentage": 10,
        "transparency_distortion_min": 150,
        "transparency_distortion_max": 255,
        "transparency_distortion_frequency": 40,
        "canny_edge_blur_thresh_lower_min": 10,
        "canny_edge_blur_thresh_lower_max": 20,
        "canny_edge_blur_thresh_upper_min": 80,
        "canny_edge_blur_thresh_upper_max": 90,
        "canny_edge_blur_kernel_min": 1,
        "canny_edge_blur_kernel_max": 6,
        "canny_edge_blur_frequency": 20,
        "random_crop_min_x": 0.01,
        "random_crop_max_x": 0.10,
        "random_crop_min_y": 0.01,
        "random_crop_max_y": 0.10,
        "random_crop_frequency": 20,
        "hue_shift_min": 1,
        "hue_shift_max": 180,
        "hue_shift_frequency": 90,
        "change_contrast_min": 0.8,
        "change_contrast_max": 1.2,
        "change_contrast_frequency": 30,
        "rotate_image_min": 2,
        "rotate_image_max": 359,
        "rotate_image_frequency": 90,
        "colors_to_change_percentage_max": 75,
        "colors_to_change_percentage_min": 1,
        "colors_to_change_frequency": 90,
        "colors_to_change_r_min": 5,
        "colors_to_change_r_max": 150,
        "colors_to_change_g_min": 5,
        "colors_to_change_g_max": 150,
        "colors_to_change_b_min": 5,
        "colors_to_change_b_max": 150,
        "flip_image_left_right_frequency": 2,
        "flip_image_up_down_frequency": 2,
        "verbose": True,
        "bloom_kernel_min": 1,
        "bloom_kernel_max": 25,
        "bloom_sigmaX_min": 140,
        "bloom_sigmaX_max": 240,
        "bloom_intensity_min": 4.5,
        "bloom_intensity_max": 20.5,
        "bloom_frequency": 20,
        "fish_distortion_min1": 0.01,
        "fish_distortion_max1": 0.6,
        "fish_distortion_min2": 0.01,
        "fish_distortion_max2": 0.6,
        "fish_distortion_min3": 0.01,
        "fish_distortion_max3": 0.6,
        "fish_distortion_min4": 0.01,
        "fish_distortion_max4": 0.04,
        "fish_divider_1_min": 1,
        "fish_divider_1_max": 2,
        "fish_divider_2_min": 1,
        "fish_divider_2_max": 4,
        "fish_divider_3_min": 1,
        "fish_divider_3_max": 2,
        "fish_divider_4_min": 2,
        "fish_divider_4_max": 6,
        "fish_border_add": 0.1,
        "fish_frequency": 20,
    }
    allinis = ""
    for _class in allclasses:
        _maindict = maindict.copy()
        _maindict.update(_class)
        allinis += _generate_ini_file(**_maindict)
    return allinis
