from pymongo import MongoClient
from pymongo.encryption import ClientEncryption


def decrypt_global_economy():
    # This must be the same master key that was used to create
    # the encryption key.
    local_master_key = b'u=\xb6(\x1d\xed\xab->;\x007S+\x8a\xb4*\x17\xa8\xfe(\xe6\r\xf2\xeb\x91\x10\xb8#I\xe4\x0f\x95"\xc9\xa7\x18\xf4\x19\x05)=\xec(\xe8/\xdb\xefl\x86p\xdc"z\'\xdf\x0fB\xa0\xec\xcdX\xe6\xeb\xdf1\xf8 \x06&<\x9ci\x92\xe4\xc6g\x8f-\x97\x0c\xf8\xf6\x16\xdb>\xfdV\x1b\x85HR\xbc\x11?I'

    print(f"local_master_key: {local_master_key}")
    kms_providers = {"local": {"key": local_master_key}}

    # The MongoDB namespace (db.collection) used to store
    # the encryption data keys.
    key_vault_namespace = "encryption.__pymongoTestKeyVault"

    # The MongoClient used to read/write application data
    client = MongoClient('mongodb://localhost:27017')
    mydb = client['twitter_db']
    coll = mydb['global_economy']

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
        record['Code'] = client_encryption.decrypt(record['Code'])
        print(record['Code'])

    # Cleanup resources
    client_encryption.close()
    client.close()


if __name__ == "__main__":
    decrypt_global_economy()