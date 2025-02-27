# **Password Manager**

A secure and user-friendly password manager application to generate, store, and manage your passwords.

## Features

- **Password Generation**: Generate strong and secure passwords.
- **Password Storage**: Store passwords securely using encryption.
                        All passwords are saved locally.
- **User Management**: Manage multiple users with individual password storage.
- **Password Visibility Toggle**: Show or hide passwords with a single click.
- **Scrollable List**: Display saved sites in a scrollable list with site names and 
                       dates saved.
- **Add New Passwords**: Easily add new passwords through a user-friendly interface.
- **Encryption**: Encryption logic uses a Feistel-based encryption in combination with 
                  XOR encryption.
  - `Feistel encryption`: Takes a password in plaintext and encodes each character using 
                          a masterkey that is unique to each user.
  - `XOR`: Once the Feistel rounds are complete, the encoded password is ran through
           a XOR encryption for an addional layer of security.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/password_manager.git
    cd password_manager
    ```
2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
3. **Run the application**:
    ```sh
    python main.py
    ```

## Usage

- **Dashboard**: The main interface where you can view and manage your saved passwords.
- **Add New Password**: Click the "New Password" button to add a new password.
- **Show Password**: Click on a site in the list to view the password in a new window.
- **Toggle Password Visibility**: Use the "Show/Hide" button to toggle the visibility of the password.

## File Structure

- **src**
  - **UI/**
     - `dashboard.py`: The main dashboard interface.
     - `newPasswordSave.py`: Interface for adding new passwords.
     - `showPassword.py`: Interface for displaying passwords.
     - `login.py`: Interface for login screen, application launches at this window
     - `styles.py`: Styling constants and functions for the UI.
  - **database/**
     - `userPasswords.py`: Functions for opening and saving passwords for currently logged user.
     - `passwordStorage.py`: Functions for checking login details.
  - **security/**
     - `generatePassword.py`: Password generation logic.
     - `encrypt.py`: Functions for encoding and decoding passwords.
  

- **Security**
  - Passwords are stored in JSON files with encryption.
  - Sensitive files are ignored by Git using the `.gitignore` file.

- **Contributing**
  - Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- Tkinter for the GUI framework.
- Python for the programming language.
- GitHub Copilot for code assistance.

### This project is a work in progress, and the README will be updated as development continues.