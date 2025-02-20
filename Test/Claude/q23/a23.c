int max(int x, int y) {
    return (x > y) ? x : y;
}

int max_of_four(int a, int b, int c, int d) {
    int max1 = max(a, b);    // Compare first pair
    int max2 = max(c, d);    // Compare second pair
    return max(max1, max2);  // Compare results
}

// Example main function for testing
int main() {
    int a, b, c, d;
    scanf("%d %d %d %d", &a, &b, &c, &d);
    int ans = max_of_four(a, b, c, d);
    printf("%d", ans);
    
    return 0;
}