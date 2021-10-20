import cv2
import base64
import requests
import json



def test_upload():
    # upload_url = r'http://127.0.0.1:8080/pyocr/savemnistdata'
    # upload_url = r"http://192.168.6.30:30956/pyocr/savemnistdata"
    # upload_url = r"http://192.168.6.35:32481/pyocr/savemnistdata"
    upload_url = r'http://api.k12china.com/pyocr/savemnistdata'
    headers = {
        'accept': "*/*",
        'cache-control': "no-cache",
        'content-type': "application/x-www-form-urlencoded"
    }
    jstr = '[{"mnist": "1", "b64": "_9j_4AAQSkZJRgABAQAAAQABAAD_2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBggLDAsKDAkKCgr_2wBDAQICAgICAgUDAwUKBwYHCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgr_wAARCAAcABwDASIAAhEBAxEB_8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL_8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4-Tl5ufo6erx8vP09fb3-Pn6_8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL_8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3-Pn6_9oADAMBAAIRAxEAPwD9_K_N7_g59_bz_aw_4J3fsDeEfjX-x38V_wDhD_E2qfF_T9EvtS_sKw1DzLCTStVneHy76CaMZltoW3BQw2YBALA_pDX5Af8AB6r_AMosvAX_AGcBpX_pj1ygD9f6KKKACvwh_wCDwr9oPx38cPin8BP-CQHwX8Cf2p4m8X-ILHxYpuBFB9rv7ue70TR7O3uZLhI498smoef5yKq5tGWUATCv3erjNc_Z9-AniH4x6T-0b4g-B_g-_wDiFoOntYaF47vfDNrLrOnWrLOGggvWjM8MRFxcAojhSJ5Rj52yAdnRRRQB_9k="}, {"mnist": "2", "b64": "_9j_4AAQSkZJRgABAQAAAQABAAD_2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBggLDAsKDAkKCgr_2wBDAQICAgICAgUDAwUKBwYHCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgr_wAARCAAcABwDASIAAhEBAxEB_8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL_8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4-Tl5ufo6erx8vP09fb3-Pn6_8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL_8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3-Pn6_9oADAMBAAIRAxEAPwD9_K_N7_g59_bz_aw_4J3fsDeEfjX-x38V_wDhD_E2qfF_T9EvtS_sKw1DzLCTStVneHy76CaMZltoW3BQw2YBALA_pDX5Af8AB6r_AMosvAX_AGcBpX_pj1ygD9f6KKKACvwh_wCDwr9oPx38cPin8BP-CQHwX8Cf2p4m8X-ILHxYpuBFB9rv7ue70TR7O3uZLhI498smoef5yKq5tGWUATCv3erjNc_Z9-AniH4x6T-0b4g-B_g-_wDiFoOntYaF47vfDNrLrOnWrLOGggvWjM8MRFxcAojhSJ5Rj52yAdnRRRQB_9k="}]'
    # jstr = '11'
    payload = 'ver=100&num=11&mnistresult=' + str(jstr) + '&paths=[[[155.0,285.0],[168.18538,286.31854],[194.84285,293.26617],[217.08528,305.98547],[228.66692,320.58362],[241.26956,346.6739],[245.23463,377.05396],[229.64398,414.3222],[206.08345,451.53687],[179.0,483.0],[153.20532,504.8656],[136.28,520.41],[130.23961,525.7604],[125.76774,529.15485],[124.58261,531.8348],[142.2578,535.51605],[180.32312,537.218],[224.23785,540.4056],[260.96143,548.9896],[283.21854,558.7206],[290.24985,574.99963],[292.0,600.84717],[271.0,637.0],[230.95673,680.8321],[192.6739,721.84937],[157.91132,747.80853],[137.55695,764.3692],[125.18443,772.5437],[121.58304,774.6113],[121.0,775.0],[128.0,774.0]],[[504.0,309.0],[488.235,394.80872],[489.0,438.0],[496.2431,479.84625],[508.33807,525.8327],[526.2083,555.31244],[544.1234,583.1954],[563.6458,601.2425],[596.991,613.59686],[623.4826,618.54987],[648.5,616.5],[665.407,608.2696],[677.94116,598.71246],[680.0,597.0]],[[645.0,348.0],[614.72394,408.31708],[589.59906,484.80304],[572.8146,566.8808],[561.5011,643.91986],[552.2982,702.3687],[543.9609,752.55505],[538.036,786.54297],[538.0,805.0]],[[904.0,377.0],[902.92633,387.73645],[898.5,420.0],[900.0,476.70868],[901.2862,541.73676],[902.0,585.8002],[904.1077,624.4546],[899.69836,660.281],[890.3735,682.27203],[870.9457,711.276],[838.3928,735.1512],[800.83295,755.58356],[776.9968,764.1188],[762.35315,765.0],[753.264,763.8773],[751.0,761.0],[752.0,752.0]],[[949.0,389.0],[977.31146,405.7459],[1010.1399,421.35577],[1034.0,427.0]]]'
    # payload = 'mnistresult=' + str(
    #     jstr) + '&paths=[[[155.0,285.0],[168.18538,286.31854],[194.84285,293.26617],[217.08528,305.98547],[228.66692,320.58362],[241.26956,346.6739],[245.23463,377.05396],[229.64398,414.3222],[206.08345,451.53687],[179.0,483.0],[153.20532,504.8656],[136.28,520.41],[130.23961,525.7604],[125.76774,529.15485],[124.58261,531.8348],[142.2578,535.51605],[180.32312,537.218],[224.23785,540.4056],[260.96143,548.9896],[283.21854,558.7206],[290.24985,574.99963],[292.0,600.84717],[271.0,637.0],[230.95673,680.8321],[192.6739,721.84937],[157.91132,747.80853],[137.55695,764.3692],[125.18443,772.5437],[121.58304,774.6113],[121.0,775.0],[128.0,774.0]],[[504.0,309.0],[488.235,394.80872],[489.0,438.0],[496.2431,479.84625],[508.33807,525.8327],[526.2083,555.31244],[544.1234,583.1954],[563.6458,601.2425],[596.991,613.59686],[623.4826,618.54987],[648.5,616.5],[665.407,608.2696],[677.94116,598.71246],[680.0,597.0]],[[645.0,348.0],[614.72394,408.31708],[589.59906,484.80304],[572.8146,566.8808],[561.5011,643.91986],[552.2982,702.3687],[543.9609,752.55505],[538.036,786.54297],[538.0,805.0]],[[904.0,377.0],[902.92633,387.73645],[898.5,420.0],[900.0,476.70868],[901.2862,541.73676],[902.0,585.8002],[904.1077,624.4546],[899.69836,660.281],[890.3735,682.27203],[870.9457,711.276],[838.3928,735.1512],[800.83295,755.58356],[776.9968,764.1188],[762.35315,765.0],[753.264,763.8773],[751.0,761.0],[752.0,752.0]],[[949.0,389.0],[977.31146,405.7459],[1010.1399,421.35577],[1034.0,427.0]]]'
    print(payload)
    response = requests.request("POST", upload_url, data=payload.encode(), headers=headers)
    print("response.text = ", response.text)

def test_upload2():
    # upload_url = r'http://127.0.0.1:8080/pyocr/savemnistdata2'
    # upload_url = r"http://192.168.6.31:30956/pyocr/savemnistdata2"
    upload_url = r"http://192.168.6.35:32481/pyocr/savemnistdata2"
    # upload_url = r'http://api.k12china.com/pyocr/savemnistdata2'
    headers = {
        'accept': "*/*",
        'cache-control': "no-cache",
        'content-type': "application/x-www-form-urlencoded"
    }

    payload = 'split=T&mnistresult=345&paths=[[[155.0,285.0],[168.18538,286.31854],[194.84285,293.26617],[217.08528,305.98547],[228.66692,320.58362],[241.26956,346.6739],[245.23463,377.05396],[229.64398,414.3222],[206.08345,451.53687],[179.0,483.0],[153.20532,504.8656],[136.28,520.41],[130.23961,525.7604],[125.76774,529.15485],[124.58261,531.8348],[142.2578,535.51605],[180.32312,537.218],[224.23785,540.4056],[260.96143,548.9896],[283.21854,558.7206],[290.24985,574.99963],[292.0,600.84717],[271.0,637.0],[230.95673,680.8321],[192.6739,721.84937],[157.91132,747.80853],[137.55695,764.3692],[125.18443,772.5437],[121.58304,774.6113],[121.0,775.0],[128.0,774.0]],[[504.0,309.0],[488.235,394.80872],[489.0,438.0],[496.2431,479.84625],[508.33807,525.8327],[526.2083,555.31244],[544.1234,583.1954],[563.6458,601.2425],[596.991,613.59686],[623.4826,618.54987],[648.5,616.5],[665.407,608.2696],[677.94116,598.71246],[680.0,597.0]],[[645.0,348.0],[614.72394,408.31708],[589.59906,484.80304],[572.8146,566.8808],[561.5011,643.91986],[552.2982,702.3687],[543.9609,752.55505],[538.036,786.54297],[538.0,805.0]],[[904.0,377.0],[902.92633,387.73645],[898.5,420.0],[900.0,476.70868],[901.2862,541.73676],[902.0,585.8002],[904.1077,624.4546],[899.69836,660.281],[890.3735,682.27203],[870.9457,711.276],[838.3928,735.1512],[800.83295,755.58356],[776.9968,764.1188],[762.35315,765.0],[753.264,763.8773],[751.0,761.0],[752.0,752.0]],[[949.0,389.0],[977.31146,405.7459],[1010.1399,421.35577],[1034.0,427.0]]]'
    print(payload)
    response = requests.request("POST", upload_url, data=payload.encode(), headers=headers)
    print(response.text)
    assert response.status_code == 200

# def test_upload():
#     upload_url = r'http://127.0.0.1:8080/pyocr/savemnistdata'
#     upload_url = r"http://192.168.6.31:30956 /pyocr/savemnistdata"
#     headers = {
#         'accept': "*/*",
#         'cache-control': "no-cache",
#         'content-type': "application/x-www-form-urlencoded"
#     }
#
#     im = cv2.imread('1.jpg')
#     b = cv2.imencode('.jpg', im)[1].tostring()
#     b = base64.urlsafe_b64encode(b)
#     bstr = b.decode()
#     obj = [
#         {
#             'mnist':'1',
#             'b64':bstr,
#         },
#         {
#             'mnist': '2',
#             'b64': bstr,
#         },
#     ]
#
#     jstr = json.dumps(obj, ensure_ascii=False, )
#     print('send data : ', jstr)
#     print('size : ', len(jstr))
#     payload = 'mnistresult='+jstr
#     response = requests.request("POST", upload_url, data=payload.encode(), headers=headers)
#     print(response.text)