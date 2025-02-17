# Grea Plant Tower
Interest in sustainability has taken on new meaning as research reinforces the threat of climate change. One great way to practice personal sustainability is by growing food at home. However, agriculture is complex, and in urban environments, limited availability of space and sunlight can prevent individuals from starting their own gardens.

The Grea Plant Tower addresses all of these needs by providing an easy-to-use hydroponic plant growth system that is compact, quick to assemble, cost-effective, and self-monitoring. It allows users with limited budgets, restrictive spaces, and busy lives to engage with sustainability and create a positive impact on their own health.

## Repository Structure
* /CAD - STEP files containing the geometry for 3D-printed tower parts
* /Docs - PDF files containing project documentation and assembly instructions
* /Embedded - Code for the Raspberry Pi Pico 2 platform with attached ADC and addressable LED strips. A TDS sensor should be attached to channel 0, and a water level sensor should be attached to channel 1. The setpoint constants should be set before use.

Default pin settings: ADC via I2C- GP21, GP20 ; LED via PWM - GP28
