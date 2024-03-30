from config import scripts_to_run, target_url

def target_url_needed_for_script(script_name):
    # Add logic to determine if target_url is needed for the script
    # For example, check if the script contains certain keywords or patterns
    # Return True if target_url is needed, False otherwise
    
    if script_name == "process_0_scrape.py":
        return True
    else:
        return False
    
# Iterate over the scripts and run them
for script in scripts_to_run:
    module = __import__(script.replace('.py', ''))
    if target_url_needed_for_script(script):
        module.main(target_url)
    else:
        module.main()