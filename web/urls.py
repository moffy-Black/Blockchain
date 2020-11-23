from controllers import api, TransactionController, MineController, ChainController, RegisterController, ResolveController

api.add_route('/transactions/new', TransactionController)
api.add_route('/mine', MineController)
api.add_route('/chain', ChainController)
api.add_route('/nodes/register', RegisterController)
api.add_route('/nodes/resolve', ResolveController)