# RaspberryPi-Motion-Detection-stream

## Essential Libraries to Install

To set up the project, you need to install several libraries. Run the following commands in your terminal:

1. Clone the repository:

   ```
   git clone https://github.com/Mr-Jerry-Haxor/RaspberryPi-MachineLearning.git
   ```
2. Navigate to the project directory:

   ```
   cd RaspberryPi-MachineLearning
   ```
3. Install the required libraries:

   ```
   sudo apt-get install -y libqt5gui5 libqt5webkit5 libqt5test5 software-properties-common ffmpeg
   ```

   ```
   sudo apt-get install -y libopenjp2-7-dev libhdf5-dev libatlas-base-dev python3-pip python3-h5py python3-opencv autoconf automake build-essential pkgconf libtool git libzip-dev libjpeg-dev gettext libmicrohttpd-dev libavformat-dev libavcodec-dev libavutil-dev libswscale-dev libavdevice-dev default-libmysqlclient-dev libpq-dev libsqlite3-dev libwebp-dev
   ```
4. change the config,

   ```
   sudo nano /boot/firmware/cmdline.txt
   ```

   append below line in same line to the cmdline.txt file,(dont append in next line)

   ```
    dwc_otg.fiq_enable=1 dwc_otg.fiq_fsm_enable=1 dwc_otg.fiq_fsm_mask=0x3
   ```

   removing the other processes of using camera

   ```
   sudo kill $(sudo lsof -t /dev/video0)
   ```

   ## Run the application


   ```
   chmod +777 mediamtx
   ```

   ```
   ./mediamtx > /dev/null 2>&1
   ```

## Accessing the Application

Reconnect the USB camera again and Open your browser and type the following URL:

```
http://<raspberry_pi_ip-address>:8889/stream/?streamtype=camera
```

```
http://<raspberry_pi_ip-address>:8889/stream/?streamtype=motiondetection
```

```
http://<raspberry_pi_ip-address>:8889/stream/?streamtype=both
```

***or***

```
http://<raspberry_pi_ip-address>:8889/stream1/?streamtype=camera
```

```
http://<raspberry_pi_ip-address>:8889/stream1/?streamtype=motiondetection
```

```
http://<raspberry_pi_ip-address>:8889/stream1/?streamtype=both
```


### Known Issues

If you encounter any issues while installing libraries like python3-opencv or flask, run the following command to update your package lists and fix any missing package dependencies:

```
sudo apt-get update --fix-missing
```
