# Project_Python_Git_Linux_Robinson_Paul

## Project Overview

We developed a professional interactive dashboard designed for an asset management context.  
The application retrieves financial market data, applies quantitative analysis, and displays results in a clear and user-friendly way.

## Project Structure

The dashboard is composed of two main modules:

### Quant A – Single Asset Analysis
- Analysis of one asset at a time  
- Historical price visualization  
- Strategy backtesting (e.g. buy & hold, momentum)  
- Performance metrics:
  - Sharpe Ratio  
  - Volatility  
  - Maximum Drawdown  
- Interactive controls for strategy parameters  
- Main chart showing:
  - Raw asset price  
  - Cumulative strategy performance  

---

### Quant B – Multi-Asset Portfolio Analysis
- Portfolio construction using at least 3 CAC 40 assets  
- Portfolio simulation:
  - Equal-weight allocation  
  - Custom weights  
- Portfolio performance visualization (base 100)  
- Correlation matrix between assets  
- Diversification analysis  
- Portfolio metrics:
  - Annualized return  
  - Volatility  
  - Sharpe Ratio  
  - Maximum Drawdown  
- Visual comparison between individual assets and the portfolio  

---

## Technologies Used

- Python  
- Streamlit  
- Pandas  
- NumPy  
- Matplotlib  
- Seaborn  
- yFinance  
- Git & GitHub  
- Linux
- AWS EC2  
- Nginx 

---

## Deployment & Infrastructure

### Linux Virtual Machine

The application is deployed on a Linux virtual machine hosted on AWS EC2

- OS: Ubuntu  
- Cloud provider: AWS  
- Instance type: t3.micro  
- Public IPv4 enabled  
- SSH access using key-based authentication  

This setup ensures the application runs independently from local machines and can be accessed externally.

---

## ACCESS

The application is publicly accessible at : http://56.228.42.115

---
