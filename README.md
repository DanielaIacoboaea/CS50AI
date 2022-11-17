

# CS50’s Introduction to Artificial Intelligence with Python

This course explores some of the ideas, techniques and algorithms that are at the 
foundation of **AI**. 

The projects from this repository are `python` programs that incorporate them, focused on starting from existing code, understand it and complete specific tasks.


Topics covered throughout the course:

* [Search](#search)
* [Knowledge](#knowledge)
* [Uncertainty](#uncertainty) 
* [Optimization](#optimization) 
* [Learning](#learning) 
* [Neural Networks](#neural-networks) 
* [Language](#language)


### [Search](/Week0_Search)


Search problems, an environment in which the agent is in and needs to find a solution to a problem.  
There are different types of search problems: get from point A to point B or adverserial search problems (Tic-Tac-Toe).

* **Degrees** - write a program that determines how many “degrees of separation” apart two actors are:  

    >    * `python3 degrees.py large`  

    
* **Tic-Tac-Toe** - using Minimax, implement an **AI** to play **Tic-Tac-Toe** optimally:  

    >    * `pip3 install -r requirements.txt`
    >    * `python3 runner.py`




### [Knowledge](/Week1_Knowledge)


Build knowledge based agents that are able to draw some additional conclusions based on knowledge.


* **Knights** - write a program to solve **logic puzzles**:  

    >    * `python3 puzzle.py`  

* **Minesweeper** - write an **AI** to play **Minesweeper**:  

    >    * `pip3 install -r requirements.txt`  
    >    * `python3 runner.py`  
    
    

### [Uncertainty](/Week2_Uncertainty)

How computers learn to deal with uncertain events and draw conclusions with a certain probability.

* **PageRank** - write an AI to rank web pages by importance:  

    >    * `python3 pagerank.py corpus0` 


* **Heredity** - write an AI to assess the likelihood that a person will have a particular genetic trait:  

    >    * `python3 heredity.py data/family0.csv` 


### [Optimization](/Week3_Optimization/crossword/)

Choosing the best option from a set of options. 


* **Crossword** - write an AI to generate crossword puzzles:  

    >    * `pip3 install -r requirements.txt`  
    >    * `python3 generate.py data/structure1.txt data/words1.txt output.png`
`  
    

### [Learning](/Week4_Learning)

Instead of giving the AI some instructions on how to solve a problem, in machine learning, it has access to information that needs to analyze and understand patters to be able to perform a task on it's own.

* **Shopping** - write an AI to predict whether online shopping customers will complete a purchase:  

    >    * `pip3 install scikit-learn`  
    >    * `python3 shopping.py shopping.csv`


* **Nim** - write an AI that teaches itself to play **Nim** through reinforcement learning:  

    >    * `python3 play.py`
    

### [Neural Networks](/Week5_Neural-networks/traffic)


One of the most popular tools in **Machine Learning** are **Neural Networks**.

* **Traffic** - write an AI to identify which traffic sign appears in a photograph:  

    >    * `pip3 install -r requirements.txt`  
    >    * `python3 traffic.py gtsrb`

    >   **YouTube Demo**:  
    
    >   [![Watch the video](https://img.youtube.com/vi/Nv-NeZdIxoc/maxresdefault.jpg)](https://youtu.be/Nv-NeZdIxoc)
    


### [Language](/Week6_Language)

Algorithms that will allow an AI to process and understand natural language.


* **Parser** - write an AI to parse sentences and extract noun phrases:  

    >    * `pip3 install -r requirements.txt`  
    >    * `python3 parser.py`


* **Questions** - Write an AI to answer questions:  

    >    * `pip3 install -r requirements.txt`  
    >    * `python3 questions.py corpus`




