import fitz

def generate_resume():
    doc = fitz.open()
    page = doc.new_page(width=595.28, height=841.89)  # Standard A4 (595.28 x 841.89)

    # Color Palette (Crisp High-Contrast Executive Navy & Slate for ATS scanners)
    DARK = (0.05, 0.08, 0.14)         # #0d1424
    PRIMARY = (0.10, 0.16, 0.26)      # #1a2942
    ACCENT = (0.18, 0.32, 0.65)       # #2e52a6
    MUTED = (0.40, 0.46, 0.54)        # #66758a
    BODY = (0.16, 0.20, 0.26)         # #293342
    DIVIDER = (0.80, 0.84, 0.90)

    MARGIN_X = 40
    CONTENT_W = 595.28 - (MARGIN_X * 2)

    # 1. Header
    y = 50
    page.insert_text(fitz.Point(MARGIN_X, y), 'MOHD AREEB AHMAD', fontsize=22, fontname='hebo', color=DARK)
    y += 18
    page.insert_text(fitz.Point(MARGIN_X, y), 'Machine Learning Engineer   |   B.Tech CSE (AI & ML)   |   AI & Data Science Specialist', fontsize=10.0, fontname='helv', color=ACCENT)

    y += 15
    # Clickable Contact Bar
    contacts = [
        ('Phone: +91 9336376310', 'tel:+919336376310'),
        ('Email: areebahmad239@gmail.com', 'mailto:areebahmad239@gmail.com'),
        ('LinkedIn: areeb-ahmad-15078835b', 'https://www.linkedin.com/in/areeb-ahmad-15078835b/'),
        ('GitHub: github.com/areeb239', 'https://github.com/areeb239')
    ]

    contact_x = MARGIN_X
    for i, (text, url) in enumerate(contacts):
        page.insert_text(fitz.Point(contact_x, y), text, fontsize=8.6, fontname='helv', color=BODY)
        text_len = fitz.get_text_length(text, fontname='helv', fontsize=8.6)
        if url:
            link_rect = fitz.Rect(contact_x, y - 9, contact_x + text_len, y + 2)
            page.insert_link({'kind': fitz.LINK_URI, 'from': link_rect, 'uri': url})
        contact_x += text_len
        if i < len(contacts) - 1:
            sep = '   |   '
            page.insert_text(fitz.Point(contact_x, y), sep, fontsize=8.6, fontname='helv', color=MUTED)
            contact_x += fitz.get_text_length(sep, fontname='helv', fontsize=8.6)

    y += 10
    page.draw_line(fitz.Point(MARGIN_X, y), fitz.Point(MARGIN_X + CONTENT_W, y), color=ACCENT, width=1.5)
    y += 20

    def draw_section_heading(title, y_pos):
        page.insert_text(fitz.Point(MARGIN_X, y_pos), title.upper(), fontsize=10.8, fontname='hebo', color=ACCENT)
        w = fitz.get_text_length(title.upper(), fontname='hebo', fontsize=10.8)
        page.draw_line(fitz.Point(MARGIN_X + w + 12, y_pos - 4), fitz.Point(MARGIN_X + CONTENT_W, y_pos - 4), color=DIVIDER, width=0.8)
        return y_pos + 15

    # 2. Professional Summary
    y = draw_section_heading('Professional Summary', y)
    summary_text = (
        "Results-oriented Machine Learning Engineer and B.Tech CSE (AI & ML) student with demonstrated expertise in "
        "supervised learning, predictive data pipelines, and production MLOps workflows. Proficient in Python, Scikit-Learn, "
        "FastAPI, Docker, and MLflow, with technical leadership in developing the 'Bhurakshak' early warning platform for "
        "Smart India Hackathon 2026 (Ministry of Development of North Eastern Region) and an NPTEL Elite certification from IIT Madras."
    )
    rect = fitz.Rect(MARGIN_X, y - 8.5, MARGIN_X + CONTENT_W, y + 45)
    page.insert_textbox(rect, summary_text, fontsize=8.4, fontname='helv', color=BODY, lineheight=1.22)
    est_lines = 1 + int(fitz.get_text_length(summary_text, fontname='helv', fontsize=8.4) // CONTENT_W)
    y += (est_lines * 11.0) + 10

    # 3. Technical Skills
    y = draw_section_heading('Technical Skills', y)
    skill_groups = [
        ('Machine Learning & AI:', 'Supervised & Unsupervised Learning, Random Forest, XGBoost, SVM, Naive Bayes, Clustering (K-Means, DBSCAN), Feature Engineering, Hyperparameter Tuning, Cross-Validation, Regularization (L1/L2), Model Evaluation (ROC-AUC, Precision, Recall, F1)'),
        ('Programming Languages:', 'Python, Java, Kotlin, SQL, JavaScript (ES6+), C, C++, HTML5 / CSS3'),
        ('Libraries & Frameworks:', 'Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn, FastAPI, Jetpack Compose, Firebase'),
        ('MLOps & Cloud Tools:', 'Docker, MLflow, Git, GitHub Actions (CI/CD), PyTest, Jupyter Notebook, VS Code, Kaggle')
    ]

    for s_title, s_val in skill_groups:
        page.insert_text(fitz.Point(MARGIN_X, y), s_title, fontsize=8.5, fontname='hebo', color=PRIMARY)
        rect = fitz.Rect(MARGIN_X + 138, y - 8.5, MARGIN_X + CONTENT_W, y + 30)
        page.insert_textbox(rect, s_val, fontsize=8.3, fontname='helv', color=BODY, lineheight=1.20)
        est_lines = 1 + int(fitz.get_text_length(s_val, fontname='helv', fontsize=8.3) // (CONTENT_W - 138))
        y += (est_lines * 10.5) + 4

    y += 7
    # 4. Technical Projects
    y = draw_section_heading('Technical Projects', y)

    projects = [
        {
            'title': 'Bhurakshak - AI-Based Landslide Early Warning System',
            'tech': 'Python, FastAPI, Kotlin, Jetpack Compose, Random Forest, XGBoost',
            'points': [
                "Spearheaded development of an AI-powered landslide risk monitoring platform for India's North Eastern Region as part of Smart India Hackathon 2026 (Problem Statement 26001, for Ministry of Development of North Eastern Region - MDoNER).",
                "Achieved 91.4% recall on imbalanced geospatial hazard data by training and hyperparameter-tuning Random Forest and XGBoost classifiers across 700+ NASA satellite catalog points, reducing missed hazard warnings by 35%.",
                "Architected low-latency REST inference APIs with FastAPI (<60ms response latency) supporting offline caching and Firebase Cloud Messaging alerts.",
                "Developed native Android reporting app using Jetpack Compose (Kotlin) with interactive GIS maps, real-time AI hazard inference, incident logging, and radar weather screens."
            ]
        },
        {
            'title': 'CreditWise - ML-Based Loan Eligibility Prediction Pipeline',
            'tech': 'Python, Scikit-Learn, Pandas, NumPy, Data Pipeline',
            'points': [
                "Formulated an end-to-end production ML pipeline for loan qualification prediction with strict train/test split discipline, missing-value imputation, and categorical encoding.",
                "Reduced feature dimensionality by 40% and accelerated training speed by 2.5x using variance-thresholding and correlation-based feature selection.",
                "Benchmarked Logistic Regression, Decision Trees, and Random Forest models across 5,000+ applicant records, attaining an 88.6% ROC-AUC score."
            ]
        },
        {
            'title': 'Email / SMS Spam Classifier - Production MLOps Pipeline',
            'tech': 'Python, Scikit-Learn, MLflow, FastAPI, Docker, CI/CD, PyTest',
            'points': [
                "Constructed an automated spam detection pipeline on the UCI SMS dataset applying TF-IDF vectorization and custom text preprocessing.",
                "Evaluated Naive Bayes, Logistic Regression, and Linear SVM models, tracking hyperparameter experiments and model versioning via MLflow.",
                "Containerized the inference microservice with Docker, implemented 95% unit test coverage via PyTest, and automated CI/CD using GitHub Actions."
            ]
        }
    ]

    for p in projects:
        page.insert_text(fitz.Point(MARGIN_X, y), p['title'], fontsize=9.6, fontname='hebo', color=DARK)
        w_t = fitz.get_text_length(p['title'], fontname='hebo', fontsize=9.6)
        page.insert_text(fitz.Point(MARGIN_X + w_t + 16, y), '|   ' + p['tech'], fontsize=8.3, fontname='helv', color=ACCENT)
        y += 12

        for pt in p['points']:
            bullet_x = MARGIN_X + 4
            text_x = MARGIN_X + 14
            text_w = CONTENT_W - 14

            page.insert_text(fitz.Point(bullet_x, y), '•', fontsize=8.2, fontname='helv', color=ACCENT)
            rect = fitz.Rect(text_x, y - 8.5, text_x + text_w, y + 40)
            page.insert_textbox(rect, pt, fontsize=8.2, fontname='helv', color=BODY, lineheight=1.20)
            est_lines = 1 + int(fitz.get_text_length(pt, fontname='helv', fontsize=8.2) // text_w)
            y += (est_lines * 10.5) + 3

        y += 5

    y += 3
    # 5. Education
    y = draw_section_heading('Education', y)
    page.insert_text(fitz.Point(MARGIN_X, y), 'Babu Banarasi Das Northern India Institute of Technology (BBDNIIT)', fontsize=10.0, fontname='hebo', color=DARK)
    loc_text = 'Lucknow, India'
    w_loc = fitz.get_text_length(loc_text, fontname='helv', fontsize=9.0)
    page.insert_text(fitz.Point(MARGIN_X + CONTENT_W - w_loc, y), loc_text, fontsize=9.0, fontname='helv', color=MUTED)
    y += 13
    page.insert_text(fitz.Point(MARGIN_X, y), 'Bachelor of Technology in Computer Science & Engineering (AI & ML)', fontsize=9.0, fontname='helv', color=PRIMARY)
    date_text = '2024 – 2028'
    w_date = fitz.get_text_length(date_text, fontname='helv', fontsize=9.0)
    page.insert_text(fitz.Point(MARGIN_X + CONTENT_W - w_date, y), date_text, fontsize=9.0, fontname='helv', color=MUTED)
    y += 12
    page.insert_text(fitz.Point(MARGIN_X, y), 'Relevant Coursework: Data Structures & Algorithms, Machine Learning, OOP (Java, Kotlin, Dart), DBMS, SQL, Operating Systems', fontsize=8.2, fontname='helv', color=BODY)
    y += 20

    # 6. Certifications & Honors
    y = draw_section_heading('Certifications & Honors', y)
    page.insert_text(fitz.Point(MARGIN_X, y), 'NPTEL Online Certification — Introduction to Machine Learning (Elite — 60%)', fontsize=9.6, fontname='hebo', color=DARK)
    cert_date = 'Jan – Apr 2026'
    w_cdate = fitz.get_text_length(cert_date, fontname='helv', fontsize=8.8)
    page.insert_text(fitz.Point(MARGIN_X + CONTENT_W - w_cdate, y), cert_date, fontsize=8.8, fontname='helv', color=MUTED)
    y += 12
    cert_detail = 'IIT Madras & SWAYAM (MoE, Govt. of India)  |  Online Assignments: 24/25  |  Proctored Exam: 35.51/75  |  Roll No: NPTEL26CS74S259800581'
    page.insert_text(fitz.Point(MARGIN_X, y), cert_detail, fontsize=8.3, fontname='helv', color=PRIMARY)
    y += 11
    page.insert_text(fitz.Point(MARGIN_X, y), 'Smart India Hackathon 2026 (SIH): Selected participant developing AI Landslide Early Warning platform for Ministry of DoNER', fontsize=8.2, fontname='helv', color=BODY)

    doc.save('c:/Users/HP/.gemini/antigravity-ide/scratch/portfolio/assets/resume.pdf')
    print('Generated High-Scoring ATS Resume! Final Y:', y, 'Total pages:', len(doc))

def sync_standalone():
    with open('c:/Users/HP/.gemini/antigravity-ide/scratch/portfolio/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    with open('c:/Users/HP/.gemini/antigravity-ide/scratch/portfolio/style.css', 'r', encoding='utf-8') as f:
        css = f.read()
    with open('c:/Users/HP/.gemini/antigravity-ide/scratch/portfolio/script.js', 'r', encoding='utf-8') as f:
        js = f.read()

    html = html.replace('<link rel="stylesheet" href="style.css" />', f'<style>\n{css}\n</style>')
    html = html.replace('<script src="script.js"></script>', f'<script>\n{js}\n</script>')

    with open('c:/Users/HP/.gemini/antigravity-ide/scratch/portfolio/portfolio_areeb.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Synced portfolio_areeb.html!')

if __name__ == '__main__':
    generate_resume()
    sync_standalone()
