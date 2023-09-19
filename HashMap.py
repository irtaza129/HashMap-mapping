class ChainingHashTable:
    # Constructor that initializes each bucket within the table as empty.
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserting an item within the hash table.
    # If item already exists, updates item.
    def insert(self, key, item):
        # Creating an index.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # If the key does not exist, append the new key-value pair.
        bucket_list.append([key, item])

    # Searching for the corresponding key to return.
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return
