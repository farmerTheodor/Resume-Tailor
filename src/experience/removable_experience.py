from pydantic import BaseModel


def get_all_removable_experience(experience) -> list:
    if experience is None:
        return []

    all_removable_experience = []

    if _is_removable_experience(experience):
        all_removable_experience.append(experience)

    if isinstance(experience, list):
        for item in experience:
            all_removable_experience.extend(get_all_removable_experience(item))
    elif isinstance(experience, dict):
        for key, value in experience.items():
            all_removable_experience.extend(get_all_removable_experience(value))

    elif isinstance(experience, BaseModel):
        for field_name, field_info in type(experience).model_fields.items():
            field_value = getattr(experience, field_name)
            all_removable_experience.extend(get_all_removable_experience(field_value))

    sorted_removable_experience = sorted(
        all_removable_experience, key=lambda x: x.rank, reverse=True
    )

    return sorted_removable_experience


def remove_experience(experience, experience_to_remove) -> None:
    new_experience = experience

    if experience == experience_to_remove:
        return None
    if isinstance(experience, list):
        new_experience = []
        for item in experience:
            result = remove_experience(item, experience_to_remove)
            if result is not None:
                new_experience.append(result)
    elif isinstance(experience, dict):
        new_experience = {}
        for key, value in experience.items():
            result = remove_experience(value, experience_to_remove)
            if result is not None:
                new_experience[key] = result
    elif isinstance(experience, BaseModel):
        for field_name, _ in type(experience).model_fields.items():
            field_value = getattr(experience, field_name)
            result = remove_experience(field_value, experience_to_remove)
            setattr(experience, field_name, result)

    return new_experience


def _is_removable_experience(experience) -> bool:
    return (
        isinstance(experience, BaseModel)
        and type(experience).model_fields.get("rank", False)
        and type(experience).model_fields.get("value", False)
    )
