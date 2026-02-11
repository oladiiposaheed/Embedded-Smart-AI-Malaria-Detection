# data_setup.py
import os
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms

class MalariaDataset(Dataset):
    def __init__(self, root_dir, classes, transform=None):
        self.root_dir = root_dir
        self.classes = classes
        self.transform = transform
        self.image_paths = []
        self.labels = []
        
        for idx, cls in enumerate(classes):
            img_path = os.path.join(root_dir, cls)
            for img_name in os.listdir(img_path):
                self.image_paths.append(os.path.join(img_path, img_name))
                self.labels.append(idx)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        label = self.labels[idx]
        img = Image.open(img_path).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, label

def get_loaders(root_dir="data/raw", batch_size=32, split_ratio=0.8):
    classes = ["Parasitized", "Uninfected"]

    transform = transforms.Compose([
        transforms.Resize((150, 150)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5],
                             std=[0.5, 0.5, 0.5])
    ])

    malaria_dataset = MalariaDataset(root_dir=root_dir, classes=classes, transform=transform)

    train_size = int(split_ratio * len(malaria_dataset))
    test_size = len(malaria_dataset) - train_size
    train_dataset, test_dataset = random_split(malaria_dataset, [train_size, test_size])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader, classes
if __name__ == "__main__":
    train_loader, test_loader, classes = get_loaders()
    print(f"Number of training batches: {len(train_loader)}")
    print(f"Number of testing batches: {len(test_loader)}")