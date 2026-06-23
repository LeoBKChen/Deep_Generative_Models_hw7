from __future__ import annotations


def to_float(value) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_int(value) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def to_bool(value) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in {"是", "yes", "true", "1"}:
        return True
    if text in {"否", "no", "false", "0"}:
        return False
    return None


def text_or_unknown(value) -> str:
    text = "" if value is None else str(value).strip()
    return text or "Not provided"


def build_qa_profile(species, shell_length_cm) -> dict:
    return {
        "species": text_or_unknown(species),
        "shell_length_cm": to_float(shell_length_cm),
    }


def build_diagnosis_profile(
    species,
    number_of_turtles,
    shell_length_cm,
    tank_length_cm,
    tank_width_cm,
    tank_height_cm,
    water_depth_cm,
    has_basking_area,
    has_uvb_light,
    heating_equipment,
    filtration_method,
    feeding_content,
    mixed_species,
    current_concern,
) -> dict:
    return {
        "species": text_or_unknown(species),
        "number_of_turtles": to_int(number_of_turtles),
        "shell_length_cm": to_float(shell_length_cm),
        "tank_size_cm": {
            "length": to_float(tank_length_cm),
            "width": to_float(tank_width_cm),
            "height": to_float(tank_height_cm),
        },
        "water_depth_cm": to_float(water_depth_cm),
        "has_basking_area": to_bool(has_basking_area),
        "has_uvb_light": to_bool(has_uvb_light),
        "heating_equipment": text_or_unknown(heating_equipment),
        "filtration_method": text_or_unknown(filtration_method),
        "feeding_content": text_or_unknown(feeding_content),
        "mixed_species": to_bool(mixed_species),
        "current_concern": text_or_unknown(current_concern),
    }


def build_design_profile(
    species,
    tank_length_cm,
    tank_width_cm,
    tank_height_cm,
    water_depth_cm,
    desired_style,
    required_elements,
    elements_to_avoid,
    user_wants_image,
) -> dict:
    return {
        "species": text_or_unknown(species),
        "tank_size_cm": {
            "length": to_float(tank_length_cm),
            "width": to_float(tank_width_cm),
            "height": to_float(tank_height_cm),
        },
        "water_depth_cm": to_float(water_depth_cm),
        "desired_style": text_or_unknown(desired_style),
        "required_elements": text_or_unknown(required_elements),
        "elements_to_avoid": text_or_unknown(elements_to_avoid),
        "user_wants_image": bool(user_wants_image),
    }


def _bool_text(value: bool | None) -> str:
    if value is True:
        return "Yes"
    if value is False:
        return "No"
    return "Not provided"


def format_profile(profile: dict) -> str:
    tank = profile.get("tank_size_cm", {})
    lines = [
        f"Species: {profile.get('species', 'Not provided')}",
        f"Shell length: {profile.get('shell_length_cm') or 'Not provided'} cm",
        f"Number of turtles: {profile.get('number_of_turtles') or 'Not provided'}",
        f"Tank size: {tank.get('length') or 'Not provided'} x {tank.get('width') or 'Not provided'} x {tank.get('height') or 'Not provided'} cm",
        f"Water depth: {profile.get('water_depth_cm') or 'Not provided'} cm",
        f"Has basking area: {_bool_text(profile.get('has_basking_area'))}",
        f"Has UVB light: {_bool_text(profile.get('has_uvb_light'))}",
        f"Heating equipment: {profile.get('heating_equipment', 'Not provided')}",
        f"Filtration method: {profile.get('filtration_method', 'Not provided')}",
        f"Feeding content: {profile.get('feeding_content', 'Not provided')}",
        f"Mixed species: {_bool_text(profile.get('mixed_species'))}",
        f"Current concern: {profile.get('current_concern', 'Not provided')}",
        f"Desired style: {profile.get('desired_style', 'Not provided')}",
        f"Required elements: {profile.get('required_elements', 'Not provided')}",
        f"Elements to avoid: {profile.get('elements_to_avoid', 'Not provided')}",
    ]
    return "\n".join(lines)
