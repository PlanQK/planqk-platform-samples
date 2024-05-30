import torch
from torch import nn
from loguru import logger

# parameters with ~ 80 % acc after training
# c1=48
# c2=96
# l1=256

class ConfigNet(nn.Module):
    def __init__(self, c1=10, c2=10, l1=50, dropout=0.1):
        super().__init__()
        self.dropout = dropout
        
        # first arg: #channel, 2nd arg: # output channels, 3rd arg: filter dim
        self.conv1 = nn.Conv2d(3, c1, 3)
        self.conv2 = nn.Conv2d(c1, c1, 3)
        self.conv3 = nn.Conv2d(c1, c2, 3)
        self.conv4 = nn.Conv2d(c2, c2, 3, stride=2)
        self.flat = nn.Flatten()
        
        # 96 channels of 12 x 12 pixel images after 4 conv layers
        self.batch_norm = nn.BatchNorm1d(c2 * 12 * 12) 
        self.fc1 = nn.Linear(c2 * 12 * 12, l1)
        
        self.fc2 = nn.Linear(l1, 10)
        # 10 classes: 'airplane','automobile','bird','cat','deer',
        # 'dog','frog','horse','ship','truck']

    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = nn.functional.dropout(x, self.dropout)
        x = nn.functional.relu(self.conv3(x))
        x = nn.functional.relu(self.conv4(x))
        x = nn.functional.dropout(x, 0.5)
        x = self.flat(x)
        x = nn.functional.relu(self.batch_norm(x))
        x = nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def train_model(dataloader, model, loss_fn, optimizer, device, interim_info_batch=200):
    size = len(dataloader.dataset)
    model.train()
    
    for batch_idx, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)
        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)
        optimizer.zero_grad() # don't accumulate gradient over multiple batches
        loss.backward() # backpropagation
        optimizer.step()
        if batch_idx % interim_info_batch == 0:
            loss, current = loss.item(), batch_idx * len(X)
            logger.info(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
            
def test_model(dataloader, model, loss_fn, device, ):
    size = len(dataloader.dataset)
    n_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    
    with torch.no_grad():
        for X,y in dataloader:
            X,y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= n_batches
    correct/= size
    
    logger.info(f"Test Error: Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

