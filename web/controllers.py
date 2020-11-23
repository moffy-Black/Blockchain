import responder
import os
from uuid import uuid4

from blockchain import Blockchain

node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

api = responder.API(
  templates_dir='templates',
  static_dir='static',
  static_route='/static',
  secret_key=os.urandom(24)
)

class TransactionController:
  async def on_post(self, req, resp):
    data = await req.media()
    required = ['sender', 'recipient', 'amount']
    if not all(data.get('{}'.format(key)) for key in required):
      resp.status_code = 400
    index = blockchain.new_transaction(data.get('sender'),data.get('recipient'),data.get('amount'))
    response = {'message':f'トランザクションはブロック{index}に追加されました'}
    resp.media = response
    
class MineController:
  async def on_get(self, req, resp):
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
      sender="0",
      recipient=node_identifier,
      amount=1
    )

    block = blockchain.new_block(proof)

    response = {
      'message': '新しいブロックを採掘しました',
      'index': block['index'],
      'transactions': block['transactions'],
      'proof': block['proof'],
      'previous_hash': block['previous_hash']
    }
    resp.media = response

class ChainController:
  async def on_get(self, req, resp):
    response = {
      'chain': blockchain.chain,
      'length': len(blockchain.chain),
    }
    resp.media = response

class RegisterController:
  async def on_post(self, req, resp):
    data = await req.media()
    nodes = data.get('nodes')
    if nodes is None:
      resp.status_code = 400
    
    for node in nodes:
      blockchain.register_node(node)
    
    response = {
      'message': '新しいノードが追加されました',
      'total_nodes': list(blockchain.nodes),
    }
    resp.media = response

class ResolveController:
  async def on_get(self, req, resp):
    replaced = blockchain.resolve_conflicts() #error

    if replaced:
      response = {
        'message': 'チェーンが置き換えられました',
        'new_chain': blockchain.chain
      }
    
    else:
      response = {
        'message': 'チェーンが確認されました',
        'new_chain': blockchain.chain
      }

    resp.media = response