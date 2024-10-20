import subprocess
import sys

# List of Python scripts to run sequentially
scripts = [
    "scripts/add_hospital.py",
    "scripts/check_hospital.py",
    "scripts/newcampaign.py",
    "scripts/hospitalapprove.py",
    "scripts/donate.py",
    "scripts/check_campaign.py",
    "scripts/donate.py",
    "scripts/check_campaign.py"
]

def run_scripts():
    for script in scripts:
        print(f"Running: {script}")

        # Run the script using subprocess and wait for it to finish
        result = subprocess.run(
            ["brownie", "run", script, "--network", "ganache-local"],
            capture_output=True,
            text=True
        )

        # Print the script's output
        print(result.stdout)

        # If there's an error, print it and stop the execution
        if result.returncode != 0:
            print(f"Error in {script}:")
            print(result.stderr)
            sys.exit(1)  # Exit the program if a script fails

    print("All scripts executed successfully.")

if __name__ == "__main__":
    run_scripts()
