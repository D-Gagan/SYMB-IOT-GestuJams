import torch
from torchvision.transforms import ToTensor, Grayscale, Resize, Compose
import torch.nn as nn
import numpy
import cv2 as cv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import random

device = torch.device("cpu")

class GestureModel(nn.Module):
    
    def __init__(self):
        super().__init__()
        # input: m x 1 x 28 x 28
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(16),
        ) # m x 16 x 28 x 28
        self.conv2 = nn.Sequential(
            # nn.Dropout(p=0.2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(2),
        ) # m x 32 x 14 x 14
        self.conv3 = nn.Sequential(
            # nn.Dropout(p=0.2),
            nn.Conv2d(32, 64, kernel_size=3),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(2),
        ) # m x 64 x 6 x 6
        self.conv4 = nn.Sequential(
            # nn.Dropout(p=0.2),
            nn.Conv2d(64, 128, kernel_size=3),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(2),
        ) # m x 128 x 2 x 2
        self.classifier = nn.Sequential(
            nn.Flatten(), # m x 128*2*2
            nn.Dropout(p=0.2),
            nn.Linear(128*2*2, 4),
            nn.Softmax(dim=1),
        ) # m x 4

    def forward(self, input):
        x = self.conv1(input)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        output = self.classifier(x)
        return output

service = Service(r'C:\Users\Gagan D\Downloads\geckodriver-v0.33.0-win32\geckodriver')

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2F")

time.sleep(5)

username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")
login_button = driver.find_element_by_class_name("_35KWN1fW7kA9ui9VLLk3E3")

username.send_keys("your_username")
password.send_keys("your_password")
login_button.click()

time.sleep
