def merge_data(inspection, thermal):
    merged = {}

    for item in inspection + thermal:
        area = item.get("area", "Unknown")

        if area not in merged:
            merged[area] = {
                "issues": [],
                "temperature": [],
                "conflict": False
            }

        merged[area]["issues"].append(item.get("issue", "Not Available"))
        merged[area]["temperature"].append(item.get("temperature", "Not Available"))

    # conflict detection
    for area in merged:
        temps = merged[area]["temperature"]
        if len(set(temps)) > 1:
            merged[area]["conflict"] = True

    return merged