# 🔒 Trustify — AI-Powered Product Authenticity Verification

## 📖 Overview
**Trustify** is an AI + Blockchain project designed to verify the authenticity of products before automated blockchain transactions occur.  
By combining **Convolutional Neural Networks (CNNs)** for image-based verification and **Ethereum Smart Contracts** for secure automation, Trustify ensures only genuine products are transacted—improving **trust**, **transparency**, and **security** in e-commerce.

---

## 💡 Problem Statement
Counterfeit goods cause billions in losses annually and undermine consumer trust in online marketplaces.  
Traditional verification methods are **manual**, **inconsistent**, and **not scalable**.  
Trustify solves this by using **AI** to verify a product’s authenticity from an image and triggering a **smart contract** that only executes if the product is genuine.

---

## 🧠 My Role
- Collected and preprocessed image datasets of **authentic vs counterfeit AirPods**.  
- Trained a **VGG16-based CNN model** in TensorFlow for binary classification.  
- Developed the **AI verification script** (`predict_image.py`) to analyze individual uploads.  
- Built the **front-end prototype** using **Streamlit** for image uploads and model integration.  
- Collaborated with the blockchain team to align smart contract integration and data flow.  
- Assisted in presentation preparation and technical Q&A documentation.

---

## ⚙️ Tech Stack
| Component | Tools Used |
|------------|-------------|
| **AI / ML** | Python, TensorFlow, Keras, OpenCV, NumPy |
| **Blockchain** | Solidity, Ethereum, Ganache, Remix |
| **Frontend / Integration** | Streamlit |
| **Dataset** | Custom dataset of real vs fake AirPods |
| **Version Control** | Git, GitHub |

---

## 🧩 System Architecture
1. **Data Collection & Preprocessing** — Images of real/fake AirPods collected and labeled.  
2. **Model Training** — Fine-tuned a pre-trained **VGG16 CNN** for binary classification.  
3. **Blockchain Smart Contract** — Solidity contract records and verifies authenticity flags.  
4. **Integration Layer** — Flask app and `web3.py` bridge model outputs with blockchain.  
5. **Frontend** — Simple upload interface for users to check authenticity and trigger contracts.

---

## 📊 Model Performance
- **Base Model:** VGG16 (transfer learning)  
- **Test Accuracy:** ~90%  
- **Loss Function:** Binary Crossentropy  
- **Optimizer:** Adam  
- **Evaluation Metrics:** Accuracy, Precision, Recall, F1-score  
- **Single Image Prediction:** Displays image and outputs "Real" or "Fake" with probability score.
