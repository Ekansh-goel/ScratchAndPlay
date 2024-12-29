# Scrollable Scratch-to-Reveal Game

A simple yet engaging Python game built using **Pygame**. The game allows you to scroll through a grid of hidden messages and reveal them by scratching the surface with your mouse. Perfect for creating interactive experiences or surprises!

## Features
- **Scrollable Grid:** Navigate through a virtual grid that can be larger than the visible screen.
- **Scratch to Reveal:** Use your mouse to scratch surfaces and uncover hidden messages.
- **Customizable:** Easily modify grid size, hidden messages, colors, and other parameters.

## How to Run
1. Make sure you have Python installed (version 3.6 or higher).
2. Install Pygame by running:
   ```bash
   pip install pygame
   ```
3. Clone this repository or copy the script to your local machine.
4. Create a `hidden_messages2.txt` file with your custom messages (one per line).
5. Run the script:
   ```bash
   python index.py
   ```

## Controls
- **Mouse Left Click:** Scratch the surface to reveal messages.
- **Arrow Keys:** Scroll through the grid.
- **Right Mouse Button (Hold):** Drag to scroll.

## File Structure
- `index.py`: Main game script.
- `hidden_messages2.txt`: File containing hidden messages. Ensure it exists in the same directory as the script.

## Customization
You can easily adjust the following parameters in the code:
- **Grid size**: Change `GRID_SIZE` to modify the number of circles in the grid.
- **Colors**: Modify `BLACK`, `WHITE`, and `GREY` to customize the theme.
- **Scratch Radius**: Adjust `SCRATCH_RADIUS` to change the scratch effect size.

## Example Hidden Messages
Create a file named `hidden_messages2.txt` and add your custom messages, one per line. Example:
```
Congratulations!
You found me!
Better luck next time!
Keep scratching!
```

## Screenshot
![Screenshot Placeholder](#) *(Add a screenshot here showing the grid and scratch effect)*

## Requirements
- Python 3.6+
- Pygame

## License
This project is open-source and available under the MIT License. Feel free to modify and distribute as you like.

## Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.
