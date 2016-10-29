# we need random to generate the coin flips
import random, math

# class defining each node in skiplist
class skipnode:
	def __init__(self, value = None, prev = None, next = None):
		self.value = value
		self.next = next
		self.prev = prev
		self.down = None
		self.skip_count = 0

	def insert(self, value, skip_levels):

		# inserting at the end of the list
		if self.next is None:

			# check if we should insert into this layer or not
			if skip_levels <= 0:
				new_node = skipnode(value, self)

				self.next = new_node

				if self.down:
					new_node.down = self.down.insert(value, skip_levels - 1)

				base_skip_distance = new_node.get_prev_base_distance()
				new_node.skip_count = self.skip_count - base_skip_distance
				self.skip_count = base_skip_distance

				return new_node

			else:

				# just try to insert into the layer below
				if self.down:
					self.skip_count += 1
					return self.down.insert(value, skip_levels - 1)

			return

		# inserting in the middle of the list
		if self.next.value >= value:
			if skip_levels <= 0:
				new_node = skipnode(value, self, self.next)

				self.next.prev = new_node
				self.next = new_node

				# just try to insert into the layer below
				if self.down:
					new_node.down = self.down.insert(value, skip_levels - 1)

				base_skip_distance = new_node.get_prev_base_distance()
				new_node.skip_count = self.skip_count - base_skip_distance
				self.skip_count = base_skip_distance

				return new_node
			else:
				# just try to insert into the layer below
				if self.down:
					self.skip_count += 1
					return self.down.insert(value, skip_levels - 1)
			return


		return self.next.insert(value, skip_levels)

	# finds an element
	def find(self, value, remove = False):
		# return node if found
		if self.value == value:
			return self

		# try to go down if next is none
		if self.next is None:
			if self.down:
				# if possible go down and look for the element there
				found = self.down.find(value)
				if found:
					self.skip_count -= 1
				return found
			else:
				# element not present if no down and no next
				return None

		if value < self.next.value:
			if self.down:
				# go down if value is lower than next in current layer.
				found = self.down.find(value)
				if found:
					self.skip_count -= 1
				return found
			else:
				# if element is between values in current layer, which is also the base layer, the elmenent is not present
				return None

		# if value is larger or equal to next value, just go next
		found = self.next.find(value)
		# if found:
		# 	self.skip_count -= 1
		return found

	# deletes self
	def burn(self):
		if self.prev:
			self.prev.next = self.next
			self.prev.skip_count += self.skip_count

		if self.next:
			self.next.prev = self.prev

		if self.down:
			self.down.burn()


	# converts the remaining linked list into regular python list
	def to_list(self):
		lst = [{
				'value': self.value,
				'skip_count': self.skip_count
			}]

		if self.next:
			lst += self.next.to_list()

		return lst

	# finds the specified index in average log(n). Used to find the median.
	def find_index(self, index_at, index_to_find):
		# print('searching for {}, currently at {} with value {}'.format(index_to_find, index_at, self.value))
		if index_at == index_to_find:
			return self.value

		if self.next is None or index_at + 1 + self.skip_count > index_to_find:
			# print('down', self.next, self.skip_count)
			return self.down.find_index(index_at, index_to_find)

		if index_at + 1 + self.skip_count <= index_to_find:
			# print('right', 1 + self.skip_count)
			return self.next.find_index(index_at + 1 + self.skip_count, index_to_find)


	def get_prev_base_distance(self):
		prev_base_node = self.prev.get_base()
		n = prev_base_node
		distance = 0
		while n.next.value != self.value:
			distance += 1
			n = n.next

		return distance

	def get_base(self):
		n = self
		while n.down:
			n = n.down
		return n



# main skiplist class
class skippity:
	def __init__(self, expected_items = 20):
		self.height = math.floor(math.log(expected_items, 2))
		self.root = skipnode()
		self.count = 0

		n = self.root
		for i in range(self.height - 1):
			n.down = skipnode()
			n = n.down


	# inserts one element
	def insert(self, value, level = False):

		# increment number of elements in skiplist
		self.count += 1

		# cointoss to get the level of the currently inserted element
		if not level:
			level = self.get_level()
		self.root.insert(value, self.height - level)


	# finds an item in the skiplist
	def find(self, value):
		return self.root.find(value)


	# removes an item from the skiplist
	def remove(self, value):
		found = self.find(value)

		if found:
			# delete the item
			found.burn()

			# decrease element counter
			self.count -= 1

			return True

		return False


	# do the coinflipping to determine the level
	def get_level(self):
		level = 1
		for i in range(self.height - 1):
			flip = bool(random.getrandbits(1))
			if not flip:
				return level
			level += 1
		return self.height


	# get all elements in the skiplists by going to base layer and converting it to list
	def get_elements(self):
		n = self.root
		while n.down is not None:
			n = n.down
		return n.to_list()


	# returns median of the array
	def median(self):

		if self.count == 0:
			return False

		# if count is odd pick the middle
		if self.count % 2 == 1:
			return self.root.find_index(0, self.count // 2 + 1)
		else:
			median = (self.root.find_index(0, self.count // 2) + self.root.find_index(0, self.count // 2 + 1)) / 2
			if median % 1 == 0:
				return int(median)
			return median
		# if count is even pick middle two elements and average them



	# prints out the skiplist
	def debug(self, display_right_count = False):
		full_list = self.get_elements()
		full_length = len(full_list)

		n = self.root
		do_next = True
		while do_next:
			current_list = n.to_list()
			pos = 0
			for i in range(0, full_length):
				if pos < len(current_list) and full_list[i]['value'] == current_list[pos]['value']:
					if display_right_count:
						print('{:3} '.format(current_list[pos]['skip_count']), end = '_')
					else:
						print('{:3} '.format(full_list[i]['value'] if full_list[i]['value'] else ''), end = '_')
					pos += 1
				else:
					print('_____', end = '')

			print()
			do_next = True if n.down is not None else False
			n = n.down

		print()


s = skippity(8)

s.insert(1)
s.insert(2)
s.insert(3)
s.insert(4)
s.insert(5)
s.insert(6)
s.insert(7)

# print(s.median())

s.debug(True)
s.debug()
