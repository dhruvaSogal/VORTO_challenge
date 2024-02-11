# Solution File: my_solution.py
## Solution Summary:
### -Utilizing Simulated Annealing Approach  

### -Starting at naive solution of one driver per delivery  

 ### -Then remove drivers/combine deliveries  

 ### -Change the order of deliveries or add new drivers  

 ### -Randomly change the order of every sub list  

 ### - Hit local minima ~57k average, tuning did not improve  

  ### - start of a Linear programming approach in refactor.py  

###  -References contained in solution_ideas_notes.txt  

## Profile Notes:
### Distance calculation of routes (as opposed to solutions) was most costly for CPU. This is unsurprising as it is used to check the validity of mutations as well  
### It would also be good to improve the swap_and_shift function as this took a significant amount of cpu usage. I did not expect this as it was only called 20% of the iterations
## Things to Improve
### Better utilization of evaluation code to save time in file processing/structuring  
### Starting with a less stochastic approach like Linear Programming then moving towards something random

