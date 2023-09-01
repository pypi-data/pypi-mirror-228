# pnnx_package
pnnx python wrapper



## How to use

```shell
pip install pnnx
```


**example**

```python
import pnnx
import torch
import torchvision

def test_pnnx_export():
    resnet_test_model = torchvision.models.resnet18()
    x = torch.rand(1, 3, 224, 224)
    pnnx.export(resnet_test_model, x)

if __name__ == "__main__":
    test_pnnx_export()
```

You should combine inputs use **tuple**, e.g. inputshape, moduleop...
Here is a more complex example:
```
    pnnx.export(your_model, inputshape=(x,y), inputshape2=(x2,y2), optlevel=0, pnnxparam="model.pnnx.param",  device= "gpu",  moduleop =("models.common.Focus","models.yolo.Detect"))
```