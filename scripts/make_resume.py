import fitz

def generate_resume():
    doc = fitz.open()
    page = doc.new_page(width=595.28, height=841.89)  # Standard A4 (595.28 x 841.89)

    # Color Palette (Executive Navy & Professional Slate)
    DARK = (0.05, 0.08, 0.14)         # #0d1424
    PRIMARY = (0.10, 0.16, 0.26)      # #1a2942
    ACCENT = (0.18, 0.32, 0.65)       # #2e52a6
    MUTED = (0.40, 0.46, 0.54)        # #66758a
    BODY = (0.16, 0.20, 0.26)         # #293342
    DIVIDER = (0.80, 0.84, 0.90)

    MARGIN_X = 40
    CONTENT_W = 595.28 - (MARGIN_X * 2)

    # 1. Header
    y = 48
    page.insert_text(fitz.Point(MARGIN_X, y), 'MOHD AREEB AHMAD', fontsize=22, fontname='hebo', color=DARK)
    y += 18
    page.insert_text(fitz.Point(MARGIN_X, y), 'B.Tech in Computer Science & Engineering (AI & ML)   |   Machine Learning & AI Engineer', fontsize=10.2, fontname='helv', color=ACCENT)

    y += 16
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

    # 2. Education
    y = draw_section_heading('Education', y)
    page.insert_text(fitz.Point(MARGIN_X, y), 'Babu Banarasi Das Northern India Institute of Technology (BBDNIIT)', fontsize=10.2, fontname='hebo', color=DARK)
    loc_text = 'Lucknow, India'
    w_loc = fitz.get_text_length(loc_text, fontname='helv', fontsize=9.2)
    page.insert_text(fitz.Point(MARGIN_X + CONTENT_W - w_loc, y), loc_text, fontsize=9.2, fontname='helv', color=MUTED)
    y += 14
    page.insert_text(fitz.Point(MARGIN_X, y), 'Bachelor of Technology in Computer Science & Engineering (AI & ML)', fontsize=9.2, fontname='helv', color=PRIMARY)
    date_text = '2024 – 2028'
    w_date = fitz.get_text_length(date_text, fontname='helv', fontsize=9.2)
    page.insert_text(fitz.Point(MARGIN_X + CONTENT_W - w_date, y), date_text, fontsize=9.2, fontname='helv', color=MUTED)
    y += 13
    page.insert_text(fitz.Point(MARGIN_X, y), 'Relevant Coursework: Data Structures & Algorithms, Machine Learning, OOP (Java, Kotlin, Dart), DBMS, SQL, Operating Systems', fontsize=8.2, fontname='helv', color=BODY)
    y += 20

    # 3. Certifications & Honors
    y = draw_section_heading('Certifications & Honors', y)
    page.insert_text(fitz.Point(MARGIN_X, y), 'NPTEL Online Certification — Introduction to Machine Learning (Elite)', fontsize=10.0, fontname='hebo', color=DARK)
    cert_date = 'Jan – Apr 2026'
    w_cdate = fitz.get_text_length(cert_date, fontname='helv', fontsize=9.0)
    page.insert_text(fitz.Point(MARGIN_X + CONTENT_W - w_cdate, y), cert_date, fontsize=9.0, fontname='helv', color=MUTED)
    y += 13
    cert_detail = 'IIT Madras & SWAYAM (MoE, Govt. of India)  |  Consolidated Score: 60% (Elite)  |  Assignments: 24/25  |  Proctored Exam: 35.51/75'
    page.insert_text(fitz.Point(MARGIN_X, y), cert_detail, fontsize=8.6, fontname='helv', color=PRIMARY)
    y += 12
    page.insert_text(fitz.Point(MARGIN_X, y), 'Roll No: NPTEL26CS74S259800581  |  12-Week Intensive Foundation in Mathematical ML, Algorithms & Optimization', fontsize=8.0, fontname='helv', color=MUTED)
    y += 20

    # 4. Featured Projects
    y = draw_section_heading('Featured Technical Projects', y)

    projects = [
        {
            'title': 'Bhurakshak — AI-Based Landslide Early Warning System',
            'tech': 'Python, FastAPI, Kotlin, Jetpack Compose, Random Forest, XGBoost',
            'points': [
                "Building an early-warning and landslide risk monitoring system for India's North Eastern Region as part of Smart India Hackathon 2026 (Problem Statement 26001), for the Ministry of Development of North Eastern Region (MDoNER).",
                "Trained a Random Forest / XGBoost classification model optimized for recall on imbalanced landslide event data, using 700+ landslide data points sourced from NASA's Global Landslide Catalog and High Mountain Asia Landslide Catalog.",
                "Built the backend with FastAPI to serve the ML model and REST APIs, supporting offline sync and Firebase Cloud Messaging alerts.",
                "Developed the field-reporting Android app in Jetpack Compose (Kotlin), with a dashboard, AI hazard inference, GIS map, disaster incident reporting, and weather radar screens."
            ]
        },
        {
            'title': 'CreditWise — ML-Based Loan Eligibility Prediction System',
            'tech': 'Python, Scikit-Learn, Pandas, NumPy, Data Pipeline',
            'points': [
                "Built an end-to-end ML pipeline for loan eligibility prediction: train/test split discipline, structural EDA, missing-value imputation, and encoding.",
                "Applied correlation-based and variance-threshold feature selection to reduce dimensionality and improve model interpretability.",
                "Compared multiple classification algorithms (Logistic Regression, Decision Trees, Random Forest) to identify the best-performing approach for predicting loan eligibility from applicant data."
            ]
        },
        {
            'title': 'Email / SMS Spam Classifier — End-to-End MLOps Pipeline',
            'tech': 'Python, Scikit-Learn, MLflow, FastAPI, Docker, CI/CD, PyTest',
            'points': [
                "Built a spam classification pipeline on the UCI SMS Spam Collection dataset using TF-IDF feature extraction.",
                "Trained and compared Naive Bayes, Logistic Regression, and Linear SVM models, tracking experiments with MLflow.",
                "Served the trained model through a FastAPI layer, containerized the app with Docker, and validated it with a pytest test suite.",
                "Set up continuous integration with GitHub Actions for automated linting, test runs, and container build verification."
            ]
        }
    ]

    for p in projects:
        page.insert_text(fitz.Point(MARGIN_X, y), p['title'], fontsize=9.6, fontname='hebo', color=DARK)
        w_t = fitz.get_text_length(p['title'], fontname='hebo', fontsize=9.6)
        page.insert_text(fitz.Point(MARGIN_X + w_t + 12, y), '|   ' + p['tech'], fontsize=8.4, fontname='helv', color=ACCENT)
        y += 12

        for pt in p['points']:
            bullet_x = MARGIN_X + 4
            text_x = MARGIN_X + 14
            text_w = CONTENT_W - 14

            page.insert_text(fitz.Point(bullet_x, y), '•', fontsize=8.2, fontname='helv', color=ACCENT)
            rect = fitz.Rect(text_x, y - 8.5, text_x + text_w, y + 40)
            rc = page.insert_textbox(rect, pt, fontsize=8.2, fontname='helv', color=BODY, lineheight=1.20)
            
            # Count wrapped lines accurately
            est_lines = 1 + int(fitz.get_text_length(pt, fontname='helv', fontsize=8.2) // text_w)
            line_step = 10.5
            y += (est_lines * line_step) + 3

        y += 4

    y += 2
    # 5. Technical Skills
    y = draw_section_heading('Technical Skills & Expertise', y)

    skill_groups = [
        ('Data Science & ML:', 'Classification & Regression, Feature Engineering, EDA, Ensemble Methods (Random Forest, XGBoost, Bagging/Boosting), SVM, Naive Bayes, Clustering (K-Means, DBSCAN), PCA, Regularization (Ridge/Lasso), Model Evaluation'),
        ('Mathematics & Stats:', 'Probability Distributions, Hypothesis Testing, Confidence Intervals, Linear Algebra, Optimization'),
        ('Programming Languages:', 'Python, Java, Kotlin, JavaScript (ES6+), C, C++, SQL, HTML5/CSS3'),
        ('Frameworks & Libraries:', 'Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn, FastAPI, Jetpack Compose, Firebase'),
        ('Developer Tools & MLOps:', 'Git, GitHub, Docker, MLflow, GitHub Actions (CI/CD), Jupyter Notebook, VS Code, Kaggle')
    ]

    for s_title, s_val in skill_groups:
        page.insert_text(fitz.Point(MARGIN_X, y), s_title, fontsize=8.5, fontname='hebo', color=PRIMARY)
        rect = fitz.Rect(MARGIN_X + 130, y - 8.5, MARGIN_X + CONTENT_W, y + 30)
        page.insert_textbox(rect, s_val, fontsize=8.2, fontname='helv', color=BODY, lineheight=1.20)
        
        est_lines = 1 + int(fitz.get_text_length(s_val, fontname='helv', fontsize=8.2) // (CONTENT_W - 130))
        y += (est_lines * 10.5) + 3

    y += 4
    # 6. Key Achievements
    y = draw_section_heading('Achievements & Hackathons', y)
    achievements = [
        ("Smart India Hackathon 2026 (SIH)", "Selected for developing 'Bhurakshak' AI Early Warning Landslide System for Ministry of Development of North Eastern Region (MDoNER)."),
        ("NPTEL Elite Honor (60%)", "Awarded Elite status by IIT Madras & SWAYAM for excellence in Introduction to Machine Learning (Assignments: 24/25).")
    ]
    for a_title, a_desc in achievements:
        page.insert_text(fitz.Point(MARGIN_X + 4, y), '•', fontsize=8.2, fontname='helv', color=ACCENT)
        prefix = f"{a_title}: "
        page.insert_text(fitz.Point(MARGIN_X + 14, y), prefix, fontsize=8.2, fontname='hebo', color=PRIMARY)
        w_p = fitz.get_text_length(prefix, fontname='hebo', fontsize=8.2)
        
        rect = fitz.Rect(MARGIN_X + 14 + w_p, y - 8.5, MARGIN_X + CONTENT_W, y + 25)
        page.insert_textbox(rect, a_desc, fontsize=8.2, fontname='helv', color=BODY, lineheight=1.20)
        est_lines = 1 + int(fitz.get_text_length(a_desc, fontname='helv', fontsize=8.2) // (CONTENT_W - 14 - w_p))
        y += (est_lines * 10.5) + 3

    doc.save('c:/Users/HP/.gemini/antigravity-ide/scratch/portfolio/assets/resume.pdf')
    print('Generated balanced bold resume! Final Y:', y, 'Total pages:', len(doc))

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
