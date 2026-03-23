FLAGR-AI

FLAGR-AI is an evolving backend system designed to build intelligent financial analysis tools and automated fraud-risk evaluation pipelines.

The project focuses on constructing reliable data ingestion, normalization, and scoring workflows over publicly available corporate financial statements.

Current Capabilities
Resolve official company names and common aliases to NSE ticker symbols
Ingest multi-period financial statements using yfinance
Normalize and clean inconsistent financial data structures across companies
Compute Beneish M-Score based fraud-risk signals
Persist structured financial datasets for downstream analytics
Symbol-based storage pipeline to ensure consistent multi-company processing
FastAPI-driven modular endpoints for data ingestion and fraud scoring
Early support for Nifty-universe batch evaluation workflows

Tech Stack
Python
FastAPI
Pandas
yfinance
SQLAlchemy (planned persistence layer)

Future Work
Beneish M-Score integration
ML-based fraud prediction models
Financial statement upload parsing
Risk scoring dashboards