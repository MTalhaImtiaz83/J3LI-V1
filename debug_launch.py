import sys, os, traceback

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug_log.txt")

with open(LOG, "w") as f:
    f.write(f"Python: {sys.executable}\n")
    f.write(f"Version: {sys.version}\n")
    f.write(f"CWD: {os.getcwd()}\n")
    f.write(f"Script dir: {os.path.dirname(os.path.abspath(__file__))}\n")
    f.write(f"sys.path: {sys.path}\n\n")

    try:
        f.write("Importing uvicorn...\n")
        import uvicorn
        f.write(f"  uvicorn OK: {uvicorn.__version__}\n")
    except Exception as e:
        f.write(f"  FAILED: {e}\n")
        traceback.print_exc(file=f)

    try:
        f.write("Importing fastapi...\n")
        import fastapi
        f.write(f"  fastapi OK: {fastapi.__version__}\n")
    except Exception as e:
        f.write(f"  FAILED: {e}\n")
        traceback.print_exc(file=f)

    try:
        f.write("Importing j3li.api.main...\n")
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from j3li.api.main import app
        f.write(f"  j3li.api.main OK\n")
    except Exception as e:
        f.write(f"  FAILED: {e}\n")
        traceback.print_exc(file=f)

    f.write("\nAll checks done.\n")

print("Debug log written to:", LOG)
