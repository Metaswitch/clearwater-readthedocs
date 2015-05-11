## Setup M/Monit box

### Setup

- Launch an m1.small ubuntu instance on EC2 and add a DNS name if required. Use the M/Monit security group created by the Chef automated install.
- Download mmonit from here: http://mmonit.com/download/, e.g. `curl -o mmonit.tar.gz http://mmonit.com/dist/mmonit-2.4-linux-x64.tar.gz`
- Unpack the tar file to `/usr/local/mmonit` (can be anywhere, but init.d script expects it to be here) and launch `bin/mmonit` (see Installation in http://mmonit.com/documentation/mmonit_manual.pdf)
- You can now access M/Monit through a browser at port 8080 (to change to 80, see below). Credentials are admin:swordfish
- To have mmonit start at boot, add it to init.d/: `cp doc/startup/mmonit_init /etc/init.d/mmonit` (make script executable). Then configure to start at boot: `sudo update-rc.d mmonit defaults`

### Notes

- To stop mmonit: `bin/mmonit stop`

- By default mmonit will run on port 8080. To change this, edit conf/server.xml. To run on port 80, you will need to run mmonit as root.

- By default mmonit will run in the background. To run it in the foreground, use the -i option.

## Pointing servers at M/Monit

When creating a instance pass it the mmonit hostname in `/etc/clearwater/config`, eg: mmonit_hostname=mmonit.example.com. To configure an existing instance without this in the user data, simply stop the instance, modify the file and start it again.

The clearwater-infrastructure package will add an mmonit script to /etc/clearwater/scripts/ and configure the monit daemon to point at the M/Monit host specfied in the user data. To monitor specific processes, add .monit config files to /etc/monit/conf.d/
