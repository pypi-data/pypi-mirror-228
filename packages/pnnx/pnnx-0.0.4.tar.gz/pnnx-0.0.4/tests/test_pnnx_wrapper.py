if '__file__' in globals():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


import pnnx
import torch
import torchvision
import torch.nn as nn

class TestNet(nn.Module):
    def __init__(self):
        super(TestNet, self).__init__()
        self.fc1 = nn.Linear(10,10)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(10,2)
    def forward(self,x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        return x

class TestNet_multi_input(nn.Module):
    def __init__(self):
        super(TestNet_multi_input, self).__init__()
        self.fc1_1 = nn.Linear(10, 10)
        self.fc1_2 = nn.Linear(5, 5)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(15, 10)  
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(10, 2)

    def forward(self, x1, x2):
        x1 = self.fc1_1(x1)
        x2 = self.fc1_2(x2)
        
        x = torch.cat((x1, x2), dim=1)  
        x = self.fc2(x)
        x = self.relu2(x)
        
        x = self.fc3(x)
        return x

class TestNet_dynamic_input(nn.Module):
    def __init__(self):
        super(TestNet_dynamic_input, self).__init__()
        self.conv = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)

    def forward(self, x):
        return self.conv(x)


def test_pnnx_export():
    test_model = TestNet()
    x = torch.rand(32, 10)
    pnnx.export(test_model, x)

def test_pnnx_export_multi_input():
    test_model_multi_input = TestNet_multi_input()
    x1 = torch.rand(32, 10)
    x2 = torch.rand(32, 5)
    pnnx.export(test_model_multi_input, (x1, x2))

def test_pnnx_export_dynamic_input():
    test_model_export_dynamic_input = TestNet_dynamic_input()
    x1 = torch.rand(32, 3, 224, 224)
    x2 = torch.rand(32, 3, 512, 512)
    pnnx.export(test_model_export_dynamic_input, x1, x2)


def test_pnnx_run():

    torchscript_path = "test_model.pt"

    # x = torch.rand(1, 3, 224, 224)
    x = torch.rand(1,10)

    pnnx.run(torchscript_path, x, optlevel=0)



# def test_pnnx_export():
    
#     resnet_test_model = torchvision.models.resnet18()

#     x = torch.rand(1, 3, 224, 224)

#     pnnx.export(resnet_test_model, x)


def test_pnnx_run():

    torchscript_path = "resnet_test_model.pt"

    # x = torch.rand(1, 3, 224, 224)
    x = torch.rand(1, 3, 224, 224)
    y = torch.rand(1, 3)
    z = torch.rand(1, 3, 224, 224)

    x2 = torch.rand(1, 3)
    y2 = torch.rand(1, 3, 224, 224)
    z2 = torch.rand(1, 3)

    # pnnx.run(torchscript_path, x)
    # pnnx.run(torchscript_path, x, pnnxparam="model.pnnx.param",  device= "cpu",  moduleop =("models.common.Focus","models.yolo.Detect"))
    pnnx.run(torchscript_path, inputshape=(x,y,z), inputshape2=(x2,y2,z2), optlevel=0, pnnxparam="model.pnnx.param",  device= "gpu",  moduleop =("models.common.Focus","models.yolo.Detect"))



if __name__ == "__main__":
    # test_pnnx_export()
    # test_pnnx_export_multi_input()
    # test_pnnx_export_dynamic_input()
    test_pnnx_run()
