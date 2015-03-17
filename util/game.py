import curses
import time
import pyaudio
import wave
import time
import sys
import queue
from random import randint

from util import play
from util import audio
from util import song_util

KEY_DELAY = 6
SPACING = 13
BUMPERS_INDEX = 16
HEADER_SIZE = 5
DEL_KEY = -9999

keys = []
noteStream = queue.Queue()

def renderHead(stdscr, song, score, chain):
    height, width = stdscr.getmaxyx()
    
    stdscr.addstr(1, 1, song)
    
    stdscr.addstr(1, width-20, "Score: " + str(score))
    stdscr.addstr(2, width-20, "Chain: " + str(chain))
    
    for i in range(0, width-1):
        stdscr.addstr(4, i, " ", curses.A_REVERSE)

def renderBumpers(stdscr, bumpers_index, colorcode):
    height, width = stdscr.getmaxyx()
    start = 1
    for i in range(4):
        for j in range(5):
            if j == 2:
                stdscr.addstr(height-start-j, bumpers_index+i*SPACING, "+")
                stdscr.addstr(height-start-j, bumpers_index+i*SPACING+5, "+")
            else:
                stdscr.addstr(height-start-j, bumpers_index+i*SPACING, "|")
                stdscr.addstr(height-start-j, bumpers_index+i*SPACING+5, "|")
            if colorcode[i]:
                stdscr.addstr(height-start-j, bumpers_index+i*SPACING+1, "    ", curses.color_pair(colorcode[i]))
             
def pushNote(note):
    noteStream.put(note)

def addNote(index):
    keys.append([index, HEADER_SIZE])
    
def cleanUp(stdscr, wave_file, player, stream):
    stdscr.nodelay(0)
    play.end_playback(wave_file, player, stream)

def game(stdscr, song_notes):
    height, width = stdscr.getmaxyx()

    bumpers_width = SPACING * 3 + 7
    bumpers_index = width // 2 - bumpers_width // 2

    curses.curs_set(0)
    stdscr.clear()
    stdscr.nodelay(1)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_MAGENTA)

    score = 0
    chain = 0

    keys.append([2,1])
    keyDelay = KEY_DELAY
    keyPrev = -1
    
    (wf, player, stream) = play.start_song(song_notes, (height-4.0-HEADER_SIZE) / 30.0, pushNote)
    while 1:
        time.sleep(1/30.0)

        colorcode = [0, 0, 0, 0]
        
        if not noteStream.empty():
            addNote(noteStream.get())

        keyNum = stdscr.getch()
        stdscr.clear()
        
        if keyNum == -1 and keyDelay > 0:
            keyDelay -= 1
            keyNum = keyPrev
        elif keyNum == ord('d'):
            keyDelay = KEY_DELAY
            keyNum = 0
        elif keyNum == ord('f'):
            keyDelay = KEY_DELAY
            keyNum = 1
        elif keyNum == ord('j'):
            keyDelay = KEY_DELAY
            keyNum = 2
        elif keyNum == ord('k'):
            keyDelay = KEY_DELAY
            keyNum = 3
        if keyNum == ord('q'):
            cleanUp(stdscr, wf, player, stream)
            return
        
        keyPrev = keyNum
        
        for key in keys:
            if key[0] == -1 and key[1] == height-3:
                cleanUp(stdscr, wf, player, stream)
                return
            elif key[0] == -1:
                key[1] += 1
                continue
            
            if key[1] >= height:
                colorcode[key[0]] = 1
                chain = 0
                score -= 100
                key[0] = DEL_KEY # Mark key for deletion
            elif key[1] < height and key[1] > height-5:
                if keyNum == key[0]:
                    dist = abs(key[1] - height + 2)
                    colorcode[key[0]] = 2 + dist
                    score += 100 + chain * 50 - dist * 25
                    chain += 1
                    key[0] = DEL_KEY # Mark key for deletion
                else:
                    stdscr.addstr(int(key[1]), key[0]*SPACING + bumpers_index, " ++++ ")
            else:
                stdscr.addstr(int(key[1]), key[0]*SPACING + bumpers_index, " ++++ ")
            
            key[1] += 1

        # Delete marked keys
        i = 0
        while i < len(keys):
            if keys[i][0] == DEL_KEY:
                del keys[i]
            else:
                i += 1

        renderBumpers(stdscr, bumpers_index, colorcode)
        renderHead(stdscr, song_notes, score, chain)

        stdscr.refresh()
