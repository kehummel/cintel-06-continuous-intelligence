# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Glossary** - project terms and concepts

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)

## Custom Project - Phase 5

### Dataset
CPU Performance Metrics (System Monitoring Logs)

### Signals
Power consumption per CPU Usage
temperature per CPU usage
cache miss rate per cpu usage

Calculated the rolling mean for 102 rows, which is an hours worth of data.

MAXIMUM THRESHOLDS
Threshold of cps usage over 100
cpu temperature over 110
cache miss rate over 9
power usage over 110

### Experiments
I calculated a rolling mean for hour of usage to make sure there were no drifts in my data.
I flagged anomalies in my data so that they can be looked at more carefully to figure out why they exist.
I calculated the power, the temperature, and the cache miss rate per cpu percent used.
I then created thresholds to make sure the averages were within the normal range.

### Results
The rolling mean for CPU usage stayed within 47 and 53, which is not a lot of variance.
All of the averages were well below the threshold.

### Interpretation
The CPU system is running efficiently and there do not seem to be any issues with it. System was found to be stable.
