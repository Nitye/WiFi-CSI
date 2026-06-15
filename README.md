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

#### DeepFi by Wang et al:
DeepFi follows a slightly similar pproach in using CSI rather than RSSI for localisation of targets in indoor, GPS-denied environments. They present 3 hypotheses - first is that CSI values for the same location are stable (also demonstrated by researchers modelling SpotFi). Second is multipath effects cause clusters of subcarrier variation in particular frequency bands, the number of clusters correspinds to less or more of multipath effect. Third being CSI captured at different antennas can be treated as seperate signals (and hence act as seperate data points while training their deep learning model) since the CSI for the same packets also differ widely (due to phase difference attributed to AoA at different antennas as shown in the paper presenting SpotFi, however, they don't utilise AoA or phase difference).

The system utilises a vector of 90 CSI values (3 antennas * 30 subcarriers) for a single packet reception. One key difference between SpotFi and DeepFi is that they only use the amplitude responses for these 90 values for fingerprinting the inddor environment. The deep learning model uses 4 hidden layers with multiple neurons, and the weights between these layers are pretrained. The pretrained model is fine-tuned and the weights are used in the localisation of unknown environments thorugh unrolling. Unrolling is the process of feeding in data captured from unknown environments to through the trained weighted model to find features like furniture in the indoor environment.

The weights are trained using a greedy learning algorithm. It basically tries to find the weights at each layer in sequential order, freezes the weights at first layer and then uses those for determining weights for further layers. The localisation is then conducted through a bayesian probbality model which estimated the possibility of a mobile device being in multiple locations and chooses the location with the highest probability.

DeepFi achieves a precision of about 0.95 metres in a lower multipath effect environment which outperforms techniques based on RSSI values however, it is not as precise as SpotFi due to only use of amplitude signals. 

#### WiFi Sensing with Channel State Information SUrvey by Ma et al
This is a survey that goes over multiple methods of CSI decoding including modeling based, learning based and hybrid alorithms. It also covers signal pre-processing like noise reduction, signal transforms and signal extraction and practical applications of WiFi CSI.

Noise reduction is done using phase offset removal, phase offset is caused by known and somewhat measurable effects like sampling time and frequency offsets, and outliers can be removed by generic averaging techniques like moving averages and filters. Signal transform techniques are fourier transforms and discrete wavelet transforms. Signal extraction includes compression, filtering and composition using signals from multiple antennas, frequency bands and packets.

Sensing algorithms include modelling based, learning based and hybrid algorithms. Modelling based are hardware heavy solutions that rely on accurate measurements and simple algorthms, but they require a lot of signal processing and expensive equipment for accurate data capture. Learning based algorithms follow the software and data heavy approach with the use of millions of data points to extract features and doesn't require very high level of signal processing, however it does require high compute. Hybrid utilise modelling based approach with lower precision data for coarse extraction and learning based approaches for fine tuning of feature extraction.

Key applications outlined were 
- Human sensing, fall detection, intrusion alerts and keystroke detection (digital fingerprint and human recognising).
- Activity, motion, gesture recognition and sign language decoding
- Localisation in indoor environments
- Heart rate and breathing rate monitoring

The survey also points out challenges such as difficulty in generalisation, coexistence/interference with network services and most importantly privacy and security concerns since WiFi CSI can theoretically detect even small scale motions invisibly, through walls without any indication.   

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