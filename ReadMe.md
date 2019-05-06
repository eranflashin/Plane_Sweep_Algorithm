# Plane Sweep Line Intersection Counter

##Usage
    In main.py, edit file variable to the required file and run,
    the output appears in console. 
    Pay attention: after the last output number, there is a newline

##Design
    Avl directory contains a standart implementation of AVL tree taken from the internet. It is based on
    the comparison operator defined by the class of objects put into the avl.
    
    AVL tree is used both for the line status keeping segments as items and for already counted
    intersection points keeping points as segments
    
    tests directory contains tests and a script to run the tests
    
    GeometryAux: contains all the auxiliary classes required for the solution:
    mainly Point and Segment. 
    
    LineSweep: contains the classes required specifically to the solution. 
    such as- 
            EventQueueItem (the items inserted to EventQueue):
                wraped point class
                
            EventQueue:
                min heap of points not yet processed    
            
            LineStatus:
                Avl tree of currently intersecting segments (with the sweep line) 
                
            LineSweep:
                wraps all needed components for the solution (Eventqueue, LineStatus, intersection counter
                , foundIntersections tree). The run() method, runs the algorithm and updates the intersection
                counter. Later on, user can get the counter value using getResult() method.