
# import Parche
# Parche.main()

# import finderivatives as der
# import numpy as np
# import matplotlib.pyplot as plt

# call1 = der.Call(strike=100, maturity=2, position=1, premium=2)
# call2 = der.Call(strike=101, maturity=2, position=1, premium=2)
# put1 = der.Put(strike=100, maturity=2, position=1, premium=2)

# spots = np.arange(80, 120, 1)
# call1.set_market_inputs(spot=spots, vol=0.06, r=0.01)
# call2.set_market_inputs(spot=spots, vol=0.06, r=0.01)
# put1.set_market_inputs(spot=spots, vol=0.06, r=0.01)


# #### Portfolio 1
# port1 = call1 + call2

# #### Plot
# # fig, ax = plt.subplots()
# # ax.plot(spots, call1.payoff())
# # ax.plot(spots, call2.payoff())
# # ax.plot(spots, port1['payoff'])
# # plt.show()


# #### Portfolio 2
# port2 = call1 + put1

# #### Plot
# fig, ax = plt.subplots()
# ax.plot(spots, call1.payoff())
# ax.plot(spots, put1.payoff())
# ax.plot(spots, port2['pricing_bs'])
# plt.show()


