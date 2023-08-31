import os
from kfp.components import load_component_from_file


components = [
    x
    for x in os.listdir(os.path.dirname(__file__))
    if not x.startswith("_") and os.path.isdir(x)
]

for component in components:
    globals()[component] = load_component_from_file(
        os.path.join(
            os.path.dirname(__file__), f"{component}/{component}/component.yaml"
        )
    )

__all__ = components
