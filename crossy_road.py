import pygame, random, math, json

pygame.init()

# ============================================================
#  CROSSY ROAD —  VERSION 100,000,000
# Smooth hopping + camera easing + powerups + missions + weather
# No external assets required.
#
# Controls:
#   WASD / ARROWS = move
#   ESC           = pause
#   R             = restart after death
#   M             = menu
# ============================================================

W, H = 1100, 760
FPS = 144
TILE = 55
COLS = W // TILE
PLAYER_Y = H - 150
SAVE_FILE = "crossy_save.json"

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption(" CROSSY ROAD — ,000,000")
clock = pygame.time.Clock()

WHITE=(245,247,250); BLACK=(12,14,18); GRAY=(135,145,158)
GRASS=(72,166,82); GRASS2=(63,150,74); ROAD=(55,58,66); LINE=(235,218,115)
WATER=(48,132,190); RAIL=(89,75,68); BROWN=(121,78,46)
RED=(242,77,89); BLUE=(67,142,235); YELLOW=(250,201,70); CYAN=(67,220,225)
PURPLE=(177,105,232); ORANGE=(242,139,58); GOLD=(255,190,45)
PINK=(255,118,190); ICE=(130,210,235)

SMALL=pygame.font.SysFont("arial",18,bold=True)
FONT=pygame.font.SysFont("arial",26,bold=True)
BIG=pygame.font.SysFont("arial",48,bold=True)
HUGE=pygame.font.SysFont("arial",68,bold=True)

DEFAULT={
    "best":0,"coins":0,"xp":0,"level":1,
    "owned":["chicken"],"skin":"chicken",
    "achievements":[],
    "stats":{"runs":0,"deaths":0,"coins":0,"powerups":0},
    "settings":{"particles":True,"weather":True,"screen_shake":True}
}

SKINS={
    "chicken":{"name":"CHICKEN","price":0,"color":WHITE},
    "frog":{"name":"FROG","price":50,"color":(85,230,100)},
    "duck":{"name":"DUCK","price":110,"color":YELLOW},
    "robot":{"name":"ROBOT","price":220,"color":CYAN},
    "void":{"name":"VOID BIRD","price":400,"color":PURPLE},
    "ice":{"name":"FROSTY","price":650,"color":ICE},
}
ORDER=list(SKINS)

def fresh(): return json.loads(json.dumps(DEFAULT))

def load():
    d=fresh()
    try:
        with open(SAVE_FILE,"r",encoding="utf8") as f:
            old=json.load(f)
        for k,v in old.items():
            if isinstance(v,dict) and isinstance(d.get(k),dict):
                d[k].update(v)
            else:
                d[k]=v
    except Exception:
        pass
    if d.get("skin") not in SKINS:d["skin"]="chicken"
    return d

save=load()

def save_game():
    try:
        with open(SAVE_FILE,"w",encoding="utf8") as f:
            json.dump(save,f,indent=4)
    except OSError:
        pass

def txt(s,font,c,x,y,center=False):
    im=font.render(str(s),True,c)
    r=im.get_rect()
    if center:r.center=(x,y)
    else:r.topleft=(x,y)
    screen.blit(im,r)

def clamp(v,a,b): return max(a,min(b,v))
def lerp(a,b,t): return a+(b-a)*t
def ease_out_cubic(t): return 1-(1-t)**3
def lvl(): return 1+int(math.sqrt(max(0,save["xp"])/70))

class Particle:
    def __init__(self,x,y,c,kind="burst"):
        self.x=x;self.y=y;self.c=c;self.kind=kind
        self.life=random.uniform(.3,.8)
        if kind=="rain":
            self.vx=random.uniform(-60,-20);self.vy=random.uniform(500,760)
            self.life=random.uniform(.7,1.4)
        else:
            a=random.random()*math.tau;s=random.uniform(70,270)
            self.vx=math.cos(a)*s;self.vy=math.sin(a)*s
    def update(self,dt):
        self.x+=self.vx*dt;self.y+=self.vy*dt
        if self.kind!="rain":self.vy+=260*dt
        self.life-=dt
    def draw(self,off=(0,0)):
        if self.kind=="rain":
            pygame.draw.line(screen,self.c,(int(self.x+off[0]),int(self.y+off[1])),
                             (int(self.x+8+off[0]),int(self.y-18+off[1])),2)
        else:
            pygame.draw.circle(screen,self.c,(int(self.x+off[0]),int(self.y+off[1])),3)

class Lane:
    def __init__(self,world_y,kind=None,difficulty=0):
        self.world_y=world_y
        self.kind=kind or random.choices(["grass","road","water","rail"],[28,45,19,8])[0]
        self.dir=random.choice([-1,1])
        self.speed=random.randint(120,225)+difficulty*2
        self.items=[]
        self.timer=random.uniform(.1,1.4)
        self.train_warning=0

        if self.kind=="grass":
            for _ in range(random.randint(0,4)):
                self.items.append({"type":"tree","x":random.randrange(0,W,TILE)})

        elif self.kind=="water":
            self.speed=random.randint(85,155)+difficulty
            gap=random.randint(185,255)
            for x in range(-220,W+300,gap):
                self.items.append({
                    "type":"log",
                    "x":x+random.randint(-25,25),
                    "w":random.randint(105,175)
                })

        elif self.kind=="rail":
            self.train_warning=random.uniform(2.8,6.5)

    def update(self,dt,difficulty):
        if self.kind=="road":
            self.timer-=dt
            if self.timer<=0:
                typ=random.choice(["car","car","truck"])
                w=78 if typ=="car" else 128
                x=-w-30 if self.dir==1 else W+30
                color=random.choice([RED,BLUE,YELLOW,ORANGE,PINK])
                self.items.append({"type":typ,"x":x,"w":w,"color":color})
                self.timer=random.uniform(.72,1.55)*clamp(1-difficulty*.006,.55,1)
            for it in self.items:
                it["x"]+=self.dir*self.speed*dt
            self.items=[i for i in self.items if -240<i["x"]<W+240]

        elif self.kind=="water":
            for it in self.items:
                it["x"]+=self.dir*self.speed*dt
                if self.dir==1 and it["x"]>W+120:
                    it["x"]=-it["w"]-120
                elif self.dir==-1 and it["x"]+it["w"]<-120:
                    it["x"]=W+120

        elif self.kind=="rail":
            self.train_warning-=dt
            if self.train_warning<=0 and not any(i["type"]=="train" for i in self.items):
                x=-700 if self.dir==1 else W+50
                self.items.append({"type":"train","x":x,"w":650})
            for it in self.items:
                if it["type"]=="train":
                    it["x"]+=self.dir*(920+difficulty*4)*dt
            had_train=bool(self.items)
            self.items=[i for i in self.items if -850<i["x"]<W+850]
            if had_train and not self.items:
                self.train_warning=random.uniform(3.7,7.0)

    def draw(self,sy,theme):
        r=pygame.Rect(0,sy,W,TILE)
        grass_a,grass_b,water=theme

        if self.kind=="grass":
            pygame.draw.rect(screen,grass_a if int(self.world_y/TILE)%2 else grass_b,r)
            for it in self.items:
                x=it["x"]
                pygame.draw.rect(screen,BROWN,(x+17,sy+25,12,27))
                pygame.draw.circle(screen,(39,112,55),(x+23,sy+19),21)

        elif self.kind=="road":
            pygame.draw.rect(screen,ROAD,r)
            for x in range(0,W,90):
                pygame.draw.rect(screen,LINE,(x,sy+TILE//2,48,3))
            for it in self.items:
                pygame.draw.rect(screen,it["color"],(it["x"],sy+8,it["w"],TILE-16),border_radius=10)
                pygame.draw.rect(screen,(185,220,240),(it["x"]+15,sy+13,min(32,it["w"]-30),12),border_radius=4)
                pygame.draw.circle(screen,BLACK,(int(it["x"]+18),sy+TILE-7),7)
                pygame.draw.circle(screen,BLACK,(int(it["x"]+it["w"]-18),sy+TILE-7),7)

        elif self.kind=="water":
            pygame.draw.rect(screen,water,r)
            # little water streaks
            for x in range((pygame.time.get_ticks()//20)%70-70,W,70):
                pygame.draw.line(screen,(110,190,230),(x,sy+17),(x+25,sy+17),2)
            for it in self.items:
                pygame.draw.rect(screen,BROWN,(it["x"],sy+10,it["w"],TILE-20),border_radius=14)
                pygame.draw.circle(screen,(151,98,58),(int(it["x"]+15),sy+TILE//2),10,2)

        else:
            pygame.draw.rect(screen,RAIL,r)
            pygame.draw.line(screen,(40,40,43),(0,sy+14),(W,sy+14),7)
            pygame.draw.line(screen,(40,40,43),(0,sy+41),(W,sy+41),7)
            if self.train_warning<1.35 and not self.items:
                pygame.draw.circle(screen,RED,(W-35,sy+TILE//2),11)
                txt("!",SMALL,WHITE,W-35,sy+TILE//2,True)
            for it in self.items:
                if it["type"]=="train":
                    pygame.draw.rect(screen,(185,55,60),(it["x"],sy+3,it["w"],TILE-6),border_radius=8)
                    for wx in range(int(it["x"]+35),int(it["x"]+it["w"]-20),75):
                        pygame.draw.rect(screen,CYAN,(wx,sy+12,38,18),border_radius=4)

class Game:
    def __init__(self):
        self.state="menu"
        self.shop=0
        self.mission=random.choice([
            ("Reach score 20",20,"score"),
            ("Collect 5 coins",5,"coins"),
            ("Reach score 35",35,"score"),
        ])
        self.reset()

    def reset(self):
        self.grid_x=W//2-TILE//2
        self.world_y=0.0

        # Smooth movement state
        self.start_x=self.grid_x
        self.start_world_y=0.0
        self.target_x=self.grid_x
        self.target_world_y=0.0
        self.move_t=1.0
        self.move_duration=.135
        self.moving=False
        self.queued_move=None
        self.hop_height=0

        self.score=0
        self.run_coins=0
        self.forward_streak=0
        self.lanes=[]
        self.particles=[]
        self.dead_reason=""
        self.day=0
        self.coin=None
        self.power=None
        self.power_timer=random.uniform(7,12)
        self.shield=0
        self.magnet=0
        self.shake=0
        self.mission_done=False

        for i in range(-3,16):
            kind="grass" if i<3 else None
            self.lanes.append(Lane(-i*TILE,kind,0))

    def start(self):
        self.reset()
        save["stats"]["runs"]+=1
        self.state="play"

    def lane_at(self,wy):
        return min(self.lanes,key=lambda l:abs(l.world_y-wy))

    def burst(self,c,n=16):
        if not save["settings"]["particles"]:return
        for _ in range(n):
            self.particles.append(Particle(self.grid_x+TILE/2,PLAYER_Y+TILE/2,c))

    def die(self,why):
        if self.shield>0:
            self.shield=0
            self.shake=10
            self.burst(CYAN,28)
            return

        self.dead_reason=why
        self.burst(RED,25)
        save["stats"]["deaths"]+=1
        save["best"]=max(save["best"],self.score)
        gain=self.score*2+self.run_coins*3
        save["xp"]+=gain
        save["level"]=lvl()

        for needed,name in [(25,"ROAD WARRIOR"),(60,"WHY DID THE CHICKEN"),(100,"CENTURY CLUB")]:
            if self.score>=needed and name not in save["achievements"]:
                save["achievements"].append(name)

        if self.run_coins>=10 and "COIN GOBLIN" not in save["achievements"]:
            save["achievements"].append("COIN GOBLIN")

        save_game()
        self.state="dead"

    def can_move_to(self,nx,new_world):
        lane=self.lane_at(new_world)
        if lane.kind=="grass":
            for it in lane.items:
                if it["type"]=="tree" and abs(it["x"]-nx)<TILE*.65:
                    return False
        return True

    def request_move(self,dx,dy):
        if self.state!="play":return

        if self.moving:
            self.queued_move=(dx,dy)
            return

        nx=clamp(round(self.target_x/TILE)*TILE+dx*TILE,0,W-TILE)
        new_world=self.target_world_y-dy*TILE

        if not self.can_move_to(nx,new_world):
            self.shake=3
            return

        self.start_x=self.grid_x
        self.start_world_y=self.world_y
        self.target_x=nx
        self.target_world_y=new_world
        self.move_t=0
        self.moving=True

        if dy>0:
            new_score=max(self.score,int(round(-new_world/TILE)))
            if new_score>self.score:
                self.forward_streak+=1
            self.score=new_score
        elif dy<0:
            self.forward_streak=0

        self.ensure_world()

    def finish_move(self):
        self.grid_x=self.target_x
        self.world_y=self.target_world_y
        self.moving=False
        self.move_t=1
        self.check_hazards()

        if self.queued_move and self.state=="play":
            move=self.queued_move
            self.queued_move=None
            self.request_move(*move)

    def ensure_world(self):
        min_y=min(l.world_y for l in self.lanes)
        while min_y>self.target_world_y-14*TILE:
            min_y-=TILE
            self.lanes.append(Lane(min_y,None,self.score))
        self.lanes=[l for l in self.lanes if l.world_y<self.target_world_y+9*TILE]

    def check_hazards(self):
        lane=self.lane_at(self.world_y)
        pr=pygame.Rect(self.grid_x+9,PLAYER_Y+9,TILE-18,TILE-18)

        if lane.kind=="road":
            for it in lane.items:
                if pr.colliderect(pygame.Rect(it["x"],PLAYER_Y+8,it["w"],TILE-16)):
                    self.die("FLATTENED BY TRAFFIC 💀")
                    return

        elif lane.kind=="rail":
            for it in lane.items:
                if it["type"]=="train" and pr.colliderect(pygame.Rect(it["x"],PLAYER_Y+3,it["w"],TILE-6)):
                    self.die("TRAIN SAID NO 🚆")
                    return

        elif lane.kind=="water":
            on_log=False
            for it in lane.items:
                if pr.colliderect(pygame.Rect(it["x"],PLAYER_Y+8,it["w"],TILE-16)):
                    on_log=True
                    break
            if not on_log:
                self.die("CHICKEN CANNOT SWIM 🌊")

    def spawn_power(self):
        kind=random.choice(["SHIELD","MAGNET"])
        self.power={
            "x":random.randrange(1,COLS-1)*TILE,
            "wy":self.target_world_y-random.randint(3,8)*TILE,
            "kind":kind
        }

    def update(self,dt):
        self.day+=dt
        self.shake=max(0,self.shake-24*dt)

        # weather
        if save["settings"]["weather"] and random.random()<dt*12:
            self.particles.append(Particle(random.randint(0,W),-20,(155,195,225),"rain"))

        for p in self.particles:p.update(dt)
        self.particles=[p for p in self.particles if p.life>0 and p.y<H+100]

        if self.state!="play":return

        # Smooth hop interpolation
        if self.moving:
            self.move_t=min(1,self.move_t+dt/self.move_duration)
            t=ease_out_cubic(self.move_t)
            self.grid_x=lerp(self.start_x,self.target_x,t)
            self.world_y=lerp(self.start_world_y,self.target_world_y,t)
            self.hop_height=math.sin(self.move_t*math.pi)*18
            if self.move_t>=1:
                self.hop_height=0
                self.finish_move()

        # Update moving lanes
        for l in self.lanes:
            l.update(dt,self.score)

        # Current water lane carries us while standing still.
        if not self.moving:
            lane=self.lane_at(self.world_y)
            if lane.kind=="water":
                self.grid_x+=lane.dir*lane.speed*dt
                self.target_x=self.grid_x
                if self.grid_x<-TILE or self.grid_x>W:
                    self.die("SAILED INTO THE VOID 🌊")
                    return
                self.check_hazards()
                if self.state!="play":return

            elif lane.kind in ("road","rail"):
                self.check_hazards()
                if self.state!="play":return

        # Spawn collectibles
        if self.coin is None and random.random()<dt*.22:
            self.coin={
                "x":random.randrange(1,COLS-1)*TILE,
                "wy":self.target_world_y-random.randint(2,8)*TILE
            }

        self.power_timer-=dt
        if self.power is None and self.power_timer<=0:
            self.spawn_power()
            self.power_timer=random.uniform(10,16)

        # Magnet
        if self.magnet>0:self.magnet=max(0,self.magnet-dt)

        # Coin collision / attraction
        if self.coin:
            csy=PLAYER_Y+(self.coin["wy"]-self.world_y)
            cx=self.coin["x"]

            if self.magnet>0 and abs(csy-PLAYER_Y)<150:
                cx=lerp(cx,self.grid_x,.10)
                self.coin["x"]=cx

            if abs(csy-PLAYER_Y)<30 and abs(cx-self.grid_x)<38:
                save["coins"]+=1
                save["stats"]["coins"]+=1
                self.run_coins+=1
                self.burst(GOLD,20)
                self.coin=None
            elif csy>H+120:
                self.coin=None

        # Powerup collision
        if self.power:
            psy=PLAYER_Y+(self.power["wy"]-self.world_y)
            if abs(psy-PLAYER_Y)<30 and abs(self.power["x"]-self.grid_x)<38:
                if self.power["kind"]=="SHIELD":
                    self.shield=1
                else:
                    self.magnet=8
                save["stats"]["powerups"]+=1
                self.burst(CYAN if self.power["kind"]=="SHIELD" else PURPLE,28)
                self.power=None
            elif psy>H+120:
                self.power=None

        # Mission completion
        title,target,kind=self.mission
        val=self.score if kind=="score" else self.run_coins
        if not self.mission_done and val>=target:
            self.mission_done=True
            save["coins"]+=25
            save["xp"]+=35
            self.burst(GOLD,35)
            save_game()

    def event(self,e):
        if e.type!=pygame.KEYDOWN:return

        if self.state=="menu":
            if e.key in (pygame.K_SPACE,pygame.K_RETURN):self.start()
            elif e.key==pygame.K_g:self.state="shop"
            elif e.key==pygame.K_a:self.state="ach"
            elif e.key==pygame.K_s:self.state="settings"

        elif self.state=="play":
            if e.key in (pygame.K_UP,pygame.K_w):self.request_move(0,1)
            elif e.key in (pygame.K_DOWN,pygame.K_s):self.request_move(0,-1)
            elif e.key in (pygame.K_LEFT,pygame.K_a):self.request_move(-1,0)
            elif e.key in (pygame.K_RIGHT,pygame.K_d):self.request_move(1,0)
            elif e.key==pygame.K_ESCAPE:self.state="pause"

        elif self.state=="pause":
            if e.key==pygame.K_ESCAPE:self.state="play"
            elif e.key==pygame.K_m:self.state="menu"
            elif e.key==pygame.K_r:self.start()

        elif self.state=="dead":
            if e.key==pygame.K_r:self.start()
            elif e.key==pygame.K_m:self.state="menu"

        elif self.state=="shop":
            if e.key==pygame.K_ESCAPE:self.state="menu"
            elif e.key in (pygame.K_LEFT,pygame.K_a):self.shop=(self.shop-1)%len(ORDER)
            elif e.key in (pygame.K_RIGHT,pygame.K_d):self.shop=(self.shop+1)%len(ORDER)
            elif e.key in (pygame.K_SPACE,pygame.K_RETURN):
                sid=ORDER[self.shop];it=SKINS[sid]
                if sid in save["owned"]:
                    save["skin"]=sid
                elif save["coins"]>=it["price"]:
                    save["coins"]-=it["price"]
                    save["owned"].append(sid)
                    save["skin"]=sid
                save_game()

        elif self.state=="ach":
            if e.key==pygame.K_ESCAPE:self.state="menu"

        elif self.state=="settings":
            if e.key==pygame.K_ESCAPE:self.state="menu"
            elif e.key==pygame.K_1:
                save["settings"]["particles"]=not save["settings"]["particles"];save_game()
            elif e.key==pygame.K_2:
                save["settings"]["weather"]=not save["settings"]["weather"];save_game()
            elif e.key==pygame.K_3:
                save["settings"]["screen_shake"]=not save["settings"]["screen_shake"];save_game()

    def theme(self):
        # biome changes by score
        if self.score<30:
            return GRASS,GRASS2,WATER
        elif self.score<60:
            return (74,139,84),(63,123,75),(55,117,170)
        elif self.score<100:
            return (105,120,75),(88,103,65),(70,105,145)
        else:
            return (80,70,105),(68,60,92),(67,75,135)

    def background(self,off=(0,0)):
        screen.fill((22,27,36))
        theme=self.theme()
        for l in sorted(self.lanes,key=lambda z:z.world_y):
            sy=PLAYER_Y+(l.world_y-self.world_y)+off[1]
            if -TILE<sy<H+TILE:
                l.draw(int(sy),theme)

        if self.coin:
            sy=PLAYER_Y+(self.coin["wy"]-self.world_y)+off[1]
            if -30<sy<H+30:
                cx=int(self.coin["x"]+TILE/2+off[0])
                pygame.draw.circle(screen,GOLD,(cx,int(sy+TILE/2)),13)
                pygame.draw.circle(screen,YELLOW,(cx,int(sy+TILE/2)),7,2)

        if self.power:
            sy=PLAYER_Y+(self.power["wy"]-self.world_y)+off[1]
            if -35<sy<H+35:
                x=int(self.power["x"]+TILE/2+off[0]);y=int(sy+TILE/2)
                c=CYAN if self.power["kind"]=="SHIELD" else PURPLE
                pygame.draw.circle(screen,c,(x,y),17)
                txt("S" if self.power["kind"]=="SHIELD" else "M",SMALL,BLACK,x,y,True)

    def draw_player(self,off=(0,0)):
        c=SKINS[save["skin"]]["color"]
        x=int(self.grid_x+off[0])
        y=int(PLAYER_Y-self.hop_height+off[1])

        # shadow
        shadow_w=int(30-8*(self.hop_height/18))
        pygame.draw.ellipse(screen,(25,30,30),(x+TILE//2-shadow_w//2,PLAYER_Y+TILE-8,shadow_w,8))

        pygame.draw.rect(screen,c,(x+8,y+10,TILE-16,TILE-18),border_radius=12)
        pygame.draw.circle(screen,c,(x+TILE-13,y+15),15)
        pygame.draw.circle(screen,BLACK,(x+TILE-8,y+11),3)
        pygame.draw.polygon(screen,ORANGE,[(x+TILE+1,y+16),(x+TILE+13,y+21),(x+TILE+1,y+25)])
        pygame.draw.rect(screen,ORANGE,(x+13,y+TILE-10,8,10))
        pygame.draw.rect(screen,ORANGE,(x+32,y+TILE-10,8,10))

        if self.shield>0:
            pygame.draw.circle(screen,CYAN,(x+TILE//2,y+TILE//2),35,3)

    def hud(self):
        txt(f"SCORE {self.score}",FONT,WHITE,22,18)
        txt(f"BEST {save['best']}",SMALL,GRAY,22,54)
        txt(f"STREAK x{self.forward_streak}",SMALL,YELLOW,22,84)
        txt(f"COINS {save['coins']}",SMALL,GOLD,W-155,20)
        txt(f"LVL {save['level']}",SMALL,CYAN,W-155,50)

        if self.shield>0:txt("SHIELD READY",SMALL,CYAN,W-175,82)
        if self.magnet>0:txt(f"MAGNET {self.magnet:.1f}s",SMALL,PURPLE,W-175,108)

        title,target,kind=self.mission
        val=self.score if kind=="score" else self.run_coins
        status="DONE +25 🪙" if self.mission_done else f"{min(val,target)}/{target}"
        txt("MISSION",SMALL,GRAY,W//2,18,True)
        txt(f"{title} — {status}",SMALL,GOLD if self.mission_done else WHITE,W//2,44,True)

    def menu_bg(self):
        screen.fill((20,25,34))
        t=pygame.time.get_ticks()/1000
        for x in range(-55,W+55,55):
            xx=(x+int(t*15))%W
            pygame.draw.line(screen,(25,31,42),(xx,0),(xx,H))
        for y in range(0,H,55):
            pygame.draw.line(screen,(25,31,42),(0,y),(W,y))

    def draw(self):
        off=(0,0)
        if self.shake>0 and save["settings"]["screen_shake"]:
            s=int(self.shake)
            off=(random.randint(-s,s),random.randint(-s,s))

        if self.state in ("play","pause","dead"):
            self.background(off)
        else:
            self.menu_bg()

        if self.state=="play":
            self.draw_player(off)
            for p in self.particles:p.draw(off)
            self.hud()

        elif self.state=="menu":
            txt(" CROSSY",HUGE,WHITE,W//2,115,True)
            txt(" VERSION 100,000,000",FONT,PURPLE,W//2,180,True)

            px=W//2-27;py=250
            c=SKINS[save["skin"]]["color"]
            pygame.draw.rect(screen,c,(px+8,py+10,39,37),border_radius=12)
            pygame.draw.circle(screen,c,(px+44,py+15),15)
            pygame.draw.polygon(screen,ORANGE,[(px+55,py+15),(px+70,py+21),(px+55,py+26)])

            txt("SPACE = CROSS THE ROAD",FONT,CYAN,W//2,380,True)
            txt("G = SKIN SHOP",FONT,WHITE,W//2,435,True)
            txt("A = ACHIEVEMENTS",FONT,WHITE,W//2,485,True)
            txt("S = SETTINGS",FONT,WHITE,W//2,535,True)
            txt("SMOOTH HOPS • POWERUPS • MISSIONS • WEATHER",SMALL,GRAY,W//2,595,True)
            txt(f"BEST {save['best']}  •  COINS {save['coins']}  •  LVL {save['level']}",SMALL,GOLD,W//2,660,True)

        elif self.state=="pause":
            sh=pygame.Surface((W,H),pygame.SRCALPHA);sh.fill((0,0,0,175));screen.blit(sh,(0,0))
            txt("PAUSED",HUGE,WHITE,W//2,280,True)
            txt("ESC resume • R restart • M menu",FONT,CYAN,W//2,390,True)

        elif self.state=="dead":
            self.draw_player(off)
            sh=pygame.Surface((W,H),pygame.SRCALPHA);sh.fill((0,0,0,185));screen.blit(sh,(0,0))
            txt("ROADKILL 💀",HUGE,RED,W//2,185,True)
            txt(self.dead_reason,FONT,YELLOW,W//2,280,True)
            txt(f"SCORE {self.score}   •   COINS +{self.run_coins}",BIG,WHITE,W//2,360,True)
            txt("R = AGAIN     M = MENU",FONT,CYAN,W//2,470,True)

        elif self.state=="shop":
            txt("SKIN SHOP",HUGE,WHITE,W//2,105,True)
            sid=ORDER[self.shop];it=SKINS[sid]
            pygame.draw.circle(screen,it["color"],(W//2,305),65)
            status="EQUIPPED" if save["skin"]==sid else ("SPACE = EQUIP" if sid in save["owned"] else f"SPACE = BUY {it['price']}")
            txt(it["name"],BIG,it["color"],W//2,430,True)
            txt(status,FONT,GOLD,W//2,495,True)
            txt("← → browse • ESC back",SMALL,WHITE,W//2,590,True)

        elif self.state=="ach":
            txt("ACHIEVEMENTS",HUGE,WHITE,W//2,100,True)
            alls=["ROAD WARRIOR","WHY DID THE CHICKEN","CENTURY CLUB","COIN GOBLIN"]
            for i,a in enumerate(alls):
                got=a in save["achievements"]
                txt(("✓ " if got else "□ ")+a,FONT,(85,230,100) if got else GRAY,W//2,255+i*62,True)
            txt("ESC = back",SMALL,WHITE,W//2,570,True)

        elif self.state=="settings":
            txt("SETTINGS",HUGE,WHITE,W//2,105,True)
            txt(f"1 = PARTICLES: {'ON' if save['settings']['particles'] else 'OFF'}",FONT,WHITE,W//2,270,True)
            txt(f"2 = WEATHER: {'ON' if save['settings']['weather'] else 'OFF'}",FONT,WHITE,W//2,335,True)
            txt(f"3 = SCREEN SHAKE: {'ON' if save['settings']['screen_shake'] else 'OFF'}",FONT,WHITE,W//2,400,True)
            txt("ESC = back",SMALL,GRAY,W//2,525,True)

game=Game()
running=True
while running:
    dt=min(clock.tick(FPS)/1000,.033)
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False
        else:
            game.event(e)

    game.update(dt)
    game.draw()
    pygame.display.flip()

save_game()
pygame.quit()
