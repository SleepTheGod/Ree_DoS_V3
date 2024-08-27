# Ree_DoS_V3

Overview

Ree_DoS_V3 is an advanced network stress testing tool designed for both Layer 4 and Layer 7 attacks, as well as XML-RPC stress testing. This tool is built to impress and is suited for various security testing and network performance evaluations.

Features

- Layer 4 Attacks: Supports TCP and UDP stress testing.
- Layer 7 Attacks: Implements HTTP GET and POST requests for stress testing.
- XML-RPC Attacks: Allows for stress testing via XML-RPC methods.
- Chat Client: Connects to a server using SSL/TLS for secure communication.
- GUI: Provides a user-friendly graphical interface for stress testing.

Installation

1. Clone the repository

   git clone https://github.com/SleepTheGod/Ree_DoS_V3.git
   cd Ree_DoS_V3

2. Install the required dependencies

   pip install -r requirements.txt

Usage

Command Line Interface

- Chat Client Mode

  python main.py

- Layer 7 Stress Testing

  - GET DOS

    python main.py -t get http://example.com

  - POST DOS

    python main.py -t post http://example.com

- Layer 4 Stress Testing:

  - TCP DOS

    python main.py -l4 tcp 192.168.1.1 80

  - UDP DOS

    python main.py -l4 udp 192.168.1.1 80

- XML-RPC Stress Testing

  python main.py -x http://example.com/RPC2 method_name param1 param2 ...

GUI

1. Start the GUI application

   python gui.py

Files

- main.py: Main script for command-line functionality.
- gui.py: Graphical user interface script.
- requirements.txt: List of required Python packages.

Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any improvements or bug fixes.

License

This project is licensed under the MIT License - see the LICENSE file for details.

Contact

For any questions or support, please reach out to SleepTheGod at https://t.me/SleepTheGod Note I DO NOT HAVE A TWITTER ACCOUNT AND AM NOT ON THEIR PLATFORM ANYONE CLAIMING TO BE ME IS NOT.

