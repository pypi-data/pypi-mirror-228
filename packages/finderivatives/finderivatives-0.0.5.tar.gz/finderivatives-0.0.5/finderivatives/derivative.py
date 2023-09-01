"""

pendiente:
    incluir validaciones
    ajustar put
    

"""

from finderivatives import validations as val

#%%
class EuropeanOption():
    
    def __init__(self, strike, maturity, position, premium=0):
        self._strike = val.validate_strike(strike)
        self._maturity = val.validate_maturity(maturity)
        self._dt = val.validate_maturity(maturity)
        self._position = val.validate_position(position)
        self._premium = val.validate_premium(premium)
        # self._flows = {}
    
    
    def __str__(self):
        return 'xxxxx'
    
    
    def __add__(self, other):
        payoff = self.payoff() + other.payoff()
        profit = self.profit() + other.profit()
        pricing_bs = self.pricing_bs() + other.pricing_bs()
        addition = {
            'payoff': payoff,
            'profit': profit,
            'pricing_bs': pricing_bs
            }
        return addition
    
    
    def get_strike(self):
        return self._strike
    
    
    def get_maturity(self):
        return self._maturity
    
    
    def get_position(self):
        return self._position
    
    
    def set_spot(self, spot):
        self._spot = val.validate_spot(spot)
    
    
    def set_volatility(self, vol):
        self._vol = vol
    
    
    def set_r(self, r):
        self._r = r
    
    
    def set_market_inputs(self, spot, vol, r):
        self.set_spot(spot)
        self.set_volatility(vol)
        self.set_r(r)
    


#%% Ejecucion directa
if __name__ == '__main__':
    print(' Ejecucion directa ... \n')
    
    # strike = 105
    # maturity = 2
    # position = 1
    # spot = 102
    # spots = list(range(90, 110, 1))
    # # spots = np.arange(strike*0.8, strike*1.2, strike*0.01)
    # premium = 3
    # vol = 0.05
    # r = 0.01
    # dt = 2
    
    
    # # call = Call(strike=strike, maturity=maturity, position=position,
    #             # premium=premium)
    # call = Put(strike=strike, maturity=maturity, position=position,
    #           premium=premium)
    
    # call.set_spot(spot)
    # call_payoff1 = call.payoff()
    # print('payoff:', call_payoff1)
    
    # call.set_spot(np.array(spot))
    # call_payoff2 = call.payoff()
    # print('payoff:', call_payoff2)
    
    # call.set_spot(spots)
    # call_payoff3 = call.payoff()
    # print('payoffs:', call_payoff3)
    
    # call.set_spot(spot)
    # call_profit1 = call.profit()
    # print('profit:', call_profit1)
    
    # call.set_spot(np.array(spot))
    # call_profit2 = call.profit()
    # print('profits:', call_profit2)
    
    # call.set_spot(spots)
    # call_profit3 = call.profit()
    # print('profits:', call_profit3)

    # call.set_market_inputs(spot, vol, r)
    # call_pricing1 = call.pricing_bs()
    # print('pricing:', call_pricing1)
    
    # call.set_market_inputs(np.array(spot), vol, r)
    # call_pricing2 = call.pricing_bs()
    # print('pricings:', call_pricing2)
    
    # call.set_market_inputs(spots, vol, r)
    # call_pricing3 = call.pricing_bs()
    # print('pricings:', call_pricing3)
    
    
    
    # import matplotlib.pyplot as plt
    
    # fig, ax = plt.subplots()
    # ax.plot(spots, call_payoff3)
    # ax.plot(spots, call_pricing3)
    # plt.show()
    
    # fig, ax = plt.subplots()
    # ax.plot(spots, put.pricing_bs(spot=spots, vol=vol, r=r, dt=dt))
    # ax.plot(spots, put.payoff(spot=spots))
    # plt.show()
    
    
    # s = np.array([96, 98, 100, 102, 104])
    # print('pricing:', call.payoff(spot=s))


