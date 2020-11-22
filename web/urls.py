from controllers import api, TransactionController, MineController, ChainController

api.add_route('/transactions/new', TransactionController)
api.add_route('/mine', MineController)
api.add_route('/chain', ChainController)