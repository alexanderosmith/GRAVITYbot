### Unresolved Issues Related to Particular Sensors in ALOG Dataset 2

1. **ALS Y PLL Autolocker 5Hz Line Noise**
   - **Issue**: A persistent 5Hz line noise was observed starting around 1pm, disappeared, and then reappeared until maintenance began. Monitoring showed the noise moving between 4Hz to 8Hz. Despite various checks, the exact cause of the noise remains unidentified, making it difficult to apply a permanent fix.
   - **Explanation**: This issue involves a noise frequency that keeps appearing and disappearing in the ALS Y sensor readings. The noise interferes with the quality and reliability of the sensor's data. The cause has not been pinpointed, leaving the system susceptible to future occurrences of similar disruptions.
   - **URL**: [ALOG Entry 75827](https://alog.ligo-la.caltech.edu/aLOG/index.php?callRep=75827)

### Alterations to Particular Sensors in ALOG Dataset 2

1. **ALS Y PLL Autolocker Frequency Range Adjustment**
   - **Alteration**: The frequency range for the Fine Scan of the ALS Y PLL autolocker was adjusted from a broader range to a narrower one (from unspecified to 40MHz) to resolve issues with nonsensical values at the frequency extremes, which corrupted the system’s tuning.
   - **Explanation**: This change was made to the sensor's settings to prevent it from giving out meaningless readings when scanning at the outer limits of its frequency range. By narrowing the frequency range, less strain is put on the sensor, potentially increasing its accuracy and reliability.
   - **URL**: [ALOG Entry 75834](https://alog.ligo-la.caltech.edu/aLOG/index.php?callRep=75834)

2. **Alteration to L4C H Sensor**
   - **Alteration**: During a downtime for maintenance, the L4C H sensor was identified as having the highest features in sensor spectra, suggesting it might be related to observed noise features. Although specific adjustments or fixes are not detailed, this sensor was flagged for its notable response.
   - **Explanation**: The L4C H sensor showed unusually high readings in its data, which might be linked to noise issues observed in the system. It’s being considered for further examination and possible tweaking to ensure it doesn’t affect overall data quality.
   - **URL**: [ALOG Entry 75827](https://alog.ligo-la.caltech.edu/aLOG/index.php?callRep=75827)

These entries from ALOG Dataset 2 highlight ongoing troubleshooting and adjustments being made in the sensor systems at LIGO, reflecting the complex and dynamic nature of managing such sophisticated scientific instruments.