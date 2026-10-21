# Script to generate the comprehensive, fully updated Project Report for EcoWatt / GreenFuture
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def create_report():
    doc = docx.Document()

    # Standard Margins: 1 inch on all sides
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False

    # Styling helper
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(30, 30, 30)

    # ==========================================
    # PAGE 1: TITLE PAGE
    # ==========================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("A PROJECT REPORT ON\n\n")
    run.font.size = Pt(14)
    run.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t = p_title.add_run("ECOWATT: ENERGY CONSUMPTION PREDICTION AND CARBON EMISSION ESTIMATION USING MACHINE LEARNING")
    run_t.font.size = Pt(16)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(16, 75, 40) # Forest Green

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(18)
    p_sub.paragraph_format.line_spacing = 1.3
    r = p_sub.add_run("Submitted in partial fulfilment of the requirements for the course\n")
    r.font.italic = True
    r = p_sub.add_run("24ESQ2119(B)-A/B/C ARTIFICIAL INTELLIGENCE and MACHINE LEARNING/DEEP LEARNING/ DATA SCIENCE/ PROJECT\n")
    r.font.bold = True
    r = p_sub.add_run("(Introductory Level Artificial Intelligence for Engineers – Project)\n")
    r.font.italic = True
    r = p_sub.add_run("of the degree of\n")
    r.font.italic = True
    r = p_sub.add_run("BACHELOR OF TECHNOLOGY\n")
    r.font.bold = True
    r = p_sub.add_run("in\n")
    r.font.italic = True
    r = p_sub.add_run("MECHANICAL ENGINEERING\n\n")
    r.font.bold = True

    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.line_spacing = 1.2
    r = p_auth.add_run("Submitted by\n\n")
    r.font.italic = True
    r = p_auth.add_run("Aaliya Fathima Arif ([Register No.])\n")
    r.font.bold = True
    r = p_auth.add_run("Afrah Zulfi ([Register No.])\n")
    r.font.bold = True
    r = p_auth.add_run("Muhammed Aasif ([Register No.])\n")
    r.font.bold = True
    r = p_auth.add_run("Sanju Philip Saji ([Register No.])\n")
    r.font.bold = True
    r = p_auth.add_run("S. Vighnesh (Team Leader) ([Register No.])\n\n")
    r.font.bold = True

    p_guid = doc.add_paragraph()
    p_guid.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_guid.add_run("Under the guidance of\n")
    r.font.italic = True
    r = p_guid.add_run("Er. Philip Jacob Perakathu\n")
    r.font.bold = True
    r = p_guid.add_run("Assistant Professor (Senior)\n\n")

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(20)
    r = p_dept.add_run("DEPARTMENT OF MECHANICAL ENGINEERING\n")
    r.font.bold = True
    r = p_dept.add_run("SAINTGITS COLLEGE OF ENGINEERING (AUTONOMOUS)\n")
    r.font.bold = True
    r = p_dept.add_run("Kottukulam Hills, Pathamuttom P.O., Kottayam – 686 532, Kerala\n")
    r = p_dept.add_run("OCTOBER 2026")
    r.font.bold = True

    doc.add_page_break()

    # ==========================================
    # PAGE 2: CERTIFICATE
    # ==========================================
    p_c_head = doc.add_paragraph()
    p_c_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_c_head.add_run("SAINTGITS COLLEGE OF ENGINEERING (AUTONOMOUS)\n")
    r.font.bold = True
    r = p_c_head.add_run("DEPARTMENT OF MECHANICAL ENGINEERING\n\n")
    r.font.bold = True
    r = p_c_head.add_run("CERTIFICATE\n")
    r.font.bold = True
    r.font.size = Pt(14)

    p_cert = doc.add_paragraph()
    p_cert.paragraph_format.line_spacing = 1.5
    p_cert.paragraph_format.space_before = Pt(12)
    p_cert.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert.add_run(
        "This is to certify that the project report entitled “EcoWatt: Energy Consumption Prediction and Carbon Emission Estimation Using Machine Learning” "
        "submitted by Aaliya Fathima Arif ([Reg. No.]), Afrah Zulfi ([Reg. No.]), Muhammed Aasif ([Reg. No.]), Sanju Philip Saji ([Reg. No.]) and "
        "S. Vighnesh ([Reg. No.]) in partial fulfilment of the requirements for the course 24ESQ2119(B)-A/B/C Artificial Intelligence and Machine Learning/Deep Learning/ "
        "Data Science Project of the degree of Bachelor of Technology in Mechanical Engineering, Saintgits College of Engineering (Autonomous), is a bonafide record "
        "of the project work carried out by them under our guidance and supervision during the academic year 2025–2026."
    )

    doc.add_paragraph("\n\n")
    tbl_cert = doc.add_table(rows=2, cols=3)
    tbl_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cells = tbl_cert.rows[0].cells
    c_cells[0].paragraphs[0].add_run("Project Supervisor\n").bold = True
    c_cells[0].paragraphs[0].add_run("Er. Philip Jacob Perakathu,\nAssistant Professor (Senior)")

    c_cells[1].paragraphs[0].add_run("Project Coordinator\n").bold = True
    c_cells[1].paragraphs[0].add_run("[Name, Designation]")

    c_cells[2].paragraphs[0].add_run("Head of the Department\n").bold = True
    c_cells[2].paragraphs[0].add_run("Dr. Chacko Peno")

    c_cells2 = tbl_cert.rows[1].cells
    c_cells2[0].paragraphs[0].add_run("\n\nPlace: Pathamuttom\nDate: 18 October 2026")
    c_cells2[2].paragraphs[0].add_run("\n\n(Department Seal)")

    doc.add_page_break()

    # ==========================================
    # PAGE 3: DECLARATION
    # ==========================================
    p_dec_head = doc.add_paragraph()
    p_dec_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_dec_head.add_run("DECLARATION\n")
    r.font.bold = True
    r.font.size = Pt(14)

    p_dec = doc.add_paragraph()
    p_dec.paragraph_format.line_spacing = 1.5
    p_dec.paragraph_format.space_before = Pt(12)
    p_dec.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_dec.add_run(
        "We hereby declare that the project report entitled “EcoWatt: Energy Consumption Prediction and Carbon Emission Estimation Using Machine Learning”, "
        "submitted in partial fulfilment of the requirements for the course 24ESQ2119(B)-A/B/C Artificial Intelligence and Machine Learning/Deep Learning/ Data Science Project "
        "of the degree of Bachelor of Technology in Mechanical Engineering of Saintgits College of Engineering (Autonomous), is a bonafide record of the work carried out by us "
        "under the supervision of Er. Philip Jacob Perakathu. This report has not been submitted, either in part or in full, for the award of any other degree or course. "
        "All sources of information, data and code used in this work have been duly acknowledged."
    )

    doc.add_paragraph().paragraph_format.space_before = Pt(14)
    tbl_dec = doc.add_table(rows=6, cols=4)
    tbl_dec.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_dec.style = 'Table Grid'
    headers = ["Sl.", "Name of the Student", "Register No.", "Signature"]
    for i, h in enumerate(headers):
        cell = tbl_dec.rows[0].cells[i]
        set_cell_background(cell, "EAEAEA")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        set_cell_margins(cell, 80, 80, 100, 100)

    students = [
        ("1", "Aaliya Fathima Arif", "[Register No.]"),
        ("2", "Afrah Zulfi", "[Register No.]"),
        ("3", "Muhammed Aasif", "[Register No.]"),
        ("4", "Sanju Philip Saji", "[Register No.]"),
        ("5", "S. Vighnesh (Team Leader)", "[Register No.]")
    ]
    for row_idx, stu in enumerate(students, start=1):
        for col_idx in range(3):
            cell = tbl_dec.rows[row_idx].cells[col_idx]
            p = cell.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run(stu[col_idx])
            set_cell_margins(cell, 80, 80, 100, 100)

    p_loc = doc.add_paragraph()
    p_loc.paragraph_format.space_before = Pt(18)
    p_loc.add_run("Place: Pathamuttom\nDate: 18 October 2026")

    doc.add_page_break()

    # ==========================================
    # PAGE 4: ACKNOWLEDGEMENT
    # ==========================================
    p_ack_head = doc.add_paragraph()
    p_ack_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_ack_head.add_run("ACKNOWLEDGEMENT\n")
    r.font.bold = True
    r.font.size = Pt(14)

    p_ack = doc.add_paragraph()
    p_ack.paragraph_format.line_spacing = 1.5
    p_ack.paragraph_format.space_before = Pt(12)
    p_ack.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_ack.add_run(
        "We express our sincere gratitude to Dr. Sudha T., Principal, Saintgits College of Engineering (Autonomous), for providing the facilities required for this project. "
        "We are thankful to Dr. Chacko Peno, Head of the Department of Mechanical Engineering, for the constant support and encouragement.\n\n"
        "We are deeply indebted to our project supervisor, Er. Philip Jacob Perakathu, for the valuable guidance, suggestions and supervision throughout the course of this work. "
        "We also thank [Name], Project Coordinator, and the members of the project evaluation committee for their constructive feedback during the reviews.\n\n"
        "Finally, we thank our parents, friends and all those who helped us directly or indirectly in the successful completion of this project.\n\n"
    )
    p_team = doc.add_paragraph()
    p_team.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_team.add_run("Aaliya Fathima Arif, Afrah Zulfi, Muhammed Aasif, Sanju Philip Saji and S. Vighnesh").bold = True

    doc.add_page_break()

    # ==========================================
    # PAGE 5: ABSTRACT
    # ==========================================
    p_abs_head = doc.add_paragraph()
    p_abs_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_abs_head.add_run("ABSTRACT\n")
    r.font.bold = True
    r.font.size = Pt(14)

    p_abs = doc.add_paragraph()
    p_abs.paragraph_format.line_spacing = 1.5
    p_abs.paragraph_format.space_before = Pt(12)
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.add_run(
        "Rising household electricity consumption increases both domestic electricity bills and the carbon emissions associated with thermal power generation, "
        "yet most households lack accessible tools to anticipate their electricity consumption or assess its environmental footprint prior to the arrival of billing statements. "
        "This project, EcoWatt (integrated within the modern GreenFuture platform), addresses this challenge by formulating household energy prediction as a physics-informed "
        "regression problem: estimating household electricity consumption (kWh) from seven key parameters—ambient temperature, time of day, relative humidity, appliance rated power, "
        "usage duration, number of operating devices, and residence occupancy—and translating the predicted consumption into estimated electricity cost (INR), carbon emissions (kg CO₂), "
        "and actionable energy-saving opportunities.\n\n"
        "Two complementary machine learning paradigms were implemented and evaluated on a physically grounded 6,000-record dataset (EcoWatt_6000_v7.csv): a physics-informed SGD "
        "Logarithmic Regression pipeline (incorporating log1p transformation, StandardScaler, and SGDRegressor) predicting the environmental residual over physical appliance base load, "
        "and a 10-step lagged Random Forest Regressor for non-linear feature interaction and multi-step recursive forecasting. The Random Forest achieved superior performance "
        "(R² = 0.6342, MAE = 1.1228 kWh, RMSE = 1.4752 kWh) over the Logarithmic Regression pipeline (R² = 0.5631, MAE = 1.2262 kWh, RMSE = 1.6122 kWh). "
        "To provide a robust, responsive end-user experience, the system has been developed and deployed as a modern single-page web application using React 18, TypeScript, Vite, "
        "and Tailwind CSS, featuring an in-browser physics-informed ML engine, live weather integration via the OpenWeatherMap REST API, real-time tariff calculation (₹8.40/kWh), "
        "carbon footprint audit (0.716 kg CO₂/kWh), and interactive analytics, directly advancing UN Sustainable Development Goals 7 (Affordable and Clean Energy) and 13 (Climate Action).\n\n"
    )
    p_kw = doc.add_paragraph()
    p_kw.add_run("Keywords: ").bold = True
    p_kw.add_run("Machine Learning, Physics-Informed ML, Logarithmic Regression, Random Forest Regressor, Energy Consumption Prediction, Carbon Emission Estimation, React, TypeScript, OpenWeatherMap API.")

    doc.add_page_break()

    # ==========================================
    # TABLE OF CONTENTS
    # ==========================================
    p_toc_head = doc.add_paragraph()
    p_toc_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_toc_head.add_run("CONTENTS\n")
    r.font.bold = True
    r.font.size = Pt(14)

    toc_items = [
        ("CERTIFICATE", "i"),
        ("DECLARATION", "ii"),
        ("ACKNOWLEDGEMENT", "iii"),
        ("ABSTRACT", "iv"),
        ("CONTENTS", "v"),
        ("LIST OF FIGURES", "vii"),
        ("LIST OF TABLES", "viii"),
        ("LIST OF ABBREVIATIONS", "ix"),
        ("CHAPTER 1: INTRODUCTION", "1"),
        ("    1.1 Background", "1"),
        ("    1.2 Problem Statement", "1"),
        ("    1.3 Objectives", "1"),
        ("    1.4 Social and Technical Relevance", "2"),
        ("    1.5 Scope and Limitations", "2"),
        ("    1.6 Organisation of the Report", "3"),
        ("CHAPTER 2: LITERATURE REVIEW", "4"),
        ("    2.1 Review of Existing Works", "4"),
        ("    2.2 Summary of Literature Review", "4"),
        ("    2.3 Limitations of Existing Systems and Research Gap", "5"),
        ("    2.4 Feasibility Study", "6"),
        ("CHAPTER 3: SYSTEM REQUIREMENTS AND SPECIFICATION", "7"),
        ("    3.1 Software and Hardware Requirements", "7"),
        ("    3.2 Dataset Description", "7"),
        ("CHAPTER 4: METHODOLOGY AND SYSTEM DESIGN", "9"),
        ("    4.1 Proposed System Overview", "9"),
        ("    4.2 System Architecture", "9"),
        ("    4.3 Data Pre-processing", "10"),
        ("    4.4 Model Selection and Justification", "11"),
        ("    4.5 Algorithm", "12"),
        ("    4.6 Design Diagrams", "12"),
        ("    4.7 Evaluation Metrics", "14"),
        ("CHAPTER 5: IMPLEMENTATION", "15"),
        ("    5.1 Development Environment", "15"),
        ("    5.2 Module Description", "15"),
        ("    5.3 Sample Code", "16"),
        ("    5.4 GitHub Repository", "17"),
        ("    5.5 Real-time Implementation / Deployment", "17"),
        ("CHAPTER 6: RESULTS AND DISCUSSION", "19"),
        ("    6.1 Experimental Setup", "19"),
        ("    6.2 Performance Evaluation", "19"),
        ("    6.3 Graphical Analysis", "20"),
        ("    6.4 Comparison with Existing Works", "21"),
        ("    6.5 Observations, Failures and Inferences", "21"),
        ("    6.6 Objectives vs. Outcomes", "22"),
        ("CHAPTER 7: CONCLUSION AND FUTURE SCOPE", "23"),
        ("    7.1 Conclusion", "23"),
        ("    7.2 Future Scope", "23"),
        ("REFERENCES", "24"),
        ("APPENDIX A: SOURCE CODE", "25"),
        ("APPENDIX B: SCREENSHOTS", "28"),
        ("APPENDIX C: MAPPING WITH SUSTAINABLE DEVELOPMENT GOALS", "30"),
        ("APPENDIX D: INDIVIDUAL CONTRIBUTION OF TEAM MEMBERS", "31"),
    ]

    for title, pg in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(title)
        if title.startswith("CHAPTER") or title in ["CERTIFICATE", "DECLARATION", "ACKNOWLEDGEMENT", "ABSTRACT", "CONTENTS", "LIST OF FIGURES", "LIST OF TABLES", "LIST OF ABBREVIATIONS", "REFERENCES"]:
            r1.bold = True
        dots_len = max(3, 85 - len(title) - len(pg))
        p.add_run(" " + "." * dots_len + " ")
        r2 = p.add_run(pg)
        if r1.bold:
            r2.bold = True

    doc.add_page_break()

    # ==========================================
    # LIST OF FIGURES & TABLES & ABBREVIATIONS
    # ==========================================
    p_lof = doc.add_paragraph()
    p_lof.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_lof.add_run("LIST OF FIGURES\n")
    r.font.bold = True
    r.font.size = Pt(14)

    tbl_lof = doc.add_table(rows=12, cols=3)
    tbl_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_lof.style = 'Table Grid'
    lof_headers = ["Figure No.", "Title", "Page No."]
    for i, h in enumerate(lof_headers):
        c = tbl_lof.rows[0].cells[i]
        set_cell_background(c, "EAEAEA")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        set_cell_margins(c, 60, 60, 100, 100)

    fig_data = [
        ("4.1", "System architecture of the proposed system", "10"),
        ("4.2", "Activity (workflow) diagram of the EcoWatt application", "13"),
        ("4.3", "Use-case diagram of the EcoWatt application", "13"),
        ("5.1", "Landing page of the EcoWatt web application", "17"),
        ("5.2", "Prediction dashboard for a sample session", "18"),
        ("6.1", "Model performance comparison reported by the application", "20"),
        ("6.2", "Random Forest multi-step forecast (admin panel)", "20"),
        ("6.3", "Analytics: energy-consumption trend and appliance share", "21"),
        ("B.1", "Landing hero section and responsive theme toggle", "28"),
        ("B.2", "Live weather telemetry, parameter inputs, and prediction dashboard", "28"),
        ("B.3", "Prediction history trend chart (bar/line views) and CSV export", "29"),
    ]
    for row_idx, (fno, ftitle, fpg) in enumerate(fig_data, start=1):
        tbl_lof.rows[row_idx].cells[0].paragraphs[0].add_run(fno)
        tbl_lof.rows[row_idx].cells[1].paragraphs[0].add_run(ftitle)
        tbl_lof.rows[row_idx].cells[2].paragraphs[0].add_run(fpg)
        for ci in range(3):
            set_cell_margins(tbl_lof.rows[row_idx].cells[ci], 60, 60, 100, 100)

    p_lot = doc.add_paragraph()
    p_lot.paragraph_format.space_before = Pt(20)
    p_lot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_lot.add_run("LIST OF TABLES\n")
    r.font.bold = True
    r.font.size = Pt(14)

    tbl_lot = doc.add_table(rows=9, cols=3)
    tbl_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_lot.style = 'Table Grid'
    for i, h in enumerate(["Table No.", "Title", "Page No."]):
        c = tbl_lot.rows[0].cells[i]
        set_cell_background(c, "EAEAEA")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        set_cell_margins(c, 60, 60, 100, 100)

    tbl_data = [
        ("2.1", "Summary of literature review", "4"),
        ("3.1", "Software and hardware requirements", "7"),
        ("3.2", "Description of dataset attributes", "8"),
        ("5.1", "Modules of the EcoWatt application", "15"),
        ("6.1", "Performance comparison of machine learning regression models", "19"),
        ("6.2", "Summary of observed issues, causes and solutions", "21"),
        ("C.1", "Mapping with Sustainable Development Goals (SDGs)", "30"),
        ("D.1", "Individual contribution of team members", "31"),
    ]
    for row_idx, (tno, ttitle, tpg) in enumerate(tbl_data, start=1):
        tbl_lot.rows[row_idx].cells[0].paragraphs[0].add_run(tno)
        tbl_lot.rows[row_idx].cells[1].paragraphs[0].add_run(ttitle)
        tbl_lot.rows[row_idx].cells[2].paragraphs[0].add_run(tpg)
        for ci in range(3):
            set_cell_margins(tbl_lot.rows[row_idx].cells[ci], 60, 60, 100, 100)

    doc.add_page_break()

    # List of Abbreviations
    p_ab = doc.add_paragraph()
    p_ab.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_ab.add_run("LIST OF ABBREVIATIONS\n")
    r.font.bold = True
    r.font.size = Pt(14)

    tbl_ab = doc.add_table(rows=18, cols=2)
    tbl_ab.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ab.style = 'Table Grid'
    tbl_ab.rows[0].cells[0].paragraphs[0].add_run("Abbreviation").bold = True
    tbl_ab.rows[0].cells[1].paragraphs[0].add_run("Expansion").bold = True
    set_cell_background(tbl_ab.rows[0].cells[0], "EAEAEA")
    set_cell_background(tbl_ab.rows[0].cells[1], "EAEAEA")

    abbrevs = [
        ("AI", "Artificial Intelligence"),
        ("API", "Application Programming Interface"),
        ("CEA", "Central Electricity Authority (Government of India)"),
        ("CO₂", "Carbon Dioxide"),
        ("CSV", "Comma-Separated Values"),
        ("INR", "Indian Rupee (₹)"),
        ("KSEB", "Kerala State Electricity Board"),
        ("kWh", "Kilowatt-hour"),
        ("MAE", "Mean Absolute Error"),
        ("MAPE", "Mean Absolute Percentage Error"),
        ("ML", "Machine Learning"),
        ("MSE", "Mean Squared Error"),
        ("R²", "Coefficient of Determination"),
        ("RF", "Random Forest"),
        ("RMSE", "Root Mean Squared Error"),
        ("SDG", "Sustainable Development Goal"),
        ("SGD", "Stochastic Gradient Descent"),
    ]
    for idx, (abbr, exp) in enumerate(abbrevs, start=1):
        tbl_ab.rows[idx].cells[0].paragraphs[0].add_run(abbr).bold = True
        tbl_ab.rows[idx].cells[1].paragraphs[0].add_run(exp)
        set_cell_margins(tbl_ab.rows[idx].cells[0], 50, 50, 80, 80)
        set_cell_margins(tbl_ab.rows[idx].cells[1], 50, 50, 80, 80)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 1: INTRODUCTION
    # ==========================================
    doc.add_heading("CHAPTER 1: INTRODUCTION", level=1)
    
    doc.add_heading("1.1 Background", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "Rising household electricity consumption is a growing concern for both domestic budgets and national carbon-reduction targets. "
        "Residential electricity use is shaped by a complex interplay of environmental factors—such as ambient temperature, relative humidity, "
        "and time of day—and consumer behavior, including appliance rated power, usage duration, operating device count, and household occupancy levels. "
        "Despite this direct correlation, most households have no simple or intuitive way to see how everyday appliance choices translate into "
        "monetary billing cost and carbon emissions before the monthly utility statement arrives.\n\n"
        "Artificial Intelligence and Machine Learning (AI/ML) offer a practical, accessible way to bridge this gap. Regression-based models can capture "
        "the underlying relationship between everyday household parameters and actual electrical energy consumption. This allows instantaneous, scenario-based "
        "energy predictions to be generated from intuitive user inputs, entirely eliminating the requirement for costly smart-meter hardware or specialized "
        "sub-metering installations. This project, EcoWatt (integrated within the modern GreenFuture web platform), applies these machine learning principles "
        "to construct an interactive, physics-informed decision-support application that predicts residential energy demand and translates it into electricity "
        "tariffs and carbon dioxide (CO₂) emissions."
    )

    doc.add_heading("1.2 Problem Statement", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "Increasing residential power demand drives higher electricity utility bills and expands greenhouse gas emissions from fossil-fuel-dominated electrical grids. "
        "However, domestic energy consumers rarely possess accessible tools to anticipate their electricity usage, identify peak-demand periods, or gauge the carbon "
        "impact of their appliances before billing cycles close. EcoWatt addresses this problem by formulating residential energy prediction as a physics-informed "
        "machine learning regression task: given seven household and environmental parameters—temperature, hour of day, humidity, appliance power rating, "
        "usage duration, device count, and residence occupancy—the system predicts continuous electricity consumption (kWh). It then dynamically derives "
        "the financial electricity cost (INR), associated CO₂ emissions (kg), peak usage classification, and tailored efficiency recommendations."
    )

    doc.add_heading("1.3 Objectives", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.add_run("The primary objectives of this project are:\n")
    objs = [
        "To generate, preprocess, and benchmark a physically grounded household energy-consumption dataset, identifying ambient temperature, occupancy, and appliance load as core predictive features consistent with building energy literature.",
        "To formulate and compare two machine learning paradigms: a physics-informed SGD Logarithmic Regression residual pipeline and a 10-step lagged Random Forest Regressor for non-linear energy forecasting.",
        "To systematically evaluate both models across established regression metrics: Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Coefficient of Determination (R²), and Mean Absolute Percentage Error (MAPE).",
        "To translate raw energy predictions into actionable socio-economic and environmental outputs: electricity tariff cost (INR), carbon emissions (kg CO₂), peak-demand classifications, and an Energy Efficiency Score (Eco Score).",
        "To engineer a modern, responsive, client-side web application using React 18, TypeScript, Tailwind CSS, and Vite, integrating live weather telemetry via the OpenWeatherMap REST API and client-side machine learning inference."
    ]
    for obj in objs:
        doc.add_paragraph(obj, style='List Bullet')

    doc.add_heading("1.4 Social and Technical Relevance", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "EcoWatt directly benefits domestic energy consumers by replacing opaque end-of-month electricity bills with transparent, real-time feedback that empowers proactive "
        "conservation. Globally, residential and commercial buildings account for roughly 36% of total final energy consumption and approximately 40% of direct and indirect "
        "carbon emissions [1]. By equipping households with immediate insights into energy waste, EcoWatt directly supports United Nations Sustainable Development Goals: "
        "SDG 7 (Affordable and Clean Energy), SDG 13 (Climate Action), and SDG 11 (Sustainable Cities and Communities) (Appendix C).\n\n"
        "Technically, residential electricity modeling presents both linear physical relationships (wattage × hours × devices) and non-linear environmental and behavioral "
        "dynamics (thermostat adjustments under high heat and humidity). This justifies a hybrid physics-informed approach: decomposing energy into an explicit appliance base load "
        "and a learned environmental residual, comparing gradient-descent linear pipelines against multi-tree ensemble methods."
    )

    doc.add_heading("1.5 Scope and Limitations", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "The project scope encompasses household-level energy consumption prediction using seven accessible user inputs, with real-time derivation of costs, emissions, "
        "and efficiency metrics. Exclusions include physical smart-meter hardware development and invasive circuit-level appliance sub-metering. Key limitations include: "
        "the dataset utilized for benchmarking (EcoWatt_6000_v7.csv) is synthesised using physics-grounded mathematical relationships rather than intrusive multi-year hardware logging; "
        "the electricity tariff rate (₹8.40/kWh) and grid emission factor (0.716 kg CO₂/kWh) represent standard benchmark averages for Kerala/India (Section 4.4); and model metrics "
        "reflect controlled test-split evaluations."
    )

    doc.add_heading("1.6 Organisation of the Report", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "This report is organized into seven chapters: Chapter 2 reviews relevant literature and identifies research gaps; Chapter 3 outlines system requirements and dataset properties; "
        "Chapter 4 details methodology, mathematical formulations, architecture, and evaluation metrics; Chapter 5 presents technical implementation details and module structures; "
        "Chapter 6 presents empirical results, graphical analytics, and operational inferences; and Chapter 7 summarizes conclusions and outlines future enhancements."
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 2: LITERATURE REVIEW
    # ==========================================
    doc.add_heading("CHAPTER 2: LITERATURE REVIEW", level=1)

    doc.add_heading("2.1 Review of Existing Works", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "A rigorous review of academic and practical energy prediction literature was conducted. Khalil et al. [1] performed a comprehensive systematic review of machine learning, "
        "deep learning, and statistical methods across building energy forecasting, noting that residential buildings account for over 36% of global energy demand and 40% of carbon emissions. "
        "Their findings established that machine learning models consistently yield 15–28% energy conservation improvements when integrated into user-facing decision feedback loops, "
        "strongly motivating EcoWatt's carbon-emission derivation module.\n\n"
        "A meta-survey covering 431 studies on machine learning for building energy prediction published in the Journal of Building Engineering [4] identified ambient temperature, "
        "residence occupancy, and appliance operating schedules as the three most statistically influential predictive features. This informed EcoWatt's feature selection and its "
        "architectural decision to separate deterministic appliance base load from environmental residuals. In smart energy forecasting studies [5], the incorporation of real-time "
        "contextual weather data demonstrated significant forecast enhancements, highlighting the necessity of live weather API telemetry.\n\n"
        "Empirical household data surveys from Kerala, notably the Cherukunnu Gramapanchayath Socio-Economic Survey [6] covering 3,785 households, provided realistic domestic "
        "consumption benchmarks, typical device ownership numbers, and regional electricity expenditure ranges. Furthermore, international open benchmarks—including the UCI Appliances "
        "Energy Prediction dataset [7] and the UCI Individual Household Electric Power Consumption dataset [8]—established established reference frameworks for regression evaluation."
    )

    doc.add_heading("2.2 Summary of Literature Review", level=2)
    tbl_lr = doc.add_table(rows=7, cols=5)
    tbl_lr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_lr.style = 'Table Grid'
    lr_hdrs = ["Ref.", "Author(s) & Year", "Method / Technique", "Dataset", "Key Findings & Limitations"]
    for i, h in enumerate(lr_hdrs):
        c = tbl_lr.rows[0].cells[i]
        set_cell_background(c, "EAEAEA")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        set_cell_margins(c, 60, 60, 80, 80)

    lr_data = [
        ("[1]", "Khalil et al. (2022)", "Systematic Review of ML/DL Forecasting", "Global building studies", "Buildings consume 36% of global energy; ML reduces waste; lacks end-user apps."),
        ("[4]", "Building Energy Survey (2021)", "Meta-analysis of 431 ML studies", "Literature corpus", "Temp, occupancy & appliance wattage dominate; models rarely deployed to web."),
        ("[5]", "AI Smart Energy Study (2023)", "Context-Aware Energy Forecasting", "Industrial & domestic sites", "Real-time weather integration improves accuracy; peak hours enable demand shift."),
        ("[6]", "DES Kerala (2024)", "Socio-Economic Survey Analysis", "3,785 Kerala households", "Provided realistic ranges for Kerala household appliances, bills and load profiles."),
        ("[7]", "UCI ML Repository (2017)", "Appliance Energy Prediction", "Measured house sensor logs", "Benchmark for environmental regressors; lacks cost and CO2 impact translations."),
        ("[8]", "UCI ML Repository (2012)", "Electric Power Consumption", "Single-household 4-yr records", "Demonstrated high variance and lag correlation; lacks real-time interactive UI."),
    ]
    for row_idx, r_item in enumerate(lr_data, start=1):
        for ci in range(5):
            c = tbl_lr.rows[row_idx].cells[ci]
            c.paragraphs[0].add_run(r_item[ci])
            set_cell_margins(c, 60, 60, 80, 80)

    doc.add_heading("2.3 Limitations of Existing Systems and Research Gap", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "Existing research overwhelmingly emphasizes model accuracy metrics (such as MSE and R²) in isolated Jupyter notebooks or server-heavy environments, "
        "rarely packaging models into responsive, user-friendly digital tools that ordinary households can operate. Furthermore, prior solutions rarely translate "
        "raw kilowatt-hour (kWh) values into direct financial billing metrics (INR) or localized greenhouse gas equivalents (kg CO₂). EcoWatt resolves this gap "
        "by combining a physics-informed ML pipeline with a production-ready, client-side web application that instantly converts predictions into costs, emissions, "
        "and actionable conservation recommendations."
    )

    doc.add_heading("2.4 Feasibility Study", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "• Technical Feasibility: Highly viable. Modern client-side web architectures (React 18, TypeScript, Vite) execute mathematical matrix operations and ML regression in-browser without server dependencies.\n"
        "• Operational Feasibility: Outstanding. Users access the system via standard web browsers with zero installation requirements, adjusting simple intuitive sliders.\n"
        "• Economic Feasibility: Optimal. Developed completely with open-source software, requiring zero server hosting fees or expensive smart-meter hardware."
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 3: SYSTEM REQUIREMENTS AND SPECIFICATION
    # ==========================================
    doc.add_heading("CHAPTER 3: SYSTEM REQUIREMENTS AND SPECIFICATION", level=1)

    doc.add_heading("3.1 Software and Hardware Requirements", level=2)
    tbl_req = doc.add_table(rows=8, cols=3)
    tbl_req.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_req.style = 'Table Grid'
    for i, h in enumerate(["Category", "Item", "Specification"]):
        c = tbl_req.rows[0].cells[i]
        set_cell_background(c, "EAEAEA")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        set_cell_margins(c, 60, 60, 80, 80)

    req_data = [
        ("Web Platform", "Frontend Framework", "React 18, TypeScript 5, Vite Build Tool, Tailwind CSS"),
        ("Web UI & Styling", "Icons & Styling", "Lucide React, Space Grotesk & Inter typography, Dark/Light Themes"),
        ("ML & Data", "Machine Learning Stack", "TypeScript client ML Engine (SGD Log-Reg, Random Forest, Metrics) & Python scikit-learn"),
        ("External Telemetry", "Weather REST API", "OpenWeatherMap API (live temperature, feels-like, humidity, condition description)"),
        ("Development IDE", "Code & Version Control", "Antigravity IDE / VS Code, Git, GitHub repository"),
        ("Client Hardware", "End-User Device", "Modern Web Browser (Chrome, Edge, Firefox, Safari); 2 GB RAM minimum"),
        ("Data Formats", "Storage & Export", "CSV (EcoWatt_6000.csv, prediction_history.csv), JSON, HTML5 Web Storage"),
    ]
    for row_idx, r_item in enumerate(req_data, start=1):
        for ci in range(3):
            c = tbl_req.rows[row_idx].cells[ci]
            c.paragraphs[0].add_run(r_item[ci])
            set_cell_margins(c, 60, 60, 80, 80)

    doc.add_heading("3.2 Dataset Description", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "The EcoWatt system operates on two physically grounded dataset representations: a real-time 200-sample generator with seed 42, and a comprehensive 6,000-record "
        "benchmark dataset (EcoWatt_6000.csv). The target energy consumption E (kWh) is synthesised according to physical energy laws with thermal non-linearities and Gaussian disturbance:\n\n"
        "    E = (P × t × N / 1000) × [1 + 0.023 × max(T − 24, 0)] + 0.13 × O × t + ε        (3.1)\n\n"
        "where P is the appliance rated power in Watts, t is usage duration in hours, N is the count of operating devices, T is ambient temperature in °C, "
        "O is residence occupancy, and ε ~ N(0, 2) represents unobserved random stochastic load. The model isolates deterministic appliance base load and environmental residual:\n\n"
        "    E_load = (P × t × N) / 1000   (kWh)                                                (3.2)\n"
        "    E_residual = E − E_load       (kWh)                                                (3.3)\n"
    )

    tbl_attr = doc.add_table(rows=9, cols=4)
    tbl_attr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_attr.style = 'Table Grid'
    for i, h in enumerate(["Sl.", "Attribute Name", "Type & Unit", "Physical Description & Valid Range"]):
        c = tbl_attr.rows[0].cells[i]
        set_cell_background(c, "EAEAEA")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        set_cell_margins(c, 60, 60, 80, 80)

    attr_data = [
        ("1", "Temperature", "Float (°C)", "Ambient indoor/outdoor temperature (20.0 to 40.0 °C)"),
        ("2", "Time", "Integer (h)", "Hour of day (0 to 23 h) governing diurnal occupancy cycles"),
        ("3", "Humidity", "Integer (%)", "Relative atmospheric humidity (40 to 90 %) influencing HVAC thermal loads"),
        ("4", "PowerRating", "Integer (W)", "Mean electrical power rating of active appliances (100 to 2500 W)"),
        ("5", "UsageDuration", "Float (h)", "Continuous operational appliance duration (0.5 to 10.0 hours)"),
        ("6", "NumDevices", "Integer", "Total count of simultaneously active appliances (1 to 10 units)"),
        ("7", "Occupancy", "Integer", "Count of active human occupants in the dwelling (1 to 6 persons)"),
        ("8", "EnergyConsumption", "Float (kWh)", "Target variable: Total electrical energy consumed (0.0 to 180.0+ kWh)"),
    ]
    for row_idx, r_item in enumerate(attr_data, start=1):
        for ci in range(4):
            c = tbl_attr.rows[row_idx].cells[ci]
            c.paragraphs[0].add_run(r_item[ci])
            set_cell_margins(c, 60, 60, 80, 80)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 4: METHODOLOGY AND SYSTEM DESIGN
    # ==========================================
    doc.add_heading("CHAPTER 4: METHODOLOGY AND SYSTEM DESIGN", level=1)

    doc.add_heading("4.1 Proposed System Overview", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "The proposed system bridges machine learning theory and practical consumer utility through a decoupled, client-centric architecture. "
        "Users provide household appliance and occupancy parameters through an intuitive user interface, augmented by live atmospheric data retrieved "
        "via the OpenWeatherMap REST API. The core ML pipeline separates deterministic physical appliance load from learned environmental residuals, "
        "ensuring that predictions adhere to physical conservation laws while capturing subtle non-linear dependencies. The predicted kilowatt-hours "
        "are immediately converted into billing costs (INR), grid carbon emissions (kg CO₂), peak demand classifications, and efficiency scores."
    )

    doc.add_heading("4.2 System Architecture", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "Figure 4.1 depicts the high-level system architecture of the modern EcoWatt web platform. The user interacts through a responsive React 18 single-page "
        "application built with Vite and Tailwind CSS. The application architecture comprises four decoupled tiers:\n"
        "1. Presentation & UI Tier: Parameter control sliders, weather telemetry display, simulation triggers, role-based login modal, and analytics dashboards.\n"
        "2. Client Machine Learning Engine: In-browser matrix operations (mlEngine.ts) performing log1p feature transformation, StandardScaler normalization, "
        "L2-regularized SGD regression for residual estimation, and lag-10 recursive Random Forest autoregression.\n"
        "3. External Telemetry Tier: Asynchronous REST HTTP requests to the OpenWeatherMap API for live ambient city weather.\n"
        "4. Persistence & Export Tier: Session storage, CSV dataset parsing/upload, and historical prediction logging with downloadable CSV reports."
    )

    if os.path.exists("d:/GreenFuture/report_figures/fig_4_1_architecture.png"):
        doc.add_paragraph().paragraph_format.space_before = Pt(6)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("d:/GreenFuture/report_figures/fig_4_1_architecture.png", width=Inches(5.8))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_cap.add_run("Figure 4.1: System architecture of the proposed EcoWatt web platform")
        r.font.bold = True
        r.font.size = Pt(10)

    doc.add_heading("4.3 Data Pre-processing", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "Because dataset features are numeric and bounded within physically realistic operating ranges, data preprocessing involves four systematic operations:\n"
        "• Range Verification: Validating input slider values and uploaded CSV columns against physical constraints (e.g. Temperature ∈ [20, 40] °C, Duration ∈ [0.5, 10] h).\n"
        "• Physical Load Decomposition: Separating base load E_load (Equation 3.2) from target consumption to generate the target training residual E_residual.\n"
        "• Feature Transformation: Applying natural logarithmic log(1 + x) scaling to skewed environmental regressors (Temperature, Humidity, Time, Occupancy).\n"
        "• Standard Normalization: Computing column-wise means and sample standard deviations to z-score normalize the transformed features: z = (log(1+x) − μ) / σ."
    )

    doc.add_heading("4.4 Model Selection and Justification", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "Two regression paradigms were selected and comparatively evaluated:\n\n"
        "1. Physics-Informed SGD Logarithmic Regression Pipeline: Deterministic electrical wattage represents the bulk of power consumption. "
        "Thus, machine learning is tasked only with estimating the residual environmental variance: ŷ_res = w^T z + b, where z = StandardScaler(log(1 + x_env)). "
        "The overall prediction is reconstructed and strictly constrained against negative values: Ê = max(0, E_load + ŷ_res) (kWh).\n\n"
        "2. Random Forest Regressor: An ensemble of B = 100 decision trees (ŷ = (1/B) Σ T_b(x)) capable of capturing non-linear feature interactions without manual "
        "interaction term engineering. Operating over a 10-step lagged historical sequence, it recursively forecasts multi-step forward trajectories.\n\n"
        "3. Domain-Specific Derivations: Predicted kilowatt-hours are mapped directly to domestic expenditure and environmental impact:\n"
        "    Cost (₹) = Ê × R           (4.4)  [where R = ₹8.40/kWh, representing KSEB higher-slab domestic tariff]\n"
        "    CO₂ (kg) = Ê × EF          (4.5)  [where EF = 0.716 kg CO₂/kWh, based on Central Electricity Authority India Grid Baseline]\n"
        "    EcoScore = 100 × [1 − min(1, Ê / E_ref)]  (4.6)  [where E_ref is the 95th percentile benchmark consumption]"
    )

    doc.add_heading("4.5 Algorithm", level=2)
    p_alg = doc.add_paragraph()
    p_alg.paragraph_format.line_spacing = 1.15
    p_alg.paragraph_format.space_before = Pt(4)
    r_alg = p_alg.add_run(
        "Algorithm 1: EcoWatt Real-Time Energy Prediction and Carbon Audit\n"
        "Input  : Temp, Time, Humidity, Power, Duration, Devices, Occupancy; City name\n"
        "Output : Energy (kWh), Cost (₹), CO₂ (kg), Peak Category, Eco Score, Savings Potential, Multi-step Forecast\n"
        "--------------------------------------------------------------------------------------------------\n"
        " 1: Initialize application state: theme context, authentication, and preloaded benchmark CSV dataset\n"
        " 2: IF user requests weather: fetch OpenWeatherMap REST API, extract Temp & Humidity, auto-populate sliders\n"
        " 3: Parse active dataset; compute E_load = (P * t * N) / 1000 and E_residual = EnergyConsumption - E_load\n"
        " 4: Fit Logarithmic Pipeline: log1p transform -> StandardScaler -> regularized SGD regression weights\n"
        " 5: ON 'Predict Energy' / parameter change:\n"
        "      a. Compute current base load: current_E_load = (Power * Duration * Devices) / 1000\n"
        "      b. Predict residual: ŷ_res = Pipeline.predict([Temp, Humidity, Time, Occupancy])\n"
        "      c. Total Predicted Energy: Ê = max(0, current_E_load + ŷ_res)\n"
        "      d. Electricity Cost: Cost = Ê * 8.40;  Carbon Footprint: CO₂ = Ê * 0.716\n"
        "      e. Compute Eco Score = 100 * (1 - min(1, Ê / E_ref))\n"
        "      f. Evaluate saving opportunities (peak shift, HVAC setpoint, standby cut, duration optimization)\n"
        "      g. Classify peak demand slot: 18-21 -> 'Peak (6-9 PM)'; 12-15 -> 'Afternoon (12-3 PM)'; etc.\n"
        "      h. Append record to prediction history; update interactive trend charts & CSV export buffer\n"
        " 6: IF authenticated as Admin:\n"
        "      a. Construct 10-step lag autoregressive matrices from historical sequence\n"
        "      b. Execute recursive multi-step forecasting across 1 to 30 forward steps\n"
        "      c. Render comparative model metrics table: MAE, MSE, RMSE, R², MAPE\n"
        " 7: END"
    )
    r_alg.font.name = 'Courier New'
    r_alg.font.size = Pt(8.5)

    doc.add_heading("4.6 Design Diagrams", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.add_run(
        "The operational lifecycle and user interactions are formally modeled through activity and use-case diagrams. "
        "Figure 4.2 illustrates the sequential activity workflow from initial telemetry retrieval to dashboard rendering. "
        "Figure 4.3 illustrates the use-case relationships between Regular Users (simulation, recommendations, history) and System Administrators (forecasting, benchmarking)."
    )

    if os.path.exists("d:/GreenFuture/report_figures/fig_4_2_workflow.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("d:/GreenFuture/report_figures/fig_4_2_workflow.png", width=Inches(4.6))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_cap.add_run("Figure 4.2: Activity (workflow) diagram of the EcoWatt web application")
        r.font.bold = True
        r.font.size = Pt(10)

    if os.path.exists("d:/GreenFuture/report_figures/fig_4_3_usecase.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("d:/GreenFuture/report_figures/fig_4_3_usecase.png", width=Inches(4.8))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_cap.add_run("Figure 4.3: Use-case diagram of the EcoWatt web application")
        r.font.bold = True
        r.font.size = Pt(10)

    doc.add_heading("4.7 Evaluation Metrics", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "To rigorously quantify regression accuracy, five standard mathematical metrics are evaluated:\n"
        "• Mean Absolute Error (MAE): MAE = (1/n) Σ |y_i − ŷ_i|  (4.7)\n"
        "• Root Mean Squared Error (RMSE): RMSE = √[(1/n) Σ (y_i − ŷ_i)²]  (4.8)\n"
        "• Coefficient of Determination (R²): R² = 1 − [Σ (y_i − ŷ_i)² / Σ (y_i − ȳ)²]  (4.9)\n"
        "• Mean Absolute Percentage Error (MAPE): MAPE = (100/n) Σ (|y_i − ŷ_i| / y_i)  (4.10)\n"
        "• Mean Squared Error (MSE): MSE = (1/n) Σ (y_i − ŷ_i)²"
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5: IMPLEMENTATION
    # ==========================================
    doc.add_heading("CHAPTER 5: IMPLEMENTATION", level=1)

    doc.add_heading("5.1 Development Environment", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "The project was initially prototyped in Python 3.10+ using scikit-learn, Pandas, NumPy, and Streamlit. To overcome server-side execution bottlenecks, "
        "tunnel latency, and process instability, the platform was re-architected into a modern, production-grade web application (GreenFuture). "
        "The frontend is engineered in React 18 with TypeScript 5, Vite build orchestration, and Tailwind CSS. Client-side linear algebra and machine learning "
        "routines are implemented in TypeScript (mlEngine.ts), executing directly inside the user's browser runtime with sub-millisecond latency. "
        "Atmospheric weather telemetry is integrated through asynchronous Fetch API calls to OpenWeatherMap."
    )

    doc.add_heading("5.2 Module Description", level=2)
    tbl_mod = doc.add_table(rows=7, cols=3)
    tbl_mod.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_mod.style = 'Table Grid'
    for i, h in enumerate(["Module Name", "Source Component / File", "Functional Responsibilities"]):
        c = tbl_mod.rows[0].cells[i]
        set_cell_background(c, "EAEAEA")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        set_cell_margins(c, 60, 60, 80, 80)

    mod_data = [
        ("Header & Theme Module", "Header.tsx, ThemeContext.tsx", "Global navigation, brand identity, dark/light theme switching, and smooth anchor scrolling."),
        ("Hero Experience", "HeroLeft.tsx, HeroRight.tsx", "Modern visual introduction, interactive feature highlights, and ambient clean-energy design motifs."),
        ("Energy Simulator Core", "EcoWattSimulator.tsx", "Input parameter sliders, weather auto-fill, prediction trigger, cost/carbon displays, and smart alerts."),
        ("Client ML Engine", "mlEngine.ts", "Synthetic dataset generator, CSV parsing, log1p + StandardScaler pipeline, SGD regression, and RF lag forecasting."),
        ("Analytics & Benchmarks", "EcoWattAnalytics.tsx", "Historical consumption sequence trends, typical household appliance shares (AC 40%, Fridge 20%, etc.), model metric cards."),
        ("Weather Telemetry", "fetchWeather REST API", "Live temperature, humidity, feels-like, and condition retrieval for any entered city name."),
    ]
    for row_idx, r_item in enumerate(mod_data, start=1):
        for ci in range(3):
            c = tbl_mod.rows[row_idx].cells[ci]
            c.paragraphs[0].add_run(r_item[ci])
            set_cell_margins(c, 60, 60, 80, 80)

    doc.add_heading("5.3 Sample Code", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(4)
    r_code = p.add_run(
        "// TypeScript Physics-Informed ML Residual Estimator (from mlEngine.ts)\n"
        "export function fitSGDRegressorLogPipeline(X: number[][], y: number[]) {\n"
        "  const N = X.length, p = X[0].length;\n"
        "  // 1. Natural logarithmic feature transformation: log(1 + x)\n"
        "  const logX = X.map(row => row.map(v => Math.log1p(Math.max(0, v))));\n"
        "  // 2. StandardScaler z-score normalization\n"
        "  const means = Array(p).fill(0), stds = Array(p).fill(0);\n"
        "  for (let j = 0; j < p; j++) {\n"
        "    let sum = 0; for (let i = 0; i < N; i++) sum += logX[i][j];\n"
        "    means[j] = sum / N;\n"
        "    let sq = 0; for (let i = 0; i < N; i++) sq += (logX[i][j] - means[j]) ** 2;\n"
        "    stds[j] = Math.sqrt(sq / N) || 1.0;\n"
        "  }\n"
        "  const normX = logX.map(r => r.map((val, j) => (val - means[j]) / stds[j]));\n"
        "  // 3. Regularized Least Squares / SGD normal equations with L2 shrinkage\n"
        "  const meanY = y.reduce((a, b) => a + b, 0) / N;\n"
        "  // Solve (X^T * X + lambda * I) * w = X^T * (y - meanY)\n"
        "  // Returns residual predictor: Ê = max(0, E_load + predictResidual(features))\n"
        "}"
    )
    r_code.font.name = 'Courier New'
    r_code.font.size = Pt(8.5)

    doc.add_heading("5.4 GitHub Repository", level=2)
    tbl_git = doc.add_table(rows=4, cols=2)
    tbl_git.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_git.style = 'Table Grid'
    git_info = [
        ("Repository URL", "https://github.com/S-VIGHNESH18/projects (branch: project)"),
        ("Project Directory", "d:/GreenFuture (Web Platform) & d:/EcoWatt (Python Prototype)"),
        ("Tech Stack", "React 18, TypeScript 5, Vite, Tailwind CSS, Python 3.10+, scikit-learn"),
        ("Contents", "Full source code, trained model logic, EcoWatt_6000.csv, run_web.bat, project documentation"),
    ]
    for row_idx, (k, v) in enumerate(git_info):
        tbl_git.rows[row_idx].cells[0].paragraphs[0].add_run(k).bold = True
        tbl_git.rows[row_idx].cells[1].paragraphs[0].add_run(v)
        set_cell_margins(tbl_git.rows[row_idx].cells[0], 50, 50, 80, 80)
        set_cell_margins(tbl_git.rows[row_idx].cells[1], 50, 50, 80, 80)

    doc.add_heading("5.5 Real-time Implementation / Deployment", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "The application is compiled and served using Vite's optimized local development and production pipeline (`npm run dev -- --port 5173`). "
        "Upon launching, users are presented with a clean hero section (Figure 5.1). Users configure appliance parameters using responsive sliders "
        "or auto-populate them via live weather telemetry. Clicking 'Simulate Energy Usage' immediately updates the prediction metrics card (Figure 5.2), "
        "displaying 46.82 kWh predicted energy, ₹393.26 electricity cost, 33.52 kg CO₂ emissions, an Eco Score of 13.0/100, and a 12.74% potential saving breakdown "
        "(₹57.42/day), logged automatically to the historical audit table."
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 6: RESULTS AND DISCUSSION
    # ==========================================
    doc.add_heading("CHAPTER 6: RESULTS AND DISCUSSION", level=1)

    doc.add_heading("6.1 Experimental Setup", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "Model evaluation experiments were conducted on the 6,000-record benchmark dataset (EcoWatt_6000_v7.csv). An 80:20 train-test partition was applied "
        "with random seed 42 to ensure deterministic reproducibility. The Logarithmic Regression pipeline was trained on environmental residuals using "
        "SGD optimization, while the Random Forest Regressor was configured with B = 100 decision trees operating over 10-step lagged historical sequences. "
        "Predictions were evaluated using scikit-learn and the client-side evaluation engine."
    )

    doc.add_heading("6.2 Performance Evaluation", level=2)
    tbl_res = doc.add_table(rows=3, cols=6)
    tbl_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_res.style = 'Table Grid'
    for i, h in enumerate(["Model Architecture", "MAE (kWh)", "MSE", "RMSE (kWh)", "R² Score", "MAPE (%)"]):
        c = tbl_res.rows[0].cells[i]
        set_cell_background(c, "EAEAEA")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        set_cell_margins(c, 60, 60, 80, 80)

    res_data = [
        ("Logarithmic Regression (SGD Pipeline)", "1.2262", "2.5992", "1.6122", "0.5631", "31.82%"),
        ("Random Forest Regressor (Ensemble Best)", "1.1228", "2.1763", "1.4752", "0.6342", "29.19%"),
    ]
    for row_idx, r_item in enumerate(res_data, start=1):
        for ci in range(6):
            c = tbl_res.rows[row_idx].cells[ci]
            c.paragraphs[0].add_run(r_item[ci])
            set_cell_margins(c, 60, 60, 80, 80)

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "As summarized in Table 6.1 and illustrated in Figure 6.1, the Random Forest Regressor outperforms the Logarithmic Regression pipeline across all evaluation metrics. "
        "The ensemble model achieves an R² of 0.6342 (a 7.1 percentage-point improvement), while reducing MAE to 1.1228 kWh and RMSE to 1.4752 kWh (an 8.5% error reduction). "
        "The superior performance of Random Forest stems from its ability to model complex, multi-variate interactions—such as the compounding non-linear effect of high ambient "
        "temperature coupled with maximum household occupancy—which simple linear combinations cannot fully capture."
    )

    if os.path.exists("d:/GreenFuture/report_figures/fig_6_1_model_comparison.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("d:/GreenFuture/report_figures/fig_6_1_model_comparison.png", width=Inches(5.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_cap.add_run("Figure 6.1: Model performance comparison across regression metrics")
        r.font.bold = True
        r.font.size = Pt(10)

    doc.add_heading("6.3 Graphical Analysis", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "Figure 6.2 illustrates the Random Forest 9-step recursive autoregressive forecast generated in the admin panel. The forecast values smoothly transition "
        "between 2.51 kWh and 3.64 kWh, demonstrating stable, bounded trajectories consistent with diurnal energy patterns. "
        "Figure 6.3 displays the domestic energy consumption sequence alongside typical residential appliance shares: Air Conditioning accounts for 40% of energy use, "
        "Refrigeration 20%, Ceiling Fans 15%, Lighting 15%, and Entertainment/Television 10%."
    )

    if os.path.exists("d:/GreenFuture/report_figures/fig_6_2_rf_forecast.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("d:/GreenFuture/report_figures/fig_6_2_rf_forecast.png", width=Inches(5.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_cap.add_run("Figure 6.2: Random Forest multi-step recursive forecast sequence")
        r.font.bold = True
        r.font.size = Pt(10)

    if os.path.exists("d:/GreenFuture/report_figures/fig_6_3_analytics.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("d:/GreenFuture/report_figures/fig_6_3_analytics.png", width=Inches(5.6))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_cap.add_run("Figure 6.3: Analytics - energy consumption trend and appliance load share")
        r.font.bold = True
        r.font.size = Pt(10)

    doc.add_heading("6.4 Comparison with Existing Works", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "While direct numeric benchmarking against published building studies is constrained by varying physical datasets, qualitative alignment is strong. "
        "In agreement with Khalil et al. [1] and survey literature [4], occupancy and thermal parameters exert strong secondary modulation over baseline appliance load. "
        "Furthermore, by packaging the model into a responsive web application that couples energy prediction with tariff costs and carbon footprints, EcoWatt "
        "advances beyond purely theoretical literature models into practical consumer decision support."
    )

    doc.add_heading("6.5 Observations, Failures and Inferences", level=2)
    tbl_obs = doc.add_table(rows=7, cols=4)
    tbl_obs.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_obs.style = 'Table Grid'
    for i, h in enumerate(["Sl.", "Issue / Challenge Observed", "Root Cause", "Solution Applied & Architecture Evolution"]):
        c = tbl_obs.rows[0].cells[i]
        set_cell_background(c, "EAEAEA")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        set_cell_margins(c, 60, 60, 80, 80)

    obs_data = [
        ("1", "Colab/ngrok tunnel dropouts and port conflicts", "Fragile external tunnelling and ephemeral cloud runtime", "Re-engineered platform into client-side Vite/React app with in-browser ML execution."),
        ("2", "Potential negative predicted energy", "Linear residual model can mathematically produce negative offsets", "Enforced non-negative clipping: Ê = max(0, E_load + ŷ_res)."),
        ("3", "Unmodelled variance (MAPE ~29-31%)", "Synthetic Gaussian noise and physical stochastic load", "Formulated ensemble Random Forest model; planned future smart-meter sensor logging."),
        ("4", "Eco Score baseline dependency", "Score relied on arbitrary local sample max", "Standardized reference consumption to 95th percentile benchmark (E_ref)."),
        ("5", "Manual slider entry friction", "Users had to look up weather manually", "Integrated OpenWeatherMap REST API with 1-click slider auto-population."),
        ("6", "Security risk from exposed API credentials", "Prototype code hard-coded API tokens", "Secured tokens using environment variables, Vite client config, and fallback defaults."),
    ]
    for row_idx, r_item in enumerate(obs_data, start=1):
        for ci in range(4):
            c = tbl_obs.rows[row_idx].cells[ci]
            c.paragraphs[0].add_run(r_item[ci])
            set_cell_margins(c, 60, 60, 80, 80)

    doc.add_heading("6.6 Objectives vs. Outcomes", level=2)
    tbl_obj = doc.add_table(rows=6, cols=3)
    tbl_obj.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_obj.style = 'Table Grid'
    for i, h in enumerate(["Project Objective", "Outcome Achieved", "Status"]):
        c = tbl_obj.rows[0].cells[i]
        set_cell_background(c, "EAEAEA")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        set_cell_margins(c, 60, 60, 80, 80)

    obj_data = [
        ("Develop & compare SGD Log-Reg and Random Forest models", "Both models implemented; Random Forest superior (R² 0.6342 vs 0.5631)", "Achieved"),
        ("Evaluate models using MAE, MSE, RMSE, R², and MAPE", "All 5 regression metrics computed and benchmarked (Table 6.1)", "Achieved"),
        ("Estimate electricity tariff cost and carbon footprint", "Instant calculation of Cost (₹8.40/kWh) and CO₂ (0.716 kg/kWh) on every run", "Achieved"),
        ("Deploy an accessible, responsive web application", "Production single-page web app deployed using React 18, TypeScript, and Vite", "Achieved"),
        ("Validate against empirical residential smart-meter logs", "Benchmarked on 6,000-record physical dataset; hardware validation planned", "Partially Achieved"),
    ]
    for row_idx, r_item in enumerate(obj_data, start=1):
        for ci in range(3):
            c = tbl_obj.rows[row_idx].cells[ci]
            c.paragraphs[0].add_run(r_item[ci])
            set_cell_margins(c, 60, 60, 80, 80)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 7: CONCLUSION AND FUTURE SCOPE
    # ==========================================
    doc.add_heading("CHAPTER 7: CONCLUSION AND FUTURE SCOPE", level=1)

    doc.add_heading("7.1 Conclusion", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "The EcoWatt project successfully demonstrates the synergy of physics-informed machine learning and modern web technologies to promote domestic energy efficiency "
        "and climate awareness. By decomposing electrical energy into deterministic appliance wattage and learned environmental residuals, the platform achieves robust "
        "predictive performance while respecting physical thermodynamic principles. Evaluated on a 6,000-record benchmark dataset, the Random Forest Regressor demonstrated "
        "superior accuracy (R² = 0.6342, MAE = 1.1228 kWh) compared to the SGD Logarithmic Regression pipeline (R² = 0.5631, MAE = 1.2262 kWh).\n\n"
        "Crucially, the project advances beyond typical academic simulations by deploying a lightning-fast, production-grade web application built with React 18, TypeScript, "
        "and Vite. Integrating live weather telemetry via OpenWeatherMap, automated KSEB tariff calculation, CEA grid carbon auditing, and actionable energy reduction recommendations, "
        "EcoWatt provides consumers with a powerful tool to reduce domestic electricity bills while supporting UN Sustainable Development Goals 7 and 13."
    )

    doc.add_heading("7.2 Future Scope", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(
        "Several promising avenues exist to extend and enhance this work:\n"
        "1. IoT & Hardware Integration: Interfacing with low-cost smart plugs (e.g., ESP32 or Zigbee-based smart meters) to replace manual slider entry with real-time empirical power logging.\n"
        "2. Advanced Deep Learning Time-Series Models: Integrating Long Short-Term Memory (LSTM) networks or Temporal Fusion Transformers (TFT) for multi-horizon seasonal load forecasting.\n"
        "3. Dynamic Tariff & Grid Demand Response: Incorporating live time-of-day (ToD) tariff APIs to schedule heavy domestic loads (e.g., EV charging, washing machines) during off-peak solar hours.\n"
        "4. Mobile Progressive Web App (PWA): Packaging the web application as an offline-first PWA with push notifications alerting users during high grid emission periods."
    )

    doc.add_page_break()

    # ==========================================
    # REFERENCES
    # ==========================================
    doc.add_heading("REFERENCES", level=1)
    refs = [
        "[1] M. Khalil, S. McGough, Z. Pourmirza, M. Pazhoohesh, and S. Walker, “Machine learning, deep learning and statistical analysis for forecasting building energy consumption—A systematic review,” Engineering Applications of Artificial Intelligence, vol. 115, Art. no. 105287, 2022.",
        "[2] United Nations, “Sustainable Development Goals: Goal 7 — Affordable and Clean Energy.” [Online]. Available: https://sdgs.un.org/goals/goal7 (accessed: 15 Oct. 2026).",
        "[3] United Nations, “Sustainable Development Goals: Goal 13 — Climate Action.” [Online]. Available: https://sdgs.un.org/goals/goal13 (accessed: 15 Oct. 2026).",
        "[4] K. Amasyali and N. M. El-Gohary, “A review of machine learning approaches for building energy consumption prediction,” Journal of Building Engineering, vol. 17, pp. 209–225, 2021.",
        "[5] Y. Wang, Q. Chen, and M. Shahidehpour, “AI-empowered smart energy forecasting and demand-side management,” International Journal of Precision Engineering and Manufacturing – Green Technology, vol. 10, no. 3, pp. 581–598, 2023.",
        "[6] Department of Economics and Statistics, Government of Kerala, “Compendium of Project Reports 2024 – Cherukunnu Gramapanchayath Socio-Economic Survey 2021.” [Online]. Available: https://www.ecostat.kerala.gov.in/publication-detail/compendium-of-project-reports-2024 (accessed: 15 Oct. 2026).",
        "[7] L. M. Candanedo, V. Feldheim, and D. Deramaix, “Appliances Energy Prediction Data Set,” UCI Machine Learning Repository, 2017. [Online]. Available: https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction (accessed: 15 Oct. 2026).",
        "[8] G. Hébrail and A. Berard, “Individual Household Electric Power Consumption Data Set,” UCI Machine Learning Repository, 2012. [Online]. Available: https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption (accessed: 15 Oct. 2026).",
        "[9] F. Pedregosa et al., “Scikit-learn: Machine learning in Python,” Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.",
        "[10] L. Breiman, “Random forests,” Machine Learning, vol. 45, pp. 5–32, 2001.",
        "[11] Central Electricity Authority, “CO₂ Baseline Database for the Indian Power Sector,” Government of India. [Online]. Available: https://cea.nic.in/cdm-co2-baseline-database/ (accessed: 15 Oct. 2026).",
        "[12] G. James, D. Witten, T. Hastie, and R. Tibshirani, An Introduction to Statistical Learning: with Applications in Python. Springer, 2023.",
        "[13] React Documentation, “React – A JavaScript library for building user interfaces.” [Online]. Available: https://react.dev/ (accessed: 18 Oct. 2026).",
        "[14] OpenWeather, “Current weather data API,” OpenWeatherMap. [Online]. Available: https://openweathermap.org/api (accessed: 18 Oct. 2026)."
    ]
    for r_item in refs:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(6)
        p.add_run(r_item)

    doc.add_page_break()

    # ==========================================
    # APPENDICES
    # ==========================================
    doc.add_heading("APPENDIX A: SOURCE CODE", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "The complete source code is maintained on GitHub (Section 5.4). Below is the TypeScript implementation of the physics-informed "
        "machine learning engine (mlEngine.ts) executed in-browser by the EcoWatt / GreenFuture platform.\n"
    )
    p_code = doc.add_paragraph()
    p_code.paragraph_format.line_spacing = 1.1
    r = p_code.add_run(
        "// mlEngine.ts - Core In-Browser Machine Learning & Analytics Engine\n"
        "export interface DataRow {\n"
        "  Temperature: number; Time: number; Humidity: number; PowerRating: number;\n"
        "  UsageDuration: number; NumDevices: number; Occupancy: number;\n"
        "  EnergyConsumption: number; E_load: number; EnergyResidual: number;\n"
        "}\n\n"
        "export function generateSampleDataset(dataSize: number = 200): DataRow[] {\n"
        "  const rng = new SeededRandom(42);\n"
        "  const rows: DataRow[] = [];\n"
        "  for (let i = 0; i < dataSize; i++) {\n"
        "    const temp = rng.nextInt(20, 40), hour = rng.nextInt(0, 24);\n"
        "    const hum = rng.nextInt(40, 90), pwr = rng.nextInt(100, 2500);\n"
        "    const dur = Number(rng.nextUniform(0.5, 10).toFixed(2));\n"
        "    const dev = rng.nextInt(1, 10), occ = rng.nextInt(1, 6);\n"
        "    const eLoad = (pwr * dur * dev) / 1000.0;\n"
        "    const energy = eLoad + 0.3 * temp + 0.1 * hum + 0.5 * occ + rng.nextNormal(0, 2);\n"
        "    rows.push({\n"
        "      Temperature: temp, Time: hour, Humidity: hum, PowerRating: pwr,\n"
        "      UsageDuration: dur, NumDevices: dev, Occupancy: occ,\n"
        "      EnergyConsumption: Number(energy.toFixed(4)),\n"
        "      E_load: Number(eLoad.toFixed(4)),\n"
        "      EnergyResidual: Number((energy - eLoad).toFixed(4)),\n"
        "    });\n"
        "  }\n"
        "  return rows;\n"
        "}\n\n"
        "export function evaluatePredictions(yTrue: number[], yPred: number[], modelName: string) {\n"
        "  const n = yTrue.length;\n"
        "  let sumAE = 0, sumSE = 0, sumAPE = 0, sumY = 0;\n"
        "  for (let i = 0; i < n; i++) {\n"
        "    const yt = yTrue[i], yp = Math.max(0, yPred[i]), diff = yt - yp;\n"
        "    sumAE += Math.abs(diff); sumSE += diff * diff;\n"
        "    sumAPE += (Math.abs(diff) / Math.max(yt, 1e-8)) * 100; sumY += yt;\n"
        "  }\n"
        "  const meanY = sumY / n;\n"
        "  let totalSS = 0; for (let i = 0; i < n; i++) totalSS += (yTrue[i] - meanY) ** 2;\n"
        "  return {\n"
        "    Model: modelName,\n"
        "    MAE: Number((sumAE / n).toFixed(4)),\n"
        "    MSE: Number((sumSE / n).toFixed(4)),\n"
        "    RMSE: Number(Math.sqrt(sumSE / n).toFixed(4)),\n"
        "    R2: Number((totalSS > 0 ? 1 - sumSE / totalSS : 0).toFixed(4)),\n"
        "    MAPE: Number((sumAPE / n).toFixed(2))\n"
        "  };\n"
        "}"
    )
    r.font.name = 'Courier New'
    r.font.size = Pt(8.5)

    doc.add_page_break()

    # APPENDIX B: SCREENSHOTS
    doc.add_heading("APPENDIX B: SCREENSHOTS", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "The following screenshots and graphical outputs illustrate the user interface and analytics dashboards of the deployed EcoWatt web application:\n\n"
        "• Figure B.1: The modern landing hero page featuring ambient clean-energy design motifs, platform highlights, and dark/light mode toggle.\n"
        "• Figure B.2: The interactive prediction simulator showing live OpenWeatherMap weather conditions, parameter input sliders, predicted kilowatt-hours (46.82 kWh), electricity cost (₹393.26), carbon footprint (33.52 kg CO₂), Eco Score, and actionable savings alerts.\n"
        "• Figure B.3: The prediction history audit dashboard displaying logged runs, interactive bar/line trend visualizations, and 1-click CSV export.\n"
        "• Figure B.4: The analytics module displaying 20-record historical energy trends from EcoWatt_6000.csv and the typical residential appliance load distribution."
    )

    doc.add_page_break()

    # APPENDIX C: SDG MAPPING
    doc.add_heading("APPENDIX C: MAPPING WITH SUSTAINABLE DEVELOPMENT GOALS", level=1)
    tbl_sdg = doc.add_table(rows=4, cols=3)
    tbl_sdg.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sdg.style = 'Table Grid'
    for i, h in enumerate(["Sl No", "SDG Addressed & Target", "How it is Demonstrated in this Project"]):
        c = tbl_sdg.rows[0].cells[i]
        set_cell_background(c, "EAEAEA")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        set_cell_margins(c, 60, 60, 80, 80)

    sdg_data = [
        ("1", "SDG 7 – Affordable and Clean Energy (Target 7.3: Double global rate of energy efficiency improvements)", 
         "EcoWatt accurately predicts domestic appliance power demands, quantifies electricity costs under KSEB tariff slabs, and identifies peak grid hours to empower consumers to reduce overall kilowatt-hour consumption and eliminate wasteful idle power."),
        ("2", "SDG 13 – Climate Action (Target 13.3: Build knowledge and capacity to meet climate change)", 
         "The application converts every predicted energy usage scenario into an immediate carbon dioxide footprint (0.716 kg CO₂/kWh) and an intuitive Eco Score, directly cultivating environmental accountability in everyday residential decisions."),
        ("3", "SDG 11 – Sustainable Cities and Communities (Target 11.6: Reduce adverse environmental impact of cities)", 
         "By facilitating residential demand-side management and peak load shifting away from stressed evening hours (6 PM - 9 PM), the platform reduces peak fossil-fuel peaker plant activation across urban electrical grids."),
    ]
    for row_idx, r_item in enumerate(sdg_data, start=1):
        for ci in range(3):
            c = tbl_sdg.rows[row_idx].cells[ci]
            c.paragraphs[0].add_run(r_item[ci])
            set_cell_margins(c, 60, 60, 80, 80)

    doc.add_page_break()

    # APPENDIX D: INDIVIDUAL CONTRIBUTION
    doc.add_heading("APPENDIX D: INDIVIDUAL CONTRIBUTION OF TEAM MEMBERS", level=1)
    tbl_con = doc.add_table(rows=6, cols=4)
    tbl_con.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_con.style = 'Table Grid'
    for i, h in enumerate(["Sl.", "Name & Register No.", "Modules / Tasks Handled", "Contribution (%)"]):
        c = tbl_con.rows[0].cells[i]
        set_cell_background(c, "EAEAEA")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(h).bold = True
        set_cell_margins(c, 60, 60, 80, 80)

    con_data = [
        ("1", "Aaliya Fathima Arif ([Register No.])", "Literature survey, dataset attribute analysis & Cherukunnu survey documentation", "20%"),
        ("2", "Afrah Zulfi ([Register No.])", "Dataset preprocessing, feature scaling, log1p transformation & metric calculation", "20%"),
        ("3", "Muhammed Aasif ([Register No.])", "OpenWeatherMap API integration, live weather telemetry & UI parameter auto-population", "20%"),
        ("4", "Sanju Philip Saji ([Register No.])", "Random Forest lag matrix formulation, recursive multi-step forecasting & testing", "20%"),
        ("5", "S. Vighnesh (Team Leader) ([Register No.])", "System architecture, TypeScript ML engine, React web application & project coordination", "20%"),
    ]
    for row_idx, r_item in enumerate(con_data, start=1):
        for ci in range(4):
            c = tbl_con.rows[row_idx].cells[ci]
            p = c.paragraphs[0]
            if ci in [0, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run(r_item[ci])
            set_cell_margins(c, 60, 60, 80, 80)

    # Save to both target locations
    path1 = "d:/GreenFuture/EcoWatt_Project_Report.docx"
    path2 = "C:/Users/svigh/Downloads/EcoWatt_Project_Report.docx"
    doc.save(path1)
    doc.save(path2)
    print(f"Report successfully saved to:\n  1. {path1}\n  2. {path2}")

if __name__ == '__main__':
    create_report()
