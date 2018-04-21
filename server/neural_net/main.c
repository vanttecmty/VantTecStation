#include <stdio.h>
#include <string.h>

int main()
{
    char filename[256];
    while(1) {
        printf("Enter filename: \n");
        scanf("%s", filename);
        if (!strcmp(filename, "Exit")) {
            break;
        }
        printf("Tu nombre es %s\n", filename);
    }
    return 0;
}