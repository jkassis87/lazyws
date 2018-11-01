import subprocess

def lz_menu():
    menu_choice = input("""
    what options would you like to set?
    1)LAMP Install
    2)Lets Encrypt
    3)VHOST Setup
    4)?????????
    """)
    if menu_choice == 1:
        lamp_install()
    elif menu_choice == 2:
        lets_setup()
    elif menu_choice == 3:
        vhost()

# Need to make sure SELinux is off

#LAMP install
def lamp_install():
    # install httpd and enable in firewalld
    real_command = r"yum install -y httpd && systemctl enable httpd && systemctl start httpd && firewall-cmd --zone=public --permanent --add-service=http && firewall-cmd --permanent --add-port=80/tcp && firewall-cmd --permanent --add-port=443/tcp"
    subprocess.call(real_command, shell=True)

    # enables userdir
    the_file = r'/etc/httpd/conf.d/userdir.conf'
    with open(the_file) as f:
        userdir_enable = f.read().replace('UserDir disabled', 'UserDir enabled')
        userdir_dir = f.read().replace('#UserDir public_html', 'UserDir public_html')
    with open(the_file, "w") as f:
        f.write(userdir_enable)
        f.write(userdir_dir)
    subprocess.call('systemctl restart httpd', shell=True)
    # enables userdir in selinux
    subprocess.call('setsebool -P httpd_enable_homedirs true', shell=True)

    # install mariadb
    real_command = r"yum install -y mariadb-server mariadb && systemctl enable mariadb && systemctl start mariadb"
    subprocess.call(real_command, shell=True)

    # install php
    real_command = r'yum install -y php php-mysql && systemctl restart httpd'
    subprocess.call(real_command, shell=True)


# !!!!! add ftp server install, and other server stuff!!!!

# lets encrypt tools
def lets_setup():
    menu_choice = int(input("""
    What would you like to do?
    1 - Install Lets Encrypt
    2 - Run Lets Encrypt
    3 - Add cron auto-update SSL every 87 days
    """))

    if menu_choice == 1:
    # installs git and lets encrypt
        real_command = r"yum install git-all && mkdir ~/src && cd ~/src && git clone https://github.com/letsencrypt/letsencrypt && cd letsencrypt && sudo chmod g+x letsencrypt-auto"
        subprocess.call(real_command, shell=True)
        #subprocess.call("./letsencrypt-auto", shell=True)
    # runs LE on specified domain
    # need to add vhost check
    elif menu_choice == 2:
        ls_domain = str(input("what domain is this for?" ))
        ls_email = str(input("What's the email address for this domain? "))
        ls_script = str(f"./letsencrypt-auto --apache --email={ls_email} -d {ls_domain}")
        subprocess.call(ls_script, shell=True)
    #elif menu_choice == 3:    
        #subprocess.call("(crontab -l 2>/dev/null; echo "*/5 * * * * /path/to/job -with args") | crontab -")
        #subprocess.call("\(crontab -l 2>/dev/null; echo "\*\/5 \* \* \* \* \/path/to/job -with args") | crontab -")

# adding a vhost
def vhost():
    # this should find the httpd conf file
    # r does raw output, so / and other special characters are treated as part of the string 
    find_httpconf = r"find /etc/ -name httpd.conf"
    # puts the httpconf into a string
    # strip will remove the new line \n that gets added otherwise
    http_conf = subprocess.check_output(find_httpconf, shell=True).strip()
    # converts the string from binary into something normal, removes 'b
    http_conf = http_conf.decode("utf-8")
    the_domain = input("What domain would you like to add? ")
    # cleans the domain name
    if the_domain.startswith("https://www.") : the_domain = the_domain.replace("https://www.")
    if the_domain.startswith("http://www.") : the_domain = the_domain.replace("http://www.", "")
    if the_domain.startswith("https://") : the_domain = the_domain.replace("https://", "")
    if the_domain.startswith("http://") : the_domain = the_domain.replace("http://", "")
    if the_domain.startswith("www.") : the_domain = the_domain.replace("www.", "")

    #adds the code to the conf file
    #!!!!!!! need to add log file locations!!!!!!
    http_conf_file = open(http_conf, 'a')
    http_conf.write(f"<VirtualHost *:80 *:443>\n\tServerAdmin admin@{the_domain}\n\tServerAlias www.{the_domain}\n\tDocumentRoot /home/{the_domain}\n<VirtualHost>")

    # wil need to fix this a lot more when doing user domains

# this should add a domain
def add_domain():
    # add and cleans the domain name string !!!!should make this bit it's own function and reuse it!!!!!
    the_domain = input("What domain do you want to add? ")
    if the_domain.startswith("https://www.") : the_domain = the_domain.replace("https://www.")
    if the_domain.startswith("http://www.") : the_domain = the_domain.replace("http://www.", "")
    if the_domain.startswith("https://") : the_domain = the_domain.replace("https://", "")
    if the_domain.startswith("http://") : the_domain = the_domain.replace("http://", "")
    if the_domain.startswith("www.") : the_domain = the_domain.replace("www.", "")
    
    # adds the domain as a user in linux, !!!!!need to modify this for subdomains!!!!!
    # !!! need to also clean the username, maybe only use the first 8 char but have to check for potential duplicate!!!!!
    domain_user = the_domain.replace(".", "")
    real_command = f"useradd {domain_user}"
    subprocess.call(real_command, shell=True)

    # creates public_html, mail and folders !!!!!need to add proper perms and selinux stuff!!!!!
    real_command = f"mkdir \/home\/{domain_user}\/public_html && mkdir \/home\/{domain_user}\/mail && mkdir \/home\/{domain_user}\/logs"
    subprocess.call(real_command, shell=True)

    #!!!!!need to add letsencrypt and regular cron for it!!!!!
    #!!!!!add ssh access toggle, and dir size limits!!!
    #!!!!!need this function to also add the vhost!!!!!




# !!!! add an automatic wordpress and other things installer!!!!!
# !!!! create a basic backup feature for the above !!!!!

# exim and dovecot setup
def exim_dovecot_setup():
    subprocess.call('yum install -y exim dovecot openssl file', shell=True)


#gonna need to find multiple files eventually, can reduce the code by making a function for this
#def find_file(the_file):
#    the_file = 


lz_menu()
#lamp_install()