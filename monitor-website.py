
import requests
import smtplib
import paramiko
# import linode_api4
import digitalocean
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import schedule


MAIL_USERNAME=env.YOUR_MAIL_USERNAME
MAIL_PASSWORD=env.YOUR_MAIL_PASSWORD
MAIL_RECEIVER=env.YOUR_MAIL_RECEIVER
digital_ocean_token = env.YOUR_DIGITAL_OCEAN_TOKEN
droplet_id = env.YOUR_DROPLET_ID
hostname = env.YOUR_SERVER_IP_ADDRESS
server_username=env.YOUR_SERVER_USERNAME
ssh_key_path=env.YOUR_SSH_KEY_PATH
docker_container_id = env.YOUR_DOCKER_CONTAINER_ID
url = env.YOUR_WEBSITE_URL



def restart_server_and_app(token, droplet_id):

    # Create droplet object
    droplet = digitalocean.Droplet(
        token=token,
        id=droplet_id
    )

    # Load droplet data from API
    droplet.load()

    print("Rebooting droplet...")
    droplet.reboot()

    # Wait until droplet becomes active again
    while True:
        time.sleep(10)

        droplet.load()  # refresh droplet data from API
        print("Current droplet status:", droplet.status)

        if droplet.status == "active":
            print("Droplet is active again.")
            time.sleep(20)  # give OS time to fully boot
            restart_container()
            break



def restart_container():
    print("Restarting the application...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=server_username, key_filename=ssh_key_path)
    stdin, stdout, stderr = ssh.exec_command(f"docker start {docker_container_id}")
    print(stdout.read().decode())

    ssh.close()
    print("Application restarted successfully!")


def send_gmail(sender_email, app_password, recipient_email, subject, body):
    print("Sending email notification...")
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect and send
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")

# Usage
def monitor_application():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Website is up and running!")

        else:
            print(f"Website is down! ")

            # send notification to admin (e.g., via email or SMS)

            send_gmail(
            sender_email=MAIL_USERNAME,
            app_password=MAIL_PASSWORD,
            recipient_email=MAIL_RECEIVER,
            subject="Website Down Alert",
            body=f"The website is down!"
            )
            # restart the application or server if necessary
            restart_container()


    except Exception as e:

        send_gmail(
            sender_email=MAIL_USERNAME,
            app_password=MAIL_PASSWORD,
            recipient_email=MAIL_RECEIVER,
            subject="Website Down Alert",
            body=f"The website is down!"
        )

        # restart linode server
        # client = linode_api4.LinodeClient(digital_ocean_token)
        # linode = client.load(linode_api4.Instance, 12345678)
        # linode.reboot()

        # restart digital ocean server
        restart_server_and_app(digital_ocean_token, droplet_id)


schedule.every(5).seconds.do(monitor_application)

while True:
    schedule.run_pending()


