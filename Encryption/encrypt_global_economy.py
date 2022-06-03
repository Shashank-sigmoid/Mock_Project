from pymongo import MongoClient
from pymongo.encryption import (Algorithm, ClientEncryption)
import os


def encrypt_global_economy():
    # This must be the same master key that was used to create
    # the encryption key.
    local_master_key = b'u=\xb6(\x1d\xed\xab->;\x007S+\x8a\xb4*\x17\xa8\xfe(\xe6\r\xf2\xeb\x91\x10\xb8#I\xe4\x0f\x95"\xc9\xa7\x18\xf4\x19\x05)=\xec(\xe8/\xdb\xefl\x86p\xdc"z\'\xdf\x0fB\xa0\xec\xcdX\xe6\xeb\xdf1\xf8 \x06&<\x9ci\x92\xe4\xc6g\x8f-\x97\x0c\xf8\xf6\x16\xdb>\xfdV\x1b\x85HR\xbc\x11?I'

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
    coll = mydb['global_economy']

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
            record['Code'],
            Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic,
            key_id=data_key_id)
        my_query = {"Code": record['Code']}
        new_value = {"$set": {"Code": encrypted_field}}
        coll.update_one(my_query, new_value)

    print("Encryption completed successfully...")

    # Cleanup resources
    client_encryption.close()
    client.close()


if __name__ == "__main__":
    encrypt_global_economy()
