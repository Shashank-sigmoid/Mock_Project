from pymongo import MongoClient
from pymongo.encryption import ClientEncryption


def decrypt_cases_data():
    # This must be the same master key that was used to create
    # the encryption key.
    local_master_key = b'\x14\xcd<\xc8\x80\xc3\xbc\xd4\x8a\x85\x91kb"\x19@5\xd2zP\xcb\xf0\xf2R.\x8f\xedn\xce\xf1\x9f\xfa\xd5\x86\x91l\xa7\x86\x17\x18\x1bC\xc0\x97\xa3mC\xc6\xf0\xd5\x84\xc5q\xb7\xa3W\xe7P\xe8W[\x904\x06\x06\xb0\xe0)\xea\xf1\xcb\x8b\xca\xf8\xad!;N\xdb\xa8\xf53\n#\xc4\x8c\xc8m\xd3\x8d9-\x91\xe2\x8c\xc3'

    print(f"local_master_key: {local_master_key}")
    kms_providers = {"local": {"key": local_master_key}}

    # The MongoDB namespace (db.collection) used to store
    # the encryption data keys.
    key_vault_namespace = "encryption.__pymongoTestKeyVault"

    # The MongoClient used to read/write application data
    client = MongoClient("mongodb://root:root@localhost:27017")
    mydb = client["twitter_db"]
    coll = mydb["cases_data"]

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

    # Explicitly decrypt the field
    for record in coll.find():
        record["Code"] = client_encryption.decrypt(record["Code"])
        print(record["Code"])

    # Cleanup resources
    client_encryption.close()
    client.close()


if __name__ == "__main__":
    decrypt_cases_data()
