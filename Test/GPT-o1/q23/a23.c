#include <stdio.h>

int max(int x, int y) {
    return (x > y) ? x : y;
}

int max_of_four(int a, int b, int c, int d) {
    return max(max(a, b), max(c, d));
}

int main() {
    int a, b, c, d;
    scanf("%d", &a);
    scanf("%d", &b);
    scanf("%d", &c);
    scanf("%d", &d);
    printf("%d\n", max_of_four(a, b, c, d));
    return 0;
}