import sys
import json
import random
import qrcode
import hashlib
import datetime

# from config import mycol

# VERIFICATION_URL = "http://localhost:8080/?id="
VERIFICATION_URL = "http://127.0.0.1:5000/verify/"

class Login:

	MANF = ""
	LOGGEDIN = False
	MANUFACTURERS = {
		"DRREDDY": "password123",
		"LUPIN": "hello123",
		"KOTLIN": "qwerty",
		"ADMIN": "qwerty"
	}

	def main(self):
		loginid = input("Enter your login id:\t")
		password = input("Enter your password:\t")

		if loginid in self.MANUFACTURERS.keys():
			if self.MANUFACTURERS[loginid] == password:
				self.LOGGEDIN = True
				self.MANF = loginid

	def isLoggedIn(self):
		if self.LOGGEDIN:
			print("\nWelcome to the blockchain world\n")
		else:
			sys.exit("Please login to experience the blockchain world")

	def getManf(self):
		return self.MANF


class BlockChain:

	def __init__(self):
		self.product_brand = ""
		self.product_name = ""
		self.product_batch = ""
		self.manuf_date = ""
		self.expiry_date = ""
		self.product_id = ""
		self.product_price = ""
		self.product_size = ""
		self.product_type = ""


	def actions(self):
		choice = input("Enter 1 to ADD item or 2 to Verify BlockChain\n")

		if choice == "1":
			self.product_brand = input("Enter product brand:\n")
			self.product_name = input("Enter product name:\n")
			self.product_batch = input("Enter product batch:\n")
			self.manuf_date = input("Enter product manuf date:\n")
			self.expiry_date = input("Enter product expry date:\n")
			self.product_id = input("Enter product id:\n")
			self.product_price = input("Enter product price:\n")
			self.product_size = input("Enter product size:\n")
			self.product_type = input("Enter product type:\n")
			self.newProduct()
		
		elif choice == "2":
			if self.isBlockchainValid():
				sys.exit("BlockChain is valid")
			else:
				sys.exit("BlockChain is invalid")

		else:
			sys.exit("Logged out successfully")

	
	def newProduct(self):
		data = {
			"Manufacturer": self.product_brand,
			"ProductName": self.product_name,
			"ProductBatch": self.product_batch,
			"ProductManufacturedDate": self.manuf_date,
			"ProductExpiryDate": self.expiry_date,
			"ProductId": self.product_id,
			"ProductPrice": self.product_price,
			"ProductSize": self.product_size,
			"ProductType": self.product_type,
		}

		proHash = hashlib.sha256(str(data).encode()).hexdigest()
		print(proHash)
		data["hash"] = proHash

		# x = mycol.insert_one(data)
		
		self.createBlock(data)

		imgName  = self.imgNameFormatting()
		self.createQR(proHash, imgName)

	def addProduct(
		self,
		product_brand,
		product_name,
		product_batch,
		manuf_date,
		expiry_date,
		product_id,
		product_price,
		product_size,
		product_type
	):
		self.product_name = product_name
		data = {
			"Manufacturer": product_brand,
			"ProductName": product_name,
			"ProductBatch": product_batch,
			"ProductManufacturedDate": manuf_date,
			"ProductExpiryDate": expiry_date,
			"ProductId": product_id,
			"ProductPrice": product_price,
			"ProductSize": product_size,
			"ProductType": product_type,
		}

		proHash = hashlib.sha256(str(data).encode()).hexdigest()
		print(proHash)
		data["hash"] = proHash

		# x = mycol.insert_one(data)
		
		self.createBlock(data)

		imgName  = self.imgNameFormatting()
		self.createQR(proHash, imgName)


	def createBlock(self, data):

		if self.isBlockchainValid():
			blocks = []
			for block in open('./NODES/N1/blockchain.json', 'r'):
				blocks.append(block)
			print(blocks[-1], "jsdata===========")

			preBlock = json.loads(blocks[-1])

			index = preBlock["index"] + 1
			preHash = hashlib.sha256(str(preBlock).encode()).hexdigest()

		transaction = {
			'index': index,
			'proof': random.randint(1, 1000),
			'previous_hash': preHash,
			# 'hash': proHash,
			'timestamp': str(datetime.datetime.now()),
			'data': str(data),
		}

		with open("./NODES/N1/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))
		with open("./NODES/N2/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))
		with open("./NODES/N3/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))
		with open("./NODES/N4/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))

		# currHash = hashlib.sha256(str(transaction).encode()).hexdigest()
		# imgName  = self.imgNameFormatting()

		# self.createQR(currHash, imgName)
		return


	def createQR(self, hashc, imgName):
		img = qrcode.make(VERIFICATION_URL + hashc)
		img.save("./QRcodes/" + imgName)

		# sys.exit("Product added successfully")
		return


	def imgNameFormatting(self):
		dt = str(datetime.datetime.now())
		dt = dt.replace(" ", "_").replace("-", "_").replace(":", "_")
		return self.product_name + "_" + dt + ".png"


	def isBlockchainValid(self):
		with open("./NODES/N1/blockchain.json", "r") as file:
			n1_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n1_hash)
		with open("./NODES/N2/blockchain.json", "r") as file:
			n2_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n2_hash)
		with open("./NODES/N3/blockchain.json", "r") as file:
			n3_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n3_hash)
		with open("./NODES/N4/blockchain.json", "r") as file:
			n4_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n4_hash)

		if n1_hash == n2_hash == n3_hash == n4_hash:
			return True
		else:
			return False


if __name__ == "__main__":
	lof = Login()
	lof.main()
	lof.isLoggedIn()

	LOGGEDINUSER = lof.getManf()

	bc = BlockChain()
	bc.actions()