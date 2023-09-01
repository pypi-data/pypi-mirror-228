

# import pandas as pd
# import math as mt
# import numpy as np
# import random as rd
# from scipy.stats import norm


# #%%
# class EuropeanOption():
    
#     def __init__(self, strike, maturity, position):
#         self._strike = strike
#         self._maturity = maturity
#         self._position = position
#         # self._flows = {}
        
#     def get_strike(self):
#         return self._strike
    
#     def get_maturity(self):
#         return self._maturity
    
#     def get_position(self):
#             return self._position


# #%% Call
# class Call(EuropeanOption):
    
#     def __init__(self, strike, maturity, position):
#         super().__init__(strike, maturity, position)
    
    
#     def payoff(self, spot):
#         self._spot = spot
#         self._payoff = max([0, self._spot - self._strike]) * self._position
#         return self._payoff
    
    
#     def profit(self, spot, premium):
#         self._spot = spot
#         self._profit = self.payoff(self._spot) - premium * self._position  
#         return self._profit
        
    
#     def pricing_bs(self, spot, vol, r, dt):
#         self._spot = spot
#         self._vol = vol
#         self._r = r
#         self._dt = dt
#         # Probabilities
#         self._d1 = (mt.log(spot/self._strike) + (r - (vol**2)/2) / dt) \
#             / (vol * mt.sqrt(dt))
#         self._d2 = self._d1 - vol * mt.sqrt(dt)
#         self._n_d1 = norm.cdf(self._d1)
#         self._n_d2 = norm.cdf(self._d2)
#         # Pricing
#         self._pricing = (
#             self._spot * self._n_d1\
#             - self._strike * np.exp(-self._r*(self._dt)) * self._n_d2
#             ) * self._position
#         return self._pricing
    


# #%%  Put
# class Put(EuropeanOption):
    
#     def __init__(self, strike, maturity, position):
#         super().__init__(strike, maturity, position)
        
    
#     def payoff(self, spot):
#         self._spot = spot
#         self._payoff = max([0, self._strike - self._spot]) * self._position
#         return self._payoff
    
    
#     def profit(self, spot, premium):
#         self._spot = spot
#         self._profit = self.payoff(self._spot) - premium * self._position  
#         return self._profit
        
    
#     def pricing_bs(self, spot, vol, r, dt):
#         self._spot = spot
#         self._vol = vol
#         self._r = r
#         self._dt = dt
#         # Probabilities
#         self._d1 = (mt.log(spot/self._strike) + (r - (vol**2)/2) / dt) \
#             / (vol * mt.sqrt(dt))
#         self._d2 = self._d1 - vol * mt.sqrt(dt)
#         self._n_d1 = norm.cdf(-self._d1)
#         self._n_d2 = norm.cdf(-self._d2)
#         # Pricing
#         self._pricing = (
#             self._strike * np.exp(-self._r*(self._dt)) * self._n_d2
#             - self._spot * self._n_d1
#             ) * self._position
#         return self._pricing

    
# # # browniano
# # mu = 0.05
# # sigma = 0.02
# # s_0 = 100
# # dt = 1/12
# # s_1 = s_0 * mt.exp((mu - (sigma**2)*0.5)*dt \
# #                    + sigma * mt.sqrt(dt) * rd.normalvariate(0,1))

# # print(s_1)





# if __name__ == '__main__':
#     print(' Ejecucion directa ... \n')
    
#     call = Call(strike=100, maturity=2, position=1)
#     print('strike:', call.get_strike())
    
#     print('payoff:', )

#     print('profit:', call.profit(spot=102, premium=4))

#     print('pricing:', call.pricing_bs(spot=102, vol=0.04, r=0.01, dt=2))
    
#     # s = np.array([96, 98, 100, 102, 104])
#     # print('pricing:', call.payoff(spot=s))



# strike = 100
# position = 1
# spot = np.array([96, 98, 100, 102, 104])
# zero = 0
# payoff = np.maximum([spot - strike], zero) * position
# payoff



# spots = [96, 98, 100, 102, 104]
# spots = list(range(80, 120, 1))

# call = Call(strike=100, maturity=2, position=1)
# put = Put(strike=100, maturity=2, position=-1)

# payoffs_call = [call.payoff(spot=s) for s in spots]
# pricings_call = [call.pricing_bs(spot=s, vol=0.02, r=0.01, dt=2) for s in spots]

# payoffs_put = [put.payoff(spot=s) for s in spots]
# pricings_put = [put.pricing_bs(spot=s, vol=0.02, r=0.01, dt=2) for s in spots]


# import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# ax.plot(spots, pricings_call)
# ax.plot(spots, payoffs_call)
# plt.show()


# fig, ax = plt.subplots()
# ax.plot(spots, pricings_put)
# ax.plot(spots, payoffs_put)
# plt.show()




