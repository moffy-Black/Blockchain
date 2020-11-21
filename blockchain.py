# coding: UTF-8

import hashlib
import json
from time import time

class Blockchain(object):
  def __init__(self):
    #コンストラクタ
    self.chain = [] 
    self.current_transactions = []

    #ジェネシスブロック(一番初めのブロック)の生成。
    self.new_block(previous_hash=1, proof=100)

  def new_block(self, proof, previous_hash=None):

    # """
    # ブロックチェーンに新しいブロックを作る関数
    # :param proof: <int> プルーフ・オブ・ワークアルゴリズム(新しいブロックを作成するときのアルゴリズム)から得られるプルーフ
    # :param previous_hash: (オプション) <str> 前のブロックのハッシュ
    # :return: <dict> 新しいブロック
    # """

    block = {
      'index': len(self.chain) + 1, #Blockの番号
      'timestamp': time(), #作成された時間(UNIX)
      'transactions': self.current_transactions, #トランザクション(ここでは取引情報)
      'proof': proof, #Blockが正しいことを示す、証明番号
      'previous_hash': previous_hash or self.hash(self.chain[-1]), #前のBlockのハッシュ
    }

    self.current_transactions = [] #現在のトランザクションリストをリセット
    self.chain.append(block)
    return block

  def new_transaction(self, sender, recipient, amount):

    # """
    # 次に採掘されるブロックに加える、新しいトランザクションを作る関数
    # :param sender: <str> 送信者のアドレス
    # :param recipient: <str> 受信者のアドレス
    # :param amount: <int> (仮想通貨)量
    # :return: <int> このトランザクションを含むブロックのアドレス
    # """

    self.current_transactions.append({
      'sender': sender,
      'recipient': recipient,
      'amount': amount,
    })
    
    return self.last_block['index'] + 1

  @property
  def last_block(self):
    #チェーンの最後のブロックをリターンする関数
    return self.chain[-1]

  @staticmethod
  def hash(block):
    
    # """
    # ブロックのSHA-256ハッシュ(Blockchain用暗号学的ハッシュ関数)を作る関数
    # :param block: <dict> ブロック
    # :return: <str>
    # """

    # 必ずディクショナリ（辞書型のオブジェクト）がソートされている必要がある。そうでないと、一貫性のないハッシュとなってしまう
    # 暗号化する情報が同じでも、順序が違うと違うハッシュ値が生成されるため。
    block_string = json.dumps(block, sort_keys=True).encode() #ソートしてる
    return hashlib.sha256(block_string).hexdigest() #SHA-256ハッシュ化した情報をリターン

  def proof_of_work(self, last_proof):

    # """
    # シンプルなプルーフ・オブ・ワークのアルゴリズム:
    #   - hash(last_proof,proof) の最初の4つが0となるような p' を探す
    #   - last_proof は1つ前のブロックのプルーフ、 proof は新しいブロックのプルーフ
    # :param last_proof: <int>
    # :return: <int>
    # """

    proof = 0
    while self.valid_proof(last_proof, proof) is False:
      proof += 1

    return proof

  @staticmethod
  def valid_proof(last_proof, proof):
    # """
    # プルーフが正しいかを確認する関数: hash(last_proof, proof)の最初の4つが0となっているか？
    # :param last_proof: <int> 前のプルーフ
    # :param proof: <int> 現在のプルーフ
    # :return: <bool> 正しければ true 、そうでなれけば false
    # """

    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:4] == "0000"
  
