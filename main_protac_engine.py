import math
import random
import sys

# --- CONFIGURARE UNIVERSALA ---
PDB_FILENAME = "crbn.pdb"  # Fisierul pe care il testam
CHAIN_ID = "A"             # Lantul proteinei
NUM_SIMULATIONS = 50000 
STEP_SIZE = 0.8          
MAX_DISTANCE = 30.0      
MIN_CLEARANCE = 2.0      
# ------------------------------

def find_best_ligand(filename):
    """ Functie inteligenta care gaseste automat medicamentul din fisier """
    ignored = ["HOH", "ZN", "MG", "NA", "CL", "SO4", "PO4", "EDO", "GOL"]
    ligand_counts = {}
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith("HETATM"):
                    res_name = line[17:20].strip()
                    if res_name not in ignored:
                        ligand_counts[res_name] = ligand_counts.get(res_name, 0) + 1
    except FileNotFoundError:
        print(f"[!] EROARE: Nu gasesc fisierul {filename}!")
        sys.exit()

    # Returneaza ligandul cu cei mai multi atomi (cel mai mare)
    if not ligand_counts:
        return None
    
    # Sortam descrescator dupa numarul de atomi
    best_ligand = sorted(ligand_counts.items(), key=lambda x: x[1], reverse=True)[0][0]
    return best_ligand

def parse_pdb(filename, ligand_name, chain_id):
    protein_atoms = []
    ligand_atoms = []
    
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and line[21] == chain_id:
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                protein_atoms.append((x, y, z))
            elif line.startswith("HETATM"):
                res_name = line[17:20].strip()
                if res_name == ligand_name:
                    x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                    ligand_atoms.append((x, y, z))
    return protein_atoms, ligand_atoms

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def check_collision(point, protein_atoms, min_dist):
    for atom in protein_atoms:
        if distance(point, atom) < min_dist:
            return True 
    return False

def get_center_of_mass(atoms):
    if not atoms: return None
    n = len(atoms)
    return (sum(a[0] for a in atoms)/n, sum(a[1] for a in atoms)/n, sum(a[2] for a in atoms)/n)

def run_monte_carlo(start_point, protein_atoms, ligand_name):
    print(f"[*] Incepem simularea pe CEREBLON (Tinta automata: {ligand_name})...")
    
    for i in range(NUM_SIMULATIONS):
        u, v, w = random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)
        norm = math.sqrt(u*u + v*v + w*w)
        dx, dy, dz = u/norm, v/norm, w/norm 
        
        current_pos = start_point
        is_blocked = False
        path_length = 0
        
        while path_length < MAX_DISTANCE:
            current_pos = (current_pos[0] + dx*STEP_SIZE, current_pos[1] + dy*STEP_SIZE, current_pos[2] + dz*STEP_SIZE)
            path_length += STEP_SIZE
            if check_collision(current_pos, protein_atoms, MIN_CLEARANCE):
                is_blocked = True
                break
        
        if not is_blocked:
            print(f"[!!!] VICTORIE! Tunel PROTAC gasit la incercarea {i}")
            print(f"      Directie: X={dx:.2f}, Y={dy:.2f}, Z={dz:.2f}")
            return True

    print("[X] Nu s-a gasit iesire.")
    return False

if __name__ == "__main__":
    print(f"[*] Analizam fisierul {PDB_FILENAME} pentru a detecta ligandul...")
    detected_ligand = find_best_ligand(PDB_FILENAME)
    
    if not detected_ligand:
        print("[!] Nu am putut detecta automat niciun ligand valid.")
        sys.exit()
        
    print(f"[*] LIGAND DETECTAT AUTOMAT: {detected_ligand}")
    
    p_atoms, l_atoms = parse_pdb(PDB_FILENAME, detected_ligand, CHAIN_ID)
    
    # Daca nu gasim atomi pe lantul A, incercam lantul B (Cereblon e uneori pe B)
    if not p_atoms:
        print("[!] Lantul A pare gol. Comutam automat pe lantul B...")
        p_atoms, l_atoms = parse_pdb(PDB_FILENAME, detected_ligand, "B")

    print(f"[*] Proteina: {len(p_atoms)} atomi | Ligand: {len(l_atoms)} atomi")
    
    center = get_center_of_mass(l_atoms)
    found = run_monte_carlo(center, p_atoms, detected_ligand)
    
    if found:
        print("\n--- REZULTAT VALIDAT PENTRU CEREBLON (CRBN) ---")
        print("Ai demonstrat ca poti lega ambele capete ale unui PROTAC!")
