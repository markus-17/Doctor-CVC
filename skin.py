import torch
from torch import nn, Tensor
from torchvision import transforms, models


transform_pipe = transforms.Compose([
    transforms.Resize(size=256),
    transforms.CenterCrop(size=224),  # Image net standars
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )  # Imagenet standards
])


model = models.resnet50(pretrained=False)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2)
model.load_state_dict(torch.load('skin.pt', map_location=torch.device('cpu')))


class_names = ['benign', 'malignant']


def predict(img) -> str:
    img = img.convert('RGB')
    img_t: Tensor = transform_pipe(img)
    img_t.unsqueeze_(0)

    model.eval()
    with torch.no_grad():
        output = model(img_t)
        index = torch.max(output, dim=1)[1].item()

    return class_names[index]
