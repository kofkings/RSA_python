import random
from fractions import gcd

def RSA(plainText):
    # Generate Key
    # p, q is 2 random large prime (512 bit)
    p = generateLargePrime(512)
    q = generateLargePrime(512)
    while p == q:
        q = generateLargePrime(512)
    n = p * q
    totientN = (p - 1) * (q - 1)

    # PublicKey = random in (2, totientN - 1) | gcd(PublicKey, totientN) = 1
    # PrivateKey * PublicKey = 1 (% totientN)
    publicKey = random.randrange(2, totientN - 1)
    while not (gcd(publicKey, totientN) == 1):
        publicKey = random.randrange(2, totientN - 1)
        privateKey = bezout(publicKey, totientN)
        while privateKey < 0:
            privateKey += totientN

    print "Key:"
    print "     N:", n
    print "     Public Key:", publicKey
    print "     Private Key", privateKey

    # Encrypt CipherTextNumber = PlainTextNumber ^ PublicKey % N
    # Devide to many block | plainTextNumber < N
    blockSize = n.bit_length() / 8

    print 'Plain Text :', plainText
    # Get PlainTextNumber
    arrayPlainTextNumber = []
    for i in xrange(len(plainText) / blockSize + 1):
        arrayPlainTextNumber.append(textToNum(plainText[:blockSize]))
        plainText = plainText[blockSize:]
    print "Plain Text Number : ", arrayPlainTextNumber

    arrayCipherTextNumber = []

    for i in arrayPlainTextNumber:
        arrayCipherTextNumber.append(pow(i, publicKey, n))
    print "Cipher Text Number : ", arrayCipherTextNumber

    # Decrypt DecryptTextNumber = CipherTextNumber ^ PrivateKey % N

    decryptedText = ''
    arrayDecryptedTextNumber = []
    for i in arrayCipherTextNumber:
        decryptedNumber = pow(i, privateKey, n)
        arrayDecryptedTextNumber.append(decryptedNumber)
        decryptedText += numToText(decryptedNumber)

    print "Decrypted Text Number :", arrayDecryptedTextNumber
    print "Decrypted Text :", decryptedText


def isPrime(n):
    # Probaly large prime

    # Low base for quicker test
    lowPrimes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89,
                 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181,
                 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
                 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
                 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
                 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619,
                 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743,
                 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
                 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    if (n > 3):
        # Test base 2
        if (n & 1 != 0):

            # Test base low prime
            for p in lowPrimes:
                if (n % p == 0):
                    return False

            # Miller-Rabbin
            # n - 1 = 2 ^ s * m
            m, s = n - 1, 0
            while m & 1 == 0:
                m, s = m >> 1, s + 1
            # Loop k time (error bound 4 ^ -k)
            for i in xrange(50):
                a = random.randrange(2, n - 2)
                if not strong_pseudoprime(n, a, s, m):
                    return False
            return True
    return False


def strong_pseudoprime(n, a, s, m):
    # Odd composite number n = m * 2 ^ s + 1 is called a strong (Fermat) pseudoprime when one of the following conditions holds:
    #   a ^ m % n = 1
    # or a ^ (d * 2 ^ r) = n - 1 for 0 <= r < s
    b = pow(a, m, n)
    if b == 1:
        return True
    for i in xrange(s):
        if b == n - 1:
            return True
        b = b * b % n

    return False


def generateLargePrime(k):
    # Random number then check primality
    n = random.randrange(2 ** (k - 1), 2 ** (k))
    while not isPrime(n):
        n = random.randrange(2 ** (k - 1), 2 ** (k))
    return n


def bezout(a, b):
    # Bezout: Input a, b can find x, y, gcd(a, b) | x * a + y * b = gcd(a, b)
    # In RSA:
    #   a <=> PublicKey, b <=> totientN, x <=> PrivateKey
    x1, y1 = 1, 0
    x2, y2 = 0, 1
    while b:
        temp = a // b
        a, b = b, a % b
        x1, y1, x2, y2 = x2, y2, x1 - temp * x2, y1 - temp * y2
    return x1


def textToNum(textString):
    # ASCII as number base 256 number
    number = 0
    for character in textString:
        number = (number << 8) + ord(character)
    return number


def numToText(number):
    # ASCII as number base 256 number
    textString = ''
    while number:
        textString = chr(number % 256) + textString
        number >>= 8
    return textString


if __name__ == '__main__':
    message = raw_input("Type a message to test:")
    RSA(message)
    raw_input("Press a key to exit")

# Sorry about my English
