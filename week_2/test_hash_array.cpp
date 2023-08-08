#include <cmath>
#include <iostream>
#include <bits/stdc++.h>

using namespace std;


struct int2 {
    int x;
    int y;
};

int main() {
    int map_size = 71;
    int arr_size = 5;
    
    
    int* one = new int[arr_size * sizeof(int)];
    int* two = new int[arr_size * sizeof(int)];

    int2* hashmap = new int2[map_size * sizeof(int2)];

    for (int i = 0; i < arr_size; i++) {
        int v1 = floor(rand() % 10);
        one[i] = v1;

        int v2 = floor(rand() % 10); 
        two[i] = v2;
    }

    bool check[arr_size];

    int exp_collisions = 0;
    for (int i = 0; i < arr_size; i++) {
        int a = rand()%2;
        bool val;

        if (a == 0){
            val = false;
        } else {
            val = true;

            exp_collisions += 1;
        }

        check[i] = val;
    }

    for (int i = 0; i < map_size; i++) {
        int2 pair;
        pair.x = -1;
        pair.y = -1;

        hashmap[i] = pair;
    }

    for (int i = 0; i < arr_size; i++) {

            int on = one[i];
            int tw = two[i];

            bool chck = check[i];

            if (chck) {

                int low;
                int high;

                //printf("extent: %d, %d\n", on, tw);
                int64_t key;
                if (on > tw) {
                    low = tw;
                    high = on;
                    key = (int32_t)tw | (on << 16);
                } else {
                    low = on;
                    high = tw;
                    key = (int32_t)on | (tw << 16);
                }
                 
                int hashval = ((key ^ 0x55555555) | ((key & 0xAAAAAAAA) >> 1)) % map_size;

                //printf("hash: %d\n", key);
                //printf("hashval: %d\n", hashval);

                //printf("%d\n", i);

                bool not_inserted = true;

                // Linear probing
                while (not_inserted) {
                    int2 prev_pair = hashmap[hashval];
                    int2 pair;
                    if (prev_pair.x == -1 && prev_pair.y == -1) {
                        pair.x = low;
                        pair.y = high;
                        hashmap[hashval] = pair;
                        not_inserted = false;
                    } else if (prev_pair.x == -1 && prev_pair.y == -1) {
                        not_inserted = false;
                    } else {
                        hashval = ++hashval % map_size;
                    }
                }
            }
    }

    int n_collisions = 0;
    
    for (int i = 0; i < map_size; i++) {
        int2 collision_pair = hashmap[i];

        if (collision_pair.x == -1 && collision_pair.y == -1) {
            continue;
        }
        //printf("collision: %d\n", collision);
        int host_idx = collision_pair.x;
        int phantom_idx = collision_pair.y;

        printf("Collision between %d and %d\n", host_idx, phantom_idx);

        n_collisions += 1;
    }

    printf("Number of expected collisions: %d\n", exp_collisions);
    printf("Number of recorded collisions: %d\n", n_collisions);

    free(hashmap);
    free(one);
    free(two);

    return 0;
}