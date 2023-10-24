import numpy as np
import pandas as pd


class RiskHandler:

    @staticmethod
    def handle_get_sharpe_ratio(security_symbol: str):
        df = pd.DataFrame({
            'portfolio': [0.01, 0.02, -0.01, -0.02, 0.01, 0.02, -0.01, -0.02, 0.01, 0.02],
            'risk_free': [0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001]
        })

        # Calculate excess returns
        df['excess_return'] = df['portfolio'] - df['risk_free']

        # Calculate the Sharpe Ratio
        sharpe_ratio = np.mean(df['excess_return']) / np.std(df['excess_return'])

        # Annualize the Sharpe Ratio
        annual_factor = np.sqrt(252)  # Use 252 for daily returns, 52 for weekly returns, 12 for monthly returns
        sharpe_ratio_annualized = sharpe_ratio * annual_factor

        print('Sharpe Ratio (Annualized):', sharpe_ratio_annualized)
        return {"ratio": sharpe_ratio_annualized}
