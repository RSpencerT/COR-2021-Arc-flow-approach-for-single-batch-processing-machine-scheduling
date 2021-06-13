# Arc-flow approach for single batch-processing machine scheduling
## [Renan Spencer Trindade](https://www.renan-st.com/), [Olinto César Bassi de Araújo](http://ufsmpublica.ufsm.br/docente/13025), [Marcia Fampa](http://marciafampa.com/)
###### Computers & Operations Research, Volume 134, October 2021, 105394.
###### DOI: https://www.doi.org/10.1016/j.cor.2021.105394

Abstract:
>We address the problem of scheduling jobs with non-identical sizes and distinct processing times on a single batch-processing machine, aiming at minimizing the makespan. The extensive literature on this NP-hard problem mostly focuses on heuristics. Using an arc-flow based optimization approach, we construct a novel formulation that represents it as a problem of determining flows in graphs. The size of the formulation increases with the machine capacity and with the number of distinct sizes and processing times among the jobs, but it does not increase with the number of jobs, which makes it very effective to solve large instances to optimality, especially when multiple jobs have equal size and processing time. We compare our model to other models from the literature, showing its clear superiority on benchmark instances and proving optimality of random instances with up to 100 million jobs.

This is the official implementation of the paper.
To download the accepted manuscript, please go to the personal website: https://www.renan-st.com/publications/cor-2021-arc-flow-approach-for-single-batch-processing-machine-scheduling.

### Current project structure
```
COR-2021-Arc-flow-approach-for-single-batch-processing-machine-scheduling/
├── Dataset/
    ├── ...
├── ArcFlow.mod
├── ArcFlow.run
├── DataArcFlowAMPLgen.py
├── LICENSE
├── README.md
```

### ArcFlow.mod and ArcFlow.run

These files contain the implementation of the Arc-flow model published in the article, and are encoded in AMPL format.
To run them, you need a version of AMPL found at: https://ampl.com/.
We use CPLEX to run our tests.


### DataArcFlowAMPLgen.py

This script creates an input file for the AMPL model. 
It reads the dataset files with the values for processing time and size. Then it creates the graph and the necessary parameters for the Arc-flow model.

You need the numpy package to run it.

###### Arguments
| Option     | Description                                                                                    |
| ------     | -----------                                                                                    |
| -n         | *Number of jobs                                                                                |
| -b         | *Batch capacity                                                                                |
| -s         | Name of the file with the size values of the jobs. (default value: size.txt)                   |
| -p         | Name of the file with the processing time values of the tasks. (default value: processing.txt) |
| -o         | Name of the target file with AMPL format. (default value: DataArcFlow.dat)                     |

*Mandatory arguments

Example:
```console
$ python DataArcFlowAMPLgen.py -n 10 -b 20
```
or
```console
$ python DataArcFlowAMPLgen.py -n 10 -b 20 -p Dataset/20B/10/processing_p1s1_1.txt -s Dataset/20B/10/size_p1s1_1.txt
```
