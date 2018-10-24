from grpc.beta import implementations
import tensorflow as tf
import numpy
from logistic_regression_input import *

from tensorflow.core.framework import types_pb2
from tensorflow.python.platform import flags
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2


def main(data_pred):
    data_for_pred = numpy.float32(data_pred)
    # Prepare request
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'log_model1'
    request.inputs['inputs'].dtype = types_pb2.DT_FLOAT
    request.inputs['inputs'].CopyFrom(
        tf.contrib.util.make_tensor_proto(data_for_pred))
    request.output_filter.append('classes')
    # Send request
    host, port = FLAGS.server.split(':')
    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    prediction = stub.Predict(request, 5.0)  # 5 secs timeout
    floats = prediction.outputs['classes'].int64_val
    predicted_array = numpy.asarray(floats)
    print(prediction)

    return predicted_array
