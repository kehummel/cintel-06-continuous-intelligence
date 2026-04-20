# Continuous Intelligence Portfolio

Kim Hummel

2026-04

This page summarizes my work on **continuous intelligence** projects.

## 1. Professional Project

### Repository Link

https://github.com/kehummel/nlp-01-getting_started

### Brief Overview of Project Tools and Choices

Project 1 focused on making sure our system is up and running and verifying that we can execute the code correctly. I made minor changes to the LOGs to show that I could make edit to the code and it would still run.

## 2. Anomaly Detection

### Repository Link

https://github.com/kehummel/cintel-02-static-anomalies

### Techniques

My data focused on screen time usage so I focused on how screen time on your phone affected adults. I created minimum value for their age so that anyone who was not an adult was labeled an anomaly. I set a maximum value of 120 minutes spent on the phone before bed, making anything more than that an anomaly. And I set a maximum value of 10 hours of sleep making anything more than that an anomaly.

### Artifacts

https://github.com/kehummel/cintel-02-static-anomalies/tree/main/artifacts

The results were a csv that decreased from 15,000 rows to 1,049. This was a more manageable dataset that would allow for easy averages of the columns to calculate which habits had the most impact on sleep for adults.

### Insights

All anomalies were due to age. There were no participants that spent over 120 minutes on their phone before bed, and no participates that recorded more than 10 hours of sleep. All data that was removed was due to participants being younger than 21, which was my minimum value.

## 3. Signal Design

### Repository Link

https://github.com/kehummel/cintel-03-signal-design

### Signals
This data focused on beginning and ending weight along with other lifestyle choices, such as stress level, activity level, calorie intake, etc.

I created a height to weight ratio, found the change in weight from initial to final, and number of calories consumed per step taken. I created these signals to see the correlation between participants weight and height. I looked to see if there was a change in weight through the time span. And I wanted to see the ratio between calories and activity level per participants because if you are more active you should be consuming more calories. So I wanted to see if that rate stayed the same regardless of the activity level.

### Artifacts

https://github.com/kehummel/cintel-03-signal-design/tree/main/artifacts

All signals had their own column. It was found that the height to weight ratio varied between 1 and 2. While on average people lost weight, it was less than one kilogram, suggesting that the time between the initial weighing and final weight was not that long, or that the purpose was not to lose weight. And the number of steps per calorie consumed varied between 2 and 13.

### Insights

The signal revealed that the data needs to be separated out more in order to get more useful results. The height ratio did not vary a lot, but we should look at whether or not that is the case across all participants or if there was variation between taller and shorter participants. More data from outside the spreadsheet should be found to see if weight should even be considered as valuable data. And the number of steps per calorie should be looked at to see if its range in results came from participants who are more active (had more steps) or not.

## 4. Rolling Monitoring

### Repository Link

https://github.com/kehummel/cintel-04-rolling-monitoring

### Techniques

I calculated a rolling mean for the temperature, vibration, energy consumption, and speed for a machine. Since each row was timestamped for the minute, I created a rolling window of 30, so that I would see how the machine was working on average for the previous 30 minutes.

### Artifacts

https://github.com/kehummel/cintel-04-rolling-monitoring/tree/main/artifacts

There was small amounts of variation in the means for all four metrics. The rolling mean stayed fairly consistent throughout the morning - a 5 hour span.

### Insights

The machine would be said to be running in fair and stable conditions, with reasonable variation throughout the 5 hours of use.

## 5. Drift Detection

### Repository Link

https://github.com/kehummel/cintel-05-drift-detection

### Techniques

The I found the mean of the number of riders of public transportation on a specific route in Chicago. My reference period was January and February of 2025 and my current period was January and February 2026. I found the average number of riders and compared them from the reference period to the current period.

### Artifacts

https://github.com/kehummel/cintel-05-drift-detection/tree/main/artifacts

As you can tell by my artifacts, the mean of the number of riders decrease by over 100 riders between the reference period and current period, triggering the drifting too low flag.

### Insights

This flag actually triggers the need for more investigation. It needs to be looked into whether or not there was an environmental factor that contributed to the decrease in public transportation passengers, such as weather and construction. If the drop in ridership was due to environmental factors, it should be looked at how they can be mitigated to not lose riders. If the drop is not due to environmental factors, it might be worth looking at decreasing the number of trains that run on that line to cut costs if there are less passengers.

## 6. Continuous Intelligence Pipeline

### Repository Link

https://github.com/kehummel/cintel-06-continuous-intelligence

### Techniques

I created signals that compared the power consumption, temperature, and cache miss rate to the CPU usage. I created a rolling mean or 102 rows which would give me the average of the previous hour. I then created maximum thresholds for all of the signals that would flag if the threshold was reached.

### Artifacts
https://github.com/kehummel/cintel-06-continuous-intelligence/tree/main/artifacts

The averages were all found to be below the threshold and the rolling mean averaged between 47 and 53 for CPU usage, which is not a lot of variance and was not a consistent increase so therefore there was not any drift. I also created an artifact of any anomalies that were found so that they could be researched more and understood.

### Assessment

Since there was no drift and no maximum thresholds were reached the system is stable.
