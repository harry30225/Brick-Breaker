# BRICK BREAKER

## It is game coded in python without cursors and pygame.In this you have to break bricks with ball and manage to not let the ball fell using a paddle

## OOPS Concepts

### All the OOPS Concepts are used in developing this

* Inheritance
* Polymorphism
* Encapsulation
* Abstraction

## Controls
* A and D for the movement of paddle
* B for launch of ball if paddle grabs it or initial launch
* Q to quit the game
* H for choose new ball or new life or start a new game depending on the circumstance

## Description
* Bricks
    * Their are two types of bricks
    * Fixed Bricks : These cant be destroyed. Green in colour
    * Dynamic Bricks : Max Strength - Red Bricks , Medium Strength - Blue Bricks , Low Strength - Yellow Bricks
    * Red Bricks require 3 hits to break , blue one requires 2 and yellow one requires 1
    * After every hit the score is updated by 10 points only on Dynamic Bricks

* User
    * In a game every user has 3 lives
    * Every lives has 3 balls
    * Score and time for each round is updated

* Powerups
    * Destroying a brick completely might give a dropping down powerup
    * Paddle Enlarge  [+]  --> Paddle size doubles
    * Paddle Contract [-]  --> Paddle size half
    * Ball Multiplier [**] --> Every ball divides into two
    * Increase Ball Speed [+*] --> Increase ball speed to double
    * Thru Ball [O]  --> Can break any brick with one hit
    * Paddle Grab [_*] --> Paddle can grab the ball
    * Each powerup would be activated for only 10 secs

### Developed with :heart: and :coffee: by Harshit Sharma
