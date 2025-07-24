# 🧪 Food Adulteration Detection System
# webapp link:https://foodadulterationdetection.streamlit.app/

### Team ID: 88(2nd Year)
### Team Members:
- **Mahesweta Panda** (24CSE145)
- **Nikhilesh Padhan** (24CSEDSD40)
- **Pratyush Dalei** (24CSEE033)
- **Aditya Kumar Mahanta** (24CSEE007)
---

## 🎥 Project Demo Video 

You can watch a 3-5 minute demonstration of our project in action here. This video covers the project's features, functionality, and how to use the application.

**[https://drive.google.com/file/d/1hndTfWUYYE6_uYR26jT5oWF_UW_VJTRq/view?usp=drive_link](https://drive.google.com/file/d/1hndTfWUYYE6_uYR26jT5oWF_UW_VJTRq/view?usp=drive_link)**

---

## 📄 Project Presentation 

Our detailed project presentation is available here. You can view the file directly.
Presentation link-
https://1drv.ms/p/c/bfaa017a6c4088bc/ERtHqkjfvwFJoiHwugfCPBQBqYE1h1pBmIMXRKM6lS0P-w

---

## ✨ Project Overview

This project is a web-based dashboard built with Streamlit that uses a Machine Learning model to detect potential adulteration in raw food samples based on their sensory attributes. It provides an instant analysis of food safety and potential health risks.

![Screenshot of the App](Screenshot%202025-07-24%20075646.png)

### Key Features
- **Interactive UI**: A clean and user-friendly interface to input food sample data.
- **Machine Learning Model**: Utilizes a trained Random Forest classifier to predict adulteration status and health risk level.
- **Visual Health Gauge**: A donut chart visually represents the predicted health risk level (Safe, Low Risk, Moderate, Toxic).
- **Prediction History**: A dashboard table logs all samples analyzed during the current session.

## 💻 Tech Stack

The following technologies and tools were used in the development of this project:

* **Machine Learning Framework:** Scikit-learn (for model training, including Random Forest Classifier and `train_test_split`).
* **Data Exploration & Model Prototyping:** Jupyter Notebook.
* **User Interface:** Streamlit.
* **Development Environment:** VS Code.
* **Data Gathering:** Perplexity (for dataset acquisition/generation).

## ⚙️ Setup and Installation
To run this project locally, you'll need to have Python installed. Follow these steps to set it up:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Nikhileshpadhan/FoodAdulterationDetection.git](https://github.com/Nikhileshpadhan/FoodAdulterationDetection.git)
    cd FoodAdulterationDetection
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required libraries:**
    ```bash
    pip install streamlit pandas scikit-learn matplotlib
    ```

## ▶️ How to Run
Once the setup is complete, you can run the Streamlit application with the following command:
```bash
streamlit run app.py
