from web3 import Web3

# w3 = Web3(Web3.HTTPProvider('https://ethereum-goerli.publicnode.com'))
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
exploit = ""
privateKey = '0xe0725b9e9c66adb889b976bdb790d38797a04c100f4ac18ce8ff2fee47fe72a7'
acct = w3.eth.account.from_key(privateKey)
# 0x3F10E2A56Af26b592e8Fcc6e0395908922cA7e1F
hacker = acct.address
contractAddress = None

def get_txn(src, dst, data, value=0, gas=0x200000):
    return {
        "chainId": w3.eth.chain_id,
        "from": src,
        "to": dst,
        "gasPrice": w3.to_wei(1.1, 'gwei'),
        "gas": gas,
        "value": w3.to_wei(value, 'gwei'),
        "nonce": w3.eth.get_transaction_count(src),
        "data": data
    }

def transact(src, dst, data, value=0, gas=0x200000):
    data = get_txn(src, dst, data, value, gas)
    transaction = w3.eth.account.sign_transaction(data, privateKey).rawTransaction
    txn_hash = w3.eth.send_raw_transaction(transaction).hex()
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    return txn_receipt

def deploy():
    print(f"[+] Hacker address: {hacker}, balance: {w3.eth.get_balance(acct.address)}")
    print("[+] Deploying exploit contract...")
    txn_receipt = transact(hacker, None, exploit)
    print(f"[*] Exploit contract deployed at {txn_receipt['contractAddress']}")
    global contractAddress
    contractAddress = txn_receipt['contractAddress']

def check():
    if w3.is_connected() is False:
        raise "Connection Failed"

    print(f"[*] chainId: {w3.eth.chain_id}\n"
        f"[*] privateKey: {privateKey}\n"
        f"[*] accountAddress: {hacker}\n"
        f"[*] accountBalance: {w3.eth.get_balance(hacker)} wei\n")


if __name__ == '__main__':
    check()