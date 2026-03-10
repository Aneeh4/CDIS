Corporate Document Intelligent System (CDIS)
Overview

The Corporate Document Intelligent System (CDIS) is an AI-powered platform that automates the extraction and analysis of corporate information from financial disclosures and news sources. It converts unstructured corporate documents into structured data for analytics, benchmarking, and predictive modeling.

The system combines web scraping, natural language processing (NLP), machine learning, and ETL pipelines to provide insights into both financial performance and corporate activities.

Features

Automated Data Collection
Scrapes earnings reports, press releases, and corporate news from public sources.
<img width="492" height="746" alt="CDIS_4" src="https://github.com/user-attachments/assets/2c4f9494-5cdb-40e7-a5c3-118ad25ea49a" />

Financial KPI Extraction
Extracts metrics such as Revenue, EPS, EBITDA, margins, and guidance values.
<img width="870" height="417" alt="CDIS_1" src="https://github.com/user-attachments/assets/6fbdb27e-091c-43c8-8a86-121e7b2ce3f9" />
<img width="586" height="278" alt="CDIS_5" src="https://github.com/user-attachments/assets/7929b942-dba2-4857-b5f4-e0187b2206ae" />
<img width="602" height="337" alt="CDIS_6" src="https://github.com/user-attachments/assets/97c9c4ca-586f-4aff-85d4-5840a3d26ec0" />

News Intelligence
Collects and summarizes corporate events such as product launches, HR changes, and operational updates.
<img width="803" height="393" alt="CDIS_3" src="https://github.com/user-attachments/assets/d8ee328b-420e-4f7a-82a5-b665180449df" />

Hybrid Extraction Pipeline
Combines regex rules, fuzzy matching, and LLM-based semantic extraction.

Structured Data Storage
Stores financial metrics and event insights in a relational MySQL database.

Predictive Analytics
Forecasts financial metrics using time-series models such as ARIMA, Prophet, and LSTM.

Visualization
Provides dashboards and analytics through Python visualizations and Power BI.
<img width="837" height="322" alt="CDIS_2" src="https://github.com/user-attachments/assets/8503422a-a44a-4051-81cb-f2f133f294f7" />

System Workflow
Data Sources

   ↓
   
 
Web Scraping

   ↓
   
Document Processing (PDF/OCR)

   ↓
   
Information Extraction (Regex + NLP + LLM)

   ↓
   
Structured Database (MySQL)

   ↓
   
Analytics & Visualization

