


#%%
class Portfolio():
    
    def __init__(self, *derivatives):
        self._derivatives = derivatives
    
    
    def __str__(self):
        return 'xxxxx'
    
    
    def __add__(self, other):
        addition = Portfolio(*self.get_derivatives(), *other.get_derivatives())
        return addition
    
    
    def get_derivatives(self):

        return self._derivatives


    def payoff(self):
        self._payoff = 0
        for derivative in self._derivatives:
            self._payoff += derivative.payoff()
        
        return self._payoff
    
    
    def profit(self):
        self._profit = 0
        for derivative in self._derivatives:
            self._profit += derivative.profit()
        
        return self._profit
    
    
    def pricing_bs(self):
        self._pricing = 0
        for derivative in self._derivatives:
            self._pricing += derivative.pricing_bs()
        
        return self._pricing



#%% Ejecucion directa
if __name__ == '__main__':
    print(' Ejecucion directa ... \n')
    
    from finderivatives import Call, Put
    import numpy as np
    import matplotlib.pyplot as plt
    
    call1 = Call(strike=100, maturity=2, position=1)
    call2 = Call(strike=110, maturity=2, position=1)
    put1 = Put(strike=100, maturity=2, position=1)
    put2 = Put(strike=105, maturity=2, position=-1)
    
    spots = np.arange(80, 120, 1)
    # spots = 102
    
    call1.set_market_inputs(spot=spots, vol=0.06, r=0.01)
    call2.set_market_inputs(spot=spots, vol=0.06, r=0.01)
    put1.set_market_inputs(spot=spots, vol=0.06, r=0.01)
    put2.set_market_inputs(spot=spots, vol=0.06, r=0.01)
    
    port = Portfolio(call1, put1, call2)
    
    payoff_call1 = call1.payoff()
    payoff_call2 = call2.payoff()
    payoff_put1 = put1.payoff()
    
    payoff_port = port.payoff()
    profit_port = port.profit()
    pricing_bs_port = port.pricing_bs()
    
    
    
    
    # print(payoff_call1[39])
    # print(payoff_put1[39])
    # print(payoff_port[39])
    
    
    # fig, ax = plt.subplots()
    # ax.plot(spots, payoff_call1, '--')
    # ax.plot(spots, payoff_call2, '--')
    # ax.plot(spots, payoff_put1, '--')
    # ax.plot(spots, payoff_port, 'o')
    # plt.show()    
    
    
    
    # derivatives = port.get_derivatives()
    # print(derivatives)
    
    
    #### Portfolio 1
    port1 = Portfolio(call1, put1)
    ### Portfolio 2
    port2 = Portfolio(call2, put2)
    #### Portfolio 3
    port3 = port1 + port2
    
    port3.payoff()


    fig, ax = plt.subplots()
    ax.plot(spots, call1.payoff(), '--')
    ax.plot(spots, call2.payoff(), '--')
    ax.plot(spots, put1.payoff(), '--')
    ax.plot(spots, put2.payoff(), '--')
    ax.plot(spots, payoff_port, 'o')
    plt.show()
    

# iter(port1.get_derivatives())



    