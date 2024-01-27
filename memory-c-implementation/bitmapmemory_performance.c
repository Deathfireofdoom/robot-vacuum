#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define GRID_SIZE 200001
#define SUB_GRID_SIZE 500
#define N_SUB_GRIDS ((GRID_SIZE / SUB_GRID_SIZE) * (GRID_SIZE / SUB_GRID_SIZE))
#define ARRAY_SIZE ((SUB_GRID_SIZE * SUB_GRID_SIZE) / 8)

typedef struct {
    unsigned char *grid;
} SubGrid;

typedef struct {
    SubGrid *subgrids[N_SUB_GRIDS];
    int unique_n_visited;
} BitMapMemory;

typedef struct {
    int x;
    int y;
} Coordinate;

BitMapMemory* create_bitmap_memory() {
    BitMapMemory *bmm = malloc(sizeof(BitMapMemory));
    if (bmm == NULL) {
        return NULL;  // Memory allocation failed
    }

    for (int i = 0; i < N_SUB_GRIDS; i++) {
        bmm->subgrids[i] = NULL;
    }

    bmm->unique_n_visited = 0;
    return bmm;
}

SubGrid* get_or_create_subgrid(BitMapMemory *bmm, int x, int y) {
    if (bmm == NULL || x < 0 || x >= GRID_SIZE || y < 0 || y >= GRID_SIZE) {
        return NULL; // Out of bounds or invalid BitMapMemory
    }

    int subgrid_index = (y / SUB_GRID_SIZE) * (GRID_SIZE / SUB_GRID_SIZE) + (x / SUB_GRID_SIZE);

    if (bmm->subgrids[subgrid_index] == NULL) {
        // Allocate the SubGrid struct
        bmm->subgrids[subgrid_index] = malloc(sizeof(SubGrid));
        if (bmm->subgrids[subgrid_index] == NULL) {
            return NULL; // Allocation failed
        }

        // Allocate the grid within the SubGrid
        bmm->subgrids[subgrid_index]->grid = calloc(ARRAY_SIZE, sizeof(unsigned char));
        if (bmm->subgrids[subgrid_index]->grid == NULL) {
            free(bmm->subgrids[subgrid_index]);
            bmm->subgrids[subgrid_index] = NULL;
            return NULL; // Allocation failed
        }
    }

    return bmm->subgrids[subgrid_index];
}

Coordinate* generate_coordinates(int x_start, int y_start, int x_end, int y_end, int *size) {
    // Determine the direction of movement
    int x_step = (x_start <= x_end) ? 1 : -1;
    int y_step = (y_start <= y_end) ? 1 : -1;

    // Calculate the number of coordinates
    *size = (x_start == x_end) ? abs(y_end - y_start) + 1 : abs(x_end - x_start) + 1;
    Coordinate *coordinates = malloc(*size * sizeof(Coordinate));

    if (coordinates == NULL) {
        *size = 0;
        return NULL; // Allocation failed
    }

    for (int i = 0; i < *size; ++i) {
        if (x_start == x_end) {
            // Vertical movement
            coordinates[i].x = x_start;
            coordinates[i].y = y_start + i * y_step;
        } else {
            // Horizontal movement
            coordinates[i].x = x_start + i * x_step;
            coordinates[i].y = y_start;
        }
    }

    return coordinates;
}

void add_location(BitMapMemory *bmm, int x, int y) {
    if (bmm == NULL || x < 0 || x >= GRID_SIZE || y < 0 || y >= GRID_SIZE) {
        return;
    }

    SubGrid *subgrid = get_or_create_subgrid(bmm, x, y);

    int local_x = x % SUB_GRID_SIZE;
    int local_y = y % SUB_GRID_SIZE;    

    int index = (local_y * SUB_GRID_SIZE + local_x) / 8;
    int bit = (local_y * SUB_GRID_SIZE + local_x) % 8;


    if (!(subgrid->grid[index] & (1 << bit))) {
        subgrid->grid[index] |= (1 << bit);
        bmm->unique_n_visited++;
    }
}

void add_locations(BitMapMemory *bmm, int x_raw_start, int y_raw_start, int x_raw_end, int y_raw_end) {
    // Adjust for being negative values 
    int x_start = x_raw_start + GRID_SIZE / 2;
    int y_start = y_raw_start + GRID_SIZE / 2;
    int x_end = x_raw_end + GRID_SIZE / 2;
    int y_end = y_raw_end + GRID_SIZE / 2;

    // generate sequence of coordinates
    int size; // we need to send this to know how many elements we should loop
    Coordinate *coords = generate_coordinates(x_start, y_start, x_end, y_end, &size);

    if (coords != NULL) {
        for (int i = 0; i < size; i++) {
            add_location(bmm, coords[i].x, coords[i].y);
        }
        free(coords);
    }
}

int get_unique_n_visited(BitMapMemory *bmm) {
    if (bmm == NULL) {
        return -1;
    }
    return bmm->unique_n_visited;
}

void free_bitmap_memory(BitMapMemory *bmm) {
    if (bmm == NULL) {
        return;
    }

    for (int i = 0; i < N_SUB_GRIDS; i++) {
        if (bmm->subgrids[i] != NULL) {
            free(bmm->subgrids[i]->grid);
            free(bmm->subgrids[i]);
        }
    }

    free(bmm);
}
