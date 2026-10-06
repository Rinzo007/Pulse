from .constants import registry_metadata
from .model import MODEL_PROFILE, MODEL_VERSION


if __name__ == "__main__":
    print(f"Pulse {MODEL_VERSION} ({MODEL_PROFILE})")
    print(registry_metadata())
