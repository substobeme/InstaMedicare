# InstaMediHelp

https://github.com/user-attachments/assets/c21263d2-ff6e-44d2-823d-7e3d811097ea

**InstaMediHelp** is an intelligent healthcare support system designed to provide drug recommendations based on patient-reported symptoms. The system leverages advanced machine learning techniques, including **BERT embeddings**, to interpret textual symptom descriptions and generate accurate suggestions. The platform combines a **Streamlit frontend** for intuitive user interaction with a **FastAPI backend** that processes requests, logs recommendations, and sends prescription summaries via email.

## Features

- **Customer Mode:**  
  Users can enter personal information and describe their symptoms. The system analyzes the input using BERT-based embeddings and recommends the most suitable drugs.

- **Admin Mode:**  
  Administrators have access to a full log of all prescriptions, enabling monitoring and analysis of drug recommendations over time. Each entry includes timestamps and patient details.

- **Machine Learning Model:**  
  The recommendation engine employs pre-trained **BERT embeddings** to capture the semantic meaning of patient symptoms. An XGBoost classifier then predicts the top `k` drug options, ensuring reliable and context-aware suggestions.

- **Automatic Email Notifications:**  
  Once a prescription is generated, the system’s agent automatically sends an email containing patient details (name, age, receipt ID, symptoms) and the recommended drugs. This ensures timely communication while keeping the workflow automated and agentic.

-**Note :** Didn't upload Bert trained encoder as file to big(even zipped) 
