import curses, time, random, math
W, H, FPS, DEBUG = 50, 20, 10, False
ITEM_TYPES = {}
class Player:
    MAX_HP = 1000
    MAX_SAN = 100
    def __init__(self): 
        self.hp, self.san, self.effects, self.color = 500, 100.0, [], 8
        self.death_cause = "You don't remember how it happened."
    def clamp_stats(self):
        self.hp = max(0, min(self.hp, self.MAX_HP))
        self.san = max(0, min(self.san, self.MAX_SAN))
    def change_hp(self, amount):
        self.hp += amount
        self.clamp_stats()
    def change_san(self, amount):
        self.san += amount
        self.clamp_stats()
    def update(self, ctx):
        for e in self.effects: e.tick(self, ctx)
        self.effects[:] = [e for e in self.effects if not e.expired()]
        self.clamp_stats()
class Game:
    def __init__(self, player, pos, grid, entities, inv, face, floor, fog):
        self.player, self.pos, self.grid, self.entities = player, pos, grid, entities
        self.inv, self.face, self.used, self.lights, self.t, self.floor, self.fog = inv, face, False, [], time.time(), floor, fog
def update_fog(ctx):
    new_fog = set(ctx.fog)
    if len(ctx.fog) < 60:
        for (x, y) in list(ctx.fog):
            if random.random() < 0.15:
                nx, ny = x + random.randint(-1, 1), y + random.randint(-1, 1)
                if 0 <= nx < W and 0 <= ny < H: new_fog.add((nx, ny))
    if len(new_fog) > 20:
        for _ in range(max(1, len(new_fog)//10)): 
            if new_fog: new_fog.remove(random.choice(list(new_fog)))
    if ctx.pos in new_fog: ctx.player.san -= 0.2
    return new_fog
class SoundSystem:
    def __init__(self): self.active_sounds = []
    def emit(self, sx, sy, msg, intensity, ctx):
        px, py = ctx.pos
        dist = math.hypot(sx-px, sy-py)
        if 0 < dist <= intensity:
            dx, dy = sx-px, sy-py
            dir_str = ("East" if dx>0 else "West") if abs(dx)>abs(dy) else ("South" if dy>0 else "North")
            vol = "DEAFENING" if dist < 3 else "Clear" if dist < intensity/2 else "Faint"
            full = f"[{vol}] {msg} to the {dir_str}"
            for s in self.active_sounds:
                if s["msg"] == full: s["exp"] = time.time() + 1.5; return
            self.active_sounds.append({"msg": full, "exp": time.time() + 1.5})
    def update(self): self.active_sounds = [s for s in self.active_sounds if s["exp"] > time.time()]
class Entity:
    def __init__(self, x, y, char='X', color=1):
        self.x, self.y, self.char, self.color, self.dead, self.effects = x, y, char, color, False, []
    def update(self, ctx):
        for e in self.effects: e.tick(self, ctx)
        self.effects[:] = [e for e in self.effects if not e.expired()]
    def move_towards(self, ctx, tx, ty, speed=1, avoid='#'):
        if random.random() > speed: return
        dx, dy = (1 if tx > self.x else -1 if tx < self.x else 0), (1 if ty > self.y else -1 if ty < self.y else 0)
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < W and 0 <= ny < H and ctx.grid[ny][nx] != avoid: self.x, self.y = nx, ny
    def get_v(self, ctx): return self.char, self.color
class Chaser(Entity):
    def __init__(self, x, y): super().__init__(x, y, 'X', 6); self.cd = 0
    def update(self, ctx):
        super().update(ctx); px, py = ctx.pos
        dist = abs(self.x-px) + abs(self.y-py)
        if dist < 1: ctx.player.hp = 0
        elif dist < 10 and self.cd <= 0:
            self.move_towards(ctx, *ctx.pos); self.cd = max(1, ctx.floor // 5)
            ctx.sounds.emit(self.x, self.y, "A heavy thud", 15, ctx)
        self.cd -= 1
    def get_v(self, ctx): return (self.char, self.color) if int(ctx.t*12)%2 else ('?', 5)
class Stalker(Entity):
    def __init__(self, x, y): super().__init__(x, y, 'S', 5)
    def update(self, ctx):
        super().update(ctx)
        if visible(ctx, self.x, self.y): 
            ctx.player.san -= 1
        else:
            tx, ty = (ctx.pos if random.random() < 0.6 else (self.x+random.randint(-1,1), self.y+random.randint(-1,1)))
            self.move_towards(ctx, tx, ty, 0.3)
        if (self.x, self.y) == ctx.pos: ctx.player.change_hp(-10)
class Ambusher(Entity):
    def __init__(self, x, y): super().__init__(x, y, '#', 1); self.trig, self.cd = False, 0
    def update(self, ctx):
        super().update(ctx); px, py = ctx.pos
        dist = math.hypot(self.x-px, self.y-py)
        if dist < 3.5: 
            self.trig, self.char, self.color = True, 'A', 9
            ctx.sounds.emit(self.x, self.y, "Got you", 10, ctx)
        if self.trig:
            if dist < 1: ctx.player.hp = 0
            elif self.cd <= 0: self.move_towards(ctx, *ctx.pos); self.cd = 1
            else: self.cd -= 1
    def get_v(self, ctx): return (self.char, self.color if int(ctx.t*10)%2 else 1) if self.trig else ('#', 1)
class Item:
    char, name, color, max_stack = '?', '?', 7, 1
    def __init__(self): self.v, self.on = self.max_stack, False
    def use(self, ctx): pass
    def tick(self, ctx): pass
    @classmethod
    def get_v(cls, ctx): return cls.char, cls.color
class Water(Item):
    char, name, color = '+', 'H2O', 7
    def use(self, ctx): ctx.player.change_hp(100); ctx.used = True
class RainbowWater(Item):
    char, name, color = '*', 'H2O', 7
    def use(self, ctx): ctx.player.change_hp(200); ctx.player.change_san(10) ; ctx.used = True
    @classmethod
    def get_v(cls, ctx): return cls.char, [7, 9, 10, 3, 5][int(ctx.t*8)%5]
class Vit(Item):
    char, name, color = 'v', 'VIT', 9
    def use(self, ctx): ctx.player.change_san; ctx.used = True
class Bomb(Item):
    char, name, color = 'B', 'BOM', 11
    def use(self, ctx):
        px, py = ctx.pos
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = px+dx, py+dy
                if 0<=nx<W and 0<=ny<H and ctx.grid[ny][nx]!='E': ctx.grid[ny][nx]='.'
        for e in ctx.entities:
            if abs(e.x-px)<=1 and abs(e.y-py)<=1: e.dead = True
        ctx.lights.append({'p':ctx.pos, 'a':360, 'd':(0,0), 'r':5}); ctx.used = True
class LightSource(Item):
    def tick(self, ctx, angle, radius):
        if getattr(self, 'on', False) and self.v > 0:
            ctx.lights.append({'p':ctx.pos, 'a':angle, 'd':ctx.face, 'r':radius}); self.v -= 1
class Flashlight(LightSource):
    char, name, color, max_stack = 'F', 'LIT', 10, 800
    def tick(self, ctx): super().tick(ctx, 90, 7)
class Lantern(LightSource):
    char, name, color, max_stack = 'L', 'LAN', 10, 500
    def tick(self, ctx): super().tick(ctx, 360, 4)
ITEM_TYPES = {'+': Water, '*': RainbowWater, 'v': Vit, 'B': Bomb, 'F': Flashlight, 'L': Lantern}
def gen(floor):
    grid = [['#']*W for _ in range(H)]; rooms = []
    for _ in range(1200):
        w, h, x, y = random.randint(4,7), random.randint(3,6), random.randint(1,W-9), random.randint(1,H-7)
        if any(grid[j][i]=='.' for j in range(y-1,y+h+1) for i in range(x-1,x+w+1) if 0<=i<W and 0<=j<H): continue
        for j in range(y,y+h): grid[j][x:x+w] = ['.']*w
        rooms.append((x+w//2, y+h//2))
        if len(rooms)>1:
            cx, cy, tx, ty = *rooms[-2], *rooms[-1]
            while cx!=tx: cx+=1 if tx>cx else -1; grid[cy][cx]='.'
            while cy!=ty: cy+=1 if ty>cy else -1; grid[cy][cx]='.'
    grid[rooms[-1][1]][rooms[-1][0]] = 'E'
    ents = [random.choice([Chaser, Stalker, Ambusher])(*r) for r in random.sample(rooms[1:], min(len(rooms)-1, 3 + (20-floor)//3))]
    tiles = [(x,y) for y in range(H) for x in range(W) if grid[y][x]=='.']
    for x,y in random.sample(tiles, min(max(3, 8-(20-floor)//4), len(tiles))): grid[y][x] = random.choice(list(ITEM_TYPES.keys()))
    return grid, rooms[0], ents, {random.choice(rooms)}
def visible(ctx, x, y):
    if DEBUG or (x,y)==ctx.pos: return True
    for l in ctx.lights:
        lx, ly = x-l['p'][0], y-l['p'][1]
        d = math.hypot(lx, ly)
        if d < l['r'] and (l['a']>=360 or (d>0 and (lx*l['d'][0]+ly*l['d'][1])/d > math.cos(math.radians(l['a']/2)))): return True
    return False
def main(scr):
    curses.curs_set(0); curses.start_color(); curses.use_default_colors()
    for i,c in enumerate([7,0,6,3,5,1,4,7,2,3,1], 1): curses.init_pair(i, c, -1)
    player, floor, inv, sel, face, sound_sys = Player(), 20, [Flashlight()], 0, (1,0), SoundSystem()
    grid, pos, entities, fog = gen(floor)
    while player.hp > 0:
        t0, _ = time.time(), scr.nodelay(1)
        key = scr.getch()
        dx, dy = {ord('w'):(0,-1),ord('s'):(0,1),ord('a'):(-1,0),ord('d'):(1,0)}.get(key,(0,0))
        if dx or dy: face = (dx, dy)
        ctx = Game(player, pos, grid, entities, inv, face, floor, fog); ctx.sounds = sound_sys
        if ord('1') <= key <= ord('5'): sel = min(key - ord('1'), len(inv)-1)
        if key == ord('e') and sel < len(inv):
            it = inv[sel]; it.on = not getattr(it, 'on', False); it.use(ctx)
            if ctx.used: inv.pop(sel); sel = max(0, sel-1)  
        if dx or dy:
            player.hp -= 1; nx, ny = pos[0]+dx, pos[1]+dy
            if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] != '#':
                t = grid[ny][nx]
                if t in ITEM_TYPES and len(inv) < 5: inv.append(ITEM_TYPES[t]()); grid[ny][nx] = '.'
                if t == 'E': floor -= 1; grid, pos, entities, fog = gen(floor)
                else: pos = (nx, ny)
        player.san -= 0.01; player.update(ctx); fog = update_fog(ctx); sound_sys.update()
        for it in inv: it.tick(ctx)
        inv[:] = [i for i in inv if getattr(i, 'v', 1) > 0]; sel = min(sel, max(0, len(inv)-1))
        for e in entities: e.update(ctx)
        entities[:] = [e for e in entities if not e.dead]
        scr.erase()
        for y in range(H):
            for x in range(W):
                if not visible(ctx, x, y): continue
                ent = next((e for e in entities if (e.x, e.y)==(x,y)), None)
                if ent: ch, col = ent.get_v(ctx)
                elif (x,y)==pos: ch, col = '@', player.color
                elif (x,y) in fog: ch, col = '?', 5
                else:
                    t = grid[y][x]
                    ch, col = (t, {'#':1, '.':2, 'E':4}.get(t, 7)) if t in '#.E' else ITEM_TYPES[t].get_v(ctx)
                scr.addch(y, x, ch, curses.color_pair(col))
        scr.addstr(H, 0, "".join(f"[{i+1}:{it.name}{'*' if getattr(it,'on',0) else ''}]" if i==sel else f" {i+1}:{it.char} " for i,it in enumerate(inv)))
        scr.addstr(H+1, 0, f"FL:{floor} HP:{int(player.hp)} SAN:{int(player.san)}%", curses.color_pair(3))
        for i, s in enumerate(sound_sys.active_sounds): scr.addstr(H+3+i, 0, s["msg"], curses.color_pair(5))
        scr.refresh(); time.sleep(max(0, 1/FPS-(time.time()-t0)))