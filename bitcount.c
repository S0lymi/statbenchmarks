
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    unsigned int res = 0;
    unsigned int buf;
	char	*streamFile;
    FILE	*fp;

    streamFile = argv[1];
    if ( (fp = fopen(streamFile, "rb")) == NULL ) {
			printf("ERROR, file %s could not be opened.\n", streamFile);
			exit(-1);
	}

    while (fread(&buf, sizeof(unsigned int), 1, fp)) {
        res += __builtin_popcount(buf);
    }
    printf("Number of ones: %d", res);



    fclose(fp);


    return 1;
}
