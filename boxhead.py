'''Author: Tyler Chen
   Date: 31/5/17
   Description: Budget Boxhead
                
   CONTROLS
   
   A - move left
   D - move right
   SPACE - shoot
   
   OBJECTIVE
   
   Earn as many points as you can before you lose all your lives! Points are earned when you kill a zombie or pick up an ammo or life power-up. 
   Lives are lost when a zombie makes contact with you so watch out! If this happens, you will drop down from the top of the screen and land on the roof of the building again. 
   Zombies gain more health and speed as the game progresses. The game ends when you have no lives left. Good luck!
'''

# Import and Initialize
import pygame, boxheadSprites, random
pygame.mixer.init()
pygame.init()

def main():
    '''This function defines the 'mainline logic' for our game.'''
      
    # Display
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Budget Boxhead')
     
    # Entities
    background = pygame.image.load('./Images/background.jpg')
    screen.blit(background, (0, 0))

    # Background music
    pygame.mixer.music.load('./Audio/music.mp3')
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)      
     
    # Sprites
    player = boxheadSprites.Player(screen)
    zombie = boxheadSprites.Zombie(screen)
    statkeeper = boxheadSprites.StatKeeper()
    ammoPU = boxheadSprites.AmmoPowerUp(screen)
    ammoPUGroup = pygame.sprite.Group()
    lifePU = boxheadSprites.LifePowerUp(screen)
    lifePUGroup = pygame.sprite.Group()    
    bullets = pygame.sprite.Group()
    allSprites = pygame.sprite.Group(player, zombie, statkeeper)
 
    # ACTION
     
    # Assign 
    clock = pygame.time.Clock()
    keepGoing = True
    collectedAmmo = False
    existingAmmo = False
    collectedLife = False
    existingLife = False
    addedHits = False
    addedSpeed = False
    lastFire = pygame.time.get_ticks()
    cooldown = 1000
 
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
 
    # Loop
    while keepGoing:
     
        # Time
        clock.tick(30)
     
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.moveLeft()              
                elif event.key == pygame.K_d:
                    player.moveRight()
                elif event.key == pygame.K_SPACE:
                    now = pygame.time.get_ticks()
                    # Ensures that fire rate is limited, prevents the player from "spamming" bullets.
                    if player.getRight() and statkeeper.getAmmo() > 0 and now - lastFire >= cooldown:
                        lastFire = now
                        bullet = boxheadSprites.Bullet(player.rect.centerx, player.rect.centery + 5)
                        bullet.shootRight()
                        statkeeper.loseAmmo()
                        bullets.add(bullet)
                        allSprites = pygame.sprite.Group(player, zombie, statkeeper, bullets, ammoPUGroup, lifePUGroup)
                    elif player.getLeft() and statkeeper.getAmmo() > 0 and now - lastFire >= cooldown:
                        lastFire = now
                        bullet = boxheadSprites.Bullet(player.rect.centerx , player.rect.centery + 5)
                        bullet.shootLeft()
                        statkeeper.loseAmmo()
                        bullets.add(bullet)
                        allSprites = pygame.sprite.Group(player, zombie, statkeeper, bullets, ammoPUGroup, lifePUGroup)
                    elif statkeeper.getAmmo() <= 0:
                        statkeeper.playEmpty()
        
        # Controls zombie movement.
        if player.getXPos() < 500:
            zombie.moveLeft()
        else:
            zombie.moveRight()
        
        # Resets the player and subtracts a life from them if a zombie collides with them.
        if zombie.rect.colliderect(player.rect):
            statkeeper.loseLife()
            player.playDeath()
            player.reset()
        
        # Subtracts health from the zombie if it is hit by a bullet. If the zombie dies, it is reset off screen.
        if pygame.sprite.spritecollide(zombie, bullets, False):
            bullet.kill()
            zombie.loseCurrentHits()
            if zombie.getKilled():
                statkeeper.gainPoints()
                addedHits = False
                addedSpeed = False
                zombie.reset()
        
        # If the player's score is divisible by 10 and not equal to zero, the zombie's health will increase.
        if (statkeeper.getPoints() % 10 == 0 and statkeeper.getPoints() != 0) and addedHits == False:
            zombie.addMaxHits()
            addedHits = True
        
        # If the player's score is divisible by 30 and not equal to zero, the zombie's speed will increase.
        if (statkeeper.getPoints() % 30 == 0 and statkeeper.getPoints() != 0) and addedSpeed == False:
            zombie.addSpeed()
            addedSpeed = True
        
        # If there is no ammo power-up on currently on screen and the player's score is divisible by 4 and not equal to zero, an ammo power-up will spawn.
        if (statkeeper.getPoints() % 4 == 0 and statkeeper.getPoints() != 0) and existingAmmo == False:
            ammoPU.spawn()
            ammoPUGroup.add(ammoPU)
            allSprites = pygame.sprite.Group(player, zombie, statkeeper, bullets, ammoPUGroup, lifePUGroup)
            collectedAmmo = False
            existingAmmo = True
        
        # If the player collides with the ammo power-up, they will gain a random amount of ammo.
        if player.rect.colliderect(ammoPU.rect) and collectedAmmo == False:
            ammoPU.playCock()
            statkeeper.gainAmmo(ammoPU.getValue())
            statkeeper.gainPoints()
            ammoPU.reset()
            ammoPU.kill()
            collectedAmmo = True
            existingAmmo = False
        
        # If there is no life power-up currently on screen and the player's score is divisible by 20 and not equal to zero, a life power-up will spawn.
        if (statkeeper.getPoints() % 20 == 0 and statkeeper.getPoints() != 0) and existingLife == False:
            lifePU.spawn()
            lifePUGroup.add(lifePU)
            allSprites = pygame.sprite.Group(player, zombie, statkeeper, bullets, ammoPUGroup, lifePUGroup)
            collectedLife = False
            existingLife = True
        
        # If the player collides with the life power-up, they will gain a life.
        if player.rect.colliderect(lifePU.rect) and collectedLife == False:
            lifePU.playYes()
            statkeeper.gainLife()
            statkeeper.gainPoints()
            lifePU.reset()
            lifePU.kill()
            collectedLife = True
            existingLife = False
        
        # If the player has no lives left, the game will end.
        if statkeeper.getLives() == 0:
            keepGoing = False

        # Refresh screen
        screen.blit(background, (0, 0))
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
         
    # Unhide mouse pointer
    pygame.mouse.set_visible(True)
 
    # Close the game window
    pygame.time.delay(3000)
    pygame.quit()   
     
# Call the main function
main()