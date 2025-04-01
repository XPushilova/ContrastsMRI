import numpy as np
import matplotlib.pyplot as plt
import scipy.io

# Načtení dat
mat = scipy.io.loadmat('mozek_rez.mat')
Rhoa = mat['Rhoa']
T1a = mat['T1a']
T2a = mat['T2a']
T2Stara = mat['T2Stara']

# Definice sekvencí
epsilon = 1e-10  # Malé číslo pro zabránění dělení nulou

def S_SE(TR, TE):
    return Rhoa * (1 - np.exp(-TR / (T1a + epsilon))) * np.exp(-TE / (T2a + epsilon))

def S_GE(TR, TE, FA):
    return Rhoa * np.sin(np.radians(FA)) * (1 - np.exp(-TR / (T1a + epsilon))) * \
           np.exp(-TE / (T2Stara + epsilon)) / (1 - np.cos(np.radians(FA)) * np.exp(-TR / (T1a + epsilon)) + epsilon)

def S_IR(TR, TE, TI):
    return Rhoa * (1 - 2 * np.exp(-TI / (T1a + epsilon)) + np.exp(-TR / (T1a + epsilon))) * np.exp(-TE / (T2a + epsilon))

# Ukázkové snímky - SE
img_T1 = S_SE(0.5, 0.02)
img_T2 = S_SE(2, 0.08)
img_pd = S_SE(2, 0.02)

plt.figure(1)
plt.suptitle('Spin echo', fontsize=20, fontweight='bold')
for i, (img, title) in enumerate(zip([img_T1, img_T2, img_pd], ['T1 váhování', 'T2 váhování', 'PD váhování'])):
    plt.subplot(1, 3, i+1)
    plt.imshow(img, cmap='gray')
    plt.colorbar()
    plt.title(title)

# Ukázkové snímky - GE pro různé úhly
angles = [15, 30, 45, 90]
plt.figure(2)
plt.suptitle('Gradientní echo', fontsize=20, fontweight='bold')
for i, angle in enumerate(angles):
    img = S_GE(0.5, 0.02, angle)
    plt.subplot(2, 2, i+1)
    plt.imshow(img, cmap='gray')
    plt.colorbar()
    plt.title(f'FA {angle}°')

# Ukázkové snímky - GE pro časy TE
TEs = [0.01, 0.03, 0.06, 0.1]
plt.figure(3)
plt.suptitle('Gradientní echo', fontsize=20, fontweight='bold')
for i, TE in enumerate(TEs):
    img = S_GE(0.5, TE, 30)
    plt.subplot(2, 2, i+1)
    plt.imshow(img, cmap='gray')
    plt.colorbar()
    plt.title(f'TE {int(TE*1000)} ms')

# Ukázkové snímky - inversion recovery
IRs = [S_IR(10, 0.02, TI) for TI in [1.67, 0.37, 0.58]]
plt.figure(4)
plt.suptitle('Inversion recovery s TR>>T1', fontsize=20, fontweight='bold')
for i, (img, title) in enumerate(zip(IRs, ['Potlačení vody/CSF', 'Potlačení bílé hmoty', 'Potlačení šedé hmoty'])):
    plt.subplot(1, 3, i+1)
    plt.imshow(np.abs(img), cmap='gray')
    plt.colorbar()
    plt.title(title)

plt.show()
