import winsound
import time

# the notes
P = 0  # pause
C = 1
CS = 2  # C sharp
D = 3
DS = 4
E = 5
F = 6
FS = 7
G = 8
GS = 9
A = 10
AS = 11
B = 12
EN = 100  # eighth note
QN = 200  # quarter note
HN = 400  # half note
FN = 800  # full note


def play(octave, note, duration):
    """play note (C=1 to B=12), in octave (1-8), and duration (msec)"""
    if note == 0:  # a pause
        time.sleep(duration / 1000)
        return
    frequency = 32.7032  # C1
    for k in range(0, octave):  # compute C in given octave
        frequency *= 2
    for k in range(0, note):  # compute frequency of given note
        frequency *= 1.059463094  # 1.059463094 = 12th root of 2
    time.sleep(0.010)  # delay between keys
    winsound.Beep(int(frequency), duration)


def sound():
    play(2, G, QN)
    play(2, B, EN)
    play(3, D, EN)
    play(3, G, EN)
    play(3, B, QN)

    play(2, GS, QN)
    play(3, C, EN)
    play(3, DS, EN)
    play(3, GS, EN)
    play(4, C, QN)

    play(2, AS, QN)
    play(3, D, EN)
    play(3, F, EN)
    play(3, AS, EN)
    play(4, D, QN)


def not_sound():
    play(3, E, HN)
    play(3, CS, HN)
    play(3, C, QN)


def yes_sound():
    play(2, A, EN)
    play(2, A, EN)
    play(3, B, EN)

def smallBeep():
    play(2, A, EN)

def smallBeep2():
    play(3, A, QN)










