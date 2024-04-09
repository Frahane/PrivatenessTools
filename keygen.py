import os
import sys
from base64 import b64encode
from base64 import b64decode
import json
import urllib.parse
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from nacl.signing import SigningKey, VerifyKey
from nacl.public import PrivateKey, PublicKey
from nacl.encoding import Base64Encoder
import validators
import lxml.etree as etree

import uuid
import NessKeys.Prng as prng
from framework.Container import Container
from framework.ARGS import ARGS

class Keygen:

    def __is_integer(self, n):
        try:
            int(n)
        except ValueError:
            return False
        else:
            return True

    def __manual(self):
        print("*** PrivateNess KEY GENERATOR")
        print("### DESCRIPTION:")
        print("  Generates ciphers for NESS service nodes and NESS service node clients")
        print("  Works on ed25519 for keypairs")
        print("  Adjustable entropy when generating private keys")
        print("### USAGE:")
        print("#### Generate user Key")
        print("  user <username> \"coma,separated,tags\" <Entropy level>")
        print("  Example: $ python keygen.py user user1 \"Hello,World\" 5")
        print("#### Generate node Key")
        print("  node <Node name or URL> <Tariff> master-user-name \"coma,separated,services\"  <Entropy level>")
        print("  Example: $ python keygen.py node http://my-node.net 111 master \"prng,files\" 5")
        print("#### Generate Faucet Key")
        print("  faucet <Faucet URL> <Entropy level>")
        print("  Example: $ python keygen.py faucet http://www.faucet.net 5")
        print("#### Generate Backup Key")
        print("  backup <Entropy level>")
        print("  Example: $ python keygen.py backup 5")
        print("#### Generate seed")
        print("  seed <length> <Entropy level>")
        print("  Example: $ python keygen.py seed 32 5")        
        print("#### Show this manual")
        print("  $ python keygen.py help")
        print("  $ python keygen.py -h")

    def process(self):
        if ARGS.args(['user', str, str, str]):
            username = sys.argv[2]

            tags = sys.argv[3]

            if self.__is_integer(ARGS.arg(4)):
                entropy = int(ARGS.arg(4))

                if entropy < 1:
                    entropy = 1
            else:
                print("<Entropy level> must be integer")
                return False

            manager = Container.KeyManager()

            return manager.createUsersKey(username, tags, entropy)

        elif ARGS.args(['node', str, str, str, str, str]):
            url = sys.argv[2]

            if self.__is_integer(sys.argv[3]):
                tariff = int(sys.argv[3])
            else:
                print("<Tariff> must be integer")
                return False

            master_user = sys.argv[4]
            services = sys.argv[5]

            if self.__is_integer(sys.argv[6]):
                entropy = int(sys.argv[6])

                if entropy < 1:
                    entropy = 1
            else:
                print("<Entropy level> must be integer")
                return False

            manager = Container.KeyManager()

            return manager.createNodeKey(url, tariff, master_user, services, entropy)

        elif ARGS.args(['faucet', str, str]):
            url = sys.argv[2]

            if self.__is_integer(sys.argv[3]):
                entropy = int(sys.argv[3])

                if entropy < 1:
                    entropy = 1
            else:
                print("<Entropy level> must be integer")
                return False

            manager = Container.KeyManager()

            return manager.createFaucetkey(url, entropy)

        elif ARGS.args(['backup', str]):
            if self.__is_integer(sys.argv[2]):
                entropy = int(sys.argv[2])

                if entropy < 1:
                    entropy = 1
            else:
                print("<Entropy level> must be integer")
                return False

            manager = Container.KeyManager()

            bkey = manager.createBackupKey('node', '', entropy)

            print("Write down a seed to paper or password manager:")
            print(bkey.getSeed())

            return True

        elif len(sys.argv) == 4 and sys.argv[1].lower() == 'seed':

            if self.__is_integer(sys.argv[2]):
                length = int(sys.argv[2])

                if length < 16:
                    length = 16
            else:
                print("<length> must be integer")
                return False

            if self.__is_integer(sys.argv[3]):
                entropy = int(sys.argv[3])

                if entropy < 1:
                    entropy = 1
            else:
                print("<Entropy level> must be integer")
                return False
            
            generator = prng.UhePrng()

            for i in range (1, entropy):
                rand = ''
                with open('/dev/random', 'rb') as file:
                    rand = b64encode(file.read(1024)).decode('utf-8')
                    file.close()

                generator.add_entropy(rand, str(uuid.getnode()))

                print('+', end = " ", flush = True)

            print("")
            print (generator.string(length))

        else:
            self.__manual()

keygen = Keygen()
keygen.process()
