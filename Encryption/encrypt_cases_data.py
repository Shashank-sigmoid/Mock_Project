from pymongo import MongoClient
from pymongo.encryption import (Algorithm, ClientEncryption)


def encrypt_cases_data():

    # This must be the same master key that was used to create
    # the encryption key.
    local_master_key = b'\x14\xcd<\xc8\x80\xc3\xbc\xd4\x8a\x85\x91kb"\x19@5\xd2zP\xcb\xf0\xf2R.\x8f\xedn\xce\xf1\x9f\xfa\xd5\x86\x91l\xa7\x86\x17\x18\x1bC\xc0\x97\xa3mC\xc6\xf0\xd5\x84\xc5q\xb7\xa3W\xe7P\xe8W[\x904\x06\x06\xb0\xe0)\xea\xf1\xcb\x8b\xca\xf8\xad!;N\xdb\xa8\xf53\n#\xc4\x8c\xc8m\xd3\x8d9-\x91\xe2\x8c\xc3'

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
    client = MongoClient("mongodb://root:root@localhost:27017")
    mydb = client["twitter_db"]
    coll = mydb["cases_data"]

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
        "local", key_alt_names=["pymongo_encryption_example"])

    # Explicitly encrypt a field
    for record in coll.find():
        encrypted_field = client_encryption.encrypt(
            record["Code"],
            Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic,
            key_id=data_key_id)
        my_query = {"Code": record["Code"]}
        new_value = {"$set": {"Code": encrypted_field}}
        coll.update_one(my_query, new_value)

    print("Encryption completed successfully...")

    # Cleanup resources
    client_encryption.close()
    client.close()


if __name__ == "__main__":
    encrypt_cases_data()
