LIB = -L/share/apps/papi/5.5.0/lib -I/share/apps/papi/5.5.0/include
PAPI = -lpapi
OPT = -O2
OMP = --compiler-options "-fopenmp -ftree-vectorize -fopt-info-vec"
DEBUG = -g

CC = nvcc

all: compile

compile: matrix.cu
	$(CC) -o mat matrix.cu $(LIB) $(PAPI) $(OPT) $(OMP) $(DEBUG)

clean:
	rm mat

	 
