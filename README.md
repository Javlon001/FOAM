# Welcome to FOAM course Project! 
---
## Introduction 
Risk and Return! These are two major matrics every investor takes into consideration while constructing portfolio. In his [reasearch paper](https://www.jstor.org/stable/2975974?searchText=Harry%20Markowitz&searchUri=%2Faction%2FdoBasicSearch%3FQuery%3DHarry%2BMarkowitz%26so%3Drel&ab_segments=0%2Fbasic_search_gsv2%2Fcontrol&refreqid=fastly-default%3A6622b8ea95d00892c67808b22c753aff) published in 1952, Harry Markowizt was first to introduce Mean-Variance Model. In this model, risk and return, efficient frontier and diversification factors are used to construct optimal portfolio for investor's specific needs. By "investor's specific needs", I mean if the investor is risk averse he tends to fix the risk to some level and tries to increase the expected return, whereas the other way around is also possible, decreasing the risk for fixed expected return. This is done by identifying efficient frontier of portfolio that offers best return for a given level of risk. The optimal portfolio is therefore found where the investor's risk tolerance aligns with the efficient frontier, balancing risk and return. 

---
## Data and Methodology
This project aims to implement the Mean-Variance model to construct optimal portfolio from 20 assets given in the data. The [DATA](./data/data.xlsx) is firstly processed (cleaned and changed to efficiently work with), the ticker names were given in seperate workbook, while the data frame has headers ranging from A1 to A20 which have been switched with tickers during data cleaning.   

---
## Results

In this project we conducted multiple portfolio construction with different constraints imposed, in the first one when we chose maximum return regardless of level of risk, the model chose ENI SPA, with Expected Return = $0.0335$ but the Portfolio Variance was as high as 0.005. Thereafter, we tried to minimiz the return, if the Portfolio Variance, Risk, would go down. Result was to invest into FINMECCANICA SPA, that would yield the expected return of $-0.009$ but the variance was also exactly 0.005. Getting the balance between risk and return resulted in three more portfolios with diversified 8 assets in the first two and 6 in the last. When we fixed the expected return to $0.01$ ($\mu_3$) the portfolio variance was the smallest, with $0.0005$.   

After having imposed the upper bound $k=2$ for each $\mu$, the model found 5 optimal portfolios of 2 assets in three of them and 1 asset in 2 of them. In $\mu_1$ and $\mu_5$, the portfolio consisted only a single asset because the return was fixed even though $k=2$ is introduced, it cannot impact much. The assets selected in each $\mu$ and their corresponding portfolio variance are as follows: 
- **$\mu_1$**: FNC (Portfolio Variance: 0.0053)
- **$\mu_2$**: BUL, ENEL (Portfolio Variance: 0.0013)
- **$\mu_3$**: AL, F (Portfolio Variance: 0.0011)
- **$\mu_4$**: ENI, ES (Portfolio Variance: 0.0015)
- **$\mu_5$**: ENI (Portfolio Variance: 0.0044)

