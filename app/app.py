import sys
sys.path.insert(0, '../api/')
sys.path.insert(0, './api/')
import tkinter as tk
from tkinter import messagebox
from hydra import HydraWallet



class BlockchainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Blockchain App - MILESTONE 2")

        self.blockchain = HydraWallet()
        self.wallets = self.get_vaults()
        self.active_acc = 0
        

        # Milestone 2
        milestone2_label = tk.Label(master, text="Welcome to your Wallet")
        milestone2_label.pack(pady=5)

        # Display Account in Use

        address = self.get_state()
        account_label = tk.Label(master, text=f"Account: {address}")
        account_label.pack()

        # display balance
        wallet = self.get_acc_details()
        if wallet != None:
            balance = self.blockchain.display_address_balance()
            input_label = tk.Label(master, text=f"Balance: {balance}")
            input_label.pack()


         #Acoounts Availaible
        acc_num = len(self.wallets)
        input_label = tk.Label(master, text=f"{acc_num} Accounts Availaible")
        input_label.pack()

        # get unlock password from user
        input_label = tk.Label(master, text="Enter password to create new account: ⬇️")
        input_label.pack()
        self.entry_unlock_password = tk.Entry(master, width=40)
        self.entry_unlock_password.pack(pady=5, padx=40)
        self.button_generate_wallet = tk.Button(master, text="Generate Mnemonic & Wallet ✅", command=self.generate_wallet) #here
        self.button_generate_wallet.pack(pady=5)

        #Mnemonic phrase generated will display in the box below
        input_label = tk.Label(master, text="The generated 24-word phrase will be shown below: ⬇️")
        input_label.pack()
        self.entry_new_address = tk.Entry(master, width=40)
        self.entry_new_address.pack(pady=5)


        #Select Account to use
        # input_label = tk.Label(master, text="Change Account to Use")
        # input_label.pack()
        # self.active_num = tk.Entry(master, width=20)
        # self.active_num.pack(padx=10,pady=5)
        # self.button_set_active_account = tk.Button(master, text="swap account", command=self.active_account) #here
        # self.button_set_active_account.pack(padx=3,pady=3)



        # Generate a persona DID
        input_label = tk.Label(master, text="Password to generate did ⬇️ ")
        input_label.pack()
        self.did_password = tk.Entry(master, width=20)
        self.did_password.pack(padx=1,pady=1)
        self.button_generate_persona_did = tk.Button(master, text="Generate Persona DID ✅", command=self.generate_persona_did) #here
        self.button_generate_persona_did.pack()
        self.entry_persona_did = tk.Entry(master, width=40)
        self.entry_persona_did.insert(0, "")
        self.entry_persona_did.pack()


        #Delete Account to use
        input_label = tk.Label(master, text="Enter Index of Account to delete: ⬇️")
        input_label.pack()
        self.delete_id = tk.Entry(master, width=20)
        self.delete_id.pack(padx=1,pady=1)
        self.button_set_delete_account = tk.Button(master, text="delete account ‼️", command=self.delete_account) #here
        self.button_set_delete_account.pack(padx=2,pady=2)


        # Recover the wallet using the 24-word phrase
        input_label = tk.Label(master, text="Enter 24-word phrase to recover wallet: ⬇️")
        input_label.pack()
        self.entry_recover_wallet = tk.Entry(master, width=40)
        self.entry_recover_wallet.pack()
        input_label = tk.Label(master, text="Enter password to recover wallet: ⬇️")
        input_label.pack()
        self.entry_recover_password = tk.Entry(master, width=40)
        self.entry_recover_password.pack()
        self.button_recover_wallet = tk.Button(master, text="Recover Wallet ✅", command=self.recover_wallet) #here
        self.button_recover_wallet.pack(pady=5)

        # Send/Receive Money
        input_label = tk.Label(master, text="Enter address to send HYD to: ⬇️")
        input_label.pack(anchor="s")
        self.entry_send_address = tk.Entry(master, width=40)
        self.entry_send_address.pack(anchor='s')
        input_label = tk.Label(master, text="Enter amount to send: ⬇️")
        input_label.pack(anchor='s')
        self.entry_send_amount = tk.Entry(master, width=40)
        self.entry_send_amount.pack(anchor='s')
        input_label = tk.Label(master, text="Enter wallet password: ⬇️")
        input_label.pack(anchor='s')
        self.wallet_password = tk.Entry(master, width=40)
        self.wallet_password.pack(anchor='s')
        self.button_send = tk.Button(master, text="Send ✅", command=self.send_hyd) #here
        self.button_send.pack(anchor='s')

        # Create a Listbox and display transaction history
        input_label = tk.Label(master, text="Transaction History 🏦")
        input_label.pack()
        listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=40, height=15)
        listbox.pack(padx=10, pady=10)
        address = self.get_state()
        transactions = self.blockchain.get_account_transactions()
        if transactions != None:
            for item in transactions:
                sender, recipient = item['sender'],item['recipient']
                amount = item['amount']
                if sender == address:
                    listbox.insert(tk.END, f"Sent {amount} hyd to {recipient}")
                else:
                    listbox.insert(tk.END, f"Received {amount} hyd from {sender}")


    def send_hyd(self):
        address = self.entry_send_address.get()
        amount = self.entry_send_amount.get()
        password = self.wallet_password.get()
        if len(self.wallets) > 0 and address != "" and amount != "" and password != "":    
            txhash = self.blockchain.send_transaction(address, int(amount),password)
            messagebox.showinfo("Info", f"Transaction was successful\nTransaction ID: {txhash}")
        else:
            messagebox.showerror("Error", "Something went Wrong with your transaction.\n Make sure you filled in the receiptient address, amount and password")
   

    def delete_account(self):
        delete_id = self.delete_id.get()
        if delete_id != "":
            self.blockchain.delete_account(delete_id)
            messagebox.showinfo("Info", f"Transaction was successful\nAccount with ID: {delete_id} has been deleted")
        else:
            messagebox.showerror("Error", "Put the index of account you want to delete.")


    def get_state(self):
        if len(self.wallets) > 0:
            address = self.blockchain.get_wallet_address()
            return address
        
    def get_acc_details(self):
        if len(self.wallets) > 0:
            address = self.blockchain.get_wallet_address()
            return address

    def active_account(self):
        if len(self.wallets) > 0:
            acc_active = self.active_num.get()
            self.active_num = int(acc_active)
            print(self.active_num)
        else:
            messagebox.showerror("Error", "You do not have an active wallet.")


    def generate_wallet(self):
        unlock_password = self.entry_unlock_password.get()
        if unlock_password == '':
            messagebox.showerror("Error", "Please enter password for your wallet.")
            return
        phrase = self.blockchain.generate_phrase()
        resp = self.blockchain.generate_wallet(unlock_password,phrase)
        self.entry_new_address.insert(0, resp)

    def generate_persona_did(self):
        password = self.did_password.get()
        if len(self.wallets) > 0 and password != "":
            resp = self.blockchain.generate_did(password)
            self.entry_persona_did.insert(0,resp)
        else:
            messagebox.showerror("Error", "You do not have an active wallet or forgot to put your password")


    def recover_wallet(self):
        wallet_phrase = self.entry_recover_wallet.get()
        password = self.entry_recover_password.get()
        if wallet_phrase == '' or password == "":
            messagebox.showerror("Error", "Enter your wallet 24-word phrase and password")
            return     
        self.blockchain.recover_wallet(password,wallet_phrase)
        messagebox.showinfo("Wallet Recovered!", "Your wallet has been recovered")


    def display_account_transactions(self):
        if self.check_vault() == False:
            return
        
        if self.blockchain.address == '':
            messagebox.showerror("Error", "You need to create a vault or address")
            return
        address = self.get_state()
        transactions = self.blockchain.get_account_transactions()
        
        messagebox.showinfo("Info", "Under development, Please try again later or wait for update")


    def get_vaults(self):
        try:
            wallets = self.blockchain.load_wallets()
            return wallets
        except FileNotFoundError:
            return []



if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()