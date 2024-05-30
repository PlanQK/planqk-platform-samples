import torch
from torch import nn
from loguru import logger

DEFAULT_DATA_PATH = "tmp/torch_data"

DEFAULT_CHANNELS_CONV1 = 10 # 48
DEFAULT_CHANNELS_CONV2 = 10 # 96
DEFAULT_LINEAR_LAYER_SIZE = 20 # 256 

DEFAULT_DEVICE = "cuda"
DEFAULT_BATCH_SIZE = 32
DEFAULT_LOSS = "CrossEntropyLoss"
DEFAULT_OPTIMIZER = "Adam"
DEFAULT_LEARNING_RATE = 0.001
DEFAULT_EPOCHS = 1

AVAILABLE_DEVICES = ["cuda", "cpu"]
AVAILABLE_LOSSES = ["CrossEntropyLoss", "cel"]
AVAILABLE_OPTIMIZER = ["sgd", "adam"]

def get_num_channels_conv1(params):
    num_channels_conv1 = params.get("num_channels_conv1", None)
    if num_channels_conv1 is None or not isinstance(num_channels_conv1, int):
        logger.info(f"No valid number of output-channels for Conv-Layer 1 was provided, is set to {DEFAULT_CHANNELS_CONV1}")
        num_channels_conv1 = DEFAULT_CHANNELS_CONV1
    else:
        logger.info(f"Number of Output Channels for Conv1: {num_channels_conv1}")
    return num_channels_conv1

def get_num_channels_conv2(params):    
    num_channels_conv2 = params.get("num_channels_conv2", None)
    if num_channels_conv2 is None or not isinstance(num_channels_conv2, int):
        logger.info(f"No valid number of output-channels for Conv-Layer 2 was provided, is set to {DEFAULT_CHANNELS_CONV2}")
        num_channels_conv2 = DEFAULT_CHANNELS_CONV2
    else:
        logger.info(f"Number of Output Channels for Conv2: {num_channels_conv2}")
    return num_channels_conv2

def get_linear_layer_size(params):
    linear_layer_size = params.get("linear_layer_size", None)
    if linear_layer_size is None or not isinstance(linear_layer_size, int):
        logger.info(f"No valid linear layer size was provided, is set to {DEFAULT_LINEAR_LAYER_SIZE}")
        linear_layer_size = DEFAULT_LINEAR_LAYER_SIZE
    else:
        logger.info(f"Linear Layer Size: {linear_layer_size}")
    return linear_layer_size

def get_device(params):
    device = params.get("device", None)
    if device is None or device not in AVAILABLE_DEVICES:
        logger.info("No valid device was proviced, is set to cpu.")
        device = "cpu"
    elif device == "cuda" and not torch.cuda.is_available():
        logger.info("Device was set to cuda but no GPU is available, device is set to cpu")
        device = "cpu"
    else:
        logger.info(f"Device: {device}")
    return device

def get_batch_size(params):
    batch_size = params.get("batch_size", None)
    if not isinstance(batch_size, int):
        logger.info(f"No valid batch_size was provided, is set to {DEFAULT_BATCH_SIZE}")
        batch_size = DEFAULT_BATCH_SIZE
    else:
        logger.info(f"Batch size: {batch_size}")
    return batch_size

def get_num_epochs(params):
    epochs = params.get("epochs", None)
    if epochs is None or not isinstance(epochs, int):
        logger.info(f"No valid amount of epochs provided, is set to {DEFAULT_EPOCHS}")
        epochs = DEFAULT_EPOCHS
    else:
        logger.info(f"Epochs: {epochs}")
    return epochs

def get_loss_fn(params):        
    loss_fn = params.get("loss_fn", None)
    if loss_fn is None or loss_fn not in AVAILABLE_LOSSES:
        logger.info(f"No valid loss function was provided, is set to {DEFAULT_LOSS}")
        loss_fn = nn.CrossEntropyLoss()
    elif loss_fn.casefold() == "crossentropyloss" or "cel":
        logger.info(f"Loss function: {loss_fn}")
        loss_fn = nn.CrossEntropyLoss()
    return loss_fn
    
def get_learning_rate(params):
    learning_rate = params.get("learning_rate", None)
    if learning_rate is None or not isinstance(learning_rate, float):
        logger.info(f"No valid learning rate was provided, is set to {DEFAULT_LEARNING_RATE}")
        learning_rate = DEFAULT_LEARNING_RATE
    else:
        logger.info(f"Learning Rate: {learning_rate}")
    return learning_rate
        
def get_data_path(params):
    data_path = params.get("data_path", None)
    if data_path is None:
        data_path = DEFAULT_DATA_PATH
    return data_path

def get_optimizer(params, model, learning_rate):
    optimizer = params.get("optimizer", None)
    if optimizer is None or optimizer.casefold() not in AVAILABLE_OPTIMIZER:
        logger.info(f"No valid optimizer was provided, is set to {DEFAULT_OPTIMIZER}")
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    elif optimizer.casefold() == "sgd":
        logger.info("Optimizer: SGD")
        optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    elif optimizer.casefold() == "adam":
        logger.info("Optimizer: Adam")
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    return optimizer