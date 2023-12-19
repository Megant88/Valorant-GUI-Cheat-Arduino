# Valorant Arduino Based Color Cheat with Complex GUI written in Tkinter
Proof of concept of a full fledged external valorant cheat with a python based complex gui


# About it
This is a full fledged external valorant cheat, it contains an arduino based triggerbot/aimbot and an api based Instant Locker. 
The impressive thing about this project though is not the cheat, BUT the GUI, the GUI is made in Tkinter and honestly covers all features most native based GUI's have,
such as automatic hotkey to virtual key code mapping, a config system and pretty sliders. 
The cheat itself here is not really important, its just here to demonstrate the config system.

#Features GUI:
- Login/Cheat Page
- Page Logic
- Custom Slider
- Custom Hotkey input (press button, press key, boom new hotkey set(both keyboard&mouse))
- Automatically detects virtual key codes
- Config System (pretty hot)

#Features Cheat:
- Aimbot
- Triggerbot
- Instant Locker (api based)
- Simple RCS
everything above ofc has more sub functions.


This is not connected to any auth or anti cracking system, but it can easily connected with an auth and contributed.
I feel quite heartbroken about this project, it took me quite some time to make, I think the GUI is beautiful for python, not only for python but also for Tkinter,
but since the GUI is detected I have no use for this but I thought it be interesting to share. I had planned on selling this, if I would have it be a big project, but that plan is over.
THe GUI is being flagged since it creates a window, thus causing a flag which results in a delayed ban. The Cheat itself is undetected, but relies on a spoofed arduino r3.

Take this project as your guideline to GUI's and complexity of them, but also as a guidline for arduino based color cheats.
Im confident enough to say that this can sit on the same table as many native based guis.


# Preview
[![Watch the video](https://cdn-cf-east.streamable.com/image/t8ctpa.jpg?Expires=1703202961864&Key-Pair-Id=APKAIEYUVEN4EVB2OKEQ&Signature=kSASfwmiCV3PCK4KrUMQZ1Ekse1FQs0h3fHv8SJb3UsbEpp0xSa8fjZYpHXHhBbxEtlU9-L07iHb9Z~yDE9~ckgwrUzkDzdZ0g2rs2ccyIjaGKbtzvcNgxCp1dpR~F54nsTyD63PhzhtYMW6eZsHoe-DOfOndFjP6omQk1EAWmzoMrMBQXn5-OpoudZl0qOVdzLPeeUfdqPmIUnhSwuqQpOdIrZoYHd7XY8ZYV~azx4dCzVWvhbVHvZAWUsbrzcn4Ue1MWLnebDfdcLzLlaQwbxBVZRe8llnLNFxDoGUfeQUntSL03~4pj~C4F-dMkP3D9dVGuJ8LkZt59OG1vXkHg__)](https://streamable.com/t8ctpa)


# How to setup:
- Install Python
- Download all imports
- Download Arduino IDE
- Upload /files/MouseInstructArduino to your Arduino
- It may take a little first time opening since its getting assets from url, but once opened they should be cached

to compile with nuitka  use ```nuitka --disable-console --onefile --enable-plugin=tk-inter - main.py```

Feel free to experiment with the source, in case you have trouble with it I am available for help. But I recommend troubleshooting by yourself before coming to me, or alternative checking unknowncheats for more.
- https://www.unknowncheats.me/forum/valorant/613998-source-complex-python-gui-valorant-cheat.html

# Eductional Purpose
This project is for educational purpose only, it is proof of concept for high level cheating techniques which dont rely on memory access.
I am not responsible for any third person use of this release, do with it what you want.

But if this helped you please star the repo and checkout my UC Profile, and if you used some of my code in your project lmk, i'd love to see my work function in your project. I can even help

