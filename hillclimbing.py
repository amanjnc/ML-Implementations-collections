from random import randint
from queue import PriorityQueue
#or you could use heapq

def slope(x1,y1,x2,y2):
    if abs(y2-y1)==abs(x2-x1):
         return True
    return False 

# for the first element x1=8,y1=0


def draw_board(initialstate):
    board=[]
    #create it to be 8 by 8
    for i in range(len(initialstate)):
        for j in range(len(initialstate)):  
            board.append(0)
    for idx,element in enumerate(initialstate):
        board[element-1][idx] = "Q"    
    

def fitnessfun(initialstate,conflict_score=0):
    for i in range(len(initialstate)):
        for j in range(i+1,len(initialstate)):  
              #horizontal score check
            horizontal_conflict = initialstate[i]==initialstate[j]
            #diagonal score check
            value1=initialstate[i]
            value2=initialstate[j]
            diagonal_conflict = slope(value1,i,value2,j)==True
            if horizontal_conflict or diagonal_conflict:
                conflict_score +=1
    return conflict_score
def single_move(state,index):#for just one#so 2 possible state
    upstate=state.copy()
    downstate=state.copy()
    current_possible_state_after_move=[]
    if state[index]<8:
        upstate[index]+=1
        
        current_possible_state_after_move.append(upstate)
        
    if state[index]>1:
        downstate[index]-=1 
        current_possible_state_after_move.append(downstate)
    return current_possible_state_after_move    


        
def for_all_single_move(state):#16 possible state
    all_best=[]
    for index in range(len(state)):
        all_best.extend(single_move(state,index))
    return all_best
def hillclimbing(state):
    platue_tryno=0
    currentstate=state
    while True:
        minimum_score_state=PriorityQueue()
        possiblestates=for_all_single_move(currentstate)
        
        for  eachpossiblity in possiblestates:
            minimum_score_state.put((fitnessfun(eachpossiblity),eachpossiblity))
        score,bestsofar=minimum_score_state.get() #not pop bc we still want it????
        #score could be _
        if fitnessfun(bestsofar)>=fitnessfun(currentstate):
            return currentstate
        

        currentstate=bestsofar


def random_restart_hill_climbing():
    all_list=[]
    for i in range(1000):
        one_list=[]
        for index in range(8):
            one_list.append(randint(1,8))
        all_list.append(one_list)
    


    # for one_single_list in all_list:

    for a_list in all_list:
        x=hillclimbing(a_list)
            ###local min---whenever a value is found to be minimum it is printed it might nt be zero
        if fitnessfun(x)==0:
                print(f"we decrease the conflict_score from {fitnessfun(a_list)} to {fitnessfun(x)} and the board went from {a_list} to {x}")
            
                
random_restart_hill_climbing()    
    

# print(draw_board(initialstate))            
            


    
        

        
    
   
              
   
  


