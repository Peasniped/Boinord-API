# BoINord Waitlist API 

## Overview
This is a project designed to interact with the API on boinord.dk to fetch and display waitlist position and information about apartments that you are waitlisted for with BoINord.
It allows users to easily use their credentials to retrieve a list of apartments waitlist positions in order to track it more closely.

---


## Prerequisites
Before running the project, ensure you have the following installed:

- Python 3.7 or higher
- `requests` library

To install the `requests` library, use:
```bash
pip install requests
```

---

## Getting Started

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/Peasniped/Boinord-API.git
cd apartment-info-fetcher
```

### 2. Set Up Your Credentials
Replace the placeholder values for `username` and `password` in the `main` block and execute the script

### Example Output
If the login is successful, the script will print the apartment details:
```
Apartment Variant ID: 335-601-2-1-2
Apartment Variant: Torvegade, Birkevej, Kingosvej - Pandrup - Rækkehus/hus - 2v
Waitlist Position: 45
--------------------------------------------------
Apartment Variant ID: 335-519-1-1-2
Apartment Variant: Vrængmosevej 8 m.fl. - Østervrå - Lejlighed - 2v
Waitlist Position: 79
--------------------------------------------------
```


## Future Enhancements
- Implement a Google Apps Script, so the waitlist numbers can be automatically logged to a Google Sheet once a day.

---

## License
This project is open-source and available under the [GNU GPLv3](LICENSE).