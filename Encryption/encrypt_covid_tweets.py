from pymongo import MongoClient
from pymongo.encryption import (Algorithm, ClientEncryption)


def encrypt_covid_tweets():
    # This must be the same master key that was used to create
    # the encryption key.
    local_master_key = b'vgR\t\xd6\x8f\xf1Z_^4\x1b\xc4\xb5!g\x0f\xdb^\xce\x11gg\x0eC\x88\x05;\xb4\x953\x91\xaa\xfe\xff\xde\xc7\xc9\xbd\xdd\xbft\xd0\x14\x9e\xda\xbdF\xffm\xe3\xa4s)f\xda\x01\xd6UW\x05R\x1c\x1f\\\x07E7\x93\xe4\x87*\x05\xc2Dw\xc6\xcb\x8cL\xf5{\xc1hp<\xb8\xe2t\xb6\xfb\x0e\xd1*\xe4J'

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
    client = MongoClient('mongodb://root:root@localhost:27017')
    mydb = client['twitter_db']
    coll = mydb['covid_tweets']

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
            record['user_screen_name'],
            Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic,
            key_id=data_key_id)
        my_query = {"user_screen_name": record['user_screen_name']}
        new_value = {"$set": {"user_screen_name": encrypted_field}}
        coll.update_one(my_query, new_value)

    print("Encryption completed successfully...")

    # Cleanup resources
    client_encryption.close()
    client.close()


if __name__ == "__main__":
    encrypt_covid_tweets()
