from flask import Flask
from flask import request
from flask import jsonify
import re
import base64
import os
import json
import datetime
import string
import random
from draw_path import draw, split_draw
import cv2

is_collecting = os.getenv("is_collecting", "")


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/pyocr/savemnistdata", methods=['OPTIONS'])
def option():
    return ""


@app.route("/pyocr/savemnistdata", methods=['POST'])
def save_imgs():
    if len(is_collecting) > 0:
        ret_data = {'code': 0, 'msg': '收集服务暂不开放'}
        return jsonify(ret_data), 200
    mnist_result_str = request.form.get("mnistresult", "")
    fresult = request.form.get("num","")
    to_join = False
    if len(fresult) == 0:
        to_join = True
    paths_str = request.form.get("paths", "")
    version = request.form.get("ver", "100")
    if len(mnist_result_str) == 0:
        ret_data = {'code': 1, 'msg': 'Param error!'}
        return jsonify(ret_data), 400
    try:
        mnist_result = json.loads(mnist_result_str)
    except Exception as e:
        print(e)
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500
    # print(mnist_result)

    prefix = ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '_'+version
    ret_arr = []
    fname = []
    for obj in mnist_result:
        if isinstance(obj['mnist'], str) is not True:
            mnist = str(obj['mnist'])
        else:
            mnist = obj['mnist']
        if to_join:
            fresult += mnist
        b64 = obj['b64']

        if len(b64) == 0 or len(mnist) == 0:
            ret_data = {'code': 1, 'msg': 'Param error!'}
            return jsonify(ret_data), 400
        try:
            b64 = str.replace(b64, ' ', '+')
            if 'data:image' in b64:
                b64 = re.sub('data:image/(jpg|png|JPG|PNG);base64,', '', b64)
            imgdata = base64.urlsafe_b64decode(b64)

            date_str = str(datetime.datetime.now())
            date_str = 'mnist-' + str.split(date_str, ' ')[0]
            date_str = 'tmp/' + date_str
            if not os.path.exists(date_str):
                os.makedirs(date_str, exist_ok=True)

            index = 1
            if not to_join:
                tmp_mnist = fresult + '_' + prefix + '_' + mnist + '.jpg'
            else:
                tmp_mnist = mnist + '_' + prefix + '_' + mnist + '.jpg'
            while tmp_mnist in fname:
                tmp_mnist = tmp_mnist[:-4] + '_' + str(index) + '.jpg'
                index += 1
            mnist = tmp_mnist
            with open(date_str+"/" + mnist, 'wb') as f:
                f.write(imgdata)
            fname.append(mnist)
        except Exception as e:
            print(e)
            ret_data = {'code': 1, 'msg': str(e)}
            return jsonify(ret_data), 500
        ret_arr.append(date_str+"/" + mnist)
    try:
        if len(paths_str) > 0:
            with open(date_str+"/"+fresult + '_' + prefix+'.txt', 'w+') as f:
                f.write(paths_str)
    except Exception as e:
        print(e)
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500

    ret_data = {'code': 0, 'msg': str(ret_arr)}
    return jsonify(ret_data), 200


@app.route("/pyocr/savemnistdata2", methods=['OPTIONS'])
def option2():
    return ""


@app.route("/pyocr/savemnistdata2", methods=['POST'])
def save_imgs2():
    if len(is_collecting) > 0:
        ret_data = {'code': 0, 'msg': '收集服务暂不开放'}
        return jsonify(ret_data), 200
    paths_str = request.form.get("paths", "")
    mnist_result = request.form.get("mnistresult", "")
    version = request.form.get("ver", "")
    if len(paths_str) == 0 or len(mnist_result) == 0:
        ret_data = {'code': 1, 'msg': 'Param error!'}
        return jsonify(ret_data), 400

    try:
        paths = json.loads(paths_str)
    except Exception as e:
        print(e)
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500

    prefix = ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '_'+version+'_'
    date_str = str(datetime.datetime.now())
    date_str = 'mnist-' + str.split(date_str, ' ')[0]
    date_str = 'tmp/' + date_str

    if not os.path.exists(date_str):
        try:
            os.makedirs(date_str, exist_ok=True)
        except Exception as e:
            print(e)
            ret_data = {'code': 1, 'msg': str(e)}
            return jsonify(ret_data), 500

    img = draw(paths)
    try:
        cv2.imwrite(date_str + '/' + mnist_result + '_' + prefix[:-1] + '.jpg', img)
        with open(date_str+"/"+mnist_result + '_' + prefix[:-1]+'.txt', 'w+') as f:
            f.write(paths_str)
    except Exception as e:
        print(e)
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500
    ret_data = {'code': 0, 'msg': 'Successfully uploaded image.'}
    return jsonify(ret_data), 200

@app.route("/pyocr/savetraindata", methods=["OPTIONS"])
def optiontd():
    return ""

@app.route("/pyocr/savetraindata", methods=["POST"])
def save_train_data():
    type = request.form.get("type", 0)
    b64 = request.form.get("b64", "")
    if len(b64) == 0 or len(type) == 0:
        ret_data = {'code': 1, 'msg': 'Param error!'}
        return jsonify(ret_data), 400
    mnist_type = r" 0123456789+-×÷=><.()%[]ABCDEF√∟亅つ"
    folder = "tmp/mnist_traindata/" + str(type)
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    try:
        b64 = str.replace(b64, ' ', '+')
        if 'data:image' in b64:
            b64 = re.sub('data:image/(jpg|png|JPG|PNG);base64,', '', b64)
        imgdata = base64.urlsafe_b64decode(b64)
        prefix = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        date_str = str(datetime.datetime.now())
        date_str = 'mnist-' + str.split(date_str, ' ')[0]
        with open(folder + "/" + date_str + "-" + prefix + ".jpg", 'wb') as f:
            f.write(imgdata)
    except Exception as e:
        print(e)
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500
    ret_data = {'code': 0, 'msg': "上传成功"}
    return jsonify(ret_data), 200


@app.route("/pyocr/saveqdata", methods=['OPTIONS'])
def option3():
    return ""


@app.route("/pyocr/saveqdata", methods=['POST'])
def save_q_data():
    uid = request.form.get("uid", "")
    qid = request.form.get("qid", "")
    qdata = request.form.get("qdata", "")
    is_ans = request.form.get("ans", 0)
    if len(uid) == 0 or len(qdata) == 0 or len(qid) == 0:
        ret_data = {'code': 1, 'msg': "wrong param"}
        return jsonify(ret_data), 400

    prefix = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    date_str = str(datetime.datetime.now())
    date_str = str.split(date_str, ' ')[0]
    fname = [uid, qid, date_str, prefix]
    fname = "_".join(fname)

    folder = "tmp/"
    if is_ans == 0:
        folder = 'tmp/qdata-' + date_str
    elif is_ans == 1:
        folder = 'tmp/qans-' + date_str
    if not os.path.exists(folder):
        try:
            os.makedirs(folder, exist_ok=True)
        except Exception as e:
            print(e)
            ret_data = {'code': 1, 'msg': str(e)}
            return jsonify(ret_data), 500

    try:
        with open(folder+"/"+fname + '.txt', 'w+',encoding='utf-8') as f:
            f.write(qdata)
    except Exception as e:
        print(e)
        ret_data = {'code': 1, 'msg': str(e)}
        return jsonify(ret_data), 500
    ret_data = {'code': 0, 'msg': 'Successfully uploaded qdata.'}
    return jsonify(ret_data), 200



@app.route("/test", methods=['POST', 'GET'])
def test():
    return "test api", 200

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id,Access-Control-Allow-Origin,Content-Type,Access-Control-Allow-Credentials,cache-control')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ =='__main__':
    print("=============== Image upload server from AI project(ocr,mnist etc.)  v1.0===============")
    app.run(host="0.0.0.0", port=8080, debug=False)