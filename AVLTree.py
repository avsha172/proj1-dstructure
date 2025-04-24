def printree(root):
	if not root.is_real_node():
		return ["#"]

	root_key = str(root.key)
	left, right = printree(root.left), printree(root.right)

	lwid = len(left[-1])
	rwid = len(right[-1])
	rootwid = len(root_key)

	result = [(lwid + 1) * " " + root_key + (rwid + 1) * " "]

	ls = len(left[0].rstrip())
	rs = len(right[0]) - len(right[0].lstrip())
	result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

	for i in range(max(len(left), len(right))):
		row = ""
		if i < len(left):
			row += left[i]
		else:
			row += lwid * " "

		row += (rootwid + 2) * " "

		if i < len(right):
			row += right[i]
		else:
			row += rwid * " "

		result.append(row)

	return result

#username - complete info
#id1      - complete info 
#name1    - complete info 
#id2      - complete info
#name2    - complete info  



"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int or None
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value, is_dummy=False):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = 0 - is_dummy
		self.is_dummy = is_dummy
		self.bf = 0

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return not self.is_dummy
	
	def set_dummy(self, dummy):
		self.left = dummy
		self.right = dummy

	def update_height(self):
		self.height= max(self.left.height, self.right.height) + 1

	def update_balance_factor(self, Tree):
		prev_bf = self.bf
		self.bf = self.left.height - self.right.height
		new_bf = self.bf
		Tree.zero_bf += (new_bf == 0) - (prev_bf == 0)

"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.dummy_node = AVLNode(None, None, True)
		self.root = None
		self.length = 0
		self.zero_bf = 0


	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""
	def search(self, key):
		def search_rec(node):
			if not node.is_real_node():
				return None
			if key == node.key:
				return node
			if key < node.key:
				return search_rec(node.left)
			return search_rec(node.right)
		
		return search_rec(self.root)


	"""inserts a new node into the dictionary with corresponding key and value

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
    @param start: can be either "root" or "max"
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def _check_rotations(self, node):
		rotations = 0
		while node is not None:
			old_height = node.height
			node.update_height()
			node.update_balance_factor(self)
			if abs(node.bf) > 1:
				rot = self._balance_node(node, node.key)
				rotations += rot
			
			if node.height == old_height:
				break
			node = node.parent
		return rotations

	def insert(self, key, val, start="root"):
		self.length += 1
		if not self.root:
			self.root = AVLNode(key, val)
			self.root.set_dummy(self.dummy_node)
			self.zero_bf += 1
			return 0
		
		# Find insertion point
		parent = self._find_insertion_point(self.root, key)
		new_node = AVLNode(key, val)
		new_node.set_dummy(self.dummy_node)
		# Connect new node to parent
		if key < parent.key:
			parent.left = new_node
		else:
			parent.right = new_node
		new_node.parent = parent
		
		# Update zero_bf counter
		self.zero_bf += 1
		
		# Update heights and balance factors up the tree
		return self._check_rotations(parent)

	def _find_insertion_point(self, node, key):
		if not node.is_real_node():
			return False
		if key < node.key:
			ret = self._find_insertion_point(node.left, key)
		else:
			ret = self._find_insertion_point(node.right, key)

		if ret:
			return ret
		return node

	def _find_successor(self, node):
		if not node.right.is_real_node():
			return None
		curr = node.right
		while curr.left.is_real_node():
			curr = curr.left
		return curr

	def _balance_node(self, node, key):
		rotations = 0
		
		if node.bf > 1:  # Left heavy
			if node.left.bf < 0:  # Left-right case
				self._left_right(node)
				rotations += 1
			self._left_left(node)
		else:  # Right heavy
			if node.right.bf > 0:  # Right-left case
				self._right_left(node)
				rotations += 1
			self._right_right(node)
		
		return rotations + 1

	def _right_left(self, node):
		a = node
		b = a.right
		c = b.left
		
		# First rotation (right)
		a.right = c
		c.parent = a
		b.left = c.right
		if b.left.is_real_node():
			b.left.parent = b
		c.right = b
		b.parent = c
		
		# Update heights and balance factors
		b.update_height()
		b.update_balance_factor(self)
		c.update_height()
		c.update_balance_factor(self)

	def _left_right(self, node):
		a = node
		b = a.left
		c = b.right
		
		# First rotation (left)
		a.left = c
		c.parent = a
		b.right = c.left
		if b.right.is_real_node():
			b.right.parent = b
		c.left = b
		b.parent = c
		
		# Update heights and balance factors
		b.update_height()
		b.update_balance_factor(self)
		c.update_height()
		c.update_balance_factor(self)

	def _left_left(self, node):
		a = node
		b = a.left
		
		# Update parent pointers
		if not a.parent:
			self.root = b
			b.parent = None
		else:
			if a == a.parent.left:
				a.parent.left = b
			else:
				a.parent.right = b
			b.parent = a.parent
		
		# Update child pointers
		a.left = b.right
		if a.left.is_real_node():
			a.left.parent = a
		b.right = a
		a.parent = b
		
		# Update heights and balance factors
		a.update_height()
		a.update_balance_factor(self)
		b.update_height()
		b.update_balance_factor(self)

	def _right_right(self, node):
		a = node
		b = a.right
		
		# Update parent pointers
		if not a.parent:
			self.root = b
			b.parent = None
		else:
			if a == a.parent.left:
				a.parent.left = b
			else:
				a.parent.right = b
			b.parent = a.parent
		
		# Update child pointers
		a.right = b.left
		if a.right.is_real_node():
			a.right.parent = a
		b.left = a
		a.parent = b
		
		# Update heights and balance factors
		a.update_height()
		a.update_balance_factor(self)
		b.update_height()
		b.update_balance_factor(self)
	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		check_bf = node.parent
		
		# Case 1: Node has no right child
		if not node.right.is_real_node():
			replacement = node.left
			if node.parent:
				if node.parent.right == node:
					node.parent.right = replacement
				else:
					node.parent.left = replacement
			else:
				self.root = replacement
			if replacement.is_real_node():
				replacement.parent = node.parent
				
		# Case 2: Node has no left child
		elif not node.left.is_real_node():
			replacement = node.right
			if node.parent:
				if node.parent.right == node:
					node.parent.right = replacement
				else:
					node.parent.left = replacement
			else:
				self.root = replacement
			if replacement.is_real_node():
				replacement.parent = node.parent
				
		# Case 3: Node has two children
		else:
			successor = self._find_successor(node)
			
			# If successor is not the direct right child
			if successor.parent != node:
				check_bf = successor.parent
				# Update successor's parent's child pointer
				if successor.parent.left == successor:
					successor.parent.left = successor.right
				else:
					successor.parent.right = successor.right
				if successor.right.is_real_node():
					successor.right.parent = successor.parent
				
				# Move successor's right child
				successor.right = node.right
				if successor.right.is_real_node():
					successor.right.parent = successor
			else:
				# If successor is the direct right child, just update its left child
				check_bf = successor
				successor.right = node.right.right
				if successor.right.is_real_node():
					successor.right.parent = successor
			
			# Update parent pointers
			if node.parent:
				if node.parent.right == node:
					node.parent.right = successor
				else:
					node.parent.left = successor
			else:
				self.root = successor
			successor.parent = node.parent
			
			# Move node's left child
			successor.left = node.left
			if successor.left.is_real_node():
				successor.left.parent = successor
			successor.update_height()
			successor.update_balance_factor(self)
		# Update zero_bf counter
		if node.bf == 0:
			self.zero_bf -= 1
		
		# Decrease size
		self.length -= 1
		# Rebalance the tree
		return self._check_rotations(check_bf)


	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		def rec_traverse(node, ls):
			if node.is_real_node():
				rec_traverse(node.left, ls)
				ls.append((node.key, node.value))
				rec_traverse(node.right, ls)
		ls = []
		rec_traverse(self.root, ls)
		return ls


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self.length


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root

	"""gets amir's suggestion of balance factor

	@returns: the number of nodes which have balance factor equals to 0 devided by the total number of nodes
	"""
	def get_amir_balance_factor(self):
		if self.length == 0:
			return 0
		return self.zero_bf/self.length
	
	def __repr__(self):  # you don't need to understand the implementation of this method
		return '\n'.join(printree(self.root))

# Test the __repr__ function