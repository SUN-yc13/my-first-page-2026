import tkinter as tk
import random

class NeonWarshipUltimate:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("霓虹战机 ✦ 超时空豪华版")
        self.root.resizable(False, False)
        self.W, self.H = 480, 680
        self.canvas = tk.Canvas(self.root, width=self.W, height=self.H, bg="#020212")
        self.canvas.pack()

        self.player = self.canvas.create_rectangle(
            self.W//2-26, self.H-65, self.W//2+26, self.H-30,
            fill="#00ffff", outline="#00d9ff", width=3
        )
        self.hp = 5
        self.max_hp = 5
        self.speed = 8
        self.base_speed = 4.2
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.invulnerable = False
        self.shield = False
        self.fire_rate = 340
        self.power = 1
        self.dir = 0
        self.holding_space = False
        self.last_shot = 0
        self.particles = []
        self.enemy_bullets = []
        self.boss_active = False
        self.stage = 1
        self.item_types = [0,1,2,3]

        self.enemies = []
        self.bullets = []
        self.items = []

        self.bind_keys()
        self.spawn_enemy()
        self.spawn_item()
        self.difficulty_up()
        self.run()

    def bind_keys(self):
        self.root.bind("<Left>", lambda e: self.set_dir(-1))
        self.root.bind("<Right>", lambda e: self.set_dir(1))
        self.root.bind("<KeyRelease-Left>", lambda e: self.set_dir(0) if self.dir == -1 else None)
        self.root.bind("<KeyRelease-Right>", lambda e: self.set_dir(0) if self.dir == 1 else None)
        self.root.bind("<KeyPress-space>", lambda e: self.start_fire())
        self.root.bind("<KeyRelease-space>", lambda e: self.stop_fire())

    def set_dir(self, d):
        if not self.game_over:
            self.dir = d * self.speed

    def start_fire(self):
        if not self.game_over:
            self.holding_space = True
            if self.last_shot == 0:
                self.fire()

    def stop_fire(self):
        self.holding_space = False

    def fire(self):
        if self.game_over or not self.holding_space:
            return
        try:
            x1, y1, x2, y2 = self.canvas.coords(self.player)
        except:
            return
        
        if self.power >= 4:
            b1 = self.canvas.create_rectangle(x1+6, y1-8, x1+12, y1-2, fill="#ff00ff")
            b2 = self.canvas.create_rectangle(x2-12, y1-8, x2-6, y1-2, fill="#ff00ff")
            b3 = self.canvas.create_rectangle((x1+x2)/2-3, y1-12, (x1+x2)/2+3, y1-2, fill="#00ffcc")
            self.bullets += [b1,b2,b3]
        elif self.power >=3:
            b1 = self.canvas.create_rectangle(x1+8, y1-8, x1+14, y1-1, fill="#ffdd00")
            b2 = self.canvas.create_rectangle(x2-14, y1-8, x2-8, y1-1, fill="#ffdd00")
            self.bullets += [b1,b2]
        else:
            bx = (x1+x2)/2 -3
            b = self.canvas.create_rectangle(bx, y1-10, bx+6, y1-1, fill="#ffdd00")
            self.bullets.append(b)
        self.last_shot = self.root.after(self.fire_rate, self.fire)

    def spawn_enemy(self):
        if self.game_over or self.boss_active:
            self.root.after(300, self.spawn_enemy)
            return
        if self.score > 0 and self.score % 80 == 0 and not self.boss_active:
            self.spawn_boss()
            return
        kind = random.choices([1,2,3], [55,35,10])[0]
        if kind ==1:
            w,h,sp,hp,col = 26,26,1.0,1,"#ff3366"
        elif kind ==2:
            w,h,sp,hp,col = 36,36,0.8,2,"#ff6600"
        else:
            w,h,sp,hp,col = 42,42,0.7,3,"#ff00cc"
        x = random.randint(35, self.W -w -35)
        e = self.canvas.create_oval(x, -h, x+w,0, fill=col, outline="#fff")
        self.enemies.append([e, sp, hp, "normal"])
        if random.random() >0.7:
            self.root.after(400, lambda: self.enemy_fire(e))
        self.root.after(random.randint(420, 900), self.spawn_enemy)

    def spawn_boss(self):
        self.boss_active = True
        w,h = 90, 70
        x = self.W//2 -w//2
        self.boss = self.canvas.create_rectangle(x, 10, x+w, 10+h, fill="#ff0022", outline="#ff4400", width=4)
        self.enemies.append([self.boss, 0.1, 16, "boss"])

    def enemy_fire(self, e):
        if self.game_over:
            return
        try:
            ex1,ey1,ex2,ey2 = self.canvas.coords(e)
        except:
            return
        eb = self.canvas.create_rectangle((ex1+ex2)/2-3, ey2, (ex1+ex2)/2+3, ey2+12, fill="#ff8800")
        self.enemy_bullets.append(eb)

    def spawn_item(self):
        if self.game_over: return
        ty = random.choices(self.item_types, [50,25,15,10])[0]
        w=22
        x=random.randint(45, self.W -w -45)
        cols = ["#ff0","#0f3","#0ff","#f0f"]
        item = self.canvas.create_oval(x, -w, x+w,0, fill=cols[ty], outline="#fff")
        self.items.append([item, ty])
        self.root.after(random.randint(2200, 4000), self.spawn_item)

    def difficulty_up(self):
        if not self.game_over:
            self.base_speed +=0.06
            if self.fire_rate>160:
                self.fire_rate -=5
            if self.score > self.stage*50:
                self.stage +=1
        self.root.after(1400, self.difficulty_up)

    def create_particle(self, x,y, color):
        p = self.canvas.create_oval(x,y,x+6,y+6, fill=color)
        self.particles.append([p, random.randint(-3,3), random.randint(-3,3)])

    def flash_player(self):
        c = self.canvas.itemcget(self.player, "fill")
        n = "#fff" if c!="#fff" else "#0ff" if not self.shield else "#0ff"
        self.canvas.itemconfig(self.player, fill=n)

    def hurt(self):
        if self.invulnerable or self.shield:
            return
        self.hp -=1
        self.invulnerable = True
        self.root.after(1300, lambda: setattr(self, "invulnerable", False))
        if self.hp <=0:
            self.game_over = True
            self.high_score = max(self.score, self.high_score)

    def restart(self):
        self.canvas.delete("all")
        self.__init__()

    def run(self):
        if self.game_over:
            self.canvas.create_text(self.W//2, self.H//2-60, text="GAME OVER", fill="#ff0066", font=("",46))
            self.canvas.create_text(self.W//2, self.H//2+15, text=f"得分：{self.score}", fill="#fff", font=("",26))
            self.canvas.create_text(self.W//2, self.H//2+60, text=f"最高分：{self.high_score}", fill="#ffaa00", font=("",22))
            self.canvas.create_text(self.W//2, self.H//2+110, text="按空格重新开始", fill="#0ff", font=("",20))
            if self.holding_space:
                self.restart()
            return

        try:
            self.canvas.move(self.player, self.dir, 0)
            px,py,px2,py2 = self.canvas.coords(self.player)
            if px<0: self.canvas.move(self.player, -px,0)
            if px2>self.W: self.canvas.move(self.player, self.W-px2,0)
        except:
            return

        for p in self.particles[:]:
            try:
                self.canvas.move(p[0], p[1], p[2])
                if random.random()>0.92:
                    self.canvas.delete(p[0])
                    self.particles.remove(p)
            except:
                continue

        for b in self.bullets[:]:
            try:
                self.canvas.move(b,0,-11)
                bx1,by1,bx2,by2 = self.canvas.coords(b)
                if by2<0:
                    self.bullets.remove(b)
                    self.canvas.delete(b)
            except:
                continue

        for eb in self.enemy_bullets[:]:
            try:
                self.canvas.move(eb,0,5)
                ex,ey,ex2,ey2 = self.canvas.coords(eb)
                if ey>self.H:
                    self.enemy_bullets.remove(eb)
                    self.canvas.delete(eb)
                    continue
                if not self.invulnerable and ex2>px and ex1<px2 and ey2>py and ey1<py2:
                    self.hurt()
                    self.enemy_bullets.remove(eb)
                    self.canvas.delete(eb)
            except:
                continue

        for e_data in self.enemies[:]:
            try:
                e, sp, hp, kind = e_data
                self.canvas.move(e,0, self.base_speed*sp)
                ex1,ey1,ex2,ey2 = self.canvas.coords(e)
                if ey1>self.H:
                    self.enemies.remove(e_data)
                    self.canvas.delete(e)
                    if kind =="boss":
                        self.boss_active=False
                    continue

                hit=False
                for b in self.bullets[:]:
                    try:
                        bx1,by1,bx2,by2 = self.canvas.coords(b)
                        if ex2>bx1 and ex1<bx2 and ey2>by1 and ey1<by2:
                            self.bullets.remove(b)
                            self.canvas.delete(b)
                            e_data[2]-=1
                            self.create_particle(bx1,by1, "#ff0")
                            if e_data[2]<=0:
                                self.create_particle(ex1+10, ey1+10, "#f30")
                                self.create_particle(ex1+15, ey1+15, "#f30")
                                self.enemies.remove(e_data)
                                self.canvas.delete(e)
                                if kind =="boss":
                                    self.boss_active=False
                                    self.score +=25
                                else:
                                    self.score +=3 if sp>0.85 else 4 if sp>0.65 else 6
                                if self.score%22==0:
                                    self.power = min(self.power+1,4)
                            hit=True
                            break
                    except:
                        continue
                if hit:continue

                if not self.invulnerable and ex2>px and ex1<px2 and ey2>py and ey1<py2:
                    self.hurt()
            except:
                continue

        for it in self.items[:]:
            try:
                item, ty = it
                self.canvas.move(item,0,5)
                ix1,iy1,ix2,iy2 = self.canvas.coords(item)
                if iy1>self.H:
                    self.items.remove(it)
                    self.canvas.delete(item)
                    continue
                if ix2>px and ix1<px2 and iy2>py and iy1<py2:
                    self.items.remove(it)
                    self.canvas.delete(item)
                    if ty ==0:
                        for ed in self.enemies[:]:
                            try:
                                self.canvas.delete(ed[0])
                                self.score +=1
                            except:
                                continue
                        self.enemies.clear()
                        self.enemy_bullets.clear()
                    elif ty ==1:
                        self.hp = min(self.max_hp, self.hp+1)
                    elif ty ==2:
                        self.shield=True
                        self.root.after(5000, lambda: setattr(self, "shield", False))
                    elif ty ==3:
                        old = self.fire_rate
                        self.fire_rate = 120
                        self.root.after(4000, lambda: setattr(self, "fire_rate", old))
            except:
                continue

        self.canvas.delete("hud")
        self.canvas.create_text(20,20,anchor="nw",text=f"得分：{self.score}",fill="#fff",font=("",14),tag="hud")
        self.canvas.create_text(self.W-140,20,anchor="nw",text=f"生命：{self.hp}",fill="#ff3333",font=("",14),tag="hud")
        self.canvas.create_text(self.W//2-60,20,anchor="nw",text=f"火力：{self.power}",fill="#ff0",font=("",14),tag="hud")
        st = "护盾" if self.shield else "正常"
        self.canvas.create_text(self.W//2+40,20,anchor="nw",text=f"{st}",fill="#0ff",font=("",14),tag="hud")

        if self.invulnerable:
            self.flash_player()
        if self.shield:
            self.canvas.itemconfig(self.player, outline="#ff0", width=4)
        else:
            self.canvas.itemconfig(self.player, outline="#00d9ff", width=3)

        self.root.after(20, self.run)

if __name__ == "__main__":
    NeonWarshipUltimate()
    tk.mainloop()
