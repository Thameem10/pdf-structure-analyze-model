pdf-structure-analyzer/
│
├── app/ # Inference / Production code
│ ├── main.py
│ ├── pipeline.py
│ │
│ ├── extractor/ # Your current extraction modules
│ │ ├── pdf_loader.py
│ │ ├── text_extractor.py
│ │ ├── image_extractor.py
│ │ └── layout_parser.py
│ │
│ ├── features/
│ │ ├── feature_extractor.py
│ │ └── feature_utils.py
│ │
│ ├── models/
│ │ ├── classifier.py
│ │ └── model_loader.py
│ │
│ └── utils/
│ ├── config.py
│ └── helpers.py
│
├── data/
│ ├── raw/ # Original PDFs
│ │ └── sample.pdf
│ │
│ ├── interim/ # Extracted JSON before labeling
│ │ └── extracted_pages.json
│ │
│ ├── labeled/ # Manually labeled data
│ │ ├── train.json
│ │ ├── val.json
│ │ └── test.json
│ │
│ └── processed/ # Feature matrices
│ ├── X_train.pkl
│ ├── y_train.pkl
│ └── scaler.pkl
│
├── notebooks/ # Experimentation
│ ├── 01_exploration.ipynb
│ ├── 02_feature_engineering.ipynb
│ └── 03_model_training.ipynb
│
├── training/ # ML training scripts
│ ├── train.py
│ ├── evaluate.py
│ └── hyperparameter_tuning.py
│
├── models/ # Saved trained models
│ ├── random_forest.pkl
│ ├── xgboost.pkl
│ └── layoutlm/
│
├── configs/
│ ├── model_config.yaml
│ └── feature_config.yaml
│
├── logs/
│ └── training.log
│
├── requirements.txt
└── README.md

Run a Project :

run a main.py file to process the pdf file and converted into json . Now , move the features.json to the interim

run in a root directory

python3 -m app.main data/raw/176_Ormond_Inspection_Report.pdf

run in a data directory . It help to label the data automatically using the condition .

python3 auto_label.py

cmd to run the streamlit . It help maually correct the dataset which is wrong like in ui dashboard.

streamlit run streamlit.py
