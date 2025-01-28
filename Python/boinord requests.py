import random
import requests

# Custom exceptions
class LoginException(Exception): ...
class RequestException(Exception): ...

def fetch_apartment_info(username: str, password: str) -> dict:
    """
    Fetches information about apartments that a user is waitlisted to with BoINord using the same API as their site.

    Args:
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        dict: A dictionary containing apartment information if successful, 
        where keys are apartment IDs and values are dicts with keys "position" and "variant_string"
        containing waitlist position number and easily readable variant details, ex "Annebergvej - Lejlighed - 4v".

    Raises:
        LoginException:   If login fails due to invalid credentials.
        KeyError:         If the response data does not contain the key "MemberWishes"
        RequestException: If the request fails for some reason and 200 is not returned by the API
    """
    # Make a GET request to the API
    random_int = random.randint(1000000000000, 9999999999999) # Prevents caching of API response
    url = f"https://boinord.dk/directproviders/userhandler.ashx?action=login&user={username}&password={password}&rand={random_int}"
    response = requests.get(url)

    # Check if login was successful
    if response.json().get("result") == "login failed":
        raise LoginException("Login failed -- maybe the entered username and password are invalid?")

    # Process the response if the status code indicates success
    if response.status_code == 200:
        data = response.json()  # Assuming the response is in JSON format
        apartments = {}

        # Check if "MemberWishes" exists in the response
        if "MemberWishes" in data:
            for wish in data["MemberWishes"]:
                for match in wish.get("Matches", []):
                    # Extracting the values required
                    company_no = match["CompanyNo"]                 # Boligforening
                    department_no = match["DepartmentNo"]           # Afdelingsnummer
                    department_name = wish["DepartmentName"]        # Afdelingsnavn
                    rooms = match["Rooms"]                          # Værelser
                    tenancy_type = match["TenancyType"]             # Boligtype ID (1: Lejlighed, 2: Rækkehus/hus)
                    tenancy_type_text = wish["TenancyTypeText"]     # Boligtype i tekst
                    tenancy_lm_type = match["TenancyLmType"]        # Boligklasse (1: Familiebolig)
                    position = match["Prio"]                        # Your position on the waitlist

                    # Format the Apartment variant ID - Unique identifier
                    apartment_id = f"{company_no}-{department_no}-{tenancy_type}-{tenancy_lm_type}-{rooms}"

                    # Format the apartment variant string
                    variant_string = f"{department_name} - {tenancy_type_text} - {rooms}v"

                    apartments[apartment_id] = {"position": position, "variant_string": variant_string}
                    
            return apartments
        else:
            raise KeyError("No MemberWishes found in the response.")
    else:
        raise RequestException(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
    
def print_apartments(apartments: dict) -> None:
    """
    Prints the details of apartments in a readable format.

    Args:
        apartments (dict): A dictionary containing apartment information if successful, 
        where keys are apartment IDs and values are dicts with keys "position" and "variant_string"
        containing waitlist position and easily readable variant details, ex "Annebergvej - Lejlighed - 4v".
        (Obtained from fetch_apartment_info())

    Returns:
        None
    """
    for apartment_id in apartments:
        position    = apartments[apartment_id]["position"]
        variant     = apartments[apartment_id]["variant_string"]

        print(f"Apartment Variant ID: {apartment_id}")
        print(f"Apartment Variant: {variant}")
        print(f"Waitlist Position: {position}")
        print("-" * 50)

if __name__ == "__main__":
    # Example use:
    username = "your@email.here"
    password = "$uperSecretPassword"

    print_apartments(fetch_apartment_info(username, password))

    """ Example Output:

    Apartment Variant ID: 335-601-2-1-2
    Apartment Variant: Torvegade, Birkevej, Kingosvej - Pandrup - Rækkehus/hus - 2v
    Waitlist Position: 45
    --------------------------------------------------
    Apartment Variant ID: 335-519-1-1-2
    Apartment Variant: Vrængmosevej 8 m.fl. - Østervrå - Lejlighed - 2v
    Waitlist Position: 79
    --------------------------------------------------
    Apartment Variant ID: 693-1580-1-1-2
    Apartment Variant: Hortensiaparken - Lejlighed - 2v
    Waitlist Position: 34
    --------------------------------------------------
    Apartment Variant ID: 597-51-2-1-4
    Apartment Variant: Godfred Hansensvej 1 - 34 - Rækkehus/hus - 4v
    Waitlist Position: 98
    --------------------------------------------------
    Apartment Variant ID: 198-12-1-1-3
    Apartment Variant: Løvvangen - Vikingevej m.fl. - Lejlighed - 3v
    Waitlist Position: 147
    --------------------------------------------------
    """