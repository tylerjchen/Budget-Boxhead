'''Author: Tyler Chen
   Date: 31/5/17
   Description: Budget Boxhead 
   
   This module contains the sprites for Budget Boxhead.
'''

import pygame, random

class Player(pygame.sprite.Sprite):
    '''This class defines the player sprite.'''
    def __init__(self, screen):
        '''This intializer sets the images and position of the player sprite as well as loads sound effects.'''
        pygame.sprite.Sprite.__init__(self)
        
        self.__supplyDrop = pygame.mixer.Sound('./Audio/supplyDrop.wav')
        self.__death = pygame.mixer.Sound('./Audio/death.wav')
        
        self.__rightSprites = []
        self.__leftSprites = []
        
        # Loads images for player animation in a list.
        for imageNumber in range(4):
            image = pygame.image.load('./Images/soldierRight' + str(imageNumber + 1) + '.png')
            self.__rightSprites.append(image)

        for imageNumber in range(4):
            image = pygame.image.load('./Images/soldierLeft' + str(imageNumber + 1) + '.png')
            self.__leftSprites.append(image)
        
        self.__static = pygame.image.load('./Images/soldierStatic.png')
        self.image = self.__static
        
        self.__right = False
        self.__left = False
        
        self.__rightImage = 0
        self.__leftImage = 0        
        
        self.rect = self.image.get_rect()
        self.rect.center = (320, 420)
        
        self.__screen = screen
        self.__dx = 0
        self.__dy = 0
    
    def playDeath(self):
        '''This method polays a sound effect.'''
        self.__death.set_volume(0.5)
        self.__death.play()        

    def getRight(self):
        '''This method returns whether or not the player is moving right.'''
        return self.__right
    
    def getLeft(self):
        '''This method returns whether or not the player is moving left.'''
        return self.__left
    
    def getXPos(self):
        '''This method returns the player's x position.'''
        return self.rect.centerx
    
    def moveLeft(self):
        '''This method allows the ball to move in a leftwards direction.'''
        self.__dx = -5
        self.__left = True
        self.__right = False
        
    def moveRight(self):
        '''This method allows the ball to move in a leftwards direction.'''
        self.__dx = 5 
        self.__right = True
        self.__left = False
    
    def reset(self):
        '''This method resets the player's position when they lose a life.'''
        self.image = self.__static
        self.__right = False
        self.__left = False
        self.__rightImage = 0
        self.__leftImage = 0                
        self.rect.center = (320, -50)
        self.__dy = 6
        if self.rect.centery < 440:
            self.__supplyDrop.set_volume(0.1)
            self.__supplyDrop.play()
            
    def update(self):
        '''This method updates the position of the player.'''
        self.rect.centerx += self.__dx
        self.rect.bottom += self.__dy
        
        # Cycles through list of images to animate movement.
        if self.__right:
            if self.__rightImage <= 3:
                self.image = self.__rightSprites[self.__rightImage]
                self.__rightImage += 1
            else:
                self.__rightImage = 0
        
        if self.__left:
            if self.__leftImage <= 3:
                self.image = self.__leftSprites[self.__leftImage]
                self.__leftImage += 1
            else:
                self.__leftImage = 0
        
        if self.rect.left < 0:
            self.rect.centerx = self.__screen.get_width() - 30
        elif self.rect.right > self.__screen.get_width():
            self.rect.centerx = 50
        if self.rect.centery >= 420:
            self.rect.centery = 420

class StatKeeper(pygame.sprite.Sprite):
    '''This class defines the scorekeeper sprite.'''
    def __init__(self):
        '''This intializer sets the points, font, starting ammo, and starting lives that will be recorded and displayed.'''
        
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font('PopulationZeroBB.otf', 30)
        self.__gunshot = pygame.mixer.Sound('./Audio/gunshot.wav')
        self.__shellFall = pygame.mixer.Sound('./Audio/shellFall.wav')
        self.__empty = pygame.mixer.Sound('./Audio/empty.wav')
        
        self.__points = 0
        self.__lives = 3
        self.__ammo = 30
    
    def gainPoints(self):
        '''This method increases the player's score by one.'''
        self.__points += 1
    
    def getPoints(self):
        '''This method returns the number of points the player has earned.'''
        return self.__points
    
    def gainLife(self):
        '''This method increases the player's lives by one.'''
        self.__lives += 1
    
    def loseLife(self):
        '''This method subtracts a life from the player.'''
        self.__lives -= 1
        
    def getLives(self):
        '''This method returns the number of lives the player has remaining.'''
        return self.__lives
    
    def gainAmmo(self, ammo):
        '''This method adds ammo the the current count.'''
        self.__ammo += ammo
    
    def loseAmmo(self):
        '''This method subtracts ammo from the current count and plays sound effects.'''
        self.__ammo -= 1
        self.__gunshot.set_volume(0.1)
        self.__gunshot.play()           
        self.__shellFall.set_volume(0.1)
        self.__shellFall.play()          
    
    def getAmmo(self):
        '''This method returns the amount of ammo the player has left.'''
        return self.__ammo
    
    def playEmpty(self):
        '''This method plays a sound effect.'''
        self.__empty.set_volume(0.1)
        self.__empty.play()       
    
    def update(self):
        '''This method is called automatically to update the values it displays to the user. It also displays a game over message when the user has no lives left.'''
        if self.__lives == 0:
            self.__message = 'GAME OVER!'
            self.image = self.__font.render(self.__message, 1, (255, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.center = (320, 25)               
        else:
            self.__message = 'AMMO: ' + str(self.__ammo) + '                                  SCORE: ' + str(self.__points) + '                                  LIVES: ' + str(self.__lives)
            self.image = self.__font.render(self.__message, 1, (255, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.center = (320, 25)  

class Bullet(pygame.sprite.Sprite):
    '''This class defines the bullet sprite.'''
    def __init__(self, xPos, yPos):
        '''This intializer sets the position and loads the images of the bullet and ensures that it is static.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.__left = pygame.image.load('./Images/bulletLeft.png')
        self.__right = pygame.image.load('./Images/bulletRight.png')
        
        self.image = self.__left
        
        self.rect = self.image.get_rect()
        self.rect.centerx = xPos
        self.rect.bottom = yPos
        
        self.__dx = 0
    
    def shootRight(self):
        '''This method changes the image and direction of the bullet.'''
        self.image = self.__right
        self.__dx = 15
    
    def shootLeft(self):
        '''This method changes the image and direction of the bullet.'''
        self.image = self.__left
        self.__dx = -15     
    
    def update(self):
        '''This updates the position of the bullet.'''
        self.rect.centerx += self.__dx
        if self.rect.left < 0 or self.rect.right > 640:
            self.kill()

class AmmoPowerUp(pygame.sprite.Sprite):
    '''This class defines the ammo power up sprite.'''
    def __init__(self, screen):
        '''This intializer sets the image, position, and value of the ammo power up.'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./Images/ammo.png')
        self.__supplyDrop = pygame.mixer.Sound('./Audio/supplyDrop.wav')
        self.__cock = pygame.mixer.Sound('./Audio/cock.wav')
        
        self.rect = self.image.get_rect()
        
        # Set in such a position so that the player cannot collide with the powerup when they drop down from the screen after they die.
        self.rect.midbottom = (random.randint(40, 600), -100)
        
        self.__screen = screen
        
        self.__value = 7
        self.__dy = 0
        
    def getValue(self):
        '''This method returns the value of the ammo power up.'''
        return self.__value
    
    def spawn(self):
        '''This method allows the ammo power up to traverse downwards.'''
        self.__dy = 6
        if self.rect.bottom < 420:
            self.__supplyDrop.set_volume(0.1)
            self.__supplyDrop.play()                 
  
    def reset(self):
        '''This method resets the position of the ammo power up sprite.'''
        self.rect.midbottom = (random.randint(40, 600), -20)
        self.__dy = 0
    
    def playCock(self):
        '''This method plays a sound effect.'''
        self.__cock.set_volume(0.7)
        self.__cock.play()               

    def update(self):
        '''This method updates the position of the ammo power up sprite.'''
        self.rect.centery += self.__dy
        if self.rect.bottom >= 440:
            self.rect.bottom = 440

class LifePowerUp(pygame.sprite.Sprite):
    '''This class defines the life power up sprite.'''
    def __init__(self, screen):
        '''This intializer sets the image, position, and value of the ammo power up.'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./Images/health.png')
        self.__supplyDrop = pygame.mixer.Sound('./Audio/supplyDrop.wav')
        self.__yes = pygame.mixer.Sound('./Audio/yes.wav')
        
        self.rect = self.image.get_rect()
        
        # Ensures that the player cannot collide with the powerup when they drop down from the screen after they die.
        self.rect.midbottom = (random.randint(40, 600), -100)
        
        self.__screen = screen
        
        self.__dy = 0
    
    def spawn(self):
        '''This method allows the ammo power up to traverse downwards.'''
        self.__dy = 6
        if self.rect.bottom < 420:
            self.__supplyDrop.set_volume(0.1)
            self.__supplyDrop.play()                 
  
    def reset(self):
        '''This method resets the position of the life power up sprite.'''
        self.rect.midbottom = (random.randint(40, 600), -20)
        self.__dy = 0
    
    def playYes(self):
        '''This method plays a sound effect.'''
        self.__yes.set_volume(0.9)
        self.__yes.play()               
    
    def update(self):
        '''This method updates the position of the ammo power up sprite.'''
        self.rect.centery += self.__dy
        if self.rect.bottom >= 443:
            self.rect.bottom = 443

class Zombie(pygame.sprite.Sprite):
    '''This class defines the zombie sprite.'''
    def __init__(self, screen):
        '''This intializer sets the images and position of the zombie sprite.'''
        pygame.sprite.Sprite.__init__(self)
        
        self.__grunt = pygame.mixer.Sound('./Audio/grunt.wav')
        
        self.__aliveRightSprites = [] 
        self.__aliveLeftSprites = []
        
        # Loads images for zombie animation in a list.
        for imageNumber in range(5):
            image = pygame.image.load('./Images/zombieRight' + str(imageNumber + 1) + '.png')
            self.__aliveRightSprites.append(image)
        
        for imageNumber in range(5):
            image = pygame.image.load('./Images/zombieLeft' + str(imageNumber + 1) + '.png')
            self.__aliveLeftSprites.append(image)
   
        self.image = pygame.image.load('./Images/zombieRight1.png')
        
        self.__killed = False
        self.__right = False
        self.__left = False
        self.__maxHits = 1
        self.__currentHits = self.__maxHits
        
        self.__rightImage = 0
        self.__leftImage = 0 
        
        self.rect = self.image.get_rect()
        self.rect.center = (800, 440)
        
        self.__dx = 0
        self.__boost = 0
    
    def getKilled(self):
        '''Returns whether or not the zombie has been killed.'''
        return self.__killed
    
    def loseCurrentHits(self):
        '''This method decreases the number of hits the zombie currently has.'''
        self.__shot = True
        self.__currentHits -= 1
        if self.__currentHits <= 0:
            self.__killed = True
            self.__grunt.set_volume(0.4)
            self.__grunt.play()            
            
    def addMaxHits(self):
        '''This method increases the maximum number of hits the zombie can take.'''
        self.__maxHits += 1
    
    def addSpeed(self):
        '''This method increases the zombie's speed.'''
        self.__boost += 1
        
    def getCurrentHits(self):
        '''This method returns the current number of hits the zombie has left.'''
        return self.__currentHits
    
    def moveLeft(self):
        '''This method allows the zombie to move in a leftwards direction.'''
        if self.__dx >= -9:
            self.__dx = -6 - self.__boost
        self.__left = True
        self.__right = False
        
    def moveRight(self):
        '''This method allows the zombie to move in a rightwards direction.'''
        if self.__dx <= 9:
            self.__dx = 6 + self.__boost
        self.__right = True
        self.__left = False
    
    def reset(self):
        '''This method resets the zombie's position.'''
        self.image = pygame.image.load('./Images/zombieRight1.png')
        self.__killed = False
        self.__right = False
        self.__left = False        
        self.__currentHits = self.__maxHits 
        self.rect = self.image.get_rect()
        self.rect.center = (800, 440)
        self.__dx = 0

    def update(self):
        '''This method updates the position of the zombie.'''      
        if self.__currentHits > 0:
            self.__killed = False
            self.rect.centerx += self.__dx 
            
            # Cycles through list of images to animate movement.
            if self.__right:
                if self.__rightImage <= 4:
                    self.image = self.__aliveRightSprites[self.__rightImage]
                    self.__rightImage += 1
                else:
                    self.__rightImage = 0
            
            if self.__left:
                if self.__leftImage <= 4:
                    self.image = self.__aliveLeftSprites[self.__leftImage]
                    self.__leftImage += 1                
                else:
                    self.__leftImage = 0

        if self.rect.left < -160:
            self.rect.centerx = 600
        elif self.rect.right > 850:
            self.rect.centerx = 20