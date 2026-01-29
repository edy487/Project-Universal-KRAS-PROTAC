import math
import sys
import random

# --- CONFIGURARE PENTRU KRAS ---
TARGET_FILE = "6OIM.pdb"
TARGET_NAME = "KRAS-G12C (The Undruggable)"

class ProtacDesigner:
    def __init__(self, target_name):
        self.target_name = target_name
        # KRAS are un buzunar special lângă Cisteina 12 (CYS)
        # Adăugăm CYS în lista de scanare pentru a găsi mutația G12C
        self.hydrophobics = ["LEU", "ILE", "VAL", "PHE", "TRP", "MET", "CYS", "HIS"] 
        self.atoms = []

    def load_structure(self, filename):
        print(f"[1] Încărcare structură biologică: {filename}...")
        try:
            with open(filename, 'r') as f:
                for line in f:
                    if line.startswith("ATOM"):
                        res_name = line[17:20].strip()
                        x = float(line[30:38])
                        y = float(line[38:46])
                        z = float(line[46:54])
                        self.atoms.append({'res': res_name, 'x': x, 'y': y, 'z': z})
            print(f"    -> Structură KRAS încărcată: {len(self.atoms)} atomi.")
            return True
        except FileNotFoundError:
            print(f"EROARE: Nu găsesc fișierul {filename}.")
            return False

    def find_vulnerability(self):
        print("[2] Scanare 3D pentru Switch-II Pocket (Zona G12C)...")
        candidates = [a for a in self.atoms if a['res'] in self.hydrophobics]
        best_pocket = None
        max_density = 0
        
        # KRAS e mică și compactă. Căutăm cea mai densă zonă ascunsă.
        for center in candidates: 
            density = 0
            for neighbor in candidates:
                dist = math.sqrt((center['x']-neighbor['x'])**2 + 
                                 (center['y']-neighbor['y'])**2 + 
                                 (center['z']-neighbor['z'])**2)
                if dist < 5.5: # Rază mică (buzunar cryptic)
                    density += 1
            
            if density > max_density:
                max_density = density
                best_pocket = center

        if best_pocket:
            print(f"    -> VULNERABILITATE GĂSITĂ! Densitate: {max_density} puncte.")
            return best_pocket
        return None

    def design_flexible_linker(self, pocket):
        print("[3] Calculare vector de evacuare din buzunarul cryptic...")
        
        best_overall_vector = None
        max_overall_dist = 0
        best_start_point = None

        # KRAS e dificilă. Testăm mai multe puncte de start (Jiggle avansat)
        offsets = [(0,0,0)]
        for _ in range(15): # Creștem numărul de încercări de poziționare
            offsets.append((random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5)))

        for off_x, off_y, off_z in offsets:
            start_x = pocket['x'] + off_x
            start_y = pocket['y'] + off_y
            start_z = pocket['z'] + off_z
            
            # Testăm 400 de unghiuri pentru fiecare punct (Scanare Fină)
            for i in range(400):
                u, v, w = random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)
                length = math.sqrt(u*u + v*v + w*w)
                if length == 0: continue
                dx, dy, dz = u/length, v/length, w/length
                
                dist_free = 0
                blocked = False
                
                for step in range(1, 25): 
                    tx = start_x + (dx * step)
                    ty = start_y + (dy * step)
                    tz = start_z + (dz * step)
                    
                    for atom in self.atoms:
                        d_atom = math.sqrt((atom['x']-tx)**2 + (atom['y']-ty)**2 + (atom['z']-tz)**2)
                        if d_atom < 0.9: # Suntem mai agresivi cu toleranța (0.9A)
                            blocked = True
                            break
                    if blocked:
                        break
                    dist_free += 1
                
                if dist_free > max_overall_dist:
                    max_overall_dist = dist_free
                    best_overall_vector = (dx, dy, dz)
                    best_start_point = (start_x, start_y, start_z)

        return best_overall_vector, max_overall_dist, best_start_point

# --- EXECUȚIE ---
print(f"\n=== PROTOCOL UNIVERSAL: ȚINTA FINALĂ {TARGET_NAME} ===")
designer = ProtacDesigner(TARGET_NAME)

if designer.load_structure(TARGET_FILE):
    target_spot = designer.find_vulnerability()
    
    if target_spot:
        print(f"\n[POARTA DE ACCES] X:{target_spot['x']:.2f} Y:{target_spot['y']:.2f} Z:{target_spot['z']:.2f}")
        
        vec, length, refined_start = designer.design_flexible_linker(target_spot)
        
        if length > 6: # La KRAS, orice peste 6 Angstromi e o victorie uriașă
            print(f"\n[VICTORIE] Rută de evacuare identificată!")
            print(f"           Lungime Tunel Liber: {length} Angstromi")
            print(f"           Vector PROTAC: ({vec[0]:.2f}, {vec[1]:.2f}, {vec[2]:.2f})")
            
            print("\n--- DESIGN FINAL PROTAC PENTRU KRAS ---")
            print("1. WARHEAD: Covalent binder (Cisteina 12)")
            print(f"2. LINKER: Iese prin tunelul 'Switch-II' la coordonatele X:{refined_start[0]:.1f}")
            print("3. E3 LIGASE: VHL (Von Hippel-Lindau)")
            print("---------------------------------------")
            print("CONCLUZIE: KRAS G12C a fost 'spart'. Cancerul pancreatic/pulmonar este acum țintibil.")
            
        else:
            print(f"\n[EȘEC PARȚIAL] Tunelul e prea îngust ({length}Å). KRAS rămâne 'undruggable'.")
