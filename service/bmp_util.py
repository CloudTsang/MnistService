import cv2
import numpy as np
import json
from path_object import PathObject, get_path_objects
from model import predict
from const import IMG_SIZE
from dict import check_trace
import re


def sort_fraction_pobjs(pobjs):
    fpobjs = []
    for i in range(len(pobjs)):
        tmpObj = pobjs[i]
        is_added = False
        for j in range(len(fpobjs)-1, -1, -1):
            tmpObj2 = fpobjs[j]
            if tmpObj2.check_contain(tmpObj) or tmpObj2.check_cross(tmpObj): # 包含&大部分相交
                is_added = True
                tmpObj2.add_paths(tmpObj)
                fpobjs[j] = tmpObj2
                break;
            elif tmpObj2.check5(tmpObj) and j == len(fpobjs) - 1:  # 5
                tmpObj3 = PathObject()
                tmpObj3.add_paths(tmpObj)
                tmpObj3.add_paths(tmpObj2)
                im = tmpObj3.draw(IMG_SIZE, IMG_SIZE)
                res, _ = predict(im)
                im = None
                if res == "5":
                    tmpObj3.checked5 = True
                    is_added = True
                    fpobjs[j] = tmpObj3
        if not is_added:
            fpobjs.append(tmpObj)
    return fpobjs


def sort_pobjs(pobjs):
    fpobjs = []
    for i in range(len(pobjs)):
        tmpObj = pobjs[i]
        is_added = False
        for j in range(len(fpobjs)-1, -1, -1):
            tmpObj2 = fpobjs[j]
            if tmpObj2.check_contain(tmpObj) or tmpObj2.check_cross(tmpObj): # 包含&大部分相交
                is_added = True
                tmpObj2.add_paths(tmpObj)
                fpobjs[j] = tmpObj2
                break;
            elif tmpObj2.check5(tmpObj) and j == len(fpobjs)-1: #5
                tmpObj3 = PathObject()
                tmpObj3.add_paths(tmpObj)
                tmpObj3.add_paths(tmpObj2)
                im = tmpObj3.draw(IMG_SIZE, IMG_SIZE)
                res, _ = predict(im)
                im = None
                if res == "5":
                    tmpObj3.checked5 = True
                    is_added = True
                    fpobjs[j] = tmpObj3
            elif tmpObj2.check_chn8(tmpObj) and j == len(fpobjs)-1: #八
                im = tmpObj2.draw(IMG_SIZE, IMG_SIZE)
                res, _ = predict(im)
                im = None
                if res == "√" or res == "1":
                    tmpObj3 = PathObject()
                    tmpObj3.add_paths(tmpObj)
                    tmpObj3.add_paths(tmpObj2)
                    im = tmpObj3.draw(IMG_SIZE, IMG_SIZE)
                    res, _ = predict(im)
                    im = None
                    if res == "八":
                        tmpObj3.checked8 = True
                        is_added = True
                        fpobjs[j] = tmpObj3
        if not is_added:
            fpobjs.append(tmpObj)
        geObj = PathObject()
        for k in range(len(fpobjs)-1, len(fpobjs)-4, -1):
            if k<0:
                break
            geObj.add_paths(fpobjs[k])
            if len(geObj.paths) == 3:
                im = geObj.draw(IMG_SIZE, IMG_SIZE)
                res, _ = predict(im)
                im = None
                if res == "个":
                    fpobjs = fpobjs[:k]
                    geObj.checked5 = False
                    geObj.checked8 = False
                    geObj.checkedGe = True
                    fpobjs.append(geObj)
            elif len(geObj.paths) > 3:
                break

    mnist_result = ""
    for i in range(len(fpobjs)):
        pobj = fpobjs[i]
        if pobj.checked5:
            mnist_result += "5"
            continue
        elif pobj.checked8:
            mnist_result += "八"
            continue
        elif pobj.checkedGe:
            mnist_result += "个"
            continue
        if len(pobj.paths)==1 and i>=1:
            lastObj = fpobjs[i-1]
            lasth = lastObj.max_y - lastObj.min_y
            size1 = max(lastObj.max_x-lastObj.min_x, lastObj.max_y-lastObj.min_y)
            size2 = pobj.max_x - pobj.max_y
            if size2<size1*0.3 and pobj.min_y > lastObj.min_y + lasth/2:
                mnist_result += "."
                continue

        fras = pobj.check_fraction()
        if fras is not None:
            fra_str = ""
            up = sort_fraction_pobjs(fras[0])
            for fra_obj in up:
                if fra_obj.checked5 is True:
                    fra_str += "5"
                else:
                    im = fra_obj.draw(IMG_SIZE, IMG_SIZE)
                    res, _ = predict(im, False)
                    im = None
                    fra_str += res
            fra_str+=","
            down = sort_fraction_pobjs(fras[1])
            for fra_obj in down:
                if fra_obj.checked5 is True:
                    fra_str += "5"
                else:
                    im = fra_obj.draw(IMG_SIZE, IMG_SIZE)
                    res, _ = predict(im, False)
                    im = None
                    fra_str += res
            fra_str = "[fra]"+fra_str+"[/fra]"
            mnist_result += fra_str
            match_obj = re.match("[0-9]+\[fra\]", mnist_result)
            if match_obj is not None:
                tmp_s = match_obj.group()
                tmp_s = tmp_s.replace("[fra]", ",")
                tmp_s = "[fra]" + tmp_s
                mnist_result.replace(match_obj.group(), tmp_s)
            continue

        im = pobj.draw(IMG_SIZE, IMG_SIZE)
        res, res2 = predict(im, False)
        im = None
        if res == "÷" and len(pobj.paths) >= 4:
            res = "六"
        elif res == "六" and len(pobj.paths) == 3:
            res = "÷"
        elif res == "<" and len(pobj.paths) >= 2:
            res = "七"
        elif res == "七" and len(pobj.paths) == 1:
            res = "<"
        elif res == "4" and len(pobj.paths) == 3:
            res = "千"
        elif res == "千" and len(pobj.paths) <= 2:
            res = "4"
        mnist_result += res

    mnist_result = mnist_result.replace("m2", "㎡")
    mnist_result = mnist_result.replace("m3", "m³")
    mnist_result = mnist_result.replace("+.", "六")
    mnist_result = mnist_result.replace("÷.", "六")
    mnist_result = mnist_result.replace(".+", "六")
    mnist_result = mnist_result.replace(".÷", "六")
    mnist_result = mnist_result.replace(")四", "四")
    mnist_result = mnist_result.replace("(四", "四")
    mnist_result = mnist_result.replace("1四", "四")
    mnist_result = mnist_result.replace("1匹", "四")
    return mnist_result


def sort_pobjs_num(pobjs):
    fpobjs = []
    for i in range(len(pobjs)):
        tmpObj = pobjs[i]
        is_added = False
        for j in range(len(fpobjs) - 1, -1, -1):
            tmpObj2 = fpobjs[j]
            if tmpObj2.check_contain(tmpObj) or tmpObj2.check_cross(tmpObj):  # 包含&大部分相交
                is_added = True
                tmpObj2.add_paths(tmpObj)
                fpobjs[j] = tmpObj2
                break;
            elif tmpObj2.check5(tmpObj) and j == len(fpobjs) - 1:  # 5
                tmpObj3 = PathObject()
                tmpObj3.add_paths(tmpObj)
                tmpObj3.add_paths(tmpObj2)
                im = tmpObj3.draw(IMG_SIZE, IMG_SIZE)
                res, _ = predict(im)
                im = None
                if res == "5":
                    tmpObj3.checked5 = True
                    is_added = True
                    fpobjs[j] = tmpObj3
        if not is_added:
            fpobjs.append(tmpObj)

    mnist_result = ""
    for i in range(len(fpobjs)):
        pobj = fpobjs[i]
        if pobj.checked5:
            mnist_result += "5"
            continue
        if len(pobj.paths) == 1 and i >= 1:
            lastObj = fpobjs[i - 1]
            lasth = lastObj.max_y - lastObj.min_y
            size1 = max(lastObj.max_x - lastObj.min_x, lastObj.max_y - lastObj.min_y)
            size2 = pobj.max_x - pobj.max_y
            if size2 < size1 * 0.3 and pobj.min_y > lastObj.min_y + lasth / 2:
                mnist_result += "."
                continue
        im = pobj.draw(IMG_SIZE, IMG_SIZE)
        res, res2 = predict(im, False)
        im = None
        mnist_result += res
    return mnist_result, fpobjs


# 防止易混淆字符分摊了识别分数导致进入单笔识别
def check_if_single_word(result):
    s = '÷六七<千4'
    if s.find(result[0]['label']) and s.find(result[1]['label']):
        if result[0]['value'] + result[1]['value'] < 0.85:
            return True
    return False

def sort_pobjs_trace(pobjs):
    fpobjs = []
    for i in range(len(pobjs)):
        tmpObj = pobjs[i]
        is_added = False
        for j in range(len(fpobjs)-1, -1, -1):
            tmpObj2 = fpobjs[j]
            if tmpObj2.check_contain(tmpObj) or tmpObj2.check_cross(tmpObj): # 包含&大部分相交
                is_added = True
                tmpObj2.add_paths(tmpObj, keep_obj=True)
                fpobjs[j] = tmpObj2
                break
        if not is_added:
            fpobjs.append(tmpObj)


    mnist_result = ''
    for i in range(len(fpobjs)):
        pobj = fpobjs[i]

        if len(pobj.paths)==1 and i>=1:
            lastObj = fpobjs[i-1]
            lasth = lastObj.max_y - lastObj.min_y
            size1 = max(lastObj.max_x-lastObj.min_x, lastObj.max_y-lastObj.min_y)
            size2 = pobj.max_x - pobj.max_y
            if size2<size1*0.3 and pobj.min_y > lastObj.min_y + lasth/2:
                mnist_result += "."
                continue

        im = pobj.draw(IMG_SIZE, IMG_SIZE)
        res, res2 = predict(im, False)
        im = None
        print('res2 : ', res2)
        if len(res2)>0:
            if check_if_single_word(res2) and len(pobj.added_pobjs)>=2:
            # if res2[0]['value'] < 0.85 and len(pobj.added_pobjs)>=2: #多笔画pathobj识别分数低于0.85时拆分单笔划再识别
                apobjs = pobj.added_pobjs
                for j in range(len(apobjs)):
                    pobj2 = apobjs[j]
                    im2 = pobj2.draw(IMG_SIZE, IMG_SIZE)
                    res, _ = predict(im2, False)
                    im2 = None
                    mnist_result += res
            else:
                if res == "÷" and len(pobj.paths) >= 4:
                    res = "六"
                elif res == "六" and len(pobj.paths) == 3:
                    res = "÷"
                elif res == "<" and len(pobj.paths) >= 2:
                    res = "七"
                elif res == "七" and len(pobj.paths) == 1:
                    res = "<"
                elif res == "4" and len(pobj.paths) == 3:
                    res = "千"
                elif res == "千" and len(pobj.paths) <= 2:
                    res = "4"
                mnist_result += res
    mnist_result = check_trace(mnist_result)
    mnist_result = mnist_result.replace("m2", "㎡")
    mnist_result = mnist_result.replace("m3", "m³")
    mnist_result = mnist_result.replace("+.", "六")
    mnist_result = mnist_result.replace("÷.", "六")
    mnist_result = mnist_result.replace(".+", "六")
    mnist_result = mnist_result.replace(".÷", "六")
    mnist_result = mnist_result.replace(")四", "四")
    mnist_result = mnist_result.replace("(四", "四")
    mnist_result = mnist_result.replace("1四", "四")
    mnist_result = mnist_result.replace("1匹", "四")
    mnist_result = mnist_result.replace("つ", ">")
    return mnist_result


if __name__ == "__main__":
    # 345
    s = "[[[155.0,285.0],[168.18538,286.31854],[194.84285,293.26617],[217.08528,305.98547],[228.66692,320.58362],[241.26956,346.6739],[245.23463,377.05396],[229.64398,414.3222],[206.08345,451.53687],[179.0,483.0],[153.20532,504.8656],[136.28,520.41],[130.23961,525.7604],[125.76774,529.15485],[124.58261,531.8348],[142.2578,535.51605],[180.32312,537.218],[224.23785,540.4056],[260.96143,548.9896],[283.21854,558.7206],[290.24985,574.99963],[292.0,600.84717],[271.0,637.0],[230.95673,680.8321],[192.6739,721.84937],[157.91132,747.80853],[137.55695,764.3692],[125.18443,772.5437],[121.58304,774.6113],[121.0,775.0],[128.0,774.0]],[[504.0,309.0],[488.235,394.80872],[489.0,438.0],[496.2431,479.84625],[508.33807,525.8327],[526.2083,555.31244],[544.1234,583.1954],[563.6458,601.2425],[596.991,613.59686],[623.4826,618.54987],[648.5,616.5],[665.407,608.2696],[677.94116,598.71246],[680.0,597.0]],[[645.0,348.0],[614.72394,408.31708],[589.59906,484.80304],[572.8146,566.8808],[561.5011,643.91986],[552.2982,702.3687],[543.9609,752.55505],[538.036,786.54297],[538.0,805.0]],[[904.0,377.0],[902.92633,387.73645],[898.5,420.0],[900.0,476.70868],[901.2862,541.73676],[902.0,585.8002],[904.1077,624.4546],[899.69836,660.281],[890.3735,682.27203],[870.9457,711.276],[838.3928,735.1512],[800.83295,755.58356],[776.9968,764.1188],[762.35315,765.0],[753.264,763.8773],[751.0,761.0],[752.0,752.0]],[[949.0,389.0],[977.31146,405.7459],[1010.1399,421.35577],[1034.0,427.0]]]"
    #八个万7
    # s = "[[[674,469],[667,493],[658,517],[647,541],[634,560],[628,570],[621,578],[620,577]],[[729,397],[741,422],[753,442],[764,463],[777,483],[788,501],[799,518],[810,533],[819,542],[827,549],[834,552]],[[1019,342],[1001,385],[979,419],[958,446],[945,459],[940,465]],[[1038,362],[1068,391],[1083,406],[1100,420],[1114,431],[1128,439],[1136,446]],[[1013,403],[1017,437],[1020,483],[1019,534],[1019,579],[1019,601]],[[1278,380],[1321,374],[1352,367],[1379,361],[1398,358]],[[1328,407],[1322,422],[1306,463],[1291,503],[1280,537],[1272,562],[1265,577],[1263,585]],[[1316,458],[1337,452],[1362,442],[1385,438],[1402,436],[1413,439],[1417,445],[1417,458],[1414,483],[1413,512],[1410,539],[1409,558],[1407,573],[1404,584],[1400,593],[1395,600],[1391,600],[1384,600],[1357,590],[1334,578],[1320,567],[1310,565],[1306,565]],[[1557,386],[1586,380],[1610,375],[1630,372],[1645,371],[1654,370],[1660,371],[1663,374],[1664,379],[1649,417],[1632,464],[1617,507],[1608,538],[1604,564],[1601,581],[1596,593],[1594,600]]]"
    # ②
    # s = "[[[876,380],[864,405],[856,429],[850,456],[848,481],[851,503],[854,518],[862,533],[872,547],[886,556],[903,560],[925,558],[953,550],[983,533],[1008,511],[1024,484],[1035,456],[1037,425],[1034,401],[1025,382],[1008,360],[988,345],[965,341],[948,343],[920,358],[902,371],[888,380],[883,386],[880,391],[881,392],[882,393],[898,389],[926,378],[954,369],[972,368],[982,371],[979,380],[967,403],[946,431],[924,451],[907,463],[900,469],[898,469],[917,464],[943,457],[969,455],[995,454]]]"
    # 1/31
    # s = "[[[756,398],[790,390],[820,381],[860,374],[896,368],[934,365],[967,363],[998,363],[1023,365],[1043,368],[1058,371],[1067,376]],[[803,473],[819,469],[834,468],[849,471],[864,475],[872,483],[874,492],[872,501],[857,518],[841,529],[829,538],[823,542],[821,543],[839,542],[859,539],[881,537],[903,542],[917,546],[924,551],[923,558],[913,566],[896,575],[875,583],[856,588],[844,592],[836,594],[836,593],[837,593]],[[914,173],[913,192],[913,226],[912,263],[912,302],[912,304]],[[994,434],[991,444],[987,468],[981,502],[976,542],[970,577],[964,602],[960,618],[956,622],[952,622]]]"
    paths = json.loads(s)
    pObjs = get_path_objects(paths)
    # ocr_result = sort_pobjs(pObjs)
    ocr_result = sort_pobjs_trace(pObjs)
    print('res : ', ocr_result)