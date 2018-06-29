from urllib.request import urlopen
import urllib
    
def get_paths(url, agent_name=None):
    s = get_robots_file(url)
    s = s[s.upper().find("USER-AGENT")+12:]
    keepGoing = s.upper().find("USER-AGENT")
    disallowed_paths = []
    allowed_paths = []
    #parsing
    if (agent_name == None):
        #this is looking for "USER-AGENT" which precedes instructions and tells who the instructions are for
        while (keepGoing != -1):
            #if the name of the "User-agent" is "*" aka, if the instructions are for everyone
            if (s[:s.upper().find("\n")].upper() == "*"):
                #This is to loop over instructions for a labeled "User-agent"
                #This is looking for a stop condition, if there are no colons left, we stop. If we find a ":"  we either want to find that the index of "Allow" or "Disallow" is less than "User-agent" (meaning we are within a labeled agent's instructions) or there exists "Allow" or "Disallow" without "User-agent" (handles the case of "User-agent" == -1)
                while (s.find(":") != -1 and (s.upper().find("DISALLOW:") < s.upper().find("USER-AGENT:") or (s.upper().find("USER-AGENT:") == -1 and s.upper().find("DISALLOW:") != -1))):
                    s = s[s.upper().find("DISALLOW:")+10:]
                    disallowed_paths.append(s[0:s.find("\n")])
            keepGoing = s.upper().find("USER-AGENT:")
            s = s[s.upper().find("USER-AGENT")+12:]
                        
    else:
        agent_name = agent_name.upper()
        #this is looking for "USER-AGENT" which precedes instructions and tells who the instructions are for
        while (keepGoing != -1):
            #if the name of the "User-agent" is "*" aka, if the instructions are for everyone
            if (s[:s.find("\n")].upper() == agent_name or s[:s.upper().find("\n")].upper() == "*"):
                #This is to loop over instructions for a labeled "User-agent"
                #This is looking for a stop condition, if there are no colons left, we stop. If we find a ":"  we either want to find that the index of "Allow" or "Disallow" is less than "User-agent" (meaning we are within a labeled agent's instructions) or there exists "Allow" or "Disallow" without "User-agent" (handles the case of "User-agent" == -1)
                while (s.find(":") != -1 and (s.upper().find("DISALLOW:") < s.upper().find("USER-AGENT:") or s.upper().find("ALLOW:") < s.upper().find("USER-AGENT:") or (s.upper().find("USER-AGENT:") == -1 and s.upper().find("DISALLOW:") != -1 or s.upper().find("ALLOW:") != -1))):
                    if (s.upper().find("DISALLOW") < s.upper().find("ALLOW") or (s.upper().find("ALLOW") < 0 and not s.upper().find("DISALLOW") < 0)):
                        s = s[s.upper().find("DISALLOW:")+10:]
                        path = s[0:s.find("\n")].strip()
                        if (path not in disallowed_paths):
                            disallowed_paths.append(path)
                    elif ((s.upper().find("ALLOW") < s.upper().find("DISALLOW")) or (s.upper().find("DISALLOW") < 0 and not s.upper().find("ALLOW") < 0)):
                        s = s[s.upper().find("ALLOW:")+7:]
                        path = s[0:s.find("\n")].strip()
                        allowed_paths.append(path)
            keepGoing = s.upper().find("USER-AGENT:")
            s = s[s.upper().find("USER-AGENT")+12:]
            
        for elem in allowed_paths:
            try:
                disallowed_paths.remove(elem)
            except:
                pass
                
    return(disallowed_paths)
    

def get_robots_file(url):
    try:
        return(urlopen("http://{}/robots.txt".format(url)).read().decode("utf-8"))
    except urllib.error.URLError:
        try:
            return(urlopen("http://www.{}/robots.txt".format(url)).read().decode("utf-8"))
        except:
            return ""
            

def main():
    print("\n\n\n")
    print(get_robots_file("twitter.com"))
    print(get_paths("twitter.com"))

if __name__ == "__main__" :
    main()

                