import sys
print(f"Python: {sys.version}")
print(f"CWD: {sys.path}")
print(f"Args: {sys.argv}")

try:
    from main import app
    print(f"App loaded: {app}")
    print(f"Routes: {len(app.routes)}")
    for r in app.routes[:5]:
        if hasattr(r, 'path'):
            print(f"  {r.path}")
except Exception as e:
    print(f"Error loading app: {e}")
    import traceback
    traceback.print_exc()
