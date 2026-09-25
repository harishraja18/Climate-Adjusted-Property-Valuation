"""Compatibility wrapper for the backend project.

This repository root is intentionally kept minimal so the actual FastAPI
application lives under the TamilNadu-Climate-Property package and the app can
be started via `uvicorn app.main:app` from that directory.
"""


def main():
    print(
        "Use the FastAPI app from the TamilNadu-Climate-Property project directory. "
        "Example: uv run uvicorn app.main:app --reload"
    )


if __name__ == "__main__":
    main()
