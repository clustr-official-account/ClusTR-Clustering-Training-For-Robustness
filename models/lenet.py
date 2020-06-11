import torch
import torch.nn as nn
import torch.nn.functional as F

# Build Network
class LeNet(nn.Module):

    def __init__(self, num_classes):
        emb_dim = 512
        '''
        Define the initialization function of LeNet, this function defines
        the basic structure of the neural network
        '''
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=5, stride=1, padding=2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2)
        self.embedding = nn.Linear(64*7*7, emb_dim)
        self.classifier = nn.Linear(emb_dim, num_classes)

        self.layer1 = None
        self.layer2 = None
        self.features = None
        self.embeddings = None
        self.norm_embeddings = None

    def forward(self, x, multi_res=False):
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)
        self.layer1 = x

        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        self.layer2 = x

        x = x.view(-1, self.num_flat_features(x))
        if multi_res:
            embeddings_2 = x
        embeddings = self.embedding(x)
        logits = self.classifier(embeddings)

        if multi_res:
            return logits, embeddings, embeddings_2
        else:
            return logits, embeddings

    def num_flat_features(self, x):
        '''
        Calculate the total tensor x feature amount
        '''

        size = x.size()[1:] # All dimensions except batch dimension
        num_features = 1
        for s in size:
            num_features *= s

        return num_features

    def name(self):
        return 'lenet-magnet'
