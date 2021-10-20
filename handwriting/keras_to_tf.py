from keras import backend as K
import tensorflow as tf
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform

def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    """
    :param session: 需要转换的tensorflow的session
    :param keep_var_names:需要保留的variable，默认全部转换constant
    :param output_names:output的名字
    :param clear_devices:是否移除设备指令以获得更好的可移植性
    :return:
    """
    from tensorflow.python.framework.graph_util import convert_variables_to_constants
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        # 如果指定了output名字，则复制一个新的Tensor，并且以指定的名字命名
        if len(output_names) > 0:
            for i in range(len(output_names)):
                # 当前graph中复制一个新的Tensor，指定名字
                tf.identity(model.model.outputs[i], name=output_names[i])
        output_names += [v.op.name for v in tf.global_variables()]
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
        frozen_graph = convert_variables_to_constants(session, input_graph_def,
                                                      output_names, freeze_var_names)
        return frozen_graph


if __name__ == '__main__':
    # model = load_model("model/20190118v3.h5")
    # model = tf.keras.models.load_model("model/20190118v3.h5")
    with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        # model = load_model("model/20190118v3.h5")
        # model = load_model("model/20190322v5.h5")
        model = load_model("model/20191017v1.h5")
    print(model.input.op.name)
    print(model.output.op.name)
    frozen_graph = freeze_session(K.get_session(), output_names=["output"])
    tf.train.write_graph(frozen_graph, "./", "model3.pb", as_text=False)

