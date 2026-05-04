from srgan_model import Generator
import torch
from torch.utils.data import DataLoader
import numpy as np
from PIL import Image
from dataset import testOnly_data

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
dataset = testOnly_data(LR_path = 'test_data', in_memory = False, transform = None)
loader = DataLoader(dataset, batch_size = 1, shuffle = False, num_workers = 0)

generator = Generator(img_feat = 3, n_feats = 64, kernel_size = 3, num_block = 16)
generator.load_state_dict(torch.load('model/SRGAN_gene_069.pt'))
generator = generator.to(device)
generator.eval()
with torch.no_grad():
    for i, te_data in enumerate(loader):
        lr = te_data['LR'].to(device)
        output, _ = generator(lr)
        output = output[0].cpu().numpy()
        output = (output + 1.0) / 2.0
        output = output.transpose(1,2,0)
        result = Image.fromarray((output * 255.0).astype(np.uint8))
        result.save('./result/res_%04d.png'%i)