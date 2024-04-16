#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

unsigned long long int power(unsigned long long int x, unsigned long long int y, unsigned long long int p) {
    unsigned long long int res = 1;
    x = x % p;
    while (y > 0) {
        if (y & 1) {
            res = (res * x) % p;
        }
        y >>= 1;
        x = (x * x) % p;
    }
    return res;
}

int miillerTest(unsigned long long int d, unsigned long long int n) {
    unsigned long long int a = 2 + (rand() % (n - 4));
    unsigned long long int x = power(a, d, n);
    if (x == 1 || x == n - 1) {
        return 1;
    }
    while (d != n - 1) {
        x = (x * x) % n;
        d *= 2;
        if (x == 1) {
            return 0;
        }
        if (x == n - 1) {
            return 1;
        }
    }
    return 0;
}

int isPrime(unsigned long long int n, int k) {
    if (n <= 1 || n == 4) {
        return 0;
    }
    if (n <= 3) {
        return 1;
    }
    unsigned long long int d = n - 1;
    while (d % 2 == 0) {
        d /= 2;
    }
    int result = 1;
    #pragma omp parallel for
    for (int i = 0; i < k; i++) {
        if (!miillerTest(d, n)) {
            result = 0;
        }
    }
    return result;
}

int main() {
    unsigned long long int num1 = 3042162;
    // Benchmarking
    int k = 10000000 ; // Increase k for better accuracy
    clock_t start = clock();
    int result = isPrime(num1, k);
    double time_taken = ((double)clock() - start) / CLOCKS_PER_SEC;
    if (result)
        printf("%llu is prime.\n", num1);
    else
        printf("%llu is not prime.\n", num1);
    printf("Time taken for %d iterations: %f seconds\n", k, time_taken);
    return 0;
}