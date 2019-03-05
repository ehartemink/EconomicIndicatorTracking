import quandl
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


def updateEconomicIndicators():

    quandl.ApiConfig.api_key = "oJxW82c76pxy-EjeGGNU"


    CAPE = quandl.get("MULTPL/SHILLER_PE_RATIO_MONTH")
    CCC = quandl.get("ML/CCCY")
    AAA = quandl.get("ML/AAAEY")
    TREASURY = quandl.get("USTREASURY/YIELD")

    df = pd.DataFrame(index = CAPE.index.values, data = CAPE[list(CAPE.columns)[0]].values, columns = ["CAPE Ratio"])

    def insert_first_col(df, insertion_df, column_name):
        insertion = insertion_df.loc[df.index.values,list(insertion_df.columns)[0]].values
        df.insert(loc = df.shape[1], value = insertion, column = column_name)
    insert_first_col(df, CCC, "CCC Bond Yield")
    insert_first_col(df, AAA, "AAA Bond Yield")
    df.insert(loc = df.shape[1], value = TREASURY.loc[df.index.values, "1 YR"], column = "1 Yr Yield")
    df.insert(loc = df.shape[1], value = TREASURY.loc[df.index.values, "10 YR"], column = "10 Yr Yield")
    df = df.dropna(0)

    df.insert(loc = df.shape[1], value = df["10 Yr Yield"] - df["1 Yr Yield"], column = "1Y-10Y Premium")
    df.insert(loc = df.shape[1], value = df["CCC Bond Yield"] - df["AAA Bond Yield"], column= "CCC-AAA Premium")

    df.to_csv("EconomicIndicators.csv")

    alpha = 0.2

    for column in ["CAPE Ratio", "CCC-AAA Premium", "1Y-10Y Premium"]:
        plt.figure(figsize = (20, 12), dpi = 80)
        plt.ylabel(column)
        plt.xlabel("Date")
        plt.plot(df[column])
        plt.axvspan(xmin = df.index.values[0], xmax = "2000-03-01", facecolor = 'g', alpha = alpha)
        plt.axvspan(xmin = "2000-03-01", xmax = "2002-07-01", facecolor = 'r', alpha = alpha)
        plt.axvspan(xmin = "2002-07-01", xmax = "2007-12-01", facecolor = 'g', alpha = alpha)
        plt.axvspan(xmin = "2007-12-01", xmax = "2009-03-01", facecolor = 'r', alpha = alpha)
        plt.axvspan(xmin = "2009-03-01", xmax = df.index.values[-1], facecolor = 'g', alpha = alpha)
        plt.savefig(column.replace(' ', '').replace('-', '') + '.png')


if __name__ == '__main__':
    updateEconomicIndicators()


