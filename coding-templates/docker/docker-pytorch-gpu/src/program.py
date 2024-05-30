from typing import Dict, Any, Optional

from loguru import logger
import time
import torch
from torch import nn
from torch.utils.data import DataLoader

from torchvision import transforms
from torchvision.datasets import CIFAR10

from .libs.return_objects import Response, ResultResponse
# Import your own libs
from .libs.nn_utils import train_model, test_model, ConfigNet
from .libs.parameter_handler import (
    get_num_channels_conv1,
    get_num_channels_conv2,
    get_linear_layer_size,
    get_loss_fn,
    get_batch_size,
    get_data_path,
    get_device,
    get_learning_rate,
    get_num_epochs,
    get_optimizer
)


def run(data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Response:

    # Parameter handling
    num_channels_conv1 = get_num_channels_conv1(params)
    num_channels_conv2 = get_num_channels_conv2(params)
    linear_layer_size = get_linear_layer_size(params)
    device = get_device(params)
    
    batch_size = get_batch_size(params)
    num_epochs = get_num_epochs(params)
    loss_fn = get_loss_fn(params)
    learning_rate = get_learning_rate(params)
        
    data_path = get_data_path(params)
    # Preprocessing
    normalization = transforms.Compose(
                                    [transforms.ToTensor(),
                                    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    training_data = CIFAR10(root=data_path,
                            train = True,
                            download = True,
                            transform=normalization)

    test_data = CIFAR10(root = data_path,
                        train = False,
                        download = True,
                        transform = normalization)
    
    train_dataloader = DataLoader(training_data,
                                batch_size=batch_size,
                                shuffle=True,
                                num_workers=0)
    test_dataloader = DataLoader(test_data,
                                batch_size=batch_size,
                                shuffle=True,
                                num_workers=0)
    
    # instantiate model
    model = ConfigNet(c1=num_channels_conv1,
                      c2=num_channels_conv2,
                      l1=linear_layer_size).to(device)
    # defining the optimizer
    optimizer = get_optimizer(params, model, learning_rate)
    
    # main training
    training_start_time = time.time()
    for iter_step in range(num_epochs):
        logger.info(f"Epoch #{iter_step+1}/{num_epochs}")
        train_model(train_dataloader, model, loss_fn, optimizer, device)
        logger.info(" ")
        test_model(test_dataloader, model, loss_fn, device)
        logger.info(" ")
    logger.info("Finished training")
    training_time = time.time() - training_start_time
    
    optimal_parameters = model.state_dict()
    result = {key: val.tolist() for key, val in optimal_parameters.items()}
    metadata = {"training_time": training_time, "training_device": device}
    # optimal_parameters = torch.model.state_dict(), "cifar_fc.pth") # to locally store model parameters
    
    return ResultResponse(result, metadata)