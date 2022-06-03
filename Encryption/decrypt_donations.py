from pymongo import MongoClient
from pymongo.encryption import ClientEncryption


def decrypt_donations():
    # This must be the same master key that was used to create
    # the encryption key.
    local_master_key = b'\x85]\xa1\xeb\x1b \xb7\xb8\x8c\xca\xf5\xdb\xf1\x08\x96\x1f<\xac\xe9\x13\xc7\xe5\xef\x19ma\x99\xb1J=\xf2\x14J\x89\xbb]_\x88\xc8\xefz\xca\xdd9I\x13\xd7\xe3\xcc`\xf2\xfe\xcf\xbd\x18\x1c\x13Z\x9a\xb3%(z^\xa4\x08\xb5\xbb\xf5\xb7\xfc-\x0c\x11\xe1\xd4_.\xe9\xfdp\x0c\x86\xf0\xe1[\x12\xd2\xfa\xc4\xe0\x83,f%/'

    print(f"local_master_key: {local_master_key}")
    kms_providers = {"local": {"key": local_master_key}}

    # The MongoDB namespace (db.collection) used to store
    # the encryption data keys.
    key_vault_namespace = "encryption.__pymongoTestKeyVault"

    # The MongoClient used to read/write application data
    client = MongoClient('mongodb://localhost:27017')
    mydb = client['twitter_db']
    coll = mydb['donations']

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
        record['target'] = client_encryption.decrypt(record['target'])
        print(record['target'])

    # Cleanup resources
    client_encryption.close()
    client.close()


if __name__ == "__main__":
    decrypt_donations()