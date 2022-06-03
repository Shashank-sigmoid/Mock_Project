from pymongo import MongoClient
from pymongo.encryption import (Algorithm, ClientEncryption)


def encrypt_who_tweets():
    # This must be the same master key that was used to create
    # the encryption key.
    local_master_key = b'\xa4r\x8bO\xcc\xf0\xe5\xb6\x18\xbfs:N\x0f\xce14N\xcb+\xab\xad\x14X\x94\xd5\x9f;_\xc2tX\x98\xd5\xee\xa1e\xc1\xb9IEf\xfb\xbe\xf9\x18\x1a\xbeb\x81\x04\xf5\x12[Uj\xb69\x87\tLT\x1a\xf2\xbb\xba\xb2\xe6\xf6?@\xe0Z<"\xe3\xa4\x1d\x8b\\\x084\xf2\x86\xba\xa5\x8bsP\x0cs\xab\xd9\xe3A\r'

    print(f"local_master_key: {local_master_key}")
    kms_providers = {"local": {"key": local_master_key}}

    # The MongoDB namespace (db.collection) used to store
    # the encryption data keys.
    key_vault_namespace = "encryption.__pymongoTestKeyVault"
    key_vault_db_name, key_vault_coll_name = key_vault_namespace.split(".", 1)
    # key_vault_db_name: encryption
    # key_vault_coll_name: __pymongpTestKeyVault
    print(f"key_vault_db_name: {key_vault_db_name} key_vault_coll_name: {key_vault_coll_name}")

    # The MongoClient used to read/write application data
    client = MongoClient('mongodb://localhost:27017')
    mydb = client['twitter_db']
    coll = mydb['who_tweets']

    # Set up the key vault(key_vault_namespace) for this example
    key_vault = client[key_vault_db_name][key_vault_coll_name]
    print(f"key_vault: {key_vault}")

    # Ensure that two data keys cannot share the same keyAltName
    key_vault.drop()
    key_vault.create_index(
        "keyAltNames",
        unique=True,
        partialFilterExpression={"keyAltNames": {"$exists": True}})

    client_encryption = ClientEncryption(
        kms_providers,
        key_vault_namespace,
        # The MongoClient to use for reading/writing to the key vault.
        # This can be the same MongoClient used by the main application.
        client,
        # The CodecOptions class used for encrypting and decrypting.
        # This should be the same CodecOptions instance you have configured
        # on MongoClient, Database, or Collection.
        coll.codec_options)

    # Create a new data key for the encryptedField
    data_key_id = client_encryption.create_data_key(
        'local', key_alt_names=['pymongo_encryption_example'])

    # Explicitly encrypt a field
    for record in coll.find():
        encrypted_field = client_encryption.encrypt(
            record['user_name'],
            Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic,
            key_id=data_key_id)
        my_query = {"user_name": record['user_name']}
        new_value = {"$set": {"user_name": encrypted_field}}
        coll.update_one(my_query, new_value)

    print("Encryption completed successfully...")

    # Cleanup resources
    client_encryption.close()
    client.close()


if __name__ == "__main__":
    encrypt_who_tweets()
