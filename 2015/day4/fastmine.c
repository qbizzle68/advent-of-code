#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>
#include <math.h>

int main(int argc, char** argv) {
	if (argc < 4) {
		printf("Usage: %s START BATCHSIZE KEY [ZEROS]\n", argv[0]);
		return 1;
	}
	// Use long here incase we want to test for larger number of zeros (need more iterations).
	long start = atol(argv[1]);
	long batch_size = atol(argv[2]);
	char* key = argv[3];
	int zeros = argc > 4 ? atoi(argv[4]) : 5;
	
	char input[256];
	unsigned char digest[MD5_DIGEST_LENGTH];
	char hex[33];

	for (int i = start; i < start + batch_size; i++) {
		// Input is of the form <KEY><NUMBER> where number is at least 5
		// chars long (left padded with 0's).

		// Find number of digits in i via log10 (rounding up) for size of string.
		long len = ceil(log10(i)) < 6 ? 6 : ceil(log10(i));
		char padded_i[len+1];
		// Create string variable of i with left padding.
		sprintf(padded_i, "%06d", i);
		// Build input string.
		snprintf(input, sizeof(input), "%s%s", key, padded_i);

		// This is deprecated but who cares, this is a puzzle not production code.
		MD5((unsigned char*)input, strlen(input), digest);

		// Convert to hex.
		for (int j = 0; j < MD5_DIGEST_LENGTH; j++) {
			sprintf(&hex[j*2], "%02x", digest[j]);
		}

		// Check first <zeros> chars are '0'
		int match = 1;
		for (int j = 0; j < zeros; j++) {
			if (hex[j] != '0') {
				match = 0;
				break;
			}
		}

		if (match) {
			// Print successful value to stdout
			printf("%d\n", i);
			return 0;
		}
	}

	fprintf(stderr, "Failed: Unable to find result for range %ld-%ld\n", start, start + batch_size);
	return 1;
}
