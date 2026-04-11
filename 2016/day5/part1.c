#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>


int main(int argc, char** argv) {
    if (argc < 3) {
        printf("Usage: %s KEY ITERATIONS\n", argv[0]);
        return 1;
    }
    const char* key = argv[1];
    size_t iterations = atol(argv[2]);
    char index[64];
    unsigned char digest[MD5_DIGEST_LENGTH];
    char hex[33];
    char password[iterations + 1];
    for (int i = 0; i < iterations + 1; i++) {
        password[i] = '\0';
    }

    // need to hash <key><number>
    long counter = 0;
    for (int i = 0; i < iterations; i++)
    {
        while (++counter) {
            sprintf(index, "%s%ld", key, counter);

            // This is dperecated but who cares, this is a puzzle not production code
            MD5((unsigned char*)index, strlen(index), digest);

            // Convert to hex.
            for (int j = 0; j < MD5_DIGEST_LENGTH; j++) {
                sprintf(&hex[j*2], "%02x", digest[j]);
            }

            // Check first 5
            int match = 1;
            for (int j = 0; j < 5; j++) {
                if (hex[j] != '0') {
                    match = 0;
                    break;
                }
            }

            if (match) {
                password[i] = hex[5];
                break;
            }
        }
    }

    printf("The password is %s\n", password);
    return 0;
}