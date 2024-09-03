<p align="center">
  <img width="200" height="200" src="https://github.com/Ploirad/WRO-2024-ArduMASTERS/assets/148375115/122c7233-1e41-4727-894d-9d810f12458b">
</p> 

# Index
- [Members of the team](#members-and-collaborators-of-the-team)
- [Files](#files)
- [Building instructions](#building-instructions)
  1. [Components](#1-components)
  2. [Scheme](#2-make-the-scheme)
  3. [Print the 3d models](#3-print-the-3d-models)
  4. [Chassis assemble](#4-chassis-assemble)
      - [Base](#1-base)
      - [Stub axles](#2-stub-axles)
      - [Zipper](#3-zipper)
      - [Wheels and dc motors](#4-wheels-and-dc-motors)
      - [Gear and servo](#5-gear-and-servo)
      - [Battery shield and spacers](#6-battery-sield-and-spacers)
  5. [Software installation](#5-software-installation)
      - [OS installation and adjustment](#1-os-installation-and-adjustment)
      - [Auto login configuration](#2-auto-login-configuration)
      - [Update packages](#3-update-packages)
      - [Install python](#4-install-python)
      - [Install basic libraries](#5-install-basic-libraries-for-the-camera-machine-vision-and-tcs34725)
      - [Enable the i2c for the tcs34725](#6-enable-the-i2c-bus-for-the-tcs34725)
      - [Download our github repository](#7-download-our-github-repository)
      - [Automate the entrance into the repository](#8-automate-the-entrance-into-the-repository)
      - [Useful commands](#9-useful-commands)
  6. [Ending](#6-ending)




# Members and collaborators of the team
- Darío López Parada (born on June 24, 2008)
- Pablo Pietro Remartínez (born on November 25, 2007)
- Adrían Yago Benitez (born on August 3, 2009)
- Miguel Amez Riendas (born on Dicember 8, 1988)(he is our coach)
- Marío Torreiro Sevilla (born on March 14, 2008)
- Francisco Javier Abajo Alonso (born on August 21, 2008)
>The last two of us are only collaborators becouse are going to participate at the start but they are doing the pilgrims route to Santiago de Compostela
# Files
## [models](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/models)
  In this folder we got all the 3D models that are and were on the car
## [other](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/other)  
  In this folder we got our logo and a logbook based in the months
## [schemes](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/schemes)
  In this folder we got the electric scheme
## [src](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/src)
  In this folder we got all the source codes that we use and used on the team.
## [t-photos](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/t-photos)
  In this folder we got the image of our team.
## [v-photos](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/v-photos)
  In this folder we got images from all the parts of our car.
## [video](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/video)
  In this folder we got two video of our car while it is moving in the different challenges

# Building instructions
## 1. Components
   
  - [Raspberry Pi 4 model b](https://www.amazon.es/Raspberry-Modelo-Cortex-A72-1-50GHz-Bluetooth/dp/B0CJ4XHZ4G/ref=sr_1_5?sr=8-5)
  - [L298N](https://www.amazon.es/HiLetgo®-Bridge-Stepper-Controller-Arduino/dp/B07CHBRF4Z/ref=sr_1_6?__mk_es_ES=ÅMÅŽÕÑ&crid=3CJEWNNVPNLVR&dib=eyJ2IjoiMSJ9.J1IoI4lcmBqTeHP6767NOPyHf44YnyBlMhRhNQmwhLPTvn-dkeFWVvZ24iSLNdLEsOo4ooBlprGz448954UpMxjdS0bdiWc1hwVDBXMP-t9t4_4KgoZEEybMySz0g1oxw-xZU3EWznA39EtTB1fHM7-nmBE-2RSX3PxZOuCamckWiUSHLKjgWUtkx_Y0LoXIWijt19YuN4BcRkwKV_2o7n2GrYa19QQ4jJWNpDryZuy2crPCVqmgHsKvyNFtU_g5ow7OvmKWSF_494XvJaVbwU5s7gRYqkgwMPjXoGPJd48.9j7OLBLKW3YQo2MtQQEm8taLG9BbZ2LkyE7f1IlGtZ0&dib_tag=se&keywords=l298n&qid=1723974557&sprefix=l298n%2Caps%2C188&sr=8-6)
  - [DC Motors](https://www.amazon.es/dp/B0B3D789V3/ref=sspa_dk_detail_0?pd_rd_i=B08D39MFN1&pd_rd_w=FfHgH&content-id=amzn1.sym.16e80c5a-02ca-4e26-b568-17a6666ff4f0&pf_rd_p=16e80c5a-02ca-4e26-b568-17a6666ff4f0&pf_rd_r=0FGVWEZ861DAZHE7YZPK&pd_rd_wg=44LrF&pd_rd_r=eef15e0e-a984-43d4-a3cd-73a92bc02780&s=tools&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWwy&th=1)
  - [Servo MG996R](https://es.aliexpress.com/item/1005006223358432.html?src=google&src=google&albch=shopping&acnt=439-079-4345&isdl=y&slnk=&plac=&mtctp=&albbt=Google_7_shopping&aff_platform=google&aff_short_key=UneMJZVf&gclsrc=aw.ds&&albagn=888888&&ds_e_adid=&ds_e_matchtype=&ds_e_device=c&ds_e_network=x&ds_e_product_group_id=&ds_e_product_id=es1005006223358432&ds_e_product_merchant_id=5308147060&ds_e_product_country=ES&ds_e_product_language=es&ds_e_product_channel=online&ds_e_product_store_id=&ds_url_v=2&albcp=21486736708&albag=&isSmbAutoCall=false&needSmbHouyi=false&gad_source=1&gclid=CjwKCAjwxNW2BhAkEiwA24Cm9J1yyDgOGbhPpHRi51phhDtDIJgJk2Ukuv8-35oNZYhy9Rq7RbrVQxoCOIYQAvD_BwE)
  - [18650 Battery](https://es.aliexpress.com/item/1005007228231597.html?spm=a2g0o.detail.pcDetailTopMoreOtherSeller.1.2b02qaSWqaSWev&gps-id=pcDetailTopMoreOtherSeller&scm=1007.40000.327270.0&scm_id=1007.40000.327270.0&scm-url=1007.40000.327270.0&pvid=d4def50f-37a6-4321-8474-3b1b2da490f3&_t=gps-id:pcDetailTopMoreOtherSeller,scm-url:1007.40000.327270.0,pvid:d4def50f-37a6-4321-8474-3b1b2da490f3,tpp_buckets:668%232846%238109%231935&pdp_npi=4%40dis%21EUR%2112.57%211.25%21%21%2196.80%219.68%21%40211b619a17239759870871818e9591%2112000039883706387%21rec%21ES%212755819411%21X&utparam-url=scene%3ApcDetailTopMoreOtherSeller%7Cquery_from%3A)
  - [18650 Shield](https://es.aliexpress.com/item/1005005986332436.html?spm=a2g0o.detail.pcDetailTopMoreOtherSeller.2.c15cts08ts08b4&gps-id=pcDetailTopMoreOtherSeller&scm=1007.40000.327270.0&scm_id=1007.40000.327270.0&scm-url=1007.40000.327270.0&pvid=a7e2a1ef-289c-4358-9af2-3f99fd0d2d7a&_t=gps-id:pcDetailTopMoreOtherSeller,scm-url:1007.40000.327270.0,pvid:a7e2a1ef-289c-4358-9af2-3f99fd0d2d7a,tpp_buckets:668%232846%238110%231995&pdp_npi=4%40dis%21EUR%216.19%212.01%21%21%2147.54%2115.43%21%402103835c17163972291436621eb662%2112000035190946401%21rec%21ES%213002009838%21&utparam-url=scene%3ApcDetailTopMoreOtherSeller%7Cquery_from%3A)
  - [Dupond Cables](https://www.amazon.es/240Piezas-Breadboard-compatible-Arduino-Raspberry/dp/B0BRMKX5RT/ref=sr_1_6?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&sr=8-6)
  - [HC-SR04](https://www.amazon.es/sspa/click?ie=UTF8&spc=MTo2Mzc3NDc2MzU1MDAxMDAxOjE3MjM5NzcyMzA6c3BfYXRmOjIwMDUxODUwMTE1NDk4OjowOjo&url=%2FAZDelivery-Distancia-Ultras%25C3%25B3nico-Raspberry-incluido%2Fdp%2FB07TKVPPHF%2Fref%3Dsr_1_1_sspa%3Fdib%3DeyJ2IjoiMSJ9.diZ4Vfd24b4Mrhkgp0sOd4DTism6LlXDXMPyfrdNSYoBy-jQbE-avTFLDoK6PDDk-94zo2u1bWKvMjuAasWsKE66HfY92lPpsI10LsGJPz0yup8jOCSMcCNbIpL2IB5wHNLSNRaj8Lauw9RmzM5Diw14nffpN3YZHIyssfvy4Ziq9K7EuAYhyxzFENO52x29dKyQdqzLztafoyphO4leDNdRZGQ4HFJXFQrbgU6rTpJ8Ovjglaz_nFN4fikN1LLAGk-SlnhVESX5PewOuOtSkpwL0I3URCNK4L5G7NkWKYI.alFO0t23z_leXnNcGoTDRkFZMGHO-xPwZAV-MSo0cmY%26dib_tag%3Dse%26keywords%3DHC-SR04%26qid%3D1723977230%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1)
  -   [Pi Camera](https://www.amazon.es/AZDelivery-c%C3%A1mara-para-Raspberry-Pi/dp/B01M6UCEM5/ref=sr_1_1_sspa?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1&smid=A1X7QLRQH87QA3)

## 2. Make the [scheme](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Schemes/WRO_Car.jpg)

![Schemes](Schemes/WRO_Car.jpg)

>The color sensor sown in the image it's just for reference the model thar we are really using it's the TCS34725

## 3. Print the 3D models

You will need to 3D print the models in the repository ['Models/Current_Car_Models'](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Models/Current_Car_Models). In our case we have used an Ender 3, an Artillery Sidewinder X4 Pro and a Prusa Mk3s for printing the chassis out. But you can use any printer of your preference. These parts don't need to support any abnormal forces therefore can be printed in any material. In our case we printed them with PLA.  

## 4. Chassis assemble

Once we have all the parts printed it's time to put them together. Now we will show you how to.

### 1. Base
 
 ![Base](https://github.com/user-attachments/assets/74c9a0a8-6e4d-43bb-9972-99ef6d25d5de)

 First of all we place the raspberry and L298N on the base at their places:  
- The Raspberry is placed transversaly in the middle of the car.  
- The L298N is placed at the back of the car in between the motors.

### 2. Stub axels

![Stub axels](https://github.com/user-attachments/assets/ccfe2ea6-afe7-4758-b792-c431bd7df17a)

Now we place the stub axels, this will serve to transfer the rotation of the servo to the wheels to vary their direction.  
- We insert a M3 nut in each stub axel for later on
- We place the part in the hollow rods that stick out of the chassis upwards, as shown in the picture.
- We fix it in place with a M3 x 20 screw and washer, and screw it to a M3 nut at the botton of the car.

> Be careful with the hollow rod is extremly fragile.  
> Do not apply any unnecessary forces on it until it is screwed.  

### 3. Zipper

![Zipper](https://github.com/user-attachments/assets/5b64e032-9cc6-40b7-ab98-a234c3fb92f6)

Next is the install of the zipper this will syncronize the direction of bowth sides and transfer the servo direction.  
- We place the zipper as shown in the picture above and screw it with a M3 screw and nut in each side.

### 4. Wheels and DC motors

Now we mount the four wheels to the chassis
- The two frontal ones are drilled trough the middle and fixed in placed with a M3 screw.
- We fix the two DC motors in place using glue.
- The two in the back are simply snapped in place.  

### 5. Gear and servo

![Gear](https://github.com/user-attachments/assets/a04b8670-2c3e-482d-8210-b1969d9a60e9)

To finish the direction we place the gear and the servo which will guide all the direction system.  
- We insert the gear in the servo and screw it in place
- We place the servo in it's place with the gear on top of the zipper. And fix it in place with glue.  

### 6. Battery sield and spacers

![Cage_spacers](https://github.com/user-attachments/assets/f4929349-dbf2-4e2d-890b-60336d332ba4)

Finally we install the battery in place to power everything up.
- We glue the four spacers in place being careful to aling the holes as much as posible.
- We screw the battery shield trouhg the spacers and the usb looking to the front of the car.  

## 5. Software installation

Now that we have all the hardware redy to go, we need a "brain" to move it.  
So here we will guide you command by command how to setup your raspberry pi in order to work correctly with the hardware.

### 1. OS installation and adjustment

1. Install [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on your computer.

![image](https://github.com/user-attachments/assets/f455e273-b251-4d44-bf55-d4e965a86079)

2. Download the [Raspberry Pi OS Lite](https://www.raspberrypi.com/software/operating-systems/).

![image](https://github.com/user-attachments/assets/350fb464-95b8-4c5e-8286-bc4d979333ad)

3. Open Imager.

![image](https://github.com/user-attachments/assets/027e06e3-96ec-495f-bc63-9d5e86d3c364)

4. Select your model of Raspberry. In our case it's Raspberry Pi 4.

![image](https://github.com/user-attachments/assets/7f566e96-096b-4b56-923c-6cc1d759bb27)

5. Select the OS image we downloaded before.

![image](https://github.com/user-attachments/assets/95d730a1-39c8-45bc-901b-1e9dc7376636)
![image](https://github.com/user-attachments/assets/f12c07ab-5af0-4f07-ab62-4b2feced0ec4)

6. Select the SD card in wich we are going to intall the OS.

![image](https://github.com/user-attachments/assets/2aa9a7c5-b4d4-458c-94d9-fbec4c7d35f7)

7. Click the "Next" buttom. And click in "Edit Settings".

![image](https://github.com/user-attachments/assets/c2b3d18a-b10e-4a8c-b3c2-7a4568006a76)
![image](https://github.com/user-attachments/assets/7fb9bdac-12e3-47c1-8541-e15d667af66a)

8. Configure username, password and WIFI. And click on "Save".

![image](https://github.com/user-attachments/assets/08c064ea-b3e1-4257-9c1a-05f4a10c101a)

9. Click on "Yes".

![image](https://github.com/user-attachments/assets/3f938b88-6b8e-4ea2-8f78-31dfc66f7ea2)
![image](https://github.com/user-attachments/assets/6ef216c8-3c7c-4e6e-8748-492a6af70f70)

> Be carefull this proccess will erase all the information saved on the SD card.

10. Insert the SD card in to the Raspberry and power it up.

![image](https://github.com/user-attachments/assets/891760c8-1dfd-46b7-a89a-17779dc92527)

### 2. Auto-login configuration

1. Enter raspberry pi configuration.  
-       sudo raspi-config
![image](https://github.com/user-attachments/assets/72cdd631-1af4-4d94-9584-bc9f4dbf60ac)
![image](https://github.com/user-attachments/assets/2cc71732-ae75-4d74-bc13-6b557a7d86e1)

2. Enter in system options.

![image](https://github.com/user-attachments/assets/9592a369-adf3-4636-8589-9a18ec98121b)

3. Enter in Boot / Auto Login.

![image](https://github.com/user-attachments/assets/1be929a9-a5ed-44ec-9843-1e3dafc4aa82)

4. Enter in Console Autologin.

![image](https://github.com/user-attachments/assets/9f8a67af-0252-4586-9b6e-0dea8add2d85)

### 3. Update packages
-      sudo apt update & sudo apt upgrade -y

![image](https://github.com/user-attachments/assets/92bddcbb-8b0d-4ad8-a6fc-e7cb7c83e137)

### 4. Install Python
-      sudo apt install python3-pip
  
![image](https://github.com/user-attachments/assets/9d838faa-6011-40a0-9842-0ef1e9eedf00)

### 5. Install basic libraries for the camera, machine vision and tcs34725
-     sudo apt install python3-picamera
      sudo apt install python3-opencv
      sudo pip3 install adafruit-circuitpython-tcs34725
      sudo pip3 install adafruit-blinka

### 6. ENABLE THE I2C BUS FOR THE TCS34725
1. Enter raspberry pi configuration.
-       sudo raspi-config
2. Select interface options

![Tcs_1](https://github.com/user-attachments/assets/8ab8f1ec-dfc4-4d4d-bde9-c0439ee79825)


3. Select P5 I2C

![Tcs_2](https://github.com/user-attachments/assets/6e0c11a1-7a69-4a3b-bd78-6269cd5fd49d)


4. Enable it

![Tcs_3](https://github.com/user-attachments/assets/2b09168f-0e8d-41e3-ace3-1a34c674e061)


### 7. Download our github repository
1. Install git.
-      sudo apt install git

![image](https://github.com/user-attachments/assets/7f0703ba-dddd-4a07-812d-cca7b3e5780c)

2. Create directory for the repository.
-     mkdir WRO-2024-ArduMASTERS
      cd WRO-2024-ArduMASTERS
      git init
      git remote add origin https://github.com/Ploirad/WRO-2024-ArduMASTERS.git
      git config core.sparseCheckout true
      echo "Src/" >> .git/info/sparse-checkout

![image](https://github.com/user-attachments/assets/6492c86a-21e1-44e1-8be3-67b9f40e0056)

3. Download repository
-      git pull origin main

![image](https://github.com/user-attachments/assets/bd5cb9b5-5d64-41f7-ba00-5c111d0b73ba)

### 8. Automate the entrance into the repository
1. Open the bashrc with nano
-      nano ~/.bashrc

![image](https://github.com/user-attachments/assets/bbdf2699-9086-47e3-be66-60800686f33b)

2. Add the following commands to the bashcr file.

- cd /home/"username"/WRO-2024-ArduMASTERS/Src/Main
- python3 Camera_Main.py &
- python3 Movement_Main.py &
- python3 tcs_Main.py &
- python3 MAIN.py

![image](https://github.com/user-attachments/assets/a3fe665d-307e-40ff-aa0b-ba82b22afa25)

3. Reboot to verify changes
-      sudo reboot
![image](https://github.com/user-attachments/assets/215987eb-a595-4e0f-b9f0-251b51f3c8ed)

### 9. Useful commands
1. Update repository
-      git pull origin main
3. Run code
-      python3 "file name"
5. See files in current directory
-      ls
7. Go to directory
-      cd "directory name"
9. Go to the previous directory
-      cd ../

# 6. Ending

AFter reboot your car shoud work like the videos of this [readme.md](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/video) in the video folder.

If you want to test the different componets or recalibrate the camera go to [test codes](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/Test%20codes)

I hope that this guide has been useful, if you have some problemens, do not doubt about talking with us.
