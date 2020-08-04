import fbchat
import datetime
import tkinter as tk
from operator import itemgetter


class MainMenu:

	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.email = tk.StringVar()
		self.mdp = tk.StringVar()
		self.lbl1 = tk.Label(self.frame, text='Adresse courriel').grid(row=0, column=0)
		self.lbl2 = tk.Label(self.frame, text='Mot de passe').grid(row=1, column=0)
		self.input1 = tk.Entry(self.frame, textvariable=self.email).grid(row=0, column=1)
		self.input2 = tk.Entry(self.frame, textvariable=self.mdp, show='*', exportselection=0).grid(row=1, column=1)
		self.button1 = tk.Button(self.frame, text='Exit', width=25, command=self.close_windows).grid(row=2, column=0)
		self.button2 = tk.Button(self.frame, text='Run', width=25, command=self.run).grid(row=2, column=1)
		self.frame.pack()

	def close_windows(self):
		self.master.destroy()

	def run(self):
		try:
			client = fbchat.Client(self.email.get(), self.mdp.get())
		except fbchat.FBchatException:
			print("Login fail")
			return -1
		else:
			users_list = client.fetchAllUsers()
			
			message_count = []
			
			for user in users_list:
				thread_dict = client.fetchThreadInfo(user.uid)
				for thread in thread_dict.values():
					if thread.message_count == None:
						message_count.append((thread.name, 0))
					else:
						message_count.append((thread.name, thread.message_count))
			
			message_count.sort(key=itemgetter(1))
			
			message_count.reverse()
			
			count = 1
			
			t = datetime.datetime.now()
			f = open(f"MessengerCountLog/MessengerMessageCount-{t.year}-{t.month}-{t.day}", "w")
			for rank in message_count:
				f.write(f"{count} : {rank[0]} with {rank[1]} messages\n")
				
				count += 1
			
			client.logout()

def main():
	root = tk.Tk()
	app = MainMenu(root)
	root.mainloop()


if __name__ == '__main__':
	main()
	
