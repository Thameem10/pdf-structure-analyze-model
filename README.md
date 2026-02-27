Logical Layered Architecture :

    Layer 1 – Input Layer

        • Raw PDFs

    Layer 2 – Extraction Layer

        • Text extraction
        • Image extraction
        • Layout detection
        • Bounding box detection

    Layer 3 – Feature Engineering Layer

        • Font size
        • Position normalization
        • Text statistics
        • Structural features

    Layer 4 – ML Layer

        • Feature scaling
        • Model inference
        • Label prediction

    Layer 5 – Human-in-the-loop Layer

        • Auto-labeling script
        • Streamlit correction UI

Feature List Documentation :

    Feature Categories

        1. Text-Based Features

                | Feature Name       | Type    | Description                  |
                | ------------------ | ------- | ---------------------------- |
                | text_length        | Numeric | Number of characters         |
                | word_count         | Numeric | Number of words              |
                | uppercase_ratio    | Float   | Uppercase characters / total |
                | digit_ratio        | Float   | Digits / total characters    |
                | special_char_ratio | Float   | Special symbols proportion   |
                | is_all_caps        | Binary  | 1 if entire text uppercase   |


        2. Font Features

                | Feature Name | Type        | Description         |
                | ------------ | ----------- | ------------------- |
                | font_size    | Numeric     | Extracted font size |
                | is_bold      | Binary      | Bold flag           |
                | is_italic    | Binary      | Italic flag         |
                | font_family  | Categorical | Font type           |


        3. Spatial Features (Layout Features)

                | Feature Name        | Type    | Description                  |
                | ------------------- | ------- | ---------------------------- |
                | x0                  | Numeric | Left position                |
                | y0                  | Numeric | Top position                 |
                | x1                  | Numeric | Right position               |
                | y1                  | Numeric | Bottom position              |
                | box_width           | Numeric | Width of bounding box        |
                | box_height          | Numeric | Height of bounding box       |
                | relative_y_position | Float   | Normalized vertical position |
                | indentation         | Float   | Distance from left margin    |


        4. Structural Features

                | Feature Name        | Type    | Description             |
                | ------------------- | ------- | ----------------------- |
                | page_number         | Numeric | Page index              |
                | line_spacing        | Numeric | Distance between blocks |
                | block_position_rank | Numeric | Order in page           |
                | is_first_block      | Binary  | First element on page   |
                | is_last_block       | Binary  | Last element on page    |

       5. Derived Features

                | Feature Name         | Logic                     |
                | -------------------- | ------------------------- |
                | is_heading_candidate | font_size > threshold     |
                | is_footer_candidate  | relative_y_position > 0.9 |
                | is_centered          | near page center          |
                | density_score        | text_length / box_area    |

        Target Labels

                | Label      | Meaning                 |
                | ---------- | ----------------------- |
                | Heading    | Main section titles     |
                | Subheading | Section subtitles       |
                | Paragraph  | Body text               |
                | Footer     | Bottom repeated text    |
                | Table      | Tabular data            |
                | Image      | Non-text visual element |

PHASE-WISE ROADMAP

    Project: PDF Structure Analyzer

        Phase 0 – Project Planning & Research

        Objective

            Define scope, labels, and technical design before coding.

        Tasks

            • Define problem statement
            • Identify layout classes:
                • Heading
                • Subheading
                • Paragraph
                • Footer
                • Table
                • Image
            • Design folder structure
            • Create architecture diagram
            • Define feature list
            • Create labeling schema

        Phase 1 – PDF Extraction Pipeline

        Objective

            Extract structured layout blocks from raw PDFs.

        Modules

            • pdf_loader.py
            • layout_parser.py
            • text_extractor.py
            • image_extractor.py

        Tasks

            Load PDF

            Extract:

                Text
                Font size
                Font style
                Bounding boxes
                Page number

            Save extracted JSON to:

            data/interim/extracted_pages.json

        Success Criteria

            All blocks extracted
            Bounding boxes accurate
            Metadata consistent


        Phase 2 – Auto Labeling System
        Objective

        Create initial training dataset using rule-based logic.

        Script

        python3 auto_label.py

        Logic Example

            Large font + uppercase → Heading
            Medium font → Subheading
            Bottom position → Footer
            Large area without text → Image

        Output

            data/labeled/train.json

        Goal

            Generate 70–80% correct labels automatically.

        Phase 3 – Human-in-the-Loop Label Correction
        bjective

        Improve label quality manually.

        Run

            streamlit run streamlit.py

        Features

            Block visualization
            Dropdown label selection
            Save corrected dataset

        Outcome

            High-quality labeled dataset.

        Phase 4 – Feature Engineering
        Objective

        Convert JSON blocks into ML-ready features.

        Modules

            feature_extractor.py
            feature_utils.py

            Generate:

                Text features
                Font features
                Spatial features
                Derived features

        Save:

            data/processed/X_train.pkl
            data/processed/y_train.pkl
            scaler.pkl

        Phase 5 – Model Training & Evaluation
        Objective

        Train classification model.

        Script

            python3 training/train.py

        Models

            Random Forest
            XGBoost

        Metrics

            Accuracy
            Precision
            Recall
            F1-score
            Confusion Matrix

        Save:

        models/random_forest.pkl

        Phase 6 – Inference Pipeline
        Objective

        Convert new PDF → Structured JSON

        Run:

        python3 -m app.main data/raw/sample.pdf

        Flow:

            Extract blocks
            Generate features
            Scale
            Predict labels
            Save structured output


        Phase 7 – Optimization & Improvements

        Improvements

            Hyperparameter tuning
            Class imbalance handling
            Feature importance analysis
            Model comparison

Complexity :

    1. Layout Complexity (Real-World PDF Challenges)

        This is the hardest part.

        PDFs are NOT structured like HTML.

        You may face:

        Multi-column Layouts

                Text appears visually in order:

                Column 1
                Column 2

                But extraction may return:

                Row 1 col1
                Row 1 col2
                Row 2 col1
                Row 2 col2

                Logical order reconstruction becomes complex.

        Inconsistent Fonts

                Same heading:
                Page 1 → font size 18
                Page 2 → font size 16
                Rule-based logic fails.

        Scanned PDFs (Image-based)

                No text layer → need OCR
                Adds:

                    OCR noise
                    Character errors
                    Slow processing

        Tables
                Tables may be:
                    Extracted as text blocks
                    Broken into multiple lines
                    Misaligned
                    Hard to detect using simple rules.

        Repeated Headers & Footers
                Appears on every page.

        Need:

        Frequency detection
        Positional filtering

    2. Data Complexity

    Class Imbalance

    Example:

        Label       Count
        Paragraph	 8000
        Heading	     200
        Footer	     100

    Model becomes biased toward paragraphs.

    Solution:

        Class weights
        Oversampling

    3. ML Model Complexity

    Overfitting

        RandomForest may memorize layout patterns.

    Symptoms:

        High training accuracy
        Low validation accuracy

    Hyperparameter Tuning

        n_estimators
        max_depth
        min_samples_split

Project Structure :

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
