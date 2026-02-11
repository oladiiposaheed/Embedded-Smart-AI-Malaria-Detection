***Embedded Smart AI System for Malaria Detection

📖 Overview

This repository contains the implementation of an AI powered system for malaria detection using blood smear images. The project leverages Convolutional Neural Networks (CNNs) built with PyTorch, optimized for deployment on embedded devices, and integrated with a lightweight web interface for usability in resource limited healthcare settings.

2. Virtual Environment
3. 
malaria\Scripts\activate      # Windows

5. Install Dependencies
   
pip install -r requirements.txt

📂 Dataset

This project uses the Cell Images for Detecting Malaria dataset from Kaggle

⚠️ Note: The dataset is not included in this repository due to size (~630MB).

Please download it directly from Kaggle and place it in the following folder structure:
data/raw/

│── Parasitized/

│── Uninfected/

│── Corrupted/

🚀 Usage

Running the Web Application

python manage.py runserver

📊 Results

•	CNN model achieved strong accuracy in distinguishing Parasitized vs. Uninfected cells.

•	Confusion matrix and performance metrics are generated during evaluation.

•	Web interface allows offline usage for healthcare workers in rural areas.

🛡️ Ethical & Regulatory Considerations

•	Ethics: Patient privacy, informed consent, and responsible AI usage.

•	Safety: Ensuring reliability of offline detection in rural settings.

•	Regulations: Alignment with Nigeria’s National Health Act (2014), NDPR (2019), and National Malaria Strategic Plan (2021–2025).

**
