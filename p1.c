#include <stdio.h>
#include <mpi.h>

int main(int argc, char** argv) {
    int rank, size, i;
    int max_value = -1;
    int num_iterations = 500;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    for (i = 0; i < num_iterations; i++) {
        if (i % 2 == 0) {
            MPI_Send(&rank, 1, MPI_INT, (rank + 1) % size, 0, MPI_COMM_WORLD);
            MPI_Recv(&max_value, 1, MPI_INT, (rank - 1 + size) % size, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

            if (max_value == rank) {
                printf("Process %d is neutral in iteration %d.\n", rank, i);
                break;
            }
        } else {
            if (max_value == 0) {
                printf("Process %d is neutral in iteration %d.\n", rank, i);
                break;
            }

            MPI_Send(&max_value, 1, MPI_INT, (rank + 1) % size, 0, MPI_COMM_WORLD);
            MPI_Recv(&max_value, 1, MPI_INT, (rank - 1 + size) % size, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            max_value--;
        }
    }

    MPI_Finalize();
    return 0;
}
