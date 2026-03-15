
# Lab 6: Automated MLOps Pipeline using Jenkins (CI/CD)

**Student Name:** Abel Philip Joseph  
**Roll Number:** 2022BCS0068  

## 🎯 Objective
This repository contains the implementation for **Lab 6**, which transitions our Continuous Integration and Continuous Deployment (CI/CD) workflow from GitHub Actions to a self-hosted **Jenkins** server. 

The primary goal of this lab is to automate the machine learning lifecycle—training, evaluation, containerization, and deployment—using a declarative `Jenkinsfile`.

## ⚙️ Pipeline Architecture
The Jenkins pipeline automatically triggers on code changes and executes the following stages:

1. **Checkout:** Clones the latest code from this GitHub repository.
2. **Setup Environment:** Creates a Python virtual environment and installs dependencies from `requirements.txt`.
3. **Train Model:** Executes the `scripts/train.py` script to train a Random Forest model and generates performance metrics (`app/artifacts/metrics.json`) along with the serialized model (`app/artifacts/model.pkl`).
4. **Read Accuracy:** Parses the generated JSON file using `jq` to extract the current model's `r2_score`.
5. **Compare Accuracy (Conditional Logic):** Compares the newly trained model's R2 score against a baseline `best-accuracy` score securely stored in Jenkins Credentials.
6. **Build Docker Image:** If the new model outperforms the baseline, a new Docker image containing the FastAPI inference service is built.
7. **Push Docker Image:** Authenticates with Docker Hub and pushes the newly built image, tagged with the Jenkins build number and `latest`.
8. **Artifact Archiving:** Regardless of the build outcome, the pipeline automatically archives the `app/artifacts/` folder so metrics and models can be downloaded directly from the Jenkins UI.

## 📂 Repository Structure
```text
.
├── app/
│   ├── artifacts/         # Directory where Jenkins saves model.pkl and metrics.json during the build
│   └── main.py            # FastAPI application for serving the model (Inference API)
├── data/
│   └── winequality-red.csv# Dataset used for training
├── scripts/
│   └── train.py           # Script to train the ML model and output artifacts
├── Dockerfile             # Instructions to containerize the FastAPI inference service
├── Jenkinsfile            # The declarative Jenkins pipeline script orchestrating the CI/CD workflow
├── requirements.txt       # Python dependencies required for training and the API
└── .gitignore             # Git ignore file to prevent tracking local venv and pycache

```

## 🛠️ Prerequisites & Tools Used

* **Self-hosted Jenkins** (Running via Docker from Lab 5)
* **Jenkins Plugins:** Docker Pipeline, Pipeline, Git
* **Docker & Docker Hub** (For building and hosting the containerized model)
* **Python 3 & Virtualenv**

## ✅ Deliverables Configured

* [x] Securely configured Jenkins credentials (`dockerhub-creds`, `git-creds`, `best-accuracy`).
* [x] Configured a Jenkins Pipeline Job linked to this SCM repository.
* [x] Verified end-to-end execution, including conditional deployment logic based on the R2 Score.
* [x] Successfully archived training artifacts in the Jenkins UI.
* [x] Automated pushing of the containerized model to Docker Hub.


