def extract_domain(email: str) -> str:
    domain = email.split("@")
    if len(domain) != 2:
        return "N/A"

    return domain[1]


def parse_contacts(contacts: dict) -> list:
    data = []
    connections = contacts.get("connections", [{}])

    for person in connections:
        person_name = person.get("names", [{}])[0].get("displayName")
        person_email = person.get("emailAddresses", [{}])[0].get("value")

        if not person_email:
            continue

        domain = extract_domain(person_email)

        data.append(
            {
                "name": person_name,
                "email": person_email,
                "domain": domain,
            }
        )

    return data


def domains_data(contacts: list) -> dict:
    domains = {}
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


def build_domains(contacts: dict) -> dict:
    parsed_contacts = parse_contacts(contacts)
    domain_data = domains_data(parsed_contacts)
    return domain_data
