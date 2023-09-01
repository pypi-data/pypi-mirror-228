import hashlib


def calculate_file_hash(file_path, hash_algorithm="md5", chunk_size=4096):
    hash_obj = hashlib.new(hash_algorithm)
    with open(file_path, "rb") as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            hash_obj.update(data)
    return hash_obj.hexdigest()


def hash_list_of_hashes(hash_list, hash_algorithm="md5"):
    hash_obj = hashlib.new(hash_algorithm)
    # 将哈希值列表连接成一个字符串
    hash_str = ''.join(hash_list)
    # 对连接后的字符串进行哈希
    hash_obj.update(hash_str.encode())
    return hash_obj.hexdigest()
