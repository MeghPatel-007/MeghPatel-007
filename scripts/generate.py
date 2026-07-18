import subprocess
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Define the pipeline steps in sequence
PIPELINE = [
    ("prep_photo.py", "Preprocessing profile photo..."),
    ("make_ascii_svg.py", "Generating ASCII SVG..."),
    ("make_info_card.py", "Generating neofetch Info Card SVG..."),
    ("fetch_contributions.py", "Fetching GitHub contribution data..."),
    ("render_heatmap_svg.py", "Rendering contribution heatmap SVG..."),
]

def run_pipeline():
    print("Starting GitHub Profile Art Generation Pipeline...")
    print("=" * 60)
    
    for script_name, description in PIPELINE:
        script_path = os.path.join(HERE, script_name)
        print(f"\n[Running] {description}")
        
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8"
            )
            if result.stdout:
                print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"\n[Error] Step failed: {script_name}")
            print(f"Exit code: {e.returncode}")
            if e.stdout:
                print(f"Stdout:\n{e.stdout}")
            if e.stderr:
                print(f"Stderr:\n{e.stderr}")
            sys.exit(1)
            
    print("\n" + "=" * 60)
    print("Pipeline completed successfully! All assets generated.")

if __name__ == "__main__":
    run_pipeline()
