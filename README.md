# WiFi-CSI

# Part-1: Deep dive into what CSI is and its applications in Indoor Localisation

## What is CSI and Why is it Useful

CSI (Channel State Information) describes the parameters of a wireless channel.

When a Wifi router communicates with a device, the signals travel through walls, furniture and even humans via reflections, scattering and direct lines of sights. The reflection and scatteriing of these signals shows up as perturbations in the CSI as changes in amplitude and phase difference of different frequency subcarriers.

CSI effectively converts the wifi router into a radar sensor which can map out Human and obstacle presence, movements and sign monitoring such as breathing and heart rate monitoring. 

CSI is not limited by walls or obstacles since wifi signals can travel through these, it does not require expensive hardware or cameras to capture signals and it is privacy-friendy since it does record any video or audio. It can function in absence of light, both indoors and outdoors, and it is contactless & invisible. It can generate spatial maps and also recognise obstacles, humans and their movemeents precisely.

### How is CSI data captured

CSI data can be captured by inexpensive devices that connect to wifi routers and expose channel state information. This is usually done through NIC (Network Interface Card). The CSI captured can be analysed using OFDM (Orthogonal Frequency-Division Multiplexing) to get the amplitudes and phase differences in different subcarriers.

OFDM is a modulation technique that can split high-speed data into multiple parallel, slow speed streams of data. These parallel flows of information are carefully soaced to make them orthogonal which means there is no interference between these subcarriers. Hence, the information from one frequency component is not affected by others.

### Some Practical Applications

CSI has many practical applications. Since it is not limited by expensive hardware, environmental conditions and can detect movements, it finds applications in indoor localisation, obstacle detection, human tracking and health monitoring without invading privacy. Applications which produce signals in particular frequency bands are more easily identifiable from the CSI decoding, actions like breathing and heart rate can hence be decoded. 

## Indoor Localisation

CSI provides precision in localisation even in indoors, low light conditions where other localisation techniques like cameras (vSLAM) and GPS fail. Routers placed near landing or flying zones can provide localisation and position locking in for landing and path planning in indoor environments. CSI can also assist in figuring out rpm fluctuations in propellers since the rotation causes vibrations in a known frequency band.

Wireless receiver placed on a drone itself can be useful for mapping out spatial features and obstacles within a room, and use this data for path planning however moving drone would produce data with higher noise than a static station. (Will dive deep into this in part 2)

### Attempts to localise drones 

#### SpotFi by Kotaru et al:
SpotFi focuses on trying to get universally deployable accurate localisation systems. THeir architecture consists of three key algorithmic components - a Super-resolution AoA estimation, a direct path identtification and localisation. 

The Super-resolution AoA estimation is required since angle of arrival of direct paths among the multipaths are useful for localisation since they can accurately denote the distance between the target and the access point. The key insight is that for AoA estimation, changes in ToF is also present for different subcarriers of the CSI, therefore they can be estimated simultneuosly to produce a pair of estimated AoA and ToF. The previous algorithms used for this include MUSIC which uses a large antenna array (number of antennas should be higher than significant propagation paths in an indoor environment) to estimate AoAs. SpotFi intends to use standard WiFi router configurations i.e. 3 antennas to reliably estimate AoAs by treating subcarrier signals received at each of these antennas as seperate signals, this is made possible by measuring ToFs for these subcarriers, since even small differences in ToF produce significant phase difference allowing for these signals to be differentiated and execeeding number of propagation paths. 

The direct path identification exploits the fact that the estimated pair of AoA and ToF for direct paths over consecutive data packets shows much smaller variation as compared to indirect paths. Measuring variance in ToF is slightly challenging however the researchers developed a sanitization algorithm to clean the data from known causes of variance and used the results to assign each pair a likelihood of corresponding to a direct path.

The localisation algorithm combines RSSI based distance estimate with the estimation and likelihood of direct paths' AoA (not ToF since estimated ToF is not true ToF) received from all 3 APs (access points) to localise the target. 

#### WiFi CSI Based Energy-Efficient Drone Detection by Chen et al:
 Researchers used a combined approach of integrating CSI and RSSI through a RL assisted detection model to eliminate radio wave interference in outdoor environments as well reduce the energy consumption for capturing CSI through ESP32-S3. They used a high band pass filter to eliminate false alarms by differentiating birds and drones using vibrations caused due to propellers' rotation. They were able to achieve a decreased false alarm rate, a decreased miss detection rate and reduced energy consumption with this approach. 

 # Part-2: Practical testing with aa CSI Dataset

 ## Code and Test Description

 The code (generated through claude) reads data from the Widar 3.0 dataset which captures data for different users performing gestures in different rooms. For simplicity, I have just used a single session's data from a single user. The random forest classifier trained on ~4500 samples uses the mean and standard deviations of the amplitudes of subcarriers (3 antennas * 30 subcarriers) and the mean phase difference between two sets of antennas (2 * 30 subcarriers) making a total of 240 values as a vector. The model was trained with a 80-20 train-test split and tries to predict the room (a total of 5 different rooms were used to record the data) from the csi data. The model achieves an accuracy 68% from the selected dataset.   

 ## Changes with a drone

When the data capturing device is a dynamic object like a drone, the following changes might led to significant difficulties:
- The dataset was captured by a static device so the CSI noise baseline is also static, when a drone is used the noise would be dynamic making it difficult to sanitize/clean the data.
- SpotFi AoA estimation assumes the antennas are stationery hence the phase difference and ToF estimation fails under data capture using dynamic stations. Even tilting of drone would introduce another variable causing phase difference which has to be accurately measured and accounted for while estimation of AoA and ToF.     
- The localisation approaches for drones in indoor environments (based on static antennas) focus on doppler effects which modify the frequency band of the vibrations produced, however on drones, the access points would not be able to utilise the doppler effects (since the AP is itself moving at the velocity of the drone) therefore localising is difficult.
- Vibrations caused by high speed motion of the drones and rpm fluctuations of the propellers could also result in noise in CSI signals.