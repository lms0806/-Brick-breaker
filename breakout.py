import sys, pygame, random,time
from time import localtime,strftime
from pygame.locals import *
from time import sleep

class Breakout():
   def main(self):
      xspeed_init = 3  #x방향 공스피드
      yspeed_init = 3  #y방향 공 스피드
      max_lives = 5    #최대 생명력=5
      paddle_speed = 30   #막대기 스피드
      score = 0        #점수
      black = (0,0,0)  # 배경색
      GREEN = (0,255,0)   #점수 색깔
      WHITE = (255,255,255)
      width=640        #게임판 옆길이
      height=480       #게임판 높이
      size = width, height #게임판 크기

      pygame.init()     #필수
      screen = pygame.display.set_mode(size)  #게임판 만들기
      #screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

      gamestart=pygame.image.load("GAMESTART.png").convert()
      gamestartrect=gamestart.get_rect()

      paddle = pygame.image.load("stick.png").convert()
      paddlerect = paddle.get_rect()#막대기 만들기
      
      ball = pygame.image.load("ball.png").convert()
      ball.set_colorkey((255, 255, 255))
      ballrect = ball.get_rect()#공 만들기

      pong = pygame.mixer.Sound('Blip_1-Surround-147.wav')
      pong.set_volume(10)
      
      wall = Wall()           #벽돌
      wall.build_wall(width)  #벽돌 길이=맵길이
      
      # 게임 준비
      screen.blit(gamestart,(0,0))
      pygame.display.update()
      time.sleep(10)
      
      paddlerect = paddlerect.move((width / 2) - (paddlerect.right / 2), height - 20)#패들 위치 선정
      ballrect = ballrect.move(width / 2 , height / 2 )#공 위치 선정       
      xspeed = xspeed_init
      yspeed = yspeed_init
      lives = max_lives                 #최대 수명
      clock = pygame.time.Clock()
      pygame.key.set_repeat(1,30)       # 키 이동의 자연스러움       
      pygame.mouse.set_visible(0)      # 마우스 숨기기
      while 1:
         # 초당 60
         clock.tick(60)
         # 키 입력
         for event in pygame.event.get():
               if event.type == pygame.QUIT:
                  pygame.exit()
                  sys.exit()
               if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_ESCAPE:
                      sys.exit()
                  if event.key == pygame.K_LEFT:                        
                     paddlerect = paddlerect.move(-paddle_speed, 0)     
                     if (paddlerect.left < 0):                           
                           paddlerect.left = 0      
                  if event.key == pygame.K_RIGHT:                    
                     paddlerect = paddlerect.move(paddle_speed, 0)
                     if (paddlerect.right > width):                            
                           paddlerect.right = width
                              
         # 막대기가 공을 치는지 확인   
         if ballrect.bottom >= paddlerect.top and \
               ballrect.bottom <= paddlerect.bottom and \
               ballrect.right >= paddlerect.left and \
               ballrect.left <= paddlerect.right:
               yspeed = -yspeed                
               pong.play(0)
               
               offset = ballrect.center[0] - paddlerect.center[0]                          
               # offset > 0 means ball has hit RHS of paddle                   
               # 공이 막대기를 치는 위치에 따른 각도 변화                     
               if offset > 0:
                  if offset > 30:  
                     xspeed = 7
                  elif offset > 23:                 
                     xspeed = 6
                  elif offset > 17:
                     xspeed = 5 
               else:  
                  if offset < -30:                             
                     xspeed = -7
                  elif offset < -23:
                     xspeed = -6
                  elif xspeed < -17:
                     xspeed = -5     
                     
         # move paddle/ball
         ballrect = ballrect.move(xspeed, yspeed)
         if ballrect.left < 0 or ballrect.right > width:
               xspeed = -xspeed                
               pong.play(0)
         if ballrect.top < 0:
               yspeed = -yspeed                
               pong.play(0)
               
         # 공이 패들을 지나쳣는지 확인 - 목숨 깍임
         if ballrect.top > height:
               lives -= 1
               # 목숨이 깍였을때 새로운공 생김
               xspeed = xspeed_init
               rand = random.random()                
               if random.random() > 0.5:
                  xspeed = -xspeed 
               yspeed = yspeed_init            
               ballrect.center = width * random.random(), height / 2                                
               if lives == 0:                    
                  msg = pygame.font.Font(None,70).render("Game Over", True, (255,255,255))
                  msgrect = msg.get_rect()#게임오버 메시지 출력
                  msgrect = msgrect.move(width / 2 - (msgrect.center[0]), height / 3)#게임오버 메시지 위치
                  screen.blit(msg, msgrect)
                  pygame.display.flip()
                  #점수 저장
                  f=open("점수.txt","a")
                  f.write(strftime("%Y/%D %I:%M:%S",localtime()))
                  f.write("에 플레이한 플레이어의 점수는")
                  f.write(str(score))
                  f.write("입니다")
                  f.write("\n")
                  f.close()
                  
                  # process key presses
                  #     - ESC to quit
                  #     - any other key to restart game
                  while 1:
                     restart = False
                     for event in pygame.event.get():
                           if event.type == pygame.QUIT:
                              sys.exit()
                           if event.type == MOUSEBUTTONDOWN:
                              restart=True
                           if event.type == pygame.KEYDOWN:
                              if event.key == pygame.K_ESCAPE:
                                 pygame.exit()
                                 sys.exit()
                              if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                                 restart = True
                     if restart:#죽고 재시작
                           screen.fill(black)
                           wall.build_wall(width)
                           lives = max_lives
                           score = 0
                           break
                        
         if xspeed < 0 and ballrect.left < 0:
               xspeed = -xspeed                                
               pong.play(0)
         if xspeed > 0 and ballrect.right > width:
               xspeed = -xspeed                               
               pong.play(0)
               
         # 공이 벽돌에 부딪혔는지 확인하고 벽돌을 삭제하고 볼 방향을 변경
         index = ballrect.collidelist(wall.brickrect)       
         if index != -1: 
               if ballrect.center[0] > wall.brickrect[index].right or ballrect.center[0] < wall.brickrect[index].left:
                  xspeed = -xspeed
               else:
                  yspeed = -yspeed
               pong.play(0)
               wall.brickrect[index:index + 1] = []
               score += 1

         screen.fill(black)
         lifetext = pygame.font.Font(None,40).render(str(lives), True, (0,255,0), black)#생명력
         lifetextrect = lifetext.get_rect()
         lifetextrect = lifetextrect.move(width/2 - lifetextrect.right, 0)
         screen.blit(lifetext, lifetextrect)
         
         scoretext = pygame.font.Font(None,40).render(str(score), True, (0,255,0), black)#점수
         scoretextrect = scoretext.get_rect()
         scoretextrect = scoretextrect.move(width - scoretextrect.right, 0)
         screen.blit(scoretext, scoretextrect)
         
         for i in range(0, len(wall.brickrect)):
               screen.blit(wall.brick, wall.brickrect[i])    

         # 클리어 후
         if wall.brickrect == []:
               lives=max_lives
               wall.build_wall(width)                 
               xspeed = xspeed_init
               yspeed = yspeed_init                
               ballrect.center = width / 2, height / 3
               
         screen.blit(ball, ballrect)
         screen.blit(paddle, paddlerect)
         pygame.display.flip()
   
class Wall():
    def __init__(self):
        self.brick = pygame.image.load("wall.png").convert()
        brickrect = self.brick.get_rect()#벽돌 그리기
        self.bricklength = brickrect.right - brickrect.left       
        self.brickheight = brickrect.bottom - brickrect.top             
    def build_wall(self, width):        
        xpos = 0
        ypos = 60
        adj = 0
        self.brickrect = []
        for i in range (0, 52):           
            if xpos > width:
                if adj == 0:
                    adj = self.bricklength / 2
                else:
                    adj = 0
                xpos = -adj
                ypos += self.brickheight
                
            self.brickrect.append(self.brick.get_rect())    
            self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
            xpos = xpos + self.bricklength

if __name__ == '__main__':
   br = Breakout()
   br.main()
    
