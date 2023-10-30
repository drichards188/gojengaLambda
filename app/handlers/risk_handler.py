import json
from array import array

import numpy as np
import pandas as pd


# todo could these functions be non static?
class RiskHandler:
    @staticmethod
    def get_json(filepath: str) -> list:
        try:
            with open(filepath) as f:
                data = json.load(f)
            return data

        except Exception as e:
            print(f'error: {e}')

    @staticmethod
    def calculate_week_difference(week_data):
        difference = float(week_data["4. close"]) - float(week_data["1. open"])
        rounded_difference = round(difference, 2)
        print(f'--> difference is: {rounded_difference}')
        return rounded_difference

    @staticmethod
    def handle_get_sharpe_ratio(security_symbol: str) -> float:
        jsonData: list = RiskHandler.get_json('/home/drich/financedata/alphavantageIBM.json')

        day_difference_by_week: array[float] = []
        risk_free_rate: array[float] = []

        data_by_week = jsonData["Weekly Time Series"]
        for week in data_by_week:
            print(data_by_week[week])
            difference = RiskHandler.calculate_week_difference(data_by_week[week])
            day_difference_by_week.append(difference)

        for day in day_difference_by_week:
            risk_free_rate.append(0.001)

        df = pd.DataFrame({
            'portfolio': day_difference_by_week,
            'risk_free': risk_free_rate
        })

        # Calculate excess returns
        df['excess_return'] = df['portfolio'] - df['risk_free']

        # Calculate the Sharpe Ratio
        sharpe_ratio = np.mean(df['excess_return']) / np.std(df['excess_return'])

        # Annualize the Sharpe Ratio
        annual_factor = np.sqrt(252)  # Use 252 for daily returns, 52 for weekly returns, 12 for monthly returns
        sharpe_ratio_annualized = sharpe_ratio * annual_factor

        print('Sharpe Ratio (Annualized):', sharpe_ratio_annualized)
        return sharpe_ratio_annualized

    @staticmethod
    def evaluate_sharpe_ratio(ratio: float) -> object:
        result = ""

        if ratio >= 2.99:
            result = "Excellent"
        elif ratio >= 2.00:
            result = "Very good"
        elif ratio >= 1.99:
            result = "Good"
        elif ratio >= 1.00:
            result = "Adequate"
        elif ratio < 1:
            result = "Bad"
        else:
            result = "eval error"

        print('result of sharpe eval {result}')
        return {"ratio": ratio, "eval": result}
