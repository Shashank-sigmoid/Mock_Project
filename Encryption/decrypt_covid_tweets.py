from pymongo import MongoClient
from pymongo.encryption import ClientEncryption


def decrypt_covid_tweets():
    # This must be the same master key that was used to create
    # the encryption key.
    local_master_key = b'vgR\t\xd6\x8f\xf1Z_^4\x1b\xc4\xb5!g\x0f\xdb^\xce\x11gg\x0eC\x88\x05;\xb4\x953\x91\xaa\xfe\xff\xde\xc7\xc9\xbd\xdd\xbft\xd0\x14\x9e\xda\xbdF\xffm\xe3\xa4s)f\xda\x01\xd6UW\x05R\x1c\x1f\\\x07E7\x93\xe4\x87*\x05\xc2Dw\xc6\xcb\x8cL\xf5{\xc1hp<\xb8\xe2t\xb6\xfb\x0e\xd1*\xe4J'

    print(f"local_master_key: {local_master_key}")
    kms_providers = {"local": {"key": local_master_key}}

    # The MongoDB namespace (db.collection) used to store
    # the encryption data keys.
    key_vault_namespace = "encryption.__pymongoTestKeyVault"

    # The MongoClient used to read/write application data
    client = MongoClient('mongodb://root:root@localhost:27017')
    mydb = client['twitter_db']
    coll = mydb['covid_tweets']

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
        record['user_screen_name'] = client_encryption.decrypt(record['user_screen_name'])
        print(record['user_screen_name'])

    # Cleanup resources
    client_encryption.close()
    client.close()


if __name__ == "__main__":
    decrypt_covid_tweets()