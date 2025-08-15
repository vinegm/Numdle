<h1>Numdle</h1>

Numdle is a desktop number guessing game made with python, it was inspired by <a href="https://term.ooo" target="_blank" title="Check Termo Out">termo</a> and <a href="https://www.nytimes.com/games/wordle/index.html" target="_blank" title="Check Wordle Out">wordle</a>.

<h2>Installation</h2>

If you wish to play Numdle trough the .exe, you may only keep the "assets" folder and play as you like, it might only run on windows (I'm not sure if it will run on mac and linux as I don't have a way to test), if you wish to play with the .py just download the necessary libraries and have fun!

<h2>Used Libraries</h2>

<table>
  <tr>
    <th>Library</th>
    <th>Used For</th>
  </tr>
  <tr>
    <td>Tkinter</td>
    <td>Creating the GUI</td>
  </tr>
  <tr>
    <td>PIL</td>
    <td>Image processing</td>
  </tr>
  <tr>
    <td>Numpy</td>
    <td>Manipulation of numbers</td>
  </tr>
  <tr>
    <td>Sqlite3</td>
    <td>Storage of data</td>
  </tr>
</table>

<h2>The Game</h2>

This is the game window, in the window title it will display the game name and the current user, in this case being "Numdle (Guest)"

![image](https://github.com/vinegm/Numdle/assets/117782568/da73ed23-4ee7-4303-954f-6599f0c16c3f)

<h2>The Player</h2>

To change the current player you can simply click on the profile icon and type a new player nickname, it doesn't use a login system for symplicity

![image](https://github.com/vinegm/Numdle/assets/117782568/e1310417-1b21-4adf-b8c0-e65442c26892)

By clicking the icon a popup will ask you for a new nickname

![image](https://github.com/vinegm/Numdle/assets/117782568/9604d283-5505-4e92-b478-8dde2b4c72d8)

<h2>Score System</h2>

The score of the player is based on the amount of guesses made to get the genereted number, the more guesses used, the less score is earned

<table>
  <tr>
    <th>Guesses</th>
    <th>Score</th>
  </tr>
  <tr>
    <td>1</td>
    <td>5</td>
  </tr>
  <tr>
    <td>2</td>
    <td>4</td>
  </tr>
  <tr>
    <td>3</td>
    <td>3</td>
  </tr>
  <tr>
    <td>4</td>
    <td>2</td>
  </tr>
  <tr>
    <td>5</td>
    <td>1</td>
  </tr>
  <tr>
    <td>6</td>
    <td>0</td>
  </tr>
</table>

<h2>The Leaderboard</h2>

To access the leaderboad click the leaderboard icon in the game frame

![image](https://github.com/vinegm/Numdle/assets/117782568/4b2139da-854a-41b2-a69f-6d3f00944ab1)

The leaderboard displays the top 10 local players with the best score, and the current player personal best below

![image](https://github.com/vinegm/Numdle/assets/117782568/14a3d5a7-d4bf-47d8-9771-b1592cb3d27a)

<h2>Thank You!</h2>

Thanks for checking my project out!


