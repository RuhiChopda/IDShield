<<<<<<< HEAD
# StegoFace: Deep Learning-Based ID Image Security  

## 📌 Project Description  
StegoFace is a deep learning-based **steganography model** designed to enhance **ID image security** by embedding **hidden authentication data** within facial images. The system ensures **tamper detection** while preserving **image quality and integrity**, making it a reliable solution for **photo substitution attack prevention**.  

## 🔥 Features  
- 🛡️ **Deep CNN-Based Steganography** for secure message embedding.  
- 🔍 **Binary Error-Correcting Codes (BECC)** for robustness against noise and compression.  
- 🔄 **Autoencoder-Decoder Framework** for high-precision encoding and decoding.  
- 🎯 **Recurrent Proposal Network (RPN)** for accurate facial region detection.  
- ⚡ **Real-time verification** for ID security applications.  

## 🛠️ PROJECT OUTPUT
![Alt Text](https://github.com/saidhanush27/StegoFace/blob/47c66502600b9d84f0d64276ad3c58dc26453082/Stegoface-images/5.png) <br><br>
![Alt Text](https://github.com/saidhanush27/StegoFace/blob/5f46b3893a7a1747ec0a92e522d5187a6ea8547c/Stegoface-images/2.png)  <br><br>
![Alt Text](https://github.com/saidhanush27/StegoFace/blob/5f46b3893a7a1747ec0a92e522d5187a6ea8547c/Stegoface-images/3.png)  <br><br>
![Alt Text](https://github.com/saidhanush27/StegoFace/blob/5f46b3893a7a1747ec0a92e522d5187a6ea8547c/Stegoface-images/4.png)   <br><br>


  
## 🛠️ Technologies Used  
- 🐍 **Python**  
- 🤖 **TensorFlow/Keras** (Deep Learning)  
- 🖼️ **OpenCV** (Image Processing)  
- 📊 **NumPy & Pandas** (Data Handling)  
- 📈 **Matplotlib & Seaborn** (Visualization)  

## 📂 Project Structure  
📦 StegoFace <br>
┣ 📂 dataset  <br>
┣ 📂 models  <br>
┣ 📂 preprocessing <br>
┣ 📂 encoder_decoder  <br>
┣ 📂 utilss <br>
┣ 📜 requirements.txt <br>
┣ 📜 README.md  <br>
┗ 📜 main.py  <br>


## 🚀 Installation & Usage  

**1. Clone the Repository**  
```bash
git clone https://github.com/yourusername/StegoFace.git
cd StegoFace
```


2. Install Dependencies
Ensure you have all necessary libraries installed by running:

```bash

pip install -r requirements.txt
```

3. Run the Program
Execute the main script to start the system:

```bash
python main.py
```
## 📌 How It Works
Preprocessing Module: Enhances image quality and extracts facial features.

Encoding Phase: The autoencoder securely embeds authentication data into ID images.

Decoding Phase: The auto decoder retrieves hidden messages for verification.

Verification: If the extracted message is intact, the ID is considered valid; otherwise, tampering is detected.

## 👨‍💻 Contributors
Sai Dhanush V.R

M. Mukunda

Surya J

## 📜 License
This project is licensed under the MIT License.

## 🏷️ Tags
#DeepLearning #Steganography #IDSecurity #ImageProcessing #NeuralNetworks
#Autoencoder #BinaryErrorCorrection #FaceRecognition #DocumentSecurity #Python
#MachineLearning #AI #ComputerVision #SecureAuthentication #DataEmbedding
=======
# IDShield - ID Card Security System

A web-based ID card security system that uses LSB Steganography to embed hidden binary codes into ID card images and OpenCV face detection to prevent photo substitution attacks.

## Features
- Face detection and cropping from ID cards using OpenCV Haar Cascade
- LSB Steganography to embed hidden binary codes into images
- Hamming Error Correcting Code for robust binary data recovery
- Admin module to encode and manage ID cards
- User module to verify ID card authenticity
- MySQL database to store encoded image data

## Technologies Used
- Python
- Flask
- MySQL
- OpenCV
- PIL/Pillow
- NumPy

## How It Works
1. Admin uploads an ID card image with a secret message
2. System converts the message to binary and hides it in image pixels using LSB method
3. OpenCV detects and crops the face from the ID card
4. Encoded image is stored as the authenticated ID
5. During verification, hidden binary code is extracted from the image
6. If code matches database → Real ✅
7. If no code found → Fake ❌

## Installation
1. Install dependencies
   pip install -r requirements.txt

2. Set up MySQL database
   - Install XAMPP and start MySQL
   - Import faceMDT.sql into phpMyAdmin

3. Run the app
   python main.py

4. Open browser and go to
   http://127.0.0.1:5000

## License
MIT
>>>>>>> e003d549235b326f675c6a068676184e40cb480d
