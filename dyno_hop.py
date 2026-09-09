import pygame
import random
import math
import json
import os

pygame.init()

# ============================================================
#  DINO —  VERSION 6,700,000
# One-file arcade runner. No external assets required.
# Controls:
#   SPACE / UP = jump
#   DOWN       = duck / fast-fall
#   ESC        = pause
#   R          = restart after death
#   M          = menu
# ============================================================

WIDTH, HEIGHT = 1200, 700
FPS = 144
GROUND_Y = 565
SAVE_FILE = "dino_save.json"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" DINO — ,700,000")
clock = pygame.time.Clock()

# Colors
WHITE=(245,247,250); BLACK=(10,12,17); BG=(18,21,30); PANEL=(29,34,47)
GRAY=(145,153,170); DARK=(55,62,78); GREEN=(89,225,137); RED=(255,82,105)
YELLOW=(255,211,90); BLUE=(87,166,255); CYAN=(79,228,232); PURPLE=(183,116,255)
ORANGE=(255,151,73); GOLD=(255,196,55)

FONT_TINY=pygame.font.SysFont("consolas",16)
FONT_SMALL=pygame.font.SysFont("consolas",21)
FONT=pygame.font.SysFont("consolas",28,bold=True)
FONT_BIG=pygame.font.SysFont("consolas",48,bold=True)
FONT_HUGE=pygame.font.SysFont("consolas",70,bold=True)

DEFAULT_SAVE={
    "high_score":0,
    "coins":0,
    "xp":0,
    "level":1,
    "owned_skins":["classic"],
    "selected_skin":"classic",
    "achievements":[],
    "stats":{"runs":0,"deaths":0,"coins":0,"near_misses":0},
    "settings":{"particles":True,"shake":True}
}

SKINS={
    "classic":{"name":"Classic","price":0,"color":GREEN},
    "blue":{"name":"Cyber","price":40,"color":BLUE},
    "gold":{"name":"Golden","price":120,"color":GOLD},
    "void":{"name":"Void","price":250,"color":PURPLE},
}
SKIN_ORDER=list(SKINS)

def fresh_save():
    # JSON round-trip gives us a clean deep copy.
    return json.loads(json.dumps(DEFAULT_SAVE))

def load_save():
    data=fresh_save()
    try:
        with open(SAVE_FILE,"r",encoding="utf-8") as f:
            old=json.load(f)
        for k,v in old.items():
            if isinstance(v,dict) and isinstance(data.get(k),dict):
                data[k].update(v)
            else:
                data[k]=v
    except Exception:
        pass
    if data.get("selected_skin") not in SKINS:
        data["selected_skin"]="classic"
    return data

save=load_save()

def save_game():
    try:
        with open(SAVE_FILE,"w",encoding="utf-8") as f:
            json.dump(save,f,indent=4)
    except OSError:
        pass

def text(s,font,color,x,y,center=False):
    img=font.render(str(s),True,color)
    r=img.get_rect()
    if center:r.center=(x,y)
    else:r.topleft=(x,y)
    screen.blit(img,r)
    return r

def clamp(v,a,b): return max(a,min(b,v))

def level_from_xp(xp):
    return 1 + int(math.sqrt(max(0,xp)/45))

def unlock(name):
    if name not in save["achievements"]:
        save["achievements"].append(name)
        return True
    return False

class Particle:
    def __init__(self,x,y,color):
        self.p=pygame.Vector2(x,y)
        ang=random.uniform(0,math.tau); sp=random.uniform(80,300)
        self.v=pygame.Vector2(math.cos(ang),math.sin(ang))*sp
        self.life=random.uniform(.25,.65); self.max=self.life
        self.color=color; self.r=random.randint(2,5)
    def update(self,dt):
        self.p+=self.v*dt; self.v.y+=350*dt; self.life-=dt
    def draw(self,offset):
        if self.life<=0:return
        a=int(255*self.life/self.max)
        surf=pygame.Surface((14,14),pygame.SRCALPHA)
        pygame.draw.circle(surf,(*self.color,a),(7,7),self.r)
        screen.blit(surf,(self.p.x-7+offset[0],self.p.y-7+offset[1]))

class Dino:
    def __init__(self):
        self.x=180; self.y=GROUND_Y-64
        self.w=52; self.h=64; self.vy=0
        self.on_ground=True; self.duck=False
        self.anim=0
    def rect(self):
        if self.duck and self.on_ground:
            return pygame.Rect(self.x,self.y+28,72,36)
        return pygame.Rect(self.x+5,self.y+5,self.w-10,self.h-7)
    def jump(self):
        if self.on_ground:
            self.vy=-770; self.on_ground=False; self.duck=False
    def update(self,dt,down):
        self.duck=down and self.on_ground
        gravity=2350
        if down and not self.on_ground:self.vy+=gravity*1.4*dt
        self.vy+=gravity*dt
        self.y+=self.vy*dt
        floor=GROUND_Y-self.h
        if self.y>=floor:
            self.y=floor; self.vy=0; self.on_ground=True
        self.anim+=dt
    def draw(self,offset):
        c=SKINS[save["selected_skin"]]["color"]
        x=int(self.x+offset[0]); y=int(self.y+offset[1])
        if self.duck and self.on_ground:
            pygame.draw.rect(screen,c,(x,y+30,67,31),border_radius=9)
            pygame.draw.rect(screen,c,(x+48,y+19,31,29),border_radius=7)
            pygame.draw.circle(screen,WHITE,(x+68,y+27),4)
            pygame.draw.line(screen,c,(x+4,y+48),(x-18,y+37),8)
        else:
            # tail/body/head
            pygame.draw.polygon(screen,c,[(x+10,y+36),(x-22,y+25),(x+7,y+48)])
            pygame.draw.rect(screen,c,(x+4,y+24,38,37),border_radius=9)
            pygame.draw.rect(screen,c,(x+28,y+2,36,32),border_radius=7)
            pygame.draw.circle(screen,WHITE,(x+53,y+11),4)
            # tiny arm
            pygame.draw.line(screen,c,(x+35,y+37),(x+51,y+42),6)
            # legs animate
            phase=int(self.anim*12)%2
            if not self.on_ground: phase=0
            if phase==0:
                pygame.draw.line(screen,c,(x+16,y+56),(x+9,y+68),8)
                pygame.draw.line(screen,c,(x+32,y+56),(x+40,y+68),8)
            else:
                pygame.draw.line(screen,c,(x+16,y+56),(x+24,y+68),8)
                pygame.draw.line(screen,c,(x+32,y+56),(x+27,y+68),8)

class Obstacle:
    def __init__(self,score):
        self.kind=random.choices(["cactus","double","bird"],[55,25,20])[0]
        self.x=WIDTH+50
        if self.kind=="cactus":
            self.w=random.randint(28,42); self.h=random.randint(55,82); self.y=GROUND_Y-self.h
        elif self.kind=="double":
            self.w=67; self.h=62; self.y=GROUND_Y-self.h
        else:
            self.w=58; self.h=35
            self.y=random.choice([GROUND_Y-42,GROUND_Y-92,GROUND_Y-145])
        self.passed=False
    def rect(self):
        return pygame.Rect(int(self.x)+3,int(self.y)+3,self.w-6,self.h-5)
    def update(self,dt,speed): self.x-=speed*dt
    def draw(self,offset):
        x=int(self.x+offset[0]); y=int(self.y+offset[1])
        if self.kind=="bird":
            pygame.draw.ellipse(screen,RED,(x,y,self.w,self.h))
            flap=math.sin(pygame.time.get_ticks()*.02)*8
            pygame.draw.polygon(screen,ORANGE,[(x+20,y+18),(x+5,y-8+flap),(x+31,y+13)])
            pygame.draw.circle(screen,WHITE,(x+45,y+10),4)
        else:
            pygame.draw.rect(screen,GREEN,(x,y,self.w,self.h),border_radius=5)
            if self.kind=="double":
                pygame.draw.rect(screen,GREEN,(x+37,y-24,25,self.h+24),border_radius=5)
            else:
                pygame.draw.rect(screen,GREEN,(x-10,y+22,15,11),border_radius=4)
                pygame.draw.rect(screen,GREEN,(x-10,y+9,8,24),border_radius=4)

class Coin:
    def __init__(self):
        self.x=WIDTH+50; self.y=random.randint(360,GROUND_Y-65)
        self.r=12
    def rect(self): return pygame.Rect(self.x-self.r,self.y-self.r,24,24)
    def update(self,dt,speed): self.x-=speed*dt
    def draw(self,offset):
        x=int(self.x+offset[0]); y=int(self.y+offset[1])
        w=max(5,int(20*abs(math.sin(pygame.time.get_ticks()*.01))))
        pygame.draw.ellipse(screen,GOLD,(x-w//2,y-13,w,26))
        pygame.draw.ellipse(screen,YELLOW,(x-w//3,y-9,max(3,w*2//3),18),2)

class Game:
    def __init__(self):
        self.state="menu"
        self.shop_index=0
        self.notice=""; self.notice_t=0
        self.reset()
    def reset(self):
        self.dino=Dino(); self.obstacles=[]; self.coins=[]
        self.particles=[]; self.score=0; self.run_coins=0
        self.distance=0; self.speed=430; self.spawn=1.0
        self.coin_spawn=2.0; self.shake=0; self.combo=0
        self.near=0; self.boss=False; self.boss_left=0
        self.day=0.0
    def start(self):
        self.reset(); self.state="playing"; save["stats"]["runs"]+=1
    def burst(self,x,y,color,n=15):
        if save["settings"]["particles"]:
            for _ in range(n):self.particles.append(Particle(x,y,color))
    def die(self):
        save["stats"]["deaths"]+=1
        save["high_score"]=max(save["high_score"],int(self.score))
        earned=int(self.score*.6)+self.run_coins*2
        save["xp"]+=earned
        save["level"]=level_from_xp(save["xp"])
        if self.score>=10:unlock("10 CLUB")
        if self.score>=25:unlock("DINO MENACE")
        if self.score>=50:unlock("EXTINCTION WHO?")
        if self.near>=5:unlock("EDGE LORD")
        save_game(); self.state="dead"
    def update(self,dt):
        if self.notice_t>0:self.notice_t-=dt
        if self.state!="playing":return

        keys=pygame.key.get_pressed()
        down=keys[pygame.K_DOWN] or keys[pygame.K_s]
        self.dino.update(dt,down)
        self.day+=dt
        self.distance+=self.speed*dt
        self.speed=min(900,430+self.score*7+self.distance/900)
        self.spawn-=dt; self.coin_spawn-=dt

        if self.spawn<=0:
            self.obstacles.append(Obstacle(self.score))
            # Slightly tighter spawns as the run gets faster, but never unfairly tiny.
            self.spawn=random.uniform(0.95,1.45)*clamp(520/self.speed,.65,1.0)

        if self.coin_spawn<=0:
            if random.random()<.72:self.coins.append(Coin())
            self.coin_spawn=random.uniform(1.6,3.0)

        br=self.dino.rect()
        for o in self.obstacles[:]:
            o.update(dt,self.speed)
            if br.colliderect(o.rect()):
                self.burst(self.dino.x+25,self.dino.y+35,RED,25)
                if save["settings"]["shake"]:self.shake=12
                self.die(); return
            if not o.passed and o.x+o.w<self.dino.x:
                o.passed=True; self.score+=1; self.combo+=1
                # Near miss if vertical geometry was close when passed.
                if o.kind=="bird":
                    gap=abs(br.centery-o.rect().centery)
                    if gap<80:self.near+=1; save["stats"]["near_misses"]+=1
                if self.score%10==0:
                    self.notice=f"SPEED UP!  SCORE {self.score}"; self.notice_t=1.5
                if self.score>0 and self.score%25==0:
                    self.boss=True; self.boss_left=5
                    self.notice="BOSS RUSH — SURVIVE 5!"; self.notice_t=2.0
                if self.boss:
                    self.boss_left-=1
                    if self.boss_left<=0:
                        self.boss=False; save["coins"]+=10; self.run_coins+=10
                        self.notice="BOSS CLEARED +10 COINS"; self.notice_t=2
            if o.x<-120:self.obstacles.remove(o)

        for c in self.coins[:]:
            c.update(dt,self.speed)
            if br.colliderect(c.rect()):
                self.coins.remove(c); self.run_coins+=1; save["coins"]+=1
                save["stats"]["coins"]+=1
                self.burst(c.x,c.y,GOLD,12)
                continue
            if c.x<-40:self.coins.remove(c)

        for p in self.particles:p.update(dt)
        self.particles=[p for p in self.particles if p.life>0]
        self.shake=max(0,self.shake-30*dt)

    def event(self,e):
        if e.type!=pygame.KEYDOWN:return
        if self.state=="menu":
            if e.key in (pygame.K_SPACE,pygame.K_RETURN):self.start()
            elif e.key==pygame.K_g:self.state="shop"
            elif e.key==pygame.K_a:self.state="achievements"
            elif e.key==pygame.K_s:self.state="settings"
        elif self.state=="playing":
            if e.key in (pygame.K_SPACE,pygame.K_UP,pygame.K_w):self.dino.jump()
            elif e.key==pygame.K_ESCAPE:self.state="paused"
        elif self.state=="paused":
            if e.key==pygame.K_ESCAPE:self.state="playing"
            elif e.key==pygame.K_r:self.start()
            elif e.key==pygame.K_m:self.state="menu"
        elif self.state=="dead":
            if e.key==pygame.K_r:self.start()
            elif e.key==pygame.K_m:self.state="menu"
        elif self.state=="shop":
            if e.key==pygame.K_ESCAPE:self.state="menu"
            elif e.key in (pygame.K_LEFT,pygame.K_a):self.shop_index=(self.shop_index-1)%len(SKIN_ORDER)
            elif e.key in (pygame.K_RIGHT,pygame.K_d):self.shop_index=(self.shop_index+1)%len(SKIN_ORDER)
            elif e.key in (pygame.K_RETURN,pygame.K_SPACE):
                sid=SKIN_ORDER[self.shop_index]; item=SKINS[sid]
                if sid in save["owned_skins"]:
                    save["selected_skin"]=sid
                elif save["coins"]>=item["price"]:
                    save["coins"]-=item["price"]; save["owned_skins"].append(sid); save["selected_skin"]=sid
                save_game()
        elif self.state=="achievements":
            if e.key==pygame.K_ESCAPE:self.state="menu"
        elif self.state=="settings":
            if e.key==pygame.K_ESCAPE:self.state="menu"
            elif e.key==pygame.K_1:
                save["settings"]["particles"]=not save["settings"]["particles"]; save_game()
            elif e.key==pygame.K_2:
                save["settings"]["shake"]=not save["settings"]["shake"]; save_game()

    def bg(self):
        # Day/night smoothly shifts with time.
        t=(math.sin(self.day*.09)+1)/2
        col=(int(18+55*t),int(21+80*t),int(30+105*t))
        screen.fill(col)
        # moon/sun
        orb=YELLOW if t>.5 else WHITE
        pygame.draw.circle(screen,orb,(1010,105),38)
        # parallax mountains
        off=int(self.distance*.08)%360
        for x in range(-360-off,WIDTH+400,360):
            pygame.draw.polygon(screen,(35,49,62),[(x,GROUND_Y),(x+180,300),(x+360,GROUND_Y)])
        # ground
        pygame.draw.rect(screen,(38,43,50),(0,GROUND_Y,WIDTH,HEIGHT-GROUND_Y))
        pygame.draw.line(screen,WHITE,(0,GROUND_Y),(WIDTH,GROUND_Y),3)
        road=int(self.distance)%70
        for x in range(-road,WIDTH,70):
            pygame.draw.line(screen,DARK,(x,GROUND_Y+34),(x+32,GROUND_Y+34),4)

    def hud(self):
        text(f"SCORE {int(self.score)}",FONT,WHITE,25,20)
        text(f"BEST {save['high_score']}",FONT_SMALL,GRAY,25,58)
        text(f"COINS {save['coins']}",FONT_SMALL,GOLD,25,86)
        text(f"LVL {save['level']}",FONT_SMALL,CYAN,WIDTH-150,20)
        text(f"{int(self.speed)} px/s",FONT_TINY,GRAY,WIDTH-150,55)
        if self.boss:text(f"BOSS {self.boss_left}",FONT,RED,WIDTH//2,35,True)
        if self.notice_t>0:text(self.notice,FONT,YELLOW,WIDTH//2,115,True)

    def draw_playfield(self):
        self.bg()
        off=(0,0)
        if self.shake>0 and save["settings"]["shake"]:
            off=(random.randint(-int(self.shake),int(self.shake)),random.randint(-int(self.shake),int(self.shake)))
        for c in self.coins:c.draw(off)
        for o in self.obstacles:o.draw(off)
        self.dino.draw(off)
        for p in self.particles:p.draw(off)
        self.hud()

    def draw(self):
        if self.state in ("playing","paused","dead"):
            self.draw_playfield()
        else:
            self.bg()

        if self.state=="menu":
            text(" DINO",FONT_HUGE,WHITE,WIDTH//2,125,True)
            text(" VERSION 6,700,000",FONT, PURPLE,WIDTH//2,195,True)
            # preview dino
            self.dino.draw((WIDTH//2-self.dino.x-25,290-self.dino.y))
            lines=["SPACE = PLAY","G = SKIN SHOP","A = ACHIEVEMENTS","S = SETTINGS"]
            for i,line in enumerate(lines):
                text(line,FONT, CYAN if i==0 else WHITE,WIDTH//2,410+i*48,True)
            text(f"BEST {save['high_score']}   •   COINS {save['coins']}   •   LVL {save['level']}",FONT_SMALL,GOLD,WIDTH//2,625,True)

        elif self.state=="paused":
            shade=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); shade.fill((0,0,0,170)); screen.blit(shade,(0,0))
            text("PAUSED",FONT_HUGE,WHITE,WIDTH//2,250,True)
            text("ESC resume   •   R restart   •   M menu",FONT_SMALL,CYAN,WIDTH//2,350,True)

        elif self.state=="dead":
            shade=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); shade.fill((0,0,0,185)); screen.blit(shade,(0,0))
            text("EXTINCT 💀",FONT_HUGE,RED,WIDTH//2,180,True)
            text(f"SCORE {self.score}",FONT_BIG,WHITE,WIDTH//2,285,True)
            text(f"RUN COINS {self.run_coins}   •   NEAR MISSES {self.near}",FONT_SMALL,GOLD,WIDTH//2,360,True)
            text("R = AGAIN     M = MENU",FONT,CYAN,WIDTH//2,460,True)

        elif self.state=="shop":
            text("SKIN SHOP",FONT_HUGE,WHITE,WIDTH//2,100,True)
            sid=SKIN_ORDER[self.shop_index]; item=SKINS[sid]
            pygame.draw.circle(screen,item["color"],(WIDTH//2,310),75)
            owned=sid in save["owned_skins"]
            status="OWNED — SPACE TO EQUIP" if owned else f"{item['price']} COINS — SPACE TO BUY"
            if save["selected_skin"]==sid:status="EQUIPPED"
            text(item["name"],FONT_BIG,item["color"],WIDTH//2,425,True)
            text(status,FONT_SMALL,GOLD,WIDTH//2,485,True)
            text("← / → browse     ESC back",FONT_SMALL,WHITE,WIDTH//2,575,True)
            text(f"Wallet: {save['coins']}",FONT_SMALL,GOLD,WIDTH//2,620,True)

        elif self.state=="achievements":
            text("ACHIEVEMENTS",FONT_HUGE,WHITE,WIDTH//2,90,True)
            all_a=["10 CLUB","DINO MENACE","EXTINCTION WHO?","EDGE LORD"]
            for i,a in enumerate(all_a):
                got=a in save["achievements"]
                text(("✓ " if got else "□ ")+a,FONT,GREEN if got else GRAY,WIDTH//2,240+i*65,True)
            text("ESC = back",FONT_SMALL,WHITE,WIDTH//2,590,True)

        elif self.state=="settings":
            text("SETTINGS",FONT_HUGE,WHITE,WIDTH//2,110,True)
            p="ON" if save["settings"]["particles"] else "OFF"
            s="ON" if save["settings"]["shake"] else "OFF"
            text(f"1 = PARTICLES: {p}",FONT,WHITE,WIDTH//2,290,True)
            text(f"2 = SCREEN SHAKE: {s}",FONT,WHITE,WIDTH//2,360,True)
            text("ESC = back",FONT_SMALL,GRAY,WIDTH//2,500,True)

game=Game()
running=True
while running:
    dt=min(clock.tick(FPS)/1000,0.033)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:running=False
        else:game.event(event)
    game.update(dt)
    game.draw()
    pygame.display.flip()

save_game()
pygame.quit()
