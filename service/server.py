from flask import Flask
from flask import request
from flask import jsonify
import json
from path_object import PathObject, get_path_objects
from bmp_util import sort_pobjs, sort_pobjs_trace
from dict import add_trace
from model import model as tf_model
from const import IMG_SIZE
from model import predict
from vert_equal import vert_equal_mnist
import base64
import datetime
import logging
import os
import random
import string
import cv2
from hcm import hcm_req
import re

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

is_collecting_vert = os.getenv("is_collecting_vert", "")


@app.route("/mnist/detectxy", methods=["OPTIONS"])
def option():
    return ""


@app.route("/mnist/detectxy2", methods=["POST"])
def detect_xy2():
    paths_str = request.form.get("paths", "")
    try:
        if paths_str[0] == "\"":
            paths_str = paths_str[1:-1]
        paths = json.loads(paths_str)
    except Exception as e:
        print(e)
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500

    if tf_model is None:
        ret_data = {'code': 1, 'msg': "Failed loading model"}
        return jsonify(ret_data), 500

    pObjs = get_path_objects(paths)
    try:
        ocr_result = sort_pobjs(pObjs)
    except Exception as e:
        logging.exception(e)
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500
    ret_data = {'code': 0, "msg": ocr_result}
    # b64 = base64.b64encode(ocr_result.encode("utf-8"))
    # ret_data = {'code': 0, "msg": b64}
    return jsonify(ret_data)


@app.route("/mnist/detectxy", methods=["POST"])
def detect_xy():
    paths_str = request.form.get("paths", "")
    ty = request.form.get("type", '')
    if ty != '':
        ty = base64.b64decode(ty).decode()
    try:
        if paths_str[0] == "\"":
            paths_str = paths_str[1:-1]
        paths = json.loads(paths_str)
    except Exception as e:
        print(e)
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500

    if tf_model is None:
        ret_data = {'code': 1, 'msg': "Failed loading model"}
        return jsonify(ret_data), 500

    pObjs = get_path_objects(paths)
    try:
        ocr_result = sort_pobjs_trace(pObjs)
        if ty != '':
            add_trace(ocr_result, ty)
    except Exception as e:
        logging.exception(e)
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500
    ret_data = {'code': 0, "msg": ocr_result}
    # b64 = base64.b64encode(ocr_result.encode("utf-8"))
    # ret_data = {'code': 0, "msg": b64}
    return jsonify(ret_data)


@app.route("/mnist/verteq", methods=["POST"])
def func_detect_vert():
    paths_str = request.form.get("paths", "")
    try:
        if paths_str[0] == "\"":
            paths_str = paths_str[1:-1]
        paths = json.loads(paths_str)
    except Exception as e:
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500

    if tf_model is None:
        ret_data = {'code': 1, 'msg': "Failed loading model"}
        return jsonify(ret_data), 500

    try:
        strs, eq_type, po = vert_equal_mnist(paths)
    except Exception as e:
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500

    ret_data = {"code": 0, "msg": strs, "type": eq_type}
    if is_collecting_vert == "T" and po is not None:
        logging.info("save verteq image and mnist result")
        try:
            date_str = str(datetime.datetime.now())
            date_str = 'verteq-' + str.split(date_str, ' ')[0]
            date_str = 'tmp/' + date_str
            if not os.path.exists(date_str):
                os.makedirs(date_str, exist_ok=True)
            prefix = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            im = po.draw(po.max_x, po.max_y, thickness=6)
            cv2.imwrite(date_str+"/"+prefix+ ".jpg", im)
            with open(date_str+"/"+prefix+ ".txt", "w+") as f:
                f.write("\n".join(strs))
        except Exception as e:
            logging.exception(e)

    return jsonify(ret_data)


@app.route("/mnist/hcm", methods=["POST"])
def func_hcm():
    b64 = request.form.get("b64", "")
    session_id = request.form.get("sid", "")

    ret_s, ret_b = hcm_req(session_id, b64)
    if not ret_b:
        ret_data = {'code': 500, 'msg': str(ret_s)}
        return jsonify(ret_data), 500
    else:
        ret_data = {'code': 0, 'msg': str(ret_s)}
        return jsonify(ret_data)


@app.route("/mnist/test", methods=["POST"])
def func_test():
    paths_str = request.form.get("paths", "")
    # paths_str = "[[[155.0,285.0],[168.18538,286.31854],[194.84285,293.26617],[217.08528,305.98547],[228.66692,320.58362],[241.26956,346.6739],[245.23463,377.05396],[229.64398,414.3222],[206.08345,451.53687],[179.0,483.0],[153.20532,504.8656],[136.28,520.41],[130.23961,525.7604],[125.76774,529.15485],[124.58261,531.8348],[142.2578,535.51605],[180.32312,537.218],[224.23785,540.4056],[260.96143,548.9896],[283.21854,558.7206],[290.24985,574.99963],[292.0,600.84717],[271.0,637.0],[230.95673,680.8321],[192.6739,721.84937],[157.91132,747.80853],[137.55695,764.3692],[125.18443,772.5437],[121.58304,774.6113],[121.0,775.0],[128.0,774.0]],[[504.0,309.0],[488.235,394.80872],[489.0,438.0],[496.2431,479.84625],[508.33807,525.8327],[526.2083,555.31244],[544.1234,583.1954],[563.6458,601.2425],[596.991,613.59686],[623.4826,618.54987],[648.5,616.5],[665.407,608.2696],[677.94116,598.71246],[680.0,597.0]],[[645.0,348.0],[614.72394,408.31708],[589.59906,484.80304],[572.8146,566.8808],[561.5011,643.91986],[552.2982,702.3687],[543.9609,752.55505],[538.036,786.54297],[538.0,805.0]],[[904.0,377.0],[902.92633,387.73645],[898.5,420.0],[900.0,476.70868],[901.2862,541.73676],[902.0,585.8002],[904.1077,624.4546],[899.69836,660.281],[890.3735,682.27203],[870.9457,711.276],[838.3928,735.1512],[800.83295,755.58356],[776.9968,764.1188],[762.35315,765.0],[753.264,763.8773],[751.0,761.0],[752.0,752.0]],[[949.0,389.0],[977.31146,405.7459],[1010.1399,421.35577],[1034.0,427.0]]]"
    try:
        paths = json.loads(paths_str)
    except Exception as e:
        print(e)
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500

    if tf_model is None:
        ret_data = {'code': 1, 'msg': "Failed loading model"}
        return jsonify(ret_data), 500
    pobj = PathObject()
    for p in paths:
        pobj.add_path(p)
    im = pobj.draw(IMG_SIZE, IMG_SIZE)
    try:
        res, _ = predict(im)
    except Exception as e:
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500
    ret_data = {'code': 0, "msg": res}
    return jsonify(ret_data)


@app.route("/mnist/version", methods=["POST"])
def get_version():
    return "model:210407v1"

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,session_id,Access-Control-Allow-Origin,Content-Type,Access-Control-Allow-Credentials,cache-control')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    print("=============== mnist service v1.0 ===============")
    app.run(host="0.0.0.0", port=8080, debug=False)
