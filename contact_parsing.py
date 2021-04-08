def build_domains(contacts: dict) -> dict:
    """Builds the domains dictionary to be used in the index route of the app.

    Args:
        contacts (dict): response from people api.

    Returns:
        dict: data ready to be used.
    """
    parsed_contacts = _parse_contacts(contacts)
    domain_data = _domains_data(parsed_contacts)
    return domain_data


def _parse_contacts(contacts: dict) -> list:
    """Parse the response from people api to return only the needed fields.

    Args:
        contacts (dict): json response from people api.

    Returns:
        list: a list of dicts with parsed contacts.
    """
    data = []
    connections = contacts.get("connections", [{}])

    for person in connections:
        person_name = person.get("names", [{}])[0].get("displayName")
        person_email = person.get("emailAddresses", [{}])[0].get("value")

        if not person_email:
            continue

        domain = _extract_domain(person_email)

        data.append(
            {
                "name": person_name,
                "email": person_email,
                "domain": domain,
            }
        )

    return data


def _extract_domain(email: str) -> str:
    """extract the domain (part after '@') from an email string.

    Args:
        email (str): email to extract the domain from.

    Returns:
        str: the domain. if it cant find the domain returns ''.
    """
    domain = email.split("@")
    if len(domain) != 2:
        return ""

    return domain[1]


def _domains_data(contacts: list) -> dict:
    """Organizes the response from _parse_contacts() by domains.

    Args:
        contacts (list): list returned by _parse_contacts()

    Returns:
        dict: dictionary ready to be used in the main app.
    """
    domains = {}

    if len(contacts) == 0:
        return {}

    for c in contacts:
        d = c["domain"]
        if d not in domains:
            domains[d] = [
                {"name": c["name"], "email": c["email"]},
            ]

        else:
            domains[d].append(
                {
                    "name": c["name"],
                    "email": c["email"],
                }
            )

    return domains
