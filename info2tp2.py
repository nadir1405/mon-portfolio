import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Définition d'un sinus 
amplitude=2
frequence=1/5
dephasage=0

def sinus(t,amplitude,frequence,dephasage): 
    return amplitude* np.sin(2. * np.pi * t * frequence + dephasage)

#simulation d'un temps continu sur une durée D=10s
D=10
N=100
tp = np.linspace(0., D, N) # Grille plus fine pour tracer l'allure du signal parfait

signal= 2+ sinus(tp,amplitude,frequence,dephasage)
amplitude_min=np.nanmin(signal)
amplitude_max=np.nanmax(signal)

plt.figure(figsize=(15,6))
plt.plot(tp, signal,'p', label = u"Signal reel")
plt.title("signal original temps discret")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (Volt)")
plt.show()

plt.figure(figsize=(15,6))
plt.plot(tp, signal, 'b-', label = u"Signal reel")
plt.title("signal original visuellement quasi continu")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (Volt)")
plt.show()
def echantillonne(signal,pasTemporel): 
    signalE=np.full_like(signal, np.nan)
    signalE[::pasTemporel]=signal[::pasTemporel]
    return signalE

pasT=0.5
pasTsimule=int(pasT*N/D) #pasT=0.1 s echelle 100 points pour 1s
tempsDiscret = tp[::pasTsimule]

signalEch=echantillonne(signal,pasTsimule)

plt.figure(figsize=(15,6))
plt.plot(tp, signal, 'b-', label = u"Signal reel")
plt.plot(tp, signalEch,'p', c='r',label = u"Signal Ech")
plt.vlines(tempsDiscret, amplitude_min, amplitude_max ,colors='gray', linestyles='dashed')
plt.title("signal original temps discret")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (Volt)")
plt.show()

plt.figure(figsize=(15,6))
plt.plot(tp, signalEch,'p', label = u"Signal Ech")
plt.title(f"signal échantillonné pas = {pasT} s")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (Volt)")
plt.show()
def quantifie(signal, nb_bits,amplitude_min,amplitude_max):
    # Nombre de niveaux de quantification
    niveaux = 2**nb_bits

    # Calcul des limites de quantification
    amplitude_max = amplitude_max+0.000001  # Valeur maximale du signal
    pas = (amplitude_max - amplitude_min) / niveaux  # Intervalle entre deux niveaux

    # Quantification
    #signal[signal==amplitude_max]=amplitude_max-0.000001
    signal_quantifie = amplitude_min+ np.floor((signal - amplitude_min) / pas)*pas

    return signal_quantifie

#parametrs nb= nombre de bits
nb=4
pas= (amplitude_max - amplitude_min) / 2**nb
signalq = quantifie(signal, nb,amplitude_min,amplitude_max)


plt.figure(figsize=(15, 6))
plt.plot(tp, signal, 'b-', label="Signal original (continu)")
for i in range(2**nb):
    plt.axhline(y=amplitude_min + i * pas, color='gray', linestyle='--', alpha=0.5)
plt.title(f"signal avec grille de quantification ({nb} bits)")
plt.show()

plt.figure(figsize=(15, 6))
plt.plot(tp, signal, 'b-', label="Signal original (continu)")
for i in range(2**nb):
    plt.axhline(y=amplitude_min + i * pas, color='gray', linestyle='--', alpha=0.5)
plt.step(tp, signalq, 'r-', label=f"Signal quantifié ({nb} bits)",where="mid")
plt.title(f"Quantification d'un sinus ({nb} bits)")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.show()

plt.figure(figsize=(15, 6))
plt.plot(tp, signalq, 'r-', label=f"Signal quantifié ({nb} bits)")
plt.title(f"signal quantifié - temps discret({nb} bits)")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.show()
sig1=quantifie(signalEch,nb,amplitude_min,amplitude_max)
sig2=echantillonne(signalq,pasTsimule)

plt.figure(figsize=(15, 6))
plt.plot(tp, signal, 'b-', label="Signal original (continu)")
plt.step(tp, signalq, 'g-', label=f"Signal quantifié ({nb} bits)", where="mid")
plt.plot(tp, sig1, 'p', c='red',label=f"Signal numérisé")
plt.title(f"Numérisation d'une sinusoide - échantillonnage puis quantifié (({pasT}s ;{nb} bits)")
plt.vlines(tempsDiscret,amplitude_min,amplitude_max,colors='gray',linestyles='dotted')
for i in range(2**nb):
    plt.axhline(y=amplitude_min + i * pas, color='gray', linestyle='--', alpha=0.5)
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.show()

plt.figure(figsize=(15, 6))
plt.plot(tp, signal, 'b-', label="Signal original (continu)")
plt.plot(tp, signalEch, 'p',c='g', label=f"Signal échantillonné")
plt.plot(tp, sig2, 'p', c='red',label=f"Signal numérisé")
plt.vlines(tempsDiscret,amplitude_min,amplitude_max,colors='gray',linestyles='dotted')
for i in range(2**nb):
    plt.axhline(y=amplitude_min + i * pas, color='gray', linestyle='--', alpha=0.5)
plt.title(f"Numérisation d'une sinusoide - quantification puis échantillonage(({pasT}s ;{nb} bits)")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.show()

plt.figure(figsize=(15, 6))
plt.plot(tp, sig1, 'p',c='g', label=f"Signal quantifié puis échantillonné")
plt.plot(tp, sig2, 'p', c='red',label=f"Signal échantillonné puis quantifié")
plt.vlines(tempsDiscret,amplitude_min,amplitude_max,colors='gray',linestyles='dotted')
for i in range(2**nb):
    plt.axhline(y=amplitude_min + i * pas, color='gray', linestyle='--', alpha=0.5)
plt.title(f"Signal numérisé ")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.show()