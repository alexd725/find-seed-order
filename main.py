import itertools
from mnemonic import Mnemonic
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

def derive_public_address_from_seed(mnemonic):
    # Generate seed from mnemonic
    seed = Bip39SeedGenerator(mnemonic).Generate()
    # Create a Bip44 object for Ethereum (change as needed for other coins)
    bip_obj = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
    # Generate the address for the first account (Account 0, External Address Index 0)
    address = bip_obj.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()
    return address

def validate_seed(seed_phrase):
    mnemo = Mnemonic("english")
    # Check if the provided seed phrase is valid according to BIP-39
    return mnemo.check(' '.join(seed_phrase))

def generate_phrases_and_addresses(first_seven):
    # Generate all permutations of the first seven words
    permutations = itertools.permutations(first_seven)
    
    # Initialize a counter for valid seeds
    valid_count = 0
    
    # Combine each permutation with the last five words
    for perm in permutations:
        # Combine the words into a single phrase
        phrase = list(perm)
        # Check if the phrase is a valid BIP-39 seed
        if validate_seed(phrase):
            valid_count += 1
            # Generate public address for the valid mnemonic
            address = derive_public_address_from_seed(' '.join(phrase))
            print('No:', valid_count)
            print('Valid seed phrase found:', ' '.join(phrase))
            print('Derived Address:', address)

            if address == "your public address here":
                break
    
    # Output the count of valid mnemonics found
    if valid_count == 0:
        print('No valid seed phrases found.')
    else:
        print('Total valid seeds found:', valid_count)

# Example usage
first_seven = ['sda', 'sadf', 'sdaf', 'sdf', 'sa', 's', 's', 'fsf', 'zsdf', 'sfds', 'asas', 'dfsd']
# last_five = []
generate_phrases_and_addresses(first_seven)