import requests
import json


headers = {
    'accept': "*/*",
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded"
    }

def test_mnist_success():
    url = 'http://localhost/mnist/detectxy'
    # url = 'http://192.168.20.61:8080/mnist/detectxy'
    payload = 'paths=[[[155.0,285.0],[168.18538,286.31854],[194.84285,293.26617],[217.08528,305.98547],[228.66692,320.58362],[241.26956,346.6739],[245.23463,377.05396],[229.64398,414.3222],[206.08345,451.53687],[179.0,483.0],[153.20532,504.8656],[136.28,520.41],[130.23961,525.7604],[125.76774,529.15485],[124.58261,531.8348],[142.2578,535.51605],[180.32312,537.218],[224.23785,540.4056],[260.96143,548.9896],[283.21854,558.7206],[290.24985,574.99963],[292.0,600.84717],[271.0,637.0],[230.95673,680.8321],[192.6739,721.84937],[157.91132,747.80853],[137.55695,764.3692],[125.18443,772.5437],[121.58304,774.6113],[121.0,775.0],[128.0,774.0]],[[504.0,309.0],[488.235,394.80872],[489.0,438.0],[496.2431,479.84625],[508.33807,525.8327],[526.2083,555.31244],[544.1234,583.1954],[563.6458,601.2425],[596.991,613.59686],[623.4826,618.54987],[648.5,616.5],[665.407,608.2696],[677.94116,598.71246],[680.0,597.0]],[[645.0,348.0],[614.72394,408.31708],[589.59906,484.80304],[572.8146,566.8808],[561.5011,643.91986],[552.2982,702.3687],[543.9609,752.55505],[538.036,786.54297],[538.0,805.0]],[[904.0,377.0],[902.92633,387.73645],[898.5,420.0],[900.0,476.70868],[901.2862,541.73676],[902.0,585.8002],[904.1077,624.4546],[899.69836,660.281],[890.3735,682.27203],[870.9457,711.276],[838.3928,735.1512],[800.83295,755.58356],[776.9968,764.1188],[762.35315,765.0],[753.264,763.8773],[751.0,761.0],[752.0,752.0]],[[949.0,389.0],[977.31146,405.7459],[1010.1399,421.35577],[1034.0,427.0]]]'
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    assert response.status_code == 200
    obj = json.loads(response.text)
    assert obj['code'] == 0

def test_version():
    url = 'http://localhost/mnist/version'
    response = requests.request("POST", url, headers=headers)
    print(response.text)
    assert response.status_code == 200
