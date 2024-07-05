# GRAVITYbot: A Forum Summary LLM Bot

A LLM bot which summarizes the forum pages for the citizen science project [Gravity Spy](https://www.zooniverse.org/projects/zooniverse/gravity-spy).

## Description:

GRAVITYbot summarizes the ["Talk" pages](https://www.zooniverse.org/projects/zooniverse/gravity-spy/talk) of Gravity Spy, a citizen science project which classifies glitches occuring through The Laser Interferometer Gravitational-Wave Observatory (LIGO) laser interferometer sensor data. As such, it is a science communication bot with multiple uses.

The primary tasks it aims to accomplish are:

1. Summarizing Talk pages for LIGO scientists.
2. Summarizing Talk pages for citizen science.
3. Logging dynamics of citizen science learning through weekly updates.

Possible future tasks it might be applied to are:

- A chatbot for promoting locations in the project chat or the wiki.
- A chatbot which promotes contributions to the project chat or the wiki.

## Getting Started:

### Dependencies:
- Python 3.7+
- openai, datetime, dotenv, pandas
- Zooniverse Talk Pages CSV File

### Initializing the Project:
This is currently under revision, and subject to updates of the project. However, currently the project needs a directory containing prompts.py, GravityBot_main.py, the Talk Pages Data File, and an .env file. First make sure you have an env file containing an openAI key assigned to variable OPENAI_API_KEY.

Next, both GravityBot_main.py and prompts.py may need some configuration Minimally, to run the project, one must run the GravityBot_main.py after configuring it:
 
1. Set the working directory
2. Set the Talk Pages directory location with the correct csv filename.
3. Define the date-time span of Talk pages posts of which needs summary.
4. (Optional): Define which prompt function, variable you wish GRAVITYbot to run.
5. (Optional): Tuning the openAI parameters

While optional, you may further configure a custom bot by making custom prompts within prompts.py. This file contains more detailed instructions about how to create a prompt.

## Help:

Proceed with caution. This is an incomplete project which requires using funds to use openAI. We (the project developers, Gravity Spy, and/or LIGO) are not liable for any expenses you may be charged by running this project locally.

## Authors:

Initial development was written by Alexander O. Smith as a part of employment for Gravity Spy. Any specific questions can be directed towards aosmith@syr.edu or active Gravity Spy lab members.

## License:
This project is licensed under an MIT "Expat" License. See the LICENSE.md file for details.

## Acknowledgments:

We begin by acknowledging with respect the Onondaga Nation, Central Fire of the Haudenosaunee Confederacy, on whose ancestral lands we now inhabit. Wherever you are located be aware of the Indigenous Peoples on whose lands you reside. We are mindful that the technology that makes this conference possible comes from the mineral extraction by multinational corporations, which decimate and displace Indigenous people and their land all over the world. May the information you glean from this podcast motivate you to uphold Indigenous values, protect Mother Earth, Honor Indian Treaties and hold your government and various institutions accountable who stand in the way.

Additionally, Alexander would like to thank Gabriel Davila - Campos and Una Joh for advice and initial guidance in development. 