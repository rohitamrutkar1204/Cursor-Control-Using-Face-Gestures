
#Cursor-Control-Using-Face-Gestures<br>
The project has been developed with the aim of increasing Human-Computer Interaction for physically impaired people by making use of face gesture to control the mouse.

### Functionality-<br>
A] Left Click- Left eye wink <br>
B] Right Click - Right eye wink <br>
C] Activation - Symbolised by opening of mouth <br>
D] Deactivation - Symbolised by closing of mouth <br>
E] Cursor movement - Tracking the head movment. <br>
F] Scrolling - Winking of eye.<br>
***
For much better idea have a look at this video...


https://user-images.githubusercontent.com/48806865/137915733-c069e4e7-c063-445c-9213-8c4ea786d795.mp4
***
Dependencies used-<br>
1.*Python<br>
2.OpenCV<br>
3.Dlib Library<br>
4.PyAutoGUI*<br>
<br>
Dlib library comes with an inbuilt face detector module that has a very good accuracy. Dlib also marksup *facial landmarks* on the detected face.
The facial landmarks are the key for the entire gesture recognition. 
***
To see whether an eye is opened or closed, the facial landmarks associated with the eye are tracked, and their ASPECT RATIO is calculated.<br><br>
![image](https://user-images.githubusercontent.com/48806865/137919553-0049c26d-1764-4dc4-b215-e9374405a76a.png)<br><br>
<t>»If eye is closed then EAR will fall to 0.<br>
<t>»And if eye is opened then EAR will fall to a value > 0<br>

On similar terms, I have calculated MAR.<br>
***
Once identified which gesture has been done, we need to call the functionality programmatically. This is where PyAutoGUI helps in. It helps to control mouse and keyboard programmatically.


 
