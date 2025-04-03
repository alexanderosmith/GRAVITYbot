### Unresolved Issues Related to Particular Sensors in ALOG Dataset 2:

1. **ITMY HEPI Sensor Issue**:
   - The ITMY (Input Test Mass Yaw) HEPI (Horizontal Earthquake Protection Isolator) sensor was found to have problems, specifically the H sensor appeared non-functional. The troubleshooting involved swapping sensors and checking electronic settings, but it revealed a chassis issue rather than a sensor issue.
   - **Details**: In simpler terms, a particular sensor that helps stabilize the LIGO equipment against horizontal movements caused by earthquakes was not working properly. After swapping components and some testing, it was determined that the problem was with the supporting electronics, not the sensor itself.
   - **URL**: [ALOG Entry #75875](https://alog.ligo-la.caltech.edu/aLOG/index.php?callRep=75875)

2. **ALS Y PLL Locking Issues**:
   - The ALS Y (Auxiliary Laser System Yaw) PLL (Phase Locked Loop) had trouble locking, which affected the stabilization and accuracy of measurements. Adjustments were made to the crystal frequency to stabilize the system temporarily.
   - **Details**: This system is crucial for maintaining the precision in the laser system alignment. The issue was temporarily fixed by manually adjusting the frequency settings, but this indicates an ongoing issue that might need more permanent solutions.
   - **URL**: [ALOG Entry #75873](https://alog.ligo-la.caltech.edu/aLOG/index.php?callRep=75873)

### Alterations to Particular Sensors in ALOG Dataset 2:

1. **Replacement of ITMY HEPI AA Chassis**:
   - Due to the persistent noise and malfunctioning initially attributed to the ITMY HEPI sensor, the AA chassis (which is part of the electronic system supporting the sensor) was replaced to resolve the noise issues.
   - **Details**: Essentially, the support system for a key sensor was faulty and had to be switched out to ensure the sensor could accurately perform its function of stabilizing against seismic noise.
   - **URL**: [ALOG Entry #75875](https://alog.ligo-la.caltech.edu/aLOG/index.php?callRep=75875)

2. **Digital Fix Implementation for 6Hz Noise in SEI**:
   - A digital fix was tried to address a consistent 6Hz noise observed in the SEI (Seismic Isolation) systems. This involved tweaking the digital responses to better handle this specific frequency of noise.
   - **Details**: A persistent low-frequency noise was interfering with data accuracy, leading to a software-based adjustment aimed at mitigating this specific disturbance.
   - **URL**: [ALOG Entry #75872](https://alog.ligo-la.caltech.edu/aLOG/index.php?callRep=75872)

These entries show LIGO's continuous efforts to maintain and calibrate their highly sensitive equipment, ensuring the accuracy and reliability of gravitational wave detection. Each fix or troubleshooting step, though technical, plays a crucial role in the broader scientific objectives of LIGO.