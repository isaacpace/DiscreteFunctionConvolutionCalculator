### Discrete Function Convolution Calculator
### Isaac Pace
###
### When working with signal analysis, it was frequently necessary
### to sketch or calculate convolutions, a mathematical operation on 
### two functions. For continuous convolutions, I could use online tools,
### but all tools I found for discrete convolutions (convolutions of 
### functions that are only defined at integer values of n) required manually
### entering every data point to convolve, which was tedious and error-prone.
### This is my own implementation of a tool that takes definitions of discrete
### functions and can sketch their shapes, sketch their convolution's shape,
### and calculate the value of the convolution at a given point.
### to use, define f_func and h_func below, then run the program to view
### their convolution. 

def f_func( n : int ) -> float:
    return sin(pi*n/12)

def h_func( n : int ) -> float:
    return delta(n) + delta (n - 24) + delta(n - 48)


import os
from math import sin, cos, tan, e, pi # constants that are often used in these functions

VERTICAL_MARGIN = 3
CONVOLUTION_LIMITS = (-2000, 2000) # overkill for most functions I would use, but still quite fast on a decent PC
DEFAULT_WINDOW = ( -3, 1, -4, 1 )

def main():
    window_dimensions = list(DEFAULT_WINDOW)
    points = {}
    while(1):
        choice = input('[1] graph convolution, [2] graph f, [3] graph h, [4] edit window, [5] calculate point, [0] quit\n> ')
        if choice == '0':
            quit()
        elif choice == '1':
            points = display_graph( convolution_func, *window_dimensions )
        elif choice == '2':
            points = display_graph( f_func, *window_dimensions )
        elif choice == '3':
            points = display_graph( h_func, *window_dimensions )
        elif choice == '4':
            print('Change window parameter:')
            window_choice = input('[1] x_start, [2] x_step, [3] y_start, [4] y_step, [5] auto zoom y, [other] cancel\n> ')
            if window_choice == '1':
                print(f'current x_start: {window_dimensions[0]}')
                window_dimensions[0] = get_integer_input()
            elif window_choice == '2':
                print(f'current x_step: {window_dimensions[1]}')
                window_dimensions[1] = get_integer_input()
            elif window_choice == '3':
                print(f'current y_start: {window_dimensions[2]}')
                window_dimensions[2] = get_float_input()
            elif window_choice == '4':
                print(f'current y_step: {window_dimensions[3]}')
                window_dimensions[3] = get_float_input()
            elif window_choice == '5':
                points = display_graph( convolution_func , *window_dimensions )
                min_y = min(point['y'] for point in points.values())
                max_y = max(point['y'] for point in points.values())
                window_dimensions[3] = 2*(max_y - min_y)/os.get_terminal_size().lines
                window_dimensions[2] = min_y - window_dimensions[3]
            points = display_graph( convolution_func, *window_dimensions )

        elif choice == '5':
            n = get_integer_input()
            points = display_graph( convolution_func, *window_dimensions, highlight = n)
            if  n in points:
                print(f'n={n}, (f * h)[n]={points[n]["y"]}')
            else:
                print(f'n={n} is outside the displayed area. Adjust x range and try again.')
        else: 
            print(f'invalid input "{choice}".')

def get_row_from_y( y_val : float , rows_count : int , y_start : int , y_step: int ) -> int:
    '''
    returns the row in the text grid that the point should be drawn at
    '''
    for i in range( rows_count ):
        if( y_start + y_step * (i + 0.5) > y_val ):
            return i
    if y_val < y_start:
        return -1
    else:
        return rows_count

def display_graph( graphed_function : callable , x_start, x_step, y_start, y_step, highlight=None ):
    '''
    prints graph of graphed_function to console
    window and zoom are determined by x/y start/step
    '''
    points = {}
    # set window dimensions
    cols, rows = os.get_terminal_size()
    rows -= VERTICAL_MARGIN #leave space for options and input without cutting off graph top
    graph_text = []
    for i in range(rows):
        row = []
        for i in range(cols):
            row.append( ' ' )
        graph_text.append(row) # add array of blank spaces
    # graph_text is now 2-D array of blank spaces

    # draw a line for x-axis if it is within the window
    x_axis_row = get_row_from_y( 0, rows, y_start, y_step)
    if x_axis_row in range(0, rows):
        graph_text[x_axis_row] = ['-'] * cols

    # draw a line for y-axis if it is within the window
    y_axis_col = int(-x_start/x_step)
    if y_axis_col in range(0, cols):
        for i in range(rows):
            graph_text[i][y_axis_col] = '|'

    print('Graphing:')
    for i in range(cols):
        n =  x_start + i * x_step
        y_val = graphed_function(n)
        row = get_row_from_y( y_val, rows, y_start, y_step)
        points[n] = {'col' : i, 'row' : row, 'y' : y_val}
        # if point is above or below the edge of the screen, indicate with an arrow on that edge
        if row < 0:
            if(n == highlight):
                graph_text[0][i] = 'O'
            else:
                graph_text[0][i] = 'v'
        elif row >= rows:
            if(n == highlight):
                graph_text[-1][i] = 'O'
            else:
                graph_text[-1][i] = '^'
        #otherwise, just draw a point
        else:
            if(n == highlight):
                graph_text[row][i] = 'O'
            else:
                graph_text[row][i] = '*'
        print('.', flush=True, end='')
    
    print('\n')
    for line in reversed(graph_text):
        print( ''.join(line) )
        
    return points


def get_integer_input() -> int:
    n = None
    while n == None:
        try:
            n = int(input('enter integer\n> '))
        except:
            pass
    return n


def get_float_input() -> float:
    n = None
    while n == None:
        try:
            n = float(input('enter number\n> '))
        except:
            pass
    return n


def convolution_func ( n : int ) -> float:
    return sum ( f_func(k)*h_func(n - k) for k in range(*CONVOLUTION_LIMITS) )


def delta( n : int ) -> int:
    '''
    The Dirac delta function, aka the unit impulse function
    '''
    return 1 if n == 0 else 0


def step( n : int ) -> int:
    '''
    the unit step function, aka the Heaviside function.
    used to make expressions easier to enter into f and h functions
    '''
    return 1 if n >= 0 else 0


def ramp( n : int ) -> int:
    '''
    the ramp function
    used to make expressions easier to enter into f and h functions
    '''
    return n if n > 0 else 0


if __name__ == '__main__':
    main()