try:
    import flask
    from dotenv import load_dotenv
    print("All imports successful!")
except ImportError as e:
    print(f"Import error: {e}")
