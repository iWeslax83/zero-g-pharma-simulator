from vpython import sphere, box, vector, rate, color, scene, button, wtext, slider
import random, math

# ==================== AYARLAR ====================
NUM_WALKERS = 450
SPAWN_RADIUS = 70
ATTACH_DISTANCE = 3.2
STEP_SIZE = 1.6
gravity_mode = False
simulation_speed = 1.0

# ==================== SAHNE KURULUMU ====================
scene.width = 1000  # Küçük pencere
scene.height = 600  # Küçük pencere
scene.background = vector(0.01, 0.01, 0.06)
scene.title = "🧬 Zero-G Pharma Lab: Kristal Büyüme Simülasyonu"
scene.forward = vector(-0.35, -0.4, -1)
scene.range = 70  # Daha küçük sahne

# ==================== MERKEZİ ÇEKİRDEK ====================
core = sphere(pos=vector(0, 0, 0), radius=3.2, color=color.cyan, emissive=True, opacity=1, shininess=0.9)
glow_layers = []
for i in range(3):
    glow = sphere(pos=vector(0, 0, 0), radius=3.5 + i * 0.8, color=color.cyan, opacity=0.12 - i * 0.03, emissive=True)
    glow_layers.append(glow)

attached_crystals = [core]

# ==================== YÖRÜNGE HALKALARI ====================
orbit_rings = []
for i in range(3):
    ring_radius = 25 + i * 15
    num_points = 60
    for j in range(num_points):
        angle = (j / num_points) * 2 * math.pi
        x = ring_radius * math.cos(angle)
        z = ring_radius * math.sin(angle)
        point = sphere(pos=vector(x, 0, z), radius=0.3, color=vector(0, 0.4, 0.6), opacity=0.2, emissive=True)
        orbit_rings.append(point)

# ==================== PARTIKÜLLER ====================
walkers = []


def create_walker():
    theta = math.acos(2 * random.random() - 1)
    phi = 2 * math.pi * random.random()
    r = SPAWN_RADIUS + random.uniform(-8, 12)
    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)
    size = random.uniform(1.0, 1.5)
    walker_color = vector(random.uniform(0.9, 1), random.uniform(0.5, 0.7),
                          random.uniform(0.05, 0.15)) if not gravity_mode else vector(1, random.uniform(0.25, 0.4),
                                                                                      0.05)
    return sphere(pos=vector(x, y, z), radius=size, color=walker_color, opacity=0.88, emissive=True, shininess=0.7)


def spawn_all_walkers():
    for w in walkers:
        w.visible = False
        del w
    walkers.clear()
    for _ in range(NUM_WALKERS):
        walkers.append(create_walker())


spawn_all_walkers()

# ==================== İSTATİSTİK PANELİ ====================
scene.append_to_caption('\n\n')
crystal_stat = wtext(
    text='<b style="color: #00d4ff;">💎 Kristalleşen Molekül:</b> <span style="color: #2ed573; font-size: 1.3em;">1</span><br>')
walker_stat = wtext(
    text='<b style="color: #ffa502;">🔄 Aktif Molekül:</b> <span style="color: #ffa502; font-size: 1.3em;">450</span><br>')
mode_stat = wtext(
    text='<b style="color: #7b2ff7;">🚀 Mod:</b> <span style="color: #2ed573; font-size: 1.2em;">UZAY (Mikrogravite)</span><br>')
quality_stat = wtext(
    text='<b style="color: #00d4ff;">⭐ Kalite:</b> <span style="color: #2ed573; font-size: 1.2em;">Mükemmel (95%+)</span><br><br>')


# ==================== KONTROLLER ====================
def update_stats():
    crystal_count = len(attached_crystals)
    active_walkers = sum(1 for w in walkers if w.visible)
    crystal_stat.text = f'<b style="color: #00d4ff;">💎 Kristalleşen Molekül:</b> <span style="color: #2ed573; font-size: 1.3em;">{crystal_count}</span><br>'
    walker_stat.text = f'<b style="color: #ffa502;">🔄 Aktif Molekül:</b> <span style="color: #ffa502; font-size: 1.3em;">{active_walkers}</span><br>'
    if gravity_mode:
        mode_stat.text = '<b style="color: #7b2ff7;">🌍 Mod:</b> <span style="color: #ff4757; font-size: 1.2em;">DÜNYA (Yerçekimi)</span><br>'
        quality_stat.text = '<b style="color: #00d4ff;">⭐ Kalite:</b> <span style="color: #ff4757; font-size: 1.2em;">Düşük (60-75%)</span><br><br>'
    else:
        mode_stat.text = '<b style="color: #7b2ff7;">🚀 Mod:</b> <span style="color: #2ed573; font-size: 1.2em;">UZAY (Mikrogravite)</span><br>'
        quality_stat.text = '<b style="color: #00d4ff;">⭐ Kalite:</b> <span style="color: #2ed573; font-size: 1.2em;">Mükemmel (95%+)</span><br><br>'


def switch_to_space():
    global gravity_mode
    gravity_mode = False
    for i, crystal in enumerate(attached_crystals):
        crystal.color = color.cyan if i == 0 else vector(0, random.uniform(0.75, 0.95), 1)
        crystal.opacity = random.uniform(0.88, 1.0)
        crystal.shininess = 0.9
    for glow in glow_layers:
        glow.color = color.cyan
    for walker in walkers:
        walker.color = vector(random.uniform(0.9, 1), random.uniform(0.5, 0.7), random.uniform(0.05, 0.15))
    update_stats()


def switch_to_earth():
    global gravity_mode
    gravity_mode = True
    for i, crystal in enumerate(attached_crystals):
        crystal.color = vector(1, 0.3, 0) if i == 0 else vector(1, random.uniform(0.2, 0.5), random.uniform(0, 0.1))
        crystal.opacity = random.uniform(0.55, 0.8)
        crystal.shininess = 0.4
    for glow in glow_layers:
        glow.color = vector(1, 0.3, 0)
    for walker in walkers:
        walker.color = vector(1, random.uniform(0.25, 0.4), 0.05)
    update_stats()


def reset_simulation():
    global attached_crystals
    for crystal in attached_crystals[1:]:
        crystal.visible = False
        del crystal
    attached_crystals = [core]
    core.color = color.cyan if not gravity_mode else vector(1, 0.3, 0)
    spawn_all_walkers()
    update_stats()


button(text="🚀 UZAY MODU", bind=lambda: switch_to_space())
scene.append_to_caption('  ')
button(text="🌍 DÜNYA MODU", bind=lambda: switch_to_earth())
scene.append_to_caption('  ')
button(text="🔄 SIFIRLA", bind=lambda: reset_simulation())
scene.append_to_caption('<br><br>')

scene.append_to_caption('<b style="color: #ffa502;">⚡ Simülasyon Hızı:</b> ')


def update_speed(s):
    global simulation_speed
    simulation_speed = s.value


slider(min=0.3, max=3.0, value=1.0, length=220, bind=update_speed)
scene.append_to_caption('<br><br>')

# ==================== ANA SİMÜLASYON ====================
frame_counter = 0
update_interval = 20

while True:
    rate(50)
    frame_counter += 1

    # Otomatik kamera dönme
    scene.forward = vector(-0.35 * math.cos(frame_counter * 0.002), -0.4, -1 * math.sin(frame_counter * 0.002))

    # Core animasyonu
    pulse = 0.85 + 0.15 * math.sin(frame_counter * 0.04)
    core.opacity = pulse

    # Glow animasyonu
    for i, glow in enumerate(glow_layers):
        phase_shift = i * 0.8
        glow.radius = (3.5 + i * 0.8) + 0.6 * math.sin(frame_counter * 0.06 + phase_shift)
        glow.opacity = (0.12 - i * 0.03) + 0.04 * math.sin(frame_counter * 0.05 + phase_shift)

    # Yörünge halkaları
    for i, ring in enumerate(orbit_rings):
        ring.opacity = 0.15 + 0.08 * math.sin(frame_counter * 0.03 + i * 0.1)

    # Walker hareketi ve kristalleşme
    for walker in walkers:
        if not walker.visible:
            continue
        vx = random.uniform(-1, 1);
        vy = random.uniform(-1, 1);
        vz = random.uniform(-1, 1)
        mag = math.sqrt(vx * vx + vy * vy + vz * vz)
        if mag > 0: vx /= mag; vy /= mag; vz /= mag
        if gravity_mode:
            vy -= 1.1 * random.random()
            if random.random() < 0.35:
                vx += random.uniform(-0.6, 0.6);
                vz += random.uniform(-0.6, 0.6)
        walker.pos += vector(vx * STEP_SIZE * simulation_speed, vy * STEP_SIZE * simulation_speed,
                             vz * STEP_SIZE * simulation_speed)

        attached = False
        for crystal in attached_crystals:
            if (walker.pos - crystal.pos).mag <= ATTACH_DISTANCE:
                color_c = vector(0, random.uniform(0.7, 0.95), random.uniform(0.95, 1)) if not gravity_mode else vector(
                    1, random.uniform(0.15, 0.55), random.uniform(0, 0.15))
                size = random.uniform(1.6, 2.1) if not gravity_mode else random.uniform(1.2, 3.0)
                opacity = random.uniform(0.85, 0.98) if not gravity_mode else random.uniform(0.45, 0.75)
                shininess = 0.9 if not gravity_mode else 0.3
                if random.random() < 0.65:
                    new_crystal = sphere(pos=walker.pos, radius=size, color=color_c, emissive=True, opacity=opacity,
                                         shininess=shininess)
                else:
                    box_size = size * random.uniform(0.75, 1.3)
                    new_crystal = box(pos=walker.pos, size=vector(box_size, size, box_size * random.uniform(0.8, 1.2)),
                                      color=color_c, emissive=True, opacity=opacity, shininess=shininess)
                attached_crystals.append(new_crystal)
                walker.visible = False
                attached = True
                break
        if attached or walker.pos.mag > SPAWN_RADIUS * 1.9:
            theta = math.acos(2 * random.random() - 1)
            phi = 2 * math.pi * random.random()
            r = SPAWN_RADIUS + random.uniform(-8, 12)
            walker.pos = vector(r * math.sin(theta) * math.cos(phi), r * math.sin(theta) * math.sin(phi),
                                r * math.cos(theta))
            walker.visible = True

    # Kristal animasyonu
    if frame_counter % 3 == 0:
        for i, crystal in enumerate(attached_crystals):
            if i == 0: continue
            if gravity_mode:
                crystal.opacity = random.uniform(0.45, 0.75)
            else:
                phase = crystal.pos.x * 0.08 + crystal.pos.y * 0.08 + crystal.pos.z * 0.08 + frame_counter * 0.015; crystal.opacity = 0.85 + 0.13 * abs(
                    math.sin(phase))

    if frame_counter % update_interval == 0:
        update_stats()
